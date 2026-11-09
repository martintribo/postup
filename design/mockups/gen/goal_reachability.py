#!/usr/bin/env python3
"""Deterministic goal-reachability validation for PostUp mockups [M1042][M1043][M1044].

Read-only: reports findings and can recheck proposed paths. Never edits the model.

Usage (from design/mockups/):
  python3 gen/goal_reachability.py
  python3 gen/goal_reachability.py --config validation/goal-reachability.toml
  python3 gen/goal_reachability.py --spread path/to/spread.json
  python3 gen/goal_reachability.py --recheck-proposals path/to/proposals.json
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOCKUPS = HERE.parent
REPO = MOCKUPS.parent.parent  # design/mockups -> design -> repo root
sys.path.insert(0, str(HERE))
import model as M

DEFAULT_CONFIG = MOCKUPS / "validation" / "goal-reachability.toml"
RUNS_DIR = MOCKUPS / "validation" / "runs"
MODEL_FILES = [
    "users.toml", "ways.toml", "goals.toml", "segments.toml", "events.toml", "global.toml",
]


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def model_fingerprint(root: Path) -> dict:
    fps = {}
    for name in MODEL_FILES:
        p = root / name
        if p.exists():
            fps[name] = _sha256_file(p)
    screens = sorted((root / "screens").glob("*.toml"))
    flows = sorted((root / "flows").glob("*.toml"))
    fps["screens"] = hashlib.sha256(b"".join(p.read_bytes() for p in screens)).hexdigest()
    fps["flows"] = hashlib.sha256(b"".join(p.read_bytes() for p in flows)).hexdigest()
    fps["screen_count"] = len(screens)
    fps["flow_count"] = len(flows)
    return fps


def load_config(path: Path) -> dict:
    import tomllib
    if not path.exists():
        return {
            "users": ["newcomer", "registered"],
            "phases": [0, 2],
            "ways": None,
            "goals": None,
            "skips": [],
        }
    data = tomllib.loads(path.read_text())
    return {
        "users": list(data.get("users", ["newcomer", "registered"])),
        "phases": [int(p) for p in data.get("phases", [0, 2])],
        "ways": data.get("ways"),
        "goals": data.get("goals"),
        "skips": list(data.get("skips", [])),
        "spread_path": data.get("spread_path"),
    }


def case_id(user: str, way: str, phase: int, goal: str) -> str:
    return f"{user}/{way}/ph{phase}/{goal}"


def path_parts(cid: str) -> dict:
    user, way, ph, goal = cid.split("/")
    return {"user": user, "way": way, "phase": int(ph[2:]), "goal": goal}


def way_available(way: dict, phase: int) -> bool:
    wp = way.get("phase")
    return wp is None or int(wp) <= int(phase)


def goal_available(goal: dict, phase: int) -> bool:
    gp = goal.get("phase")
    return gp is None or int(gp) <= int(phase)


def match_entry(fl, fid, way, auth: str):
    """Map a way-in to the flow's entry by comparing start states (way field is not reliable on expanded outcomes)."""
    want = M.way_start(way, auth)
    ENT = M.goal_entries(fl, fid)
    for entry, ks in ENT.items():
        st = fl[ks[0]].get("start") or {}
        if st.get("screen") != want.get("screen"):
            continue
        if st.get("live") != want.get("live"):
            continue
        if st.get("auth") != want.get("auth"):
            continue
        if want.get("tab") and st.get("tab") and st.get("tab") != want.get("tab"):
            continue
        return entry, ks
    return None, []


def build_spread(sc, fl, US, WAYS, GS, cfg) -> dict:
    users = cfg["users"]
    phases = cfg["phases"]
    way_ids = cfg["ways"] or list(WAYS)
    goal_ids = cfg["goals"] or list(GS)
    cases = []
    for user in users:
        if user not in US:
            continue
        ud = US[user]
        fid = ud["main_flow"]
        if fid not in fl:
            continue
        GSU = M.load_goals(user=user)[0]
        for way_id in way_ids:
            if way_id not in WAYS:
                continue
            way = WAYS[way_id]
            if user not in way.get("users", []):
                continue
            for phase in phases:
                for goal_id in goal_ids:
                    if goal_id not in GS:
                        continue
                    if goal_id not in GSU:
                        continue  # user type does not track this goal
                    cases.append({
                        "id": case_id(user, way_id, phase, goal_id),
                        "user": user,
                        "way": way_id,
                        "phase": phase,
                        "goal": goal_id,
                        "flow": fid,
                    })
    return {
        "version": 1,
        "generated": "deterministic",
        "model_fingerprint": model_fingerprint(Path(M.ROOT)),
        "cases": cases,
    }


def validate_spread(spread: dict, expected_fp: dict) -> list[str]:
    errs = []
    if not isinstance(spread, dict):
        return ["spread must be a JSON object"]
    if spread.get("version") != 1:
        errs.append(f"unsupported spread version: {spread.get('version')!r}")
    if "cases" not in spread or not isinstance(spread["cases"], list):
        errs.append("spread.cases must be a list")
        return errs
    fp = spread.get("model_fingerprint")
    if not isinstance(fp, dict):
        errs.append("spread.model_fingerprint missing")
    else:
        for k, v in expected_fp.items():
            if fp.get(k) != v:
                errs.append(f"stale fingerprint for {k}: spread has {fp.get(k)!r}, model has {v!r}")
    for i, c in enumerate(spread["cases"]):
        for key in ("id", "user", "way", "phase", "goal"):
            if key not in c:
                errs.append(f"case[{i}] missing {key}")
        if "id" in c and "user" in c and "way" in c and "phase" in c and "goal" in c:
            expect = case_id(c["user"], c["way"], int(c["phase"]), c["goal"])
            if c["id"] != expect:
                errs.append(f"case[{i}] id {c['id']!r} does not match parts ({expect})")
    return errs


def parse_skips(raw_skips, args_skips) -> list[dict]:
    out = []
    for s in list(raw_skips or []) + list(args_skips or []):
        if isinstance(s, str):
            out.append({"path": s, "reason": "skip"})
        elif isinstance(s, dict) and s.get("path"):
            out.append({"path": str(s["path"]), "reason": s.get("reason", "skip")})
    return out


def skip_matches(case: dict, skip_path: str) -> bool:
    """Layered path: user > way > phase > goal. Shorter prefixes inherit."""
    parts = [p for p in skip_path.strip("/").split("/") if p]
    if not parts:
        return False
    cid_parts = [case["user"], case["way"], f"ph{case['phase']}", case["goal"]]
    if len(parts) > 4:
        return False
    return cid_parts[: len(parts)] == parts


def apply_skips(cases: list[dict], skips: list[dict], WAYS, US, GS) -> tuple[list, list, list]:
    """Returns (active_cases, skipped_cases, unknown_skip_errors)."""
    unknown = []
    known_users = set(US)
    known_ways = set(WAYS)
    known_goals = set(GS)
    for s in skips:
        parts = [p for p in s["path"].strip("/").split("/") if p]
        if not parts:
            unknown.append({"path": s["path"], "error": "empty skip path"})
            continue
        if parts[0] not in known_users and parts[0] not in known_ways and not parts[0].startswith("ph"):
            # first segment should be a user for our layering
            if parts[0] not in known_users:
                unknown.append({"path": s["path"], "error": f"unknown user type {parts[0]!r}"})
                continue
        if len(parts) >= 1 and parts[0] not in known_users:
            unknown.append({"path": s["path"], "error": f"unknown user type {parts[0]!r}"})
            continue
        if len(parts) >= 2 and parts[1] not in known_ways:
            unknown.append({"path": s["path"], "error": f"unknown way {parts[1]!r}"})
            continue
        if len(parts) >= 3:
            if not parts[2].startswith("ph") or not parts[2][2:].isdigit():
                unknown.append({"path": s["path"], "error": f"phase segment must look like ph0/ph2, got {parts[2]!r}"})
                continue
        if len(parts) >= 4 and parts[3] not in known_goals:
            unknown.append({"path": s["path"], "error": f"unknown goal {parts[3]!r}"})
            continue
        if len(parts) > 4:
            unknown.append({"path": s["path"], "error": "skip path deeper than user/way/phase/goal"})
    if unknown:
        return [], [], unknown

    active, skipped = [], []
    for c in cases:
        hit = None
        for s in skips:
            if skip_matches(c, s["path"]):
                hit = s
                break
        if hit:
            skipped.append({**c, "status": "skipped", "skip_path": hit["path"], "skip_reason": hit.get("reason", "skip")})
        else:
            active.append(c)
    return active, skipped, []


def has_goal_path(fl, ks, goal_id: str, phase: int) -> bool:
    for k in ks:
        f = fl[k]
        if M.flow_phase(f) > phase:
            continue
        if f.get("result") == f"goal:{goal_id}":
            return True
    return False


def goal_exception(fl, fid, entry: str, goal_id: str):
    f = fl[fid]
    for x in f.get("goal_exceptions", []):
        if x.get("entry") == entry and x.get("goal") == goal_id:
            return x
    return None


def check_case(sc, fl, US, WAYS, GS, case: dict) -> dict:
    user = case["user"]
    way_id = case["way"]
    phase = int(case["phase"])
    goal_id = case["goal"]
    ud = US[user]
    fid = ud["main_flow"]
    way = WAYS[way_id]
    goal = GS[goal_id]
    out = {**case, "flow": fid}

    if not way_available(way, phase):
        out.update(status="skipped", skip_reason=f"way {way_id} starts at phase {way.get('phase')}, not available in phase {phase}")
        return out
    if not goal_available(goal, phase):
        out.update(status="skipped", skip_reason=f"goal {goal_id} starts at phase {goal.get('phase')}, not available in phase {phase}")
        return out
    if user not in way.get("users", []):
        out.update(status="skipped", skip_reason=f"way {way_id} is not for user {user}")
        return out

    # Already holding the goal on arrival counts as complete for this entry.
    if goal_id in (way.get("holds") or []):
        out.update(status="passed", detail="way holds this goal on arrival")
        return out

    entry, ks = match_entry(fl, fid, way, ud["auth"])
    if not ks:
        out.update(status="failed", detail=f"no flow entry matches way {way_id} on {fid}", classification_hint="missing-path")
        return out
    out["entry"] = entry

    GSU = M.load_goals(user=user)[0]
    g = GSU[goal_id]
    can = M.goal_reachable(sc, fl, ks, g, phase)
    has = has_goal_path(fl, ks, goal_id, phase)
    exc = goal_exception(fl, fid, entry, goal_id)

    if can and has:
        out.update(status="passed", detail=f"reachable via links ({can}) and modeled path exists", witness=can)
        return out
    if can and not has:
        if exc:
            out.update(status="passed", detail=f"source-tagged exception: {exc.get('reason','')}", exception=exc.get("reason"))
            return out
        out.update(
            status="failed",
            detail=f"goal screens reachable by real links ({can}) but no path from this entry reaches goal:{goal_id}",
            witness=can,
            classification_hint="missing-path",
        )
        return out
    # not can
    if has:
        # modeled path claims the goal but link-reachability of milestones failed
        out.update(
            status="failed",
            detail=f"flow paths claim goal:{goal_id}, but milestone screens are not reachable by real links in phase {phase}",
            classification_hint="design-gap",
        )
        return out
    out.update(status="passed", detail="n/a: goal milestone screens are not reachable from this entry (no coverage required)")
    return out


def parse_link_ref(ref: str):
    if ":" not in ref:
        return None, None
    a, b = ref.split(":", 1)
    return a, b


def recheck_proposal(sc, fl, US, WAYS, proposal: dict) -> dict:
    """Deterministically verify a proposed path uses existing links and reaches a goal-related state."""
    cid = proposal.get("case_id")
    kind = proposal.get("kind")  # missing-path | design-gap
    links = proposal.get("links") or []
    out = {"case_id": cid, "kind": kind, "accepted": False, "errors": []}
    if kind == "design-gap":
        out.update(accepted=False, note="design gaps are for Martin; not auto-applied")
        return out
    if kind != "missing-path":
        out["errors"].append(f"unknown proposal kind {kind!r}")
        return out
    if not cid:
        out["errors"].append("missing case_id")
        return out
    try:
        parts = path_parts(cid)
    except Exception:
        out["errors"].append(f"bad case_id {cid!r}")
        return out
    user, way_id, phase, goal_id = parts["user"], parts["way"], parts["phase"], parts["goal"]
    if user not in US or way_id not in WAYS or goal_id not in M.load_goals()[0]:
        out["errors"].append("unknown user/way/goal in case_id")
        return out
    ud = US[user]
    fid = ud["main_flow"]
    entry, ks = match_entry(fl, fid, WAYS[way_id], ud["auth"])
    if not ks:
        out["errors"].append("no matching entry for way")
        return out
    # Start from entry start state
    start = dict(fl[ks[0]]["start"])
    cur = dict(
        device=start.get("device", "phone"),
        root=start["screen"],
        kids=[("sheet", start["sheet"])] if start.get("sheet") else [],
        auth=start["auth"],
        live=start["live"],
        tab=start.get("tab") if start["screen"] == "home" else None,
        phase=phase,
    )
    if cur["root"] == "home" and not cur["tab"]:
        cur["tab"] = M.dmode(cur["live"], phase)
    hist = [cur]
    for i, ref in enumerate(links):
        own, lid = parse_link_ref(ref)
        if not own or not lid:
            out["errors"].append(f"step {i+1}: link must be screen:linkid, got {ref!r}")
            return out
        if own not in sc:
            out["errors"].append(f"step {i+1}: unknown screen {own!r}")
            return out
        found = None
        for l in sc[own].get("links", []):
            if l.get("id") == lid and M.matches(l.get("when", ""), cur):
                found = l
                break
        if not found:
            # also try without phase in condition match using available()
            own2, ls = M.find_link(sc, cur, f"{own}:{lid}")
            if not ls:
                out["errors"].append(f"step {i+1}: link {ref} not available in {M.key(cur)}")
                return out
            found = ls[0]
        n = M.resolve(sc, cur, found, own)
        if n is None:
            out["errors"].append(f"step {i+1}: link {ref} did not resolve from {M.key(cur)}")
            return out
        if n == "back":
            if len(hist) < 2:
                out["errors"].append(f"step {i+1}: back with no history")
                return out
            hist.pop()
            cur = dict(hist[-1])
        else:
            cur = n
            hist.append(n)
    # After walking, check goal milestones reachable / final state matches goal progress
    GSU = M.load_goals(user=user)[0]
    g = GSU[goal_id]
    keys = [M.key(s) for s in hist]
    advs = [None] * len(keys)
    pr, _ = M.progress({goal_id: g}, keys, advs, start.get("holds") or ())
    last = pr[-1] if pr else {}
    reached = last.get(goal_id, 0) >= len(g["ms"])
    # Also accept if final state matches last milestone states
    import fnmatch
    final = keys[-1]
    last_ms = g["ms"][-1]
    state_hit = any(fnmatch.fnmatchcase(final, p) for p in last_ms.get("states", []))
    if reached or state_hit:
        out.update(accepted=True, final_state=final, milestones_reached=last.get(goal_id, 0))
    else:
        out["errors"].append(
            f"walk ended at {final} after {len(links)} links; goal {goal_id} milestones {last.get(goal_id,0)}/{len(g['ms'])}"
        )
    return out


def run_checks(cfg, spread, skips) -> dict:
    sc, fl, ev, gl = M.load()
    US = M.load_users()
    WAYS = M.load_ways()
    GS, GSH, _ = M.load_goals()
    fp = model_fingerprint(Path(M.ROOT))

    if spread is None:
        spread = build_spread(sc, fl, US, WAYS, GS, cfg)
        spread_source = "generated"
    else:
        errs = validate_spread(spread, fp)
        if errs:
            return {
                "status": "blocked",
                "reason": "invalid_or_stale_spread",
                "errors": errs,
                "model_fingerprint": fp,
            }
        spread_source = "supplied"

    active, skipped, unknown = apply_skips(spread["cases"], skips, WAYS, US, GS)
    if unknown:
        return {
            "status": "blocked",
            "reason": "unknown_skip_selectors",
            "errors": unknown,
            "model_fingerprint": fp,
        }
    if not active and skipped:
        return {
            "status": "blocked",
            "reason": "all_cases_skipped",
            "detail": "every case was skipped; that is not a pass",
            "skipped": skipped,
            "counts": {"passed": 0, "failed": 0, "blocked": 1, "skipped": len(skipped)},
            "spread": spread,
            "spread_source": spread_source,
            "model_fingerprint": fp,
        }
    if not active and not skipped:
        return {
            "status": "blocked",
            "reason": "empty_spread",
            "detail": "no cases to check",
            "model_fingerprint": fp,
        }

    results = []
    for c in active:
        # structural applicability skips inside check_case also produce skipped
        results.append(check_case(sc, fl, US, WAYS, GS, c))
    results.extend(skipped)

    counts = {"passed": 0, "failed": 0, "blocked": 0, "skipped": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    failed = [r for r in results if r["status"] == "failed"]
    status = "failed" if failed else "passed"
    return {
        "status": status,
        "counts": counts,
        "cases": results,
        "failures": failed,
        "spread": spread,
        "spread_source": spread_source,
        "model_fingerprint": fp,
        "question": "Can users complete their goals?",
    }


def write_run(report: dict, out_dir: Path | None = None) -> Path:
    ts = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d-%H%M%S")
    run_dir = out_dir or (RUNS_DIR / ts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    if report.get("spread"):
        (run_dir / "spread.json").write_text(json.dumps(report["spread"], indent=2) + "\n")
    summary = {
        "status": report.get("status"),
        "counts": report.get("counts"),
        "failure_ids": [f.get("id") for f in report.get("failures", [])],
        "spread_source": report.get("spread_source"),
        "run_dir": str(run_dir),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return run_dir


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--spread", type=Path, help="Use this saved spread instead of generating one")
    ap.add_argument("--skip", action="append", default=[], help="Skip path user[/way[/phN[/goal]]]")
    ap.add_argument("--out-dir", type=Path, help="Write run outputs here")
    ap.add_argument("--stdout-json", action="store_true", help="Print full report JSON to stdout")
    ap.add_argument("--recheck-proposals", type=Path, help="JSON file of proposed fixes to recheck")
    ap.add_argument("--proposals-inline", type=str, help="Proposals JSON string (alternative to file)")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    # optional args override config lists when provided via env-style? kept simple: CLI skips merge
    skips = parse_skips(cfg.get("skips"), [{"path": s} for s in args.skip])

    if args.recheck_proposals or args.proposals_inline:
        sc, fl, ev, gl = M.load()
        US = M.load_users()
        WAYS = M.load_ways()
        if args.proposals_inline:
            proposals = json.loads(args.proposals_inline)
        else:
            proposals = json.loads(args.recheck_proposals.read_text())
        if isinstance(proposals, dict) and "proposals" in proposals:
            proposals = proposals["proposals"]
        results = [recheck_proposal(sc, fl, US, WAYS, p) for p in proposals]
        report = {
            "status": "recheck",
            "results": results,
            "accepted": sum(1 for r in results if r.get("accepted")),
            "rejected": sum(1 for r in results if not r.get("accepted")),
        }
        run_dir = write_run(report, args.out_dir)
        report["run_dir"] = str(run_dir)
        print(json.dumps(report if args.stdout_json else {"status": report["status"], "accepted": report["accepted"], "rejected": report["rejected"], "run_dir": str(run_dir)}, indent=2))
        return 0

    spread = None
    spread_path = args.spread or (Path(cfg["spread_path"]) if cfg.get("spread_path") else None)
    if spread_path:
        spread = json.loads(Path(spread_path).read_text())

    report = run_checks(cfg, spread, skips)
    run_dir = write_run(report, args.out_dir)
    report["run_dir"] = str(run_dir)
    if args.stdout_json or report.get("status") == "blocked":
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps({
            "status": report["status"],
            "counts": report.get("counts"),
            "failure_ids": [f.get("id") for f in report.get("failures", [])],
            "run_dir": str(run_dir),
            "spread_source": report.get("spread_source"),
        }, indent=2))
    return 0 if report.get("status") in ("passed", "recheck") else 1


if __name__ == "__main__":
    raise SystemExit(main())
