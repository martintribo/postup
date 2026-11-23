# Mockup validation

## Goal reachability (`goal-reachability`)

Answers: **Can users complete their goals?**

- Config: `goal-reachability.toml` (checked in)
- Default scope is every phase in `model/phases.toml` (omit `phases` in the config). Case ids use phase ids (aliases like `ph0` still work in skip lists).
- Deterministic checker: `../gen/goal_reachability.py`
- Grok Build workflow: `../../../.grok/workflows/goal-reachability.rhai`
- Run outputs: `runs/<timestamp>/` (gitignored)

Direct check (no Grok Build required):

```bash
cd design/mockups
python3 gen/goal_reachability.py
```

Workflow (Grok Build TUI, from the PostUp repo):

```text
/workflow goal-reachability
/workflow goal-reachability {"dry_run_check_only": true}
/workflow goal-reachability {"spread_path":"design/mockups/validation/runs/YYYYMMDD-HHMMSS/spread.json"}
/workflow goal-reachability {"skips":["newcomer/home-none"]}
```

Read-only: findings and proposed fixes only. Model edits need Martin’s approval and `edit-mockup-model`.
