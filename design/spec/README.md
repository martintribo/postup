# Feature models (prototype)

This folder is an additive prototype on `proto/feature-models`. It does
not change `phases.toml` semantics or the mockup build.

The idea: when a feature is introduced it gets an open model of its
full intended scope. Each phase declares which sub-features it delivers.
A plan talks about features completed to a degree (not about phases)
and states checks that are verified against the model restricted to the
delivered set.

Start here with the postup lifecycle (cancel, extend, end, join, leave,
fills up, time runs out, host leaves, ended link opened).

## Layout

- `areas/postup-lifecycle.md` — feature map (full intended scope, including future questions).
- `mapping/phases.toml` — which sub-features each current phase delivers, with citations into the mock model.
- `scripts/check_mapping.py` — fails if the mapping and the mock model drift.
- `tla/PostupLifecycle.tla` — situations × events; each action tagged with a sub-feature id; `Delivered` selects the set.
- `tla/configs/` — one config per phase, plus broken variants used only to show that each invariant can fail.
- `tla/views/view.mjs` — words on the chart (`/statechart --view`).
- `plans/mvp-release.toml` — plan items (feature degrees, rationale, invariants).
- `scripts/run_plan.py` — for each item, earliest delivering phase, then TLC.
- `scripts/prove_invariants_fail.py` — each invariant failing once on a broken variant.
- `tla/charts/` — checked-in `chart.mmd` from a statechart run (see below).
- `tla/out/` — rerun logs; not committed.

## Tools

TLC needs Java and `tla2tools.jar`. The first `/statechart` run installs
them with mise (`java@temurin-25`, tla2tools v1.7.4). You can also
install ahead of time:

```
mise install java@temurin-25 'http:tla2tools[url=https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar,checksum=sha256:936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88]@1.7.4'
```

Or set `JAVA` (path to the `java` binary) and `TLA2TOOLS` (path to
`tla2tools.jar`) and skip mise. For the readable chart, use `/statechart`
(pstack skill). Do not hard-code a path to the statechart CLI here; the
skill owns how it is invoked.

## Cheap rerun

From the repo root (this worktree):

```
python3 design/spec/scripts/check_mapping.py
python3 design/spec/scripts/prove_invariants_fail.py
python3 design/spec/scripts/run_plan.py
```

Then `/statechart` on `design/spec/tla/PostupLifecycle.tla` with
`--config design/spec/tla/configs/share-and-chat.cfg` and
`--view design/spec/tla/views/view.mjs`, writing a fresh `--out`
folder. Copy `chart.mmd` to `design/spec/tla/charts/share-and-chat.mmd`
if the chart should stay in the branch.

## Coverage (honest scope)

This prototype models one person's situation relative to one postup:
visiting, joined, hosting, or asked to join; and the postup as live,
full, ended, or cancelled; plus whether they arrived in the app, on a
live shared link, or on an already-ended link.

It does not model: accounts and sign-in, nearby lists, chat, projects
beyond the ask-to-join path, more than one postup at a time, more than
one person as separate actors (the "who" variable is the person we are
following), clocks other than "time runs out" / "add 30 minutes", or
`postups-end` (all nearby postups ending). Host cancel-before-anyone-joins
is a question, not a rule ([M1049-draft]). Extend has no model link; the
spec only says the postup stays live.

Findings stay findings. Do not weaken an invariant to make a run pass.

## Sync record

When this folder changes, record the commit, the three script results,
and the statechart `--out` folder in the commit message or in
`VERIFY.md`.
