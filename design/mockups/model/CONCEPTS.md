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

- `situations.toml` has `groups` (id, title, order: high-level groupings shared across user types) and situations: `id`, `group`, `user` (newcomer | registered), a plain-words `title`, a source-tagged `setting` line, and an optional `phase`.
- Every flow has `situation = "<id>"`. The validator fails if the situation doesn't exist or is for the other user type.
- `flows/map.html` is the flow map by situation: one map per user type (`#newcomer`, `#registered`), with buttons that open the flows. The old user-state map is now `flows/map-states.html`.

## Phases (MVP pruning) [M1031-draft]

- `phase` is an optional positive integer on a flow, a screen, or a site state. Untagged means unclassified: it is kept, not deleted.
- Site-state overrides go in a `[state_phases]` table in `global.toml` or in a screen file, keyed by state id, e.g. `"postup+signin@out.live" = 2`.
- Derived phase: a screen or state that a phase-N flow passes through is phase N, unless it is tagged. The lowest phase wins.
- The validator fails if a phase-1 flow uses a screen or state that is explicitly tagged with a later phase.
- Flows also have `user = "newcomer"` (signed out, never used) or `"registered"` (signed in), which must match the start state's `auth`. The old `mvp` flag is gone: phase 1 replaces `mvp = true`. The MVP checkboxes in the flow pages now start from phase 1.
- Phase 1 is a pre-MVP step; phase 2 is the MVP, so the MVP is phases 1 and 2. [M1032]
- The views (flows index and grid, site map, site graph, states, maps) have a toggle that cycles "Phase: all" → "1 (pre-MVP)" → "≤2 (MVP)", and mark items with a P1 or P2 badge. [M1032]
- Merged flows keep their old ids in `aliases`; the old flow pages redirect to the merged flow. [M1032]

## Phase versions of a screen [M1035]

- **View phase** is a site-state dimension like `auth`, with values 1 and 2. It is not written in the state id: `inbox@in.live` is the same state in both phases, but it can render and link differently.
- **Which phase renders:** a phase-N flow walks and renders phase-N versions. An untagged flow, and the "All" view, use the latest phase (2).
- **Conditions:** `when` and `variants` keys accept `phase=1`, `phase>=2` or `phase<=1`, combined like any other key: `when = "live=live,tab=live,phase>=2"`; alternatives are still separated by `;`. A link with no phase condition exists in every phase.
- **HTML:** one chunk per screen holds both versions. Give an element `class="p2only"` to show it only in phase 2+, or `class="p1only"` to show it only in phase 1. `gen/phasev.py` marks every element that links to a phase-2 screen (projects, Activity) as `p2only` automatically, so phase-1 links to them don't need hand edits.
- **Mockup:** `html[data-vph]` comes from `?ph=` if present, otherwise from the shared Phase toggle (`localStorage pu-ph1`; "1" means phase 1, anything else means the latest). The mockup index has the same switch. `#inbox-one` redirects to `#inbox`.
- **Phase 1 has no Building mode on Home:** `dmode()` returns `live` there, and a phase-1 flow may not start in `.building`.
- **Validator:** each flow is replayed in its phase. The drift check parses each screen's phase-1 and phase-2 HTML separately (dropping `p2only` and `p1only` respectively) and compares them with the model links valid in that phase. The tab bar and rail are checked the same way.
- **Views:** flow players and their thumbnails load `?ph=<flow phase>`. The site map swaps in `pages/<id>--p1.webp` when the toggle is 1. On "All", the states view lists the P1 and P2 version of each state for screens that have versions. The site graph's edges are the union of both phases.
- **Screens with phase versions (from `flows/sitegraph.json` `versions`):** inbox (P1 one list, P2 Chats | Activity), the tab bar and desktop rail (no Projects in P1), and home (no Live | Building switch and no project tags in P1). Also every screen whose project links are phase 2: cafe, cafe-gfail, invite, joined, live, me, offline, post, post-edit, posted, postup, profile, quiet, quiet-feed, quiet-feed-b, where, where-search, and home-overlay-alt.

### Conventions for editing (edit-mockup-model) [M1035]

1. To drop something from phase 1, tag the target screen `phase = 2`. Then add `phase>=2` to the links that point to it on screens phase 1 still uses. The HTML for those links is hidden automatically.
2. To add phase-1-only content, wrap it in `class="p1only"` and add its links with `when = "...,phase=1"`.
3. Don't make a separate screen for a phase version, the way `inbox-one` used to be. Put both versions in one screen.

## Edit, then build

Edit the `.toml` files and, if a link changes, the HTML in `gen/*.py` as well. Then run `python3 gen/build.py`. `INDEX.md` is generated and lists every screen and flow on one line each. Every note line needs a source tag such as [FS], [F###], [M1031-draft] or [drawn].
