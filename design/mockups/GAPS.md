# Gaps: phase/final vs Fresh mockups

Checked 2026-10-19 on `http://127.0.0.1:15017` at `4287e61`, Fresh only, phone 390×844 and desktop 1440×900.

Mockup: `design/mockups/index.html?style=fresh&device=phone|desktop&notes=0&auth=out|in&live=live|none&mode=live|building#<screen>`.

The app has no `auth` / `live` / `mode` query. This pass used a signed-out session. The database had no live postups, so Home and Nearby were in the none-live fallback. Live-mode Home was also read from `src/routes/+page.svelte` (the branch that renders when `live.length` is set) and from the mockup drawings.

`#index` is the mockup switcher, not a product screen. `#home-overlay-alt` is marked alternative, not chosen. Do not build either.

Already matching, leave them:

- Phone tab bar and desktop rail: Home, Nearby, Post up, Projects, Inbox. The Home label is Home.
- Post form (`/post`): Where, Working on, project chips, Until, Who can join, lock on the submit button when signed out, Where sheet. Missing piece is in chunk 4.
- Projects filters: Nearby / Following / Mine, plus New project (top-bar on phone, button on desktop).
- Sign-in sheet component exists (`SignInSheet`) and in-page `/login` links can open it. Account routes still redirect. See chunk 5.
- Project card markup can show a cover, cafe, and "N this week". Those fields are empty on the cards that loaded.

## Chunk 1 — Home is one URL with Live and Building

Screens: `#home`. Do not ship `#home-overlay-alt`. `#quiet` is not `/`.

`/` currently picks a layout in code. Nobody live: a full projects page, no map, no switch. Someone live: map plus a Live now sheet, and Building is unreachable. The mockup keeps both modes on `/`. Default is Live when anyone is live, otherwise Building. A Live · Building control sits at the top (phone: in the header; desktop: top of the page or the right panel). Flipping it does not navigate.

| | Mockup | App now |
|---|---|---|
| Switch | Live · Building on both modes | Missing. Phone none-live header is the word "postup". |
| Building heading | "What people are building" | Desktop: "What people nearby are building". Phone: heading hidden because Home reuses `.pjs .hero`, which is `display: none` under 1024px. |
| Building body | Welcome, 3 closest project cards, See all projects, one Post up, This week cafes. A preview, not the Projects page. | Full project grid. No See all. No This week row. Phone hides the Post up button (`.newp { display: none }`). |
| Welcome | "Post up at a cafe. See who's working nearby." | "See who's working from cafes nearby. Post up, or join someone." |
| Live, people live | Map, avatar pins with a pulse and count, coffee cafe pins. Panel: Live now, This week. Right panel is about 440px on desktop. Area chip on the map ("Venice & Mar Vista"). | Map branch exists. Panel also lists projects under "Projects nearby" whenever anyone is live or a cafe had a postup this week. That heading is wrong. No mode switch, so you cannot open Building while people are live. |
| Live, nobody live | Map stays available. Copy: "Working somewhere today?" and Post up. Cafe pins can remain. No "quiet" copy. | This state is not reachable. Nobody live skips the map entirely. |
| Someone goes live while you are in Building | Banner: "Maya just posted up nearby · See map". Do not switch modes under the user. | Missing. |
| Your live postup | A "You're live" row that opens manage. | Present only in the map branch. |
| Home icon | House. | Map glyph (`Icon name="map"`). |
| Sort | Closest projects first, even when none are local. Never call them nearby unless they are. | Subtitle says "projects from people who post up around here" and "nearby". |

Scenario notes: signed out and signed in are the same screen except the lock marks and the header avatar (signed in only). Desktop rail already shows a Sign in icon when signed out. That part is fine.

## Chunk 2 — Nearby feed

Screens: `#quiet-feed` (`/nearby`, photo cards), `#quiet-feed-b` (same screen, tinted tile when a card has no photo), `#empty-area`, `#loading`, `#offline`.

`#quiet` (recent map, "Nearby this week") is the old no-live home. Not a route to build unless Martin asks. Home's Live mode covers the map.

When `feed.items` is empty, `/nearby` renders the projects grid. Checked signed out, none live:

- Phone title is "Nearby" with no hero. Mockup hero is "Good things happen at cafes", then the line "What people are building" (none live) or "6 postups nearby this week" with an avatar stack (live).
- No Post up button on the phone fallback (same `.newp` hide).
- Duplicate area line: "Near Westside, Los Angeles · recent projects…" appears above the hidden hero and would also sit in the hero.
- Cards are the project grid, which matches the none-live fallback in kind, but they are the full Projects page (no cafe, no "N this week", no 3-card limit). Heading must stay "What people are building", not "nearby", unless the projects are actually nearby.
- `NearbyFeed.svelte` (used when the week feed is non-empty) is a different layout: small "Nearby" header, text rows ("Maya is posted up at …"), no photo, no "Post up here", no "N joined", no distance. Welcome copy differs ("Post up at a cafe and see who's working nearby.").
- "You're all caught up · Map" footer is missing.
- Signed-in header avatar (green initial, links to your profile) is missing. Unsigned note in `notes/quiet-feed.md`; still drawn on the mockup.
- `#quiet-feed-b`: a card with no photo must be a tinted tile, never a grey box. E2E Project on Home and Projects renders a grey cover block. Treat a missing or broken cover as a tint.

`#empty-area`: new area is "Be the first here" plus two nearby cafes and Post up, on the map. App empty project state is "Be the first here" inside the grid, with "Share a project", and no cafe list.

`#loading`: skeleton of the Nearby hero and cards, tab bar stays. No skeleton route.

`#offline`: banner "You're offline · showing what we had" plus Retry, over a cached feed. `OfflineBanner` exists; it does not render this feed.

Desktop: mockup Nearby is a full-page photo grid with a sticky sidebar (Post up, This week). No map. App none-live desktop is the same 4-column project grid as Projects.

## Chunk 3 — Projects

Screens: `#projects`, `#project`, `#project-new`, `#project-update`, `#project-attach`, `#attach-signin`.

`#projects` (`/projects`), both sizes:

- Welcome says "See what people nearby are building." Mockup: "See what people are building. Follow along or post up to work on yours."
- Subtitle says "What people nearby are building." Mockup: "What people are building." The Nearby filter chip is correct. The heading is not.
- Cards lack covers, cafe, and the "N this week" pill. One broken cover is a grey box.
- Sort is not visibly closest-first.
- Phone has no big h1; the top bar says Projects. That matches the mockup. Desktop h1 "Projects" matches.

`#project`: shell is closer (cover, kind tag, owner, Update / Post up / Follow, live row, updates). Check against the note before editing: Post up and Follow still send signed-out users through `/login?next=` (the click interceptor can open the sheet; a full navigation must not replace the page). Updates should show "Yesterday · at Bean Theory" style lines.

`#project-new` and `#project-update`: forms exist (cover, name, kind, one line; title, notes, image). They redirect to `/login` when signed out. Mockup keeps the form and opens `#ov-signin` / the attach sheet at submit. Desktop forms should be centered dialogs.

`#project-attach` (`/post?project=`): When / Now / I was here earlier is implemented. Where is a single current cafe plus Change, not the three cafe chips drawn on the mockup. Sign-in at submit should be the sheet (`#attach-signin`), already wired via `askSignIn` on `/post`.

## Chunk 4 — Post, cafe, join, live

Screens: `#post`, `#where`, `#where-search`, `#post-signin`, `#posted`, `#post-edit`, `#live`, `#cafe`, `#cafe-gfail`, `#postup`, `#join-signin`, `#joined`, `#postup-ask`, `#ask-signin`, `#ask`, `#requested`, `#postup-ended`, `#postup-full`, `#postup-cancelled`, `#invite`, `#invite-ended`, `#invite-project`.

`#post`: add the optional "Add a photo" control. Working-on placeholder is already "Level editor for the mod". Desktop should be a centered dialog (tab bar already hidden).

`#where` / `#where-search`: the sheet exists. Search with a Maps key goes through `GooglePlaceSearch`. Mockup results say "powered by Google" and must stay inside that widget. Do not repeat Google place details in the feed.

`#post-signin`: sheet copy in the mockup is "Almost there / Sign in and your postup goes live." plus Apple, Google, Not now. App sheet matches that path when `askSignIn` runs. Also show "Use a PostUp username" (already in the component) and the dev mock button only when `OAUTH_MOCK=1`. Do not show the full `/login` page for Post up.

`#posted`: after submit the app redirects to `/postups/:id?posted=1`, which is the old postup page, not the "You're posted up" confirmation (share link, Copy, Invite friends, Add a photo of your spot, Manage postup, Map, Cafe, Project).

`#live` and `#post-edit`: manage UI is folded into `postups/[id]` (old `pu-page` stack: time-left text, requests, end confirm). Mockup is a screen: time-left ring, cafe, project, +30 min, Edit, join setting, requests with Approve / Decline, joined list, Group chat, End postup. Signed-out manage shows the sheet over the screen, not a redirect. Edit is the post form with Save.

`#cafe` (`/places/:id`): mockup is a map or hero, Here now with Join, a Google UI Kit place card, "N postups this week" plus the project, and Post up here. The page still has star reviews, wifi, and noise ("quiet / moderate / noisy"). Noise is a cafe attribute, not the banned "quiet" empty-state copy, but it is not on the mockup. `#cafe-gfail` ("Details unavailable", Open in Maps, Retry) needs a check against `GCard`; do not invent a second place-details layout outside the widget.

`#postup` and the join path: `postups/[id]` is a pre-mockup page. Rebuild it to the drawing: person, project, cafe, distance, Join with a lock when signed out, sheet `#join-signin` ("Join Maya / Sign in so Maya knows who's coming."). Ask-to-join is `#postup-ask` → sheet → `#ask` (reason) → `#requested`. Joined is its own confirmation (`#joined`: Directions, Group chat, Leave), not a line inside the postup page.

Ended / full / cancelled need the mockup headlines ("This postup ended", "This postup is full", "Maya cancelled this postup") and "See what's nearby" / "Follow Maya for next time". The page has some of these strings inside `pu-card`s.

Share landings `#invite`, `#invite-ended` (`/p/:id`) and `#invite-project` (`/projects/:id?s=1`) exist. Re-read the notes and match the short "what PostUp is" line and the ended copy before calling them done.

## Chunk 5 — Inbox, people, sheets

Screens: `#inbox`, `#activity`, `#chat`, `#profile`, `#me`, `#settings`, `#report`, `#reported`, `#ov-share`, `#ov-dirs`, `#ov-leave`, `#ov-endlive`, `#ov-more`, `#ov-msg`, `#ov-block`, `#ov-delacct`, `#ov-signin`.

Signed out, these account screens redirect to `/login` (full page: "postup.now / Welcome back", username form, dev mock). The mockup keeps the screen up and puts a sheet on it: "Your inbox / Sign in to see your chats and activity." Same pattern for chat, profile, settings, live. Inbox has no unread dot when signed out.

`#inbox`: Chats | Activity tabs on one page, rows with avatar, title, preview, time. Ended chats dimmed. No Back on this root tab. App `inbox/+page.svelte` is a separate `pu-page` with a Back link and "No chats yet…". Activity is a second route, `/activity`, also a `pu-page`.

`#chat`: header with the cafe and "Only people in this postup can see this chat.", message rows, per-message ⋯ menu (`#ov-msg`). App chat is `pu-chat` and redirects when signed out.

`#profile` / `#me`: live card, bio, "N postups · since Sep", Follow or Edit profile, regular cafes, projects, past postups. App `u/[username]` is a `pu-page`. `/me` redirects to `/login` or to `/u/:username`.

`#settings`: notification toggles (join requests, someone joins, messages, people you follow post up) and Account (Blocked people, Sign out, Delete account). App settings is a `pu-page` behind login.

`#report` → `#reported` ("Thanks for telling us", "Block Maya too"). `ReportSheet` exists; match the reason list and the reported screen.

Sheets to match in place, not as new routes: share (Copy, Messages, WhatsApp, Email), directions (Apple Maps, Google Maps), leave, end postup, more (profile, Share, Report, Block), message options, block ("She won't be told"), delete account, and the generic sign-in sheet for follow / create / update.

## Order

1. Home Live / Building on `/`.
2. Nearby feed, including none-live projects fallback, loading, offline, empty area.
3. Projects list copy and cards, then project, new, update, attach.
4. Post photo, posted confirmation, cafe, postup join and live manage, share landings.
5. Inbox and activity, chat, profile, settings, report, overlay sheets. Signed-out account pages keep their screen and open the sheet.

After each chunk: commit and push `phase/final`, refresh Vite on `127.0.0.1:15017`, recheck the screens in that chunk at phone and desktop.
