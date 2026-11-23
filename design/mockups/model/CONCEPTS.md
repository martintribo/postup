# PostUp mockup model: concepts

The model in `model/` is the single source for the mockup's screens, links, notes and flows. `gen/build.py` validates it first (`gen/validate.py`) and stops if there is any error or design gap. The screen HTML is still drawn by hand in `gen/*.py`. The build compares the two and fails if a link the HTML renders is missing from the model, or the reverse.

## Vocabulary

- **Screen**: a file in `screens/<id>.toml`. Its `kind` is one of these:
  - `page`: a full screen with a URL, `#<id>`.
  - `sheet`, `modal`, `drawer`: a child screen that opens inside a slot.
  - `tab`, `panel`: chrome, meaning the phone tab bar (`tabbar`) or the desktop rail (`rail`).
  - Every screen has a title, a group, notes, and its links.
  - A sheet also names its `host`, the page its notes URL shows it over.
- **Slot**: a named place on a screen that holds child screens. Fields: `name`, `kind` (sheet | modal | drawer | panel | tab), `accepts` (the list of screens it can hold) and an optional `device`.
  - Pages declare a `sheet` slot.
  - Pages that show the tab bar declare a `nav` tab slot for phone.
  - Every page has a `rail` panel slot for desktop.
  - Chrome links count only when no sheet is open.
- **Link**: one thing the user can tap. Fields: `id`, a short id that is unique per screen for any one condition; `label`; and `action`. The actions are:
  - `replace`: go to another page.
  - `open`: put a child into a slot.
  - `swap`: replace the open child, or change state on this screen.
  - `close`: close the top child.
  - `back`: return to the previous state.

  Links have these optional fields:
  - `to`
  - `slot`
  - `sets`: changes a dimension, e.g. `auth=in` or `tab=building`.
  - `when`: the conditions under which the link exists. Syntax is `k=v,k=v;alt`.
  - `then`: on an `open`, the page to continue to.
  - `continue`: on a child's `close`, go to the opener's `then`. This is how sign-in continues to Join, Ask or Post up.

  Flows refer to a link as `screen:id`.
- **Variants**: `variants = { "auth=out" = "inbox--out", ... }` maps a condition to the HTML element that draws it. The first match wins; otherwise the screen id is used.
- **Site state**: `page[+child]@auth.live[.tab]`, e.g. `postup+signin@out.live` or `home@in.none.building`. The dimensions are:
  - `auth`: `out` or `in`.
  - `live`: `live` or `none`. It means someone is live nearby, which is global. A postup's own status (full, cancelled or ended) is its page, not `live`.
  - `tab`: Home's Live or Building tab.
- **Events and conditions** (`events.toml`):
  - Events are things that happen without a tap, such as an alert, a postup ending, someone you follow posting up, or the network dropping.
  - Conditions are site data, such as a Google card failing or an area with no postups.
- **Flow** (`flows/<id>.toml`): a start state and then steps. Each step is one of:
  - `arrive`, for the first step.
  - `link = "screen:id"`.
  - `event = "<id>"`.
  - `gap`, which fails the build.

  Each step also has `act` (what the user does), `expect` (the site state it must reach), `thought` and `shows`. Steps that take two taps are written as two steps.
- **Sign-in**: one `signin` sheet. The old `#join-signin`, `#ask-signin`, `#post-signin` and `#attach-signin` URLs still work: they redirect to the page with the sheet open.

## Situations [M1031-draft]

- `situations.toml` has `groups` (id, title, order: high-level groupings shared across user types) and situations: `id`, `group`, `user` (newcomer | registered), a plain-words `title`, a source-tagged `setting` line, and optional `since` / `until` (see Phases).
- Every flow has `situation = "<id>"`. The validator fails if the situation doesn't exist or is for the other user type.
- `flows/map.html` is the flow map by situation: one map per user type (`#newcomer`, `#registered`), with buttons that open the flows. The old user-state map is now `flows/map-states.html`.

## Phases [M1047-draft]

- Phases are an ordered list of stable string ids in `model/phases.toml`. The current ids, named for the scope each phase adds, are `post-and-join`, `share-and-chat`, and `projects` [M1048] (Martin, Nov 22 2026). User-facing labels are **Phase 0: Post & join**, **Phase 1: Share & chat**, and **Phase 2: Projects** (badges `0` / `1` / `2`). Numeric aliases `0`, `p0`, `ph0`, `1`, `p1`, `ph1`, `2`, `p2`, `ph2` still resolve, as do the previous ids `smallest`, `pre-mvp`, and `mvp`, so saved URLs, `localStorage` `pu-ph1` values, and goal-reachability skip lists keep working.
- Phase ids and screen ids are different namespaces. The phase id `projects` is also a screen id. The screen is `#projects`. The phase uses prefixed classes and attributes only: `since-projects`, `until-…`, `only-…`, `html[data-vph="projects"]`, `data-vp`, `data-ph`, `html.ph-projects`. Never use a bare `#projects` or `id="projects"` to mean the phase.
- Availability uses `since` and `until` (inclusive phase ids) on screens, ways, goals, flows, outcomes, links, and events. **Do not use `from`:** outcomes already use `from` as the branch source. Untagged (no `since` / `until`) means the item exists in **every** phase.
- Each `[[phases]]` block may list a delta vs the previous phase (`add`, `hide`, `replace`) and a `deliverable` (goals that must be reachable, plus named rules that must hold). A newly inserted phase that omits `deliverable` / `rules` inherits the previous phase. An empty delta means the same content as the previous phase.
- Named rules currently: `no-share`, `no-inbox`, `no-chat`, `no-leave`, `no-projects`, `no-ask-to-join`, `no-building-mode`, `no-size-limit`.
- `[[exceptions]]` are explicit, source-tagged allowances for a named check (for example `way-path-in-phase`) so a known design question can stay visible without loosening the validator.
- Flows also have `user = "newcomer"` or `"registered"`, which must match the start state's `auth`. Merged flows keep their old ids in `aliases`. [M1032]
- The views have a toggle that cycles **All → each phase in list order**. All **lists every item** and **renders the latest** phase (the last block in `phases.toml`). Items are badged from `badge` in `phases.toml`.

## Phase versions of a screen [M1035] [M1047-draft]

- **View phase** is a site-state dimension like `auth`. It is not written in the state id: `inbox@in.live` is the same state in every phase, but it can render and link differently.
- **Which phase renders:** a flow with `since` walks and renders that phase. An untagged flow, and the All view, use the latest phase.
- **Conditions:** do not put `phase=`, `phase>=` or `phase<=` in `when`. Put `since` / `until` on the link (or screen, flow, event) itself. A link with neither exists in every phase.
- **HTML:** one chunk per screen holds every version. Classes are generated from the ordered list: `since-<id>`, `until-<id>`, `only-<id>` (replacing the old `p2only` / `p1up` / `p1only` / `p0only`). `data-ph` is `"all"` or a space-separated list of ids the item is available in. `gen/phasev.py` auto-marks elements that link to a screen whose `since` is not the first phase.
- **Mockup:** `html[data-vph]` comes from `?ph=` if present (id or alias `0` / `1` / `2`), otherwise from the shared Phase toggle (`localStorage pu-ph1`: `"all"` or a phase id; legacy `0` means All, `p0` / `1` / `2` still resolve). All / missing / empty renders the latest phase. The mockup index has the same switch. `#inbox-one` redirects to `#inbox`.
- **Building mode:** the `no-building-mode` rule (on `smallest` and `pre-mvp` today) makes `dmode()` return `live`, and a flow in that phase may not start in `.building`.
- **Validator:** `gen/phasechk.py` (from `gen/validate.py`) checks monotonicity, link and event targets, each phase's deliverable goals, and named rules. The drift check parses each screen once per phase (dropping the generated classes that do not apply) and compares it with the model links valid in that phase.
- **Views:** flow players and thumbnails load `?ph=<walk phase id>`. The site map swaps in `pages/<id>--p<badge>.webp` for every phase except the latest (`--p0`, `--p1` today). On All, the states view lists each phase version of a screen that has versions. The site graph's edges are the union of every phase. `window.PU_PHASES` is injected at build time from `phases.toml`.
- **Screens with phase versions (from `flows/sitegraph.json` `versions`):** derived at build time from `since` / `until` on links and from `since-` / `until-` / `only-` classes in the HTML (tab bar aside). Today that includes inbox (one list until pre-mvp, Chats | Activity since mvp), the tab bar and desktop rail (Projects since mvp), and home (no Live | Building switch and no project tags before mvp), plus every screen whose project links are since mvp.

### Conventions for editing (edit-mockup-model) [M1035] [M1047-draft]

1. To introduce something in a later phase, set `since = "<id>"` on the screen (or link, flow, event). List it in that phase's `add` in `phases.toml`. `phasev.py` hides links to it in earlier phases automatically.
2. To drop something after a phase, set `until = "<id>"` or add it to a later phase's `hide`. For a short-lived visual, use `class="until-<id>"` or `class="only-<id>"` and the matching `since` / `until` on its links.
3. Don't make a separate screen for a phase version, the way `inbox-one` used to be. Put both versions in one screen.
4. Don't loosen the validator to hide a real design gap. If a check surfaces a product question, add an explicit, source-tagged `[[exceptions]]` in `phases.toml` and flag it for Martin.

## Edit, then build

Edit the `.toml` files and, if a link changes, the HTML in `gen/*.py` as well. Then run `python3 gen/build.py`. `INDEX.md` is generated and lists every screen and flow on one line each. Every note line needs a source tag such as [FS], [F###], [M1031-draft] or [drawn].
