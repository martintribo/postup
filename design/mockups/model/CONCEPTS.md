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

## Edit, then build

Edit the `.toml` files and, if a link changes, the HTML in `gen/*.py` as well. Then run `python3 gen/build.py`. `INDEX.md` is generated and lists every screen and flow on one line each. Every note line needs a source tag such as [FS], [F###], [M1031-draft] or [drawn].
