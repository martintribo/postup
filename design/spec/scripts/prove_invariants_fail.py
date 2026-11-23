#!/usr/bin/env python3
"""Show each invariant failing once on a broken variant (able to fail).

The good model is not weakened. Each broken config sets Bug to a
deliberate fault, or (for JoinerCanLeaveNow) uses the real first-phase
delivered set, where leave is intentionally absent [M1037].
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
SPEC = SCRIPT.parents[1]
sys.path.insert(0, str(SCRIPT.parent))
import tlc_util  # noqa: E402

CONFIGS = SPEC / "tla" / "configs"
OUT = SPEC / "tla" / "out" / "broken"

# invariant -> (cfg file, why this variant should fail)
CASES = [
    (
        "TypeOK",
        "broken-bad-type.cfg",
        "Initial status is the illegal value 'bogus'.",
    ),
    (
        "NoJoinWhenClosed",
        "broken-join-when-full.cfg",
        "Join is allowed when the postup is already full, and sets illegalJoin.",
    ),
    (
        "EndedLinkNeverLive",
        "broken-ended-link-live.cfg",
        "An ended-link start is allowed to show status=live.",
    ),
    (
        "AskOnlyWhenDelivered",
        "broken-requested-without-ask.cfg",
        "Someone is already in 'requested' even though ask-to-join is not delivered.",
    ),
    (
        "FullOnlyWhenFillsDelivered",
        "broken-full-without-fills.cfg",
        "Status is already 'full' even though the size-limit feature is not delivered.",
    ),
    (
        "WayOutToEnded",
        "broken-no-way-to-end.cfg",
        "End now, time running out, and cancelled are all disabled on a still-open postup.",
    ),
]


def first_failed(output: str) -> str | None:
    for line in output.splitlines():
        if "Invariant " in line and " is violated" in line:
            return line.split("Invariant ", 1)[1].split(" is violated", 1)[0].strip()
    return None


def main() -> int:
    worst = 0
    print("Able-to-fail proofs (broken variants, not the real model)")
    print()
    for inv, cfg_name, why in CASES:
        cfg = CONFIGS / cfg_name
        out = OUT / inv
        print(f"## {inv}")
        print(f"   variant: {cfg_name}")
        print(f"   because: {why}")
        if not cfg.exists():
            print("   FAIL: missing config")
            worst = 1
            print()
            continue
        result = tlc_util.run_tlc(cfg, out)
        failed = result["failed_invariant"] or first_failed(result["output"])
        if result["ok"]:
            print("   UNEXPECTED PASS — this invariant did not fail on the broken variant")
            print(f"   log: {result['log']}")
            worst = 1
        elif failed == inv:
            print(f"   FAILED AS INTENDED ({failed})")
            print(f"   log: {result['log']}")
        else:
            print(f"   FAILED, but not the expected invariant (got {failed!r})")
            print(f"   log: {result['log']}")
            worst = 1
        print()

    # JoinerCanLeaveNow on the real post-and-join delivered set.
    print("## JoinerCanLeaveNow")
    print("   variant: real post-and-join delivered set (leave not shipped) [M1037]")
    print("   because: a joiner has no Leave action in the first phase.")
    cfg = CONFIGS / "post-and-join.cfg"
    # post-and-join.cfg does not include JoinerCanLeaveNow; add it.
    out = OUT / "JoinerCanLeaveNow"
    result = tlc_util.run_tlc(cfg, out, extra_invariants=["JoinerCanLeaveNow"])
    failed = result["failed_invariant"] or first_failed(result["output"])
    if result["ok"]:
        print("   UNEXPECTED PASS — JoinerCanLeaveNow held in post-and-join")
        print(f"   log: {result['log']}")
        worst = 1
    elif failed == "JoinerCanLeaveNow":
        print("   FAILED AS INTENDED (JoinerCanLeaveNow)")
        print(f"   log: {result['log']}")
    else:
        print(f"   FAILED, but not the expected invariant (got {failed!r})")
        print(f"   log: {result['log']}")
        worst = 1
    print()
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
