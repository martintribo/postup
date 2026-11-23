#!/usr/bin/env python3
"""Run plans/mvp-release.toml: for each item, find the earliest phase
that delivers the required sub-features, run TLC with that phase's
delivered set, and report pass/fail.

A plan item with demo = true and expected = "fail" is a deliberate
failure sample. It counts as a runner success when TLC reports the
expected invariant violation.
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

SCRIPT = Path(__file__).resolve()
SPEC = SCRIPT.parents[1]
sys.path.insert(0, str(SCRIPT.parent))
import tlc_util  # noqa: E402

PLAN = SPEC / "plans" / "mvp-release.toml"
MAPPING = SPEC / "mapping" / "phases.toml"
OUT = SPEC / "tla" / "out" / "plan"
CONFIGS = SPEC / "tla" / "configs"


def load() -> tuple[dict, dict]:
    return tomllib.loads(PLAN.read_text()), tomllib.loads(MAPPING.read_text())


def fmt_set(ids: list[str]) -> str:
    return ", ".join(f'"{i}"' for i in ids)


def write_cfg(path: Path, delivered: list[str], invariants: list[str]) -> None:
    inv = "\n".join(f"  {i}" for i in invariants)
    path.write_text(
        "SPECIFICATION Spec\n"
        "CONSTANTS\n"
        f"  Delivered = {{{fmt_set(delivered)}}}\n"
        '  Bug = "none"\n'
        "INVARIANTS\n"
        f"{inv}\n"
        "VIEW vars\n"
        "CHECK_DEADLOCK FALSE\n"
    )


def earliest_phase(requires: set[str], phases: list[dict]) -> dict | None:
    for p in phases:
        if requires.issubset(set(p["delivers"])):
            return p
    return None


def first_failed_name(output: str, wanted: list[str]) -> str | None:
    for line in output.splitlines():
        if "Invariant " in line and " is violated" in line:
            name = line.split("Invariant ", 1)[1].split(" is violated", 1)[0].strip()
            return name
    for name in wanted:
        if name in output and "violat" in output.lower():
            return name
    return None


def main() -> int:
    plan, mapping = load()
    phases = mapping["phase"]
    items = plan["item"]
    print(f"Plan: {plan.get('title', PLAN.name)}")
    print()
    worst = 0
    for item in items:
        iid = item["id"]
        label = item.get("label", iid)
        demo = bool(item.get("demo")) or item.get("expected") == "fail"
        requires = set(item["requires"])
        invs = list(item["invariants"])
        phase = earliest_phase(requires, phases)
        print(f"## {iid}: {label}")
        if demo:
            print("   [DEMO — expected to fail; not a product claim]")
        print(f"   requires: {', '.join(item['requires'])}")
        if phase is None:
            print("   FAIL: no current phase delivers all required sub-features")
            worst = 1
            print()
            continue
        delivered = list(phase["delivers"])
        print(f"   earliest phase: {phase['id']} ({len(delivered)} sub-features delivered)")
        print(f"   checks: {', '.join(invs)}")
        out = OUT / iid
        cfg = out / "item.cfg"
        out.mkdir(parents=True, exist_ok=True)
        write_cfg(cfg, delivered, invs)
        result = tlc_util.run_tlc(cfg, out)
        failed = result["failed_invariant"] or first_failed_name(result["output"], invs)
        if demo:
            if not result["ok"] and failed:
                print(f"   DEMO FAIL (as intended): {failed}")
                # Print a short readable excerpt
                excerpt = []
                for line in result["output"].splitlines():
                    if "Error:" in line or "violat" in line.lower() or line.startswith("State") or "status" in line:
                        excerpt.append(line)
                    if len(excerpt) >= 12:
                        break
                if excerpt:
                    print("   ---")
                    for line in excerpt:
                        print(f"   {line}")
                    print("   ---")
                print(f"   log: {result['log']}")
            elif not result["ok"]:
                print("   DEMO FAIL (as intended), but TLC did not name an invariant:")
                print("   " + result["output"].splitlines()[-8:][0] if result["output"] else "   (no output)")
                print(f"   log: {result['log']}")
            else:
                print("   UNEXPECTED PASS: this demo item was supposed to fail")
                print(f"   log: {result['log']}")
                worst = 1
        else:
            if result["ok"]:
                print("   PASS")
                print(f"   log: {result['log']}")
            else:
                print(f"   FAIL: {failed or 'see log'}")
                print(f"   log: {result['log']}")
                worst = 1
        print()
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
