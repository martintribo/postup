# What are the final screens of the PostUp app?

**Direct answer.** The final design is the **v1034 mockup set — 44 screens**, in four styles (Fresh default, Cozy, Night, Bold) at phone (390×844) and desktop (1440×900). They're the single static `index.html` (built by `gen/build.py` + `gen/more.py`), addressed as `/mockups/?style=<fresh|cozy|night|bold>&device=<phone|desktop>#<screen>` (overlays via `&ov=<sheet>`). The phase/final app build realizes these screens with the mockup CSS ported in and all feature flags on. Grouped, the final screens are:

**Shell / navigation**
- Phone: 5-tab bottom bar — Map · Nearby · (raised) Post up · Projects · Inbox (unread dot). Root tabs (Nearby, Projects) have no Back; forms/sheets have Back and no tab bar. Tab bar hidden on post, project new/update/edit/attach, settings; login/admin/style/agent are bare.
- Desktop: left rail — logo · Map · Nearby · Projects · Inbox · green Post up · avatar (→ own profile). "Mockups" was dropped from the rail.
- **Sign-in sheet** (`#post-signin` and the join/ask/attach variants): a global bottom sheet — Continue with Apple / Google, a dev sign-in, "Use a PostUp username" (→ /login), "Not now". Any /login link opens this sheet. Sign-in is required only at post/join/follow/new-project.

**Home** (`#home`, with `#quiet` when no one's live) — full-screen map; live pins = avatar-initial markers with a pulse ring and count badge; cafe pins = coffee icons. A panel (phone: sheet under the map; desktop: floating right panel) carries a dismissable welcome ("Post up at a cafe. See who's working nearby."), your-live row, the Live-now list, This-week cafes, then a projects section, with "Post up" shown only when someone's live.

**Nearby** (`#quiet-feed` A photos / `#quiet-feed-b` colored bands; route `/nearby`) — "Good things happen at cafes", "N postups nearby this week", big Post-up and Map buttons, feed cards (avatar, name, when/how far, working-on, project tag, cafe, "Post up here", "N joined", project-update cards).

**Projects** (`#projects`, `#project`, `#project-new`, `#project-update`, `#project-attach`) — a project-card grid with Nearby/Following/Mine filters, "+" for a new project, and a dismissible first-visit line ("See what people nearby are building. Follow along or post up to work on yours."); a project page with cover, owner, updates timeline, live postups, Post update / Post up / Follow; and the create/update/attach forms ("Now" / "I was here earlier", with attach requiring sign-in). Empty states for no projects.

**Cafe** (`#cafe`) — a Google UI-Kit place card, "Here now" people with Join, "Post up here", and the project that "was here".

**Post flow** (`#post`, `#where`, `#where-search`, `#posted`) — the post-up form (cafe preselected + Change → cafe picker, Working on, project chip / + Project, duration chips, join mode "Anyone can join / Ask to join" with "You'll get an alert whenever someone joins", optional photo); `#where` lists nearby cafes by distance with search, `#where-search` shows "powered by Google" results; `#posted` is the "You're posted up" confirmation (share link Copy / Invite friends, Add a photo, Manage postup → #live, Map, Close → home).

**Live / manage** (`#live`, `#post-edit`) — your live postup: time-left ring, cafe, project, +30 min, Edit, join setting, join requests (Approve / Decline), joined list, Group chat, Share, End postup (with confirm).

**Join** (`#postup`, `#postup-ask`, `#ask`, `#requested`, `#joined`) — someone's postup (person, project, cafe, time, Join 🔒) → sign-in → `#joined` (Directions, View cafe/project, Group chat, Leave); the ask-to-join path (`#postup-ask` "Tess approves who joins" → sign-in → `#ask` write a reason → `#requested` "Request sent").

**Chat / inbox** (`#chat`, `#inbox`, `#activity`) — a per-postup group chat ("Only people in this postup can see this chat", per-message ⋯ menu); Inbox with Chats | Activity tabs (ended chats dimmed); Activity rows for requests, joins, "said yes", messages, follows.

**Profile / settings** (`#profile`, `#me`, `#settings`) — a public profile and your own (live card, avatar, bio, "N postups · since Sep", Follow / Edit profile, regular-cafe chips, projects, past postups); Settings with notification toggles and Account (Blocked people, Sign out, Delete account).

**Share landings** (`#invite`, `#invite-ended`, `#invite-project`) — logged-out landings for a shared postup link (live: "Maya is working at Bean Theory till 4. Join her?"; ended: "This postup ended"), and a shared project link ("Maya is building Star Fox 64 mod: see updates, follow, or join her next postup"), each with a short "what PostUp is" line.

**Overlay sheets** — share, directions (Apple/Google Maps), leave, end-live, more (profile/Share/Report/Block), message options, block ("She won't be told"), delete-account; plus report/block screens `#report` → `#reported` ("Block Maya too", "They won't know you reported them"). No safety tips (Martin: "this site is for adults").

**States** — `#empty-area` ("Be the first here"), `#postup-ended`, `#postup-full`, `#postup-cancelled`, `#cafe-gfail` (place card failed → Open in Maps / Retry), `#loading` (skeleton), `#offline` (cached Nearby feed + banner, not a blank screen). Plus `#index`, the mockup switcher.

**Phone vs. desktop behaviour.** Same screens, different frame. On desktop only `#home`, recent map, `#cafe`, `#postup`, `#joined`, `#live` keep a full-screen map with a 440px right panel; everything else is a full page (Nearby grid + sticky sidebar, Projects grid, project, inbox, chat, profiles, settings, report, invites, loading/offline). Create/edit flows (post, where, post-edit, project new/update/attach) are centered dialogs on desktop. Phone carries the Nearby tab and the raised Post-up button; desktop puts Post up in the rail with the avatar.

**How they link.** Live markers/cards → `#postup`; cafe names/quiet markers → `#cafe`; project tags → `#project`; "Post up here" → `#post` with the cafe preset; Post up → sign-in → `#posted`; Join → sign-in → `#joined`; the Projects tab/rail → `#projects`; share links → the `#invite*` landings.

## Later decisions that override the mockups
Three product decisions made *after* this mockup session change what ships, and are **not** reflected in the v1034 files:
- The nav tab is always labeled **"Home"**, never "Map".
- With **no live postups**, home shows **no map** and focuses on projects.
- With **no activity this week**, home and Nearby **fall back to projects in general**.

## Earlier versions that were replaced
- v1 plain mockups (flows A–F, with a yellow "MOCKUP" strip and a 3-item Map/Projects/Post-up nav) → a pro redesign → the 4-style system → desktop → the v1034 batch. The "Quiet right now…" header and all "quiet" wording were dropped (renamed to "Nearby / Good things happen at cafes"). The desktop feed-over-map became a full-page grid. The Projects tab that opened a single project became the `#projects` list page. The 3-tab nav became the 5-tab bar. `#posted` gained Manage postup + Map; `#offline` became a cached feed with a banner rather than a blank screen.
- The UX review's suggestions that were **not** adopted (so they are not final screens): safety tips, an "I'm here"/find-me hint, location-permission screens, and followers-only visibility. "Where I'm sitting" (a description/photo to help joiners find the poster) is a dashboard TODO, not mocked.

## Where the phase/final build still differs from the mockups
- The nav code still says "Map"; the "Home" rename landed separately on phase/final (commit 36ddaad), and the no-map-when-nobody-live and projects-fallback behaviours are build-side choices not in the v1034 mockups.
- Feed photo cards are still absent in the build.
- Earlier phase branches kept old page layouts and nearly empty worktree databases, so most screens couldn't be compared; the audit put matching the mockups at ~3–4 weeks.

## Open questions
- Final style: Fresh vs. Bold (Martin likes Bold on mobile).
- Join default: instant vs. approve.
- Whether to show the cafe name before someone is approved to join.
- Launch area (code shows Playa Vista / Westside LA).
- Group-chat retention (code uses 24h).
- Capacitor vs. Cordova for the native app.
- Seeded past postups and whether anonymous posting is allowed.
