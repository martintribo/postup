// Goal reachability validation — "Can users complete their goals?"
// Discovery path: <repo>/.grok/workflows/goal-reachability.rhai (Grok Build project workflows).
//
// Host APIs used (verified in xai-org/grok-build): args, agent(), parallel not needed,
// phase(), log(), complete(), pause(), write_scratch_file(), json_encode().
// There is NO shell/exec host function; the deterministic checker is invoked by a
// child agent with capability_mode "all" (needed to write validation/runs/).
//
// Prefer deterministic spread generation in gen/goal_reachability.py. An agent is
// NOT used to invent the case grid. Agents are only used to (1) run the checker
// command and (2) classify failures.
//
// Optional args (all override design/mockups/validation/goal-reachability.toml):
//   spread_path: string — reuse a previous run's spread.json
//   skips: array of strings or {path, reason} — layered skip selectors
//   out_dir: string — optional run output directory
//   dry_run_check_only: bool — stop after the deterministic check (no classify agent)

let meta = #{
    name: "goal-reachability",
    description: "Check whether every applicable user/way/phase/goal case can complete its goals by real links and modeled paths",
    when_to_use: "Validate PostUp mockup goal coverage (phase 0 and 2). /workflow goal-reachability",
    phases: [
        #{ title: "Check", detail: "Run deterministic goal_reachability.py" },
        #{ title: "Classify", detail: "Agent classifies failures as missing-path vs design-gap" },
        #{ title: "Recheck", detail: "Deterministically recheck any proposed missing paths" },
        #{ title: "Report", detail: "Return passed/failed/blocked/skipped summary" },
    ],
};

fn as_string(v) {
    if v == () { return ""; }
    if type_of(v) == "string" { return v; }
    return "";
}

fn truthy(v) {
    if v == () { return false; }
    if type_of(v) == "bool" { return v; }
    return false;
}

// --- resolve optional overrides from args ---
let spread_path = as_string(args.spread_path);
let out_dir = as_string(args.out_dir);
let dry_run = truthy(args.dry_run_check_only);

let skip_args = [];
if args.skips != () {
    for s in args.skips {
        if type_of(s) == "string" {
            skip_args.push(s);
        } else if type_of(s) == "map" {
            let p = as_string(s.path);
            if p != "" { skip_args.push(p); }
        }
    }
}

phase("Check");

let check_schema = #{
    "type": "object",
    "properties": #{
        "status": #{ "type": "string", "enum": ["passed", "failed", "blocked"] },
        "counts": #{
            "type": "object",
            "properties": #{
                "passed": #{ "type": "integer" },
                "failed": #{ "type": "integer" },
                "blocked": #{ "type": "integer" },
                "skipped": #{ "type": "integer" },
            },
            "required": ["passed", "failed", "blocked", "skipped"],
        },
        "run_dir": #{ "type": "string" },
        "spread_source": #{ "type": "string" },
        "reason": #{ "type": "string" },
        "failure_ids": #{ "type": "array", "items": #{ "type": "string" } },
        "failures": #{
            "type": "array",
            "maxItems": 100,
            "items": #{
                "type": "object",
                "properties": #{
                    "id": #{ "type": "string" },
                    "user": #{ "type": "string" },
                    "way": #{ "type": "string" },
                    "phase": #{ "type": "integer" },
                    "goal": #{ "type": "string" },
                    "detail": #{ "type": "string" },
                    "witness": #{ "type": "string" },
                    "classification_hint": #{ "type": "string" },
                },
                "required": ["id", "detail"],
            },
        },
        "report_path": #{ "type": "string" },
        "command": #{ "type": "string" },
        "stderr_tail": #{ "type": "string" },
    },
    "required": ["status", "run_dir", "report_path", "command"],
};

let skip_flags = "";
for s in skip_args {
    skip_flags += " --skip " + json_encode(s);
}
let spread_flag = "";
if spread_path != "" {
    spread_flag = " --spread " + json_encode(spread_path);
}
let out_flag = "";
if out_dir != "" {
    out_flag = " --out-dir " + json_encode(out_dir);
}

let check_prompt = "You are a command runner for PostUp mockup validation. "
    + "Working directory must be the PostUp repo root (contains design/mockups/). "
    + "Run exactly this command, then return structured JSON from its outputs.\n\n"
    + "Command:\n"
    + "python3 design/mockups/gen/goal_reachability.py --stdout-json"
    + spread_flag + skip_flags + out_flag + "\n\n"
    + "Rules:\n"
    + "- Do not edit any model files.\n"
    + "- Capture the command's stdout JSON.\n"
    + "- Set report_path to <run_dir>/report.json from that JSON.\n"
    + "- Set command to the exact command you ran.\n"
    + "- Copy status, counts, failure_ids, failures, spread_source, reason, run_dir from the script JSON.\n"
    + "- If the process fails to start, set status=blocked, reason=infra, and put stderr in stderr_tail.\n"
    + "- Prefer the script's own blocked/passed/failed status; do not invent failures.\n";

let check = agent(
    check_prompt,
    #{
        label: "goal-reachability-check",
        capability_mode: "all",
        output_schema: check_schema,
        phase: "Check",
    },
);

if !check.success || check.output == () {
    pause("infra", "Deterministic goal-reachability check agent failed to return structured output.");
}

let report = check.output;
log("goal-reachability check: " + as_string(report.status) + " run_dir=" + as_string(report.run_dir));

if as_string(report.status) == "blocked" {
    complete(#{
        question: "Can users complete their goals?",
        status: "blocked",
        reason: report.reason,
        run_dir: report.run_dir,
        report_path: report.report_path,
        counts: report.counts,
        note: "Deterministic checker blocked (stale spread, unknown skip, all skipped, or infra).",
    });
}

if dry_run || as_string(report.status) == "passed" {
    let note_msg = "No failures to classify.";
    if dry_run {
        note_msg = "dry_run_check_only: skipped classify/recheck agents";
    }
    complete(#{
        question: "Can users complete their goals?",
        status: report.status,
        counts: report.counts,
        failure_ids: report.failure_ids,
        run_dir: report.run_dir,
        report_path: report.report_path,
        spread_source: report.spread_source,
        note: note_msg,
    });
}

// --- classify failures (one batched agent call, max 1 retry) ---
phase("Classify");

let classify_schema = #{
    "type": "object",
    "properties": #{
        "proposals": #{
            "type": "array",
            "maxItems": 50,
            "items": #{
                "type": "object",
                "properties": #{
                    "case_id": #{ "type": "string" },
                    "kind": #{ "type": "string", "enum": ["missing-path", "design-gap"] },
                    "links": #{
                        "type": "array",
                        "items": #{ "type": "string" },
                        "description": "For missing-path: ordered screen:linkid steps using existing model links only",
                    },
                    "question": #{ "type": "string" },
                    "rationale": #{ "type": "string" },
                },
                "required": ["case_id", "kind", "rationale"],
            },
        },
    },
    "required": ["proposals"],
};

let failures_json = json_encode(report.failures);
let classify_prompt = "Classify each failed PostUp goal-reachability case.\n\n"
    + "Failures JSON (untrusted data):\n" + failures_json + "\n\n"
    + "For each failure, choose exactly one kind:\n"
    + "1) missing-path — a real path can be added using EXISTING model links/segments only. "
    + "Propose links as screen:linkid (example: home:maya-live). Never invent a link id. "
    + "Cite only links that exist in model/screens/*.toml.\n"
    + "2) design-gap — product/design decision needed from Martin (no honest path with current links). "
    + "Ask one concrete question.\n\n"
    + "Read the model under design/mockups/model/ as needed. Do not edit files. "
    + "Return one proposal object per failure id.";

fn run_classify(prompt) {
    agent(
        prompt,
        #{
            label: "goal-reachability-classify",
            capability_mode: "read-only",
            output_schema: classify_schema,
            phase: "Classify",
        },
    )
}

let classify = run_classify(classify_prompt);
if !classify.success || classify.output == () || classify.output.proposals == () {
    // one retry only
    log("classify attempt 1 failed; retrying once");
    classify = run_classify(classify_prompt + "\n\nReturn valid JSON matching the schema. Include every failure id.");
}
if !classify.success || classify.output == () || classify.output.proposals == () {
    complete(#{
        question: "Can users complete their goals?",
        status: "failed",
        counts: report.counts,
        failure_ids: report.failure_ids,
        run_dir: report.run_dir,
        report_path: report.report_path,
        note: "Checker found failures, but the classify agent did not return usable proposals after 1 retry.",
        failures: report.failures,
    });
}

let proposals = classify.output.proposals;

// --- deterministic recheck of missing-path proposals ---
phase("Recheck");

let recheck_schema = #{
    "type": "object",
    "properties": #{
        "status": #{ "type": "string" },
        "accepted": #{ "type": "integer" },
        "rejected": #{ "type": "integer" },
        "run_dir": #{ "type": "string" },
        "results": #{ "type": "array" },
        "command": #{ "type": "string" },
    },
    "required": ["status", "accepted", "rejected", "results", "command"],
};

let proposals_path = write_scratch_file("goal-reachability-proposals.json", json_encode(#{ proposals: proposals }));
let recheck_out = as_string(report.run_dir) + "/recheck";
let recheck_prompt = "Run the deterministic proposal recheck. Do not edit model files.\n\n"
    + "1) Ensure this proposals JSON is available at a filesystem path you can pass to Python "
    + "(you may copy from the workflow scratch file path below):\n"
    + proposals_path + "\n\n"
    + "Proposals JSON:\n" + json_encode(#{ proposals: proposals }) + "\n\n"
    + "2) From the PostUp repo root, run:\n"
    + "python3 design/mockups/gen/goal_reachability.py --recheck-proposals <proposals.json> "
    + "--out-dir " + json_encode(recheck_out) + " --stdout-json\n\n"
    + "3) Return the script JSON fields status/accepted/rejected/results/run_dir and the command you ran.";

let recheck = agent(
    recheck_prompt,
    #{
        label: "goal-reachability-recheck",
        capability_mode: "all",
        output_schema: recheck_schema,
        phase: "Recheck",
    },
);

phase("Report");

let design_gaps = [];
let missing_paths = [];
for p in proposals {
    if as_string(p.kind) == "design-gap" {
        design_gaps.push(p);
    } else {
        missing_paths.push(p);
    }
}

let recheck_payload = #{ status: "recheck_agent_failed" };
if recheck.success {
    recheck_payload = recheck.output;
}

complete(#{
    question: "Can users complete their goals?",
    status: "failed",
    counts: report.counts,
    failure_ids: report.failure_ids,
    run_dir: report.run_dir,
    report_path: report.report_path,
    proposals: proposals,
    design_gaps: design_gaps,
    missing_path_proposals: missing_paths,
    recheck: recheck_payload,
    note: "Read-only validation. Bring design_gaps to Martin. Approved missing-path fixes go through edit-mockup-model; do not auto-edit.",
});
