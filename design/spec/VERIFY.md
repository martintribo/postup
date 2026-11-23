# Sync record — feature-models prototype

Recorded after the first complete run on `proto/feature-models`.
Rerun the commands below from the worktree root. Logs under `tla/out/` are not committed.

## Commands

```
python3 design/spec/scripts/check_mapping.py
python3 design/spec/scripts/prove_invariants_fail.py
python3 design/spec/scripts/run_plan.py
```

For the chart, use `/statechart` on `design/spec/tla/PostupLifecycle.tla` with
`--config design/spec/tla/configs/share-and-chat.cfg`,
`--view design/spec/tla/views/view.mjs`, and a fresh `--out` folder.
Copy `chart.mmd` to `design/spec/tla/charts/share-and-chat.mmd` if it should stay in the branch.

Java and tla2tools: mise `java@temurin-25` and tla2tools v1.7.4, or set `JAVA` and `TLA2TOOLS`.

## Results (22 Nov 2026, America/Los_Angeles)

- `check_mapping.py`: OK. 12 sub-features, 3 phases; every cited screen, link, event, and way exists and is available in the phases that claim it.
- `prove_invariants_fail.py`: each invariant failed as intended on its broken variant (TypeOK, NoJoinWhenClosed, EndedLinkNeverLive, AskOnlyWhenDelivered, FullOnlyWhenFillsDelivered, WayOutToEnded). `JoinerCanLeaveNow` failed as intended on the real `post-and-join` delivered set (leave is not shipped, [M1037]).
- `run_plan.py`:
  - `join-and-close` — earliest phase `post-and-join` — PASS
  - `share-leave-and-fill` — earliest phase `share-and-chat` — PASS
  - `ask-to-join` — earliest phase `projects` — PASS
  - `demo-leave-too-early` — DEMO, expected to fail — failed on `JoinerCanLeaveNow` as intended (not a product claim)
- Good-model TLC: `post-and-join` 9 distinct states; `share-and-chat` 25; `projects` / `all-features` 33. No errors.
- `/statechart` on `share-and-chat`: 12 chart states, 18 arrows. Chart at `tla/charts/share-and-chat.mmd`. The view hides live-link vs in-app entry and the +30 mark so the chart stays readable; those steps still exist in the TLA+ model.

## Findings that stay findings

- In `post-and-join`, a joiner has no Leave. That is intentional ([M1037]), not a missing screen. The demo plan item exists to show that a plan check can fail readably if someone asks for leave too early.
- The +30 min extend control is drawn and phase-gated from `share-and-chat` onward, but there is no model link in `live.toml`.
- Event `postup-cancelled` and screen `#postup-cancelled` are in every phase, but the host's only close control is "End postup". Whether "cancel before anyone joins" is a different product path is an open question ([M1049-draft]).
- After leaving, the mock lands you on `#postup` (the same postup, as a visitor). Whether you can join again is not spelled out ([M1049-draft]).
- Whether a host can extend a postup that is already full is not spelled out. The spec allows extend only while status is live ([M1049-draft]).
- There is no separate "host leaves but the postup continues" path. The host ends now, or time runs out.

## Honest scope

One person, one postup: visiting / joined / hosting / asked to join, and live / full / ended / cancelled. Not modeled: accounts, nearby lists, chat, projects beyond ask-to-join, several people as separate actors, clocks other than time-runs-out / add-30-minutes, or `postups-end` (all nearby postups ending).
