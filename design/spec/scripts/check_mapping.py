#!/usr/bin/env python3
"""Check design/spec/mapping/phases.toml against the mock model.

Fails if a cited screen, link, event, or way is missing, or is not
available in the phase that claims to deliver the sub-feature.
Deterministic. No network.
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

SCRIPT = Path(__file__).resolve()
SPEC = SCRIPT.parents[1]
REPO = SPEC.parents[1]
MOCKUPS = REPO / "design" / "mockups"
MAPPING = SPEC / "mapping" / "phases.toml"

sys.path.insert(0, str(MOCKUPS))
import gen.model as model  # noqa: E402


def load_mapping() -> dict:
    return tomllib.loads(MAPPING.read_text())


def event_by_id(ev, eid: str):
    for e in ev.get("events") or []:
        if e.get("id") == eid:
            return e
    return None


def links_named(screen: dict, lid: str) -> list[dict]:
    return [ln for ln in (screen.get("links") or []) if ln.get("id") == lid]


def main() -> int:
    mp = load_mapping()
    sc, _fl, ev, _gl = model.load()
    ways = model.load_ways()
    phases = [p["id"] for p in mp["phase"]]
    # phases must be the current model ids, in the same order
    errors: list[str] = []
    if phases != model.PIDS:
        errors.append(
            f"mapping phases {phases} do not match model.PIDS {model.PIDS}"
        )

    features = {f["id"]: f for f in mp["feature"]}
    delivered_by = {p["id"]: set(p["delivers"]) for p in mp["phase"]}

    # Every delivered id has a feature entry; later phases keep earlier deliveries.
    prev: set[str] = set()
    for i, pid in enumerate(phases):
        got = delivered_by[pid]
        unknown = got - set(features)
        if unknown:
            errors.append(f"phase {pid} delivers unknown sub-features: {sorted(unknown)}")
        if not prev.issubset(got):
            errors.append(
                f"phase {pid} dropped sub-features delivered earlier: {sorted(prev - got)}"
            )
        prev = got

    for fid, feat in features.items():
        earliest = feat["must_be_available"]
        if earliest not in delivered_by:
            errors.append(f"{fid}: must_be_available {earliest!r} is not a mapping phase")
            continue
        # The earliest phase and every later one must list the feature.
        start = phases.index(earliest) if earliest in phases else None
        if start is None:
            continue
        for pid in phases[start:]:
            if fid not in delivered_by[pid]:
                errors.append(f"{fid}: delivered in mapping from {earliest}, but {pid} does not list it")
        # Earlier phases must not list it (the mock doesn't have it yet).
        for pid in phases[:start]:
            if fid in delivered_by[pid]:
                errors.append(f"{fid}: listed on {pid}, but must_be_available is {earliest}")

        for item in feat.get("item") or []:
            kind = item["kind"]
            iid = item["id"]
            if kind == "note":
                if not item.get("source"):
                    errors.append(f"{fid}: note {iid} has no source")
                continue
            # Check existence and availability in every phase that delivers this feature.
            check_phases = phases[start:] if start is not None else phases
            for pid in check_phases:
                if kind == "screen":
                    if iid not in sc:
                        errors.append(f"{fid}: screen {iid} does not exist (cited from {item.get('source')})")
                        break
                    if not model.in_phase(sc[iid], pid):
                        errors.append(f"{fid}: screen {iid} is not available in phase {pid}")
                elif kind == "event":
                    e = event_by_id(ev, iid)
                    if e is None:
                        errors.append(f"{fid}: event {iid} does not exist (cited from {item.get('source')})")
                        break
                    if not model.in_phase(e, pid):
                        errors.append(f"{fid}: event {iid} is not available in phase {pid}")
                elif kind == "way":
                    if iid not in ways:
                        errors.append(f"{fid}: way {iid} does not exist (cited from {item.get('source')})")
                        break
                    if not model.in_phase(ways[iid], pid):
                        errors.append(f"{fid}: way {iid} is not available in phase {pid}")
                elif kind == "link":
                    if ":" not in iid:
                        errors.append(f"{fid}: link id {iid!r} must be screen:link")
                        break
                    screen_id, link_id = iid.split(":", 1)
                    if screen_id not in sc:
                        errors.append(f"{fid}: link {iid} — screen {screen_id} does not exist")
                        break
                    if not model.in_phase(sc[screen_id], pid):
                        errors.append(f"{fid}: screen {screen_id} for link {iid} is not available in phase {pid}")
                        continue
                    named = links_named(sc[screen_id], link_id)
                    if not named:
                        errors.append(f"{fid}: link {iid} does not exist (cited from {item.get('source')})")
                        break
                    if not any(model.in_phase(ln, pid) for ln in named):
                        errors.append(f"{fid}: link {iid} is not available in phase {pid}")
                else:
                    errors.append(f"{fid}: unknown item kind {kind!r}")
                    break

    if errors:
        print(f"mapping check FAILED ({len(errors)} problem{'s' if len(errors) != 1 else ''})")
        for e in errors:
            print(f"  - {e}")
        return 1
    nfeat = len(features)
    print(f"mapping check OK: {nfeat} sub-features, {len(phases)} phases, all cited model items exist and are available.")
    for pid in phases:
        print(f"  {pid}: {len(delivered_by[pid])} sub-features")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
