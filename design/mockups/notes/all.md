# PostUp mockups — implementation notes (all screens)
Source of truth for building PostUp: the v1034 mockups plus these notes. Where a note says "Overrides", the note beats the drawing.
Mockup: /mockups/?style=<fresh|cozy|night|bold>&device=<phone|desktop>&auth=<out|in>&live=<live|none>#<screen>  (overlay sheets: &ov=<sheet>)
The home page (/) is `#home`, called Home: two modes on one URL, Live and Building (`?mode=live|building`); default by whether anyone's live. `#home-overlay-alt` is an alternative, not chosen. `#quiet` is the old no-live home drawing (not /); `#quiet-feed` / `#quiet-feed-b` are Nearby (/nearby).
Screens: 41 + 9 overlay sheets.

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing.

## Global rules (every screen)
### Home page (/)
- **`/` is `#home`, called Home.** Two modes on the same URL, no redirect: **Live** (map + Live now) and **Building** (projects first). [M1018b]
- Default mode: Live when anyone's live nearby, otherwise Building. A small Live · Building switch at the top lets people flip. [M1018b]
- Someone goes live while you're in Building: show a banner ("Maya just posted up nearby · See map"); never switch under you. [M1018b]
- `#home-overlay-alt` (projects card over a dimmed map) is an **alternative, not chosen**. [M1018b]
- Building heading: **"What people are building"**, not "…nearby…". [M1018c]
- `#quiet` (recent map) is the old no-live home drawing. Not `/`. [FS] [F044]
- `#quiet-feed` and `#quiet-feed-b` are the Nearby tab (`/nearby`), photo and no-photo variants. Not `/`. [FS]

### Scenarios
- Every page has a scenario toggle: signed out / in × live nearby / none. The page renders that scenario's version; pages that don't differ say "Same in all scenarios". [M1018]
- Mockup controls (scenario, style, device, screens, sheets, notes) live in one floating menu, bottom-left; changes apply in place. [M1018]
- Signed in: 🔒 marks disappear and actions skip the sign-in sheet. [TK§1] [FS]
- Signed out: sign-in sheets open at the action; signing in from a sheet switches the toggle to Signed in. [FS] [M1018]
- None live: live pins disappear from maps. [M1018]
- Signed out: account pages (Inbox, chat, profile, settings, manage) show a sign-in sheet over themselves; the Inbox dot is hidden. [unsourced]
- Mockup default: signed out + live nearby; the mockup opens on `#home`. [M1018]
- Critical flows sit on top of scenarios: who arrives, in what situation, and the screens they step through. Each has a player at `flows/<id>.html` and notes at `flows/<id>.md` (in the menu under Flows). [M1024]
- The flow map (`flows/map.html`, source in `flows/map.md`) shows how a first-time visitor (signed out, never registered) reaches each flow's starting state; every flow is reachable from that root. [M1025]
- Mockup data model: a **site graph** of pages (screens + sheets) whose **site states** are page + auth + live (+ Home mode); edges are taps and site events derived from the mockup links (`gen/sitegraph.py`, `flows/site.html`). A **flow** is a path of steps, each = site state + user state (what they think) + action; every transition must be a site-graph edge or is reported as a design gap. The player's From here panel lists next site states and other flows enterable at that step. [M1025]

### Overrides
- The nav tab for home is always labeled **Home**, never "Map" (drawn that way since Oct 18). [F046] [R53] [M1018b]
- No live postups: home **opens in Building mode** (projects first). Live mode stays one tap away and shows the map with an invite to post up. [M1018b] [F044] [R1]
- Nothing from this week: home and Nearby fall back to **projects in general** (any age). [F043] [R3]

### Copy
- Project lists (Home Building, Nearby fallback, Projects) are sorted **closest-first** and show the closest projects available even if none are local (early launch has few nearby). Never say "nearby" about projects unless they are. Heading: "What people are building". [M1018c]
- Never empty or "quiet" copy ("No posts yet", "Nothing yet", "quiet"). Use positive invites. [F035] [R4] [TK§2]
- Short labels, 1–3 words; warm copy; little on screen at a time; drill down with Back. [F013] [TK§1]

### Behavior
- Sign-in only at the moment of action (post, join, follow, new project), as a sheet over the current screen. Apple + Google. [FS] [TK§1] [R9⚠]
- Google Places data only inside Google UI-Kit widgets. Never in the feed. Store only `place_id`. [F032] [R36] [TK§2]
- Map only on map, cafe and postup screens. Nearby and Projects never show it. [F051] [F052] [F053] [R69]
- Phone tab bar and desktop rail carry the same items. [F064] [F066] [R12]
- Everything that looks tappable goes somewhere. [F026] [TK§1]
- Photos come from users and projects. No photo: tinted tile, never a grey box. [F086] [R38]
- Desktop: map screens keep the map with a 440px right panel; everything else is a full page; create/edit flows are centered dialogs. [FS]
- Four styles, Fresh default; switcher is dev-only. Final pick (Fresh vs Bold) is open. [F036] [F076] [FS]
- Report and block, yes. No safety tips: "this site is for adults". [F059]

### Not adopted
- Safety tips, an "I'm here" hint, location-permission screens, followers-only visibility. [FS]
- "Where I'm sitting" note/photo: todo, not mocked. [F056]

### Open
- Final style, join default, cafe name before approval, launch area, chat retention, Capacitor vs Cordova. [FS] [TK§4]

### Model decisions to confirm (phase 2 draft)
- Sign-in is one sheet, `signin`, opened in the page's sheet slot. The old `#join-signin`, `#ask-signin`, `#post-signin` and `#attach-signin` pages are folded into it; their URLs redirect to the page with the sheet open, and signing in continues to the action (Join → joined, Ask → ask, Post up → posted). [M1031-draft]
- `live` means someone is live nearby (global). A postup's own status (full, cancelled, ended) is its page; ending your own postup or a postup ending does not change `live`. [M1031-draft]
- New event: someone you follow posts up. The alert lands in Activity and Nearby now has someone live. [M1031-draft]
- Activity gets a "Maya posted up at Bean Theory" row that opens the postup, as the app's alerts link to the postup. [M1031-draft]
- The More sheet's block option reads "Block"; the app can name the person in context ("Block Maya"). [M1031-draft]
- Chrome is modelled as slots: the phone tab bar is a tab slot (`tabbar`) on pages that draw it; the desktop rail is a panel slot (`rail`) on every page. Their links count only when no sheet is open. [M1031-draft]
- Two-tap flow steps are split into two steps (Back, then a tap) instead of adding shortcut links: cautious-joiner, curious-browser, stumbled, following, host-approve, invite-project, postup-states, project-builder, quick-joiner. [M1031-draft]

### Chrome: Rail (desktop) · Purpose
- Desktop left rail: Map, Nearby, Projects, Inbox, Post up. Every page has a "rail" panel slot on desktop; its links are available when no sheet is open. The right panel is the page itself on desktop (drawn beside the map). [drawn] [M1031-draft]

### Chrome: Tab bar (phone) · Purpose
- Phone tab bar: Map, Post up, Projects. Pages that show it declare a "nav" tab slot; its links are available on those pages when no sheet is open. [drawn] [M1031-draft]


---

## Mockup index (`index`)
URL: /mockups/?style=fresh&device=phone#index  ·  desktop: /mockups/?style=fresh&device=desktop#index

### Purpose
- Mockup switcher (screens, style, device). Not a product screen. [FS]

### Scenarios
- Same in all scenarios. The 2×2 scenario matrix lives here. [M1018]

### Decisions
- No "Mockups" link in the real nav. [R14⚠]

---

## Home page (/) (`home`)
URL: /mockups/?style=fresh&device=phone#home  ·  desktop: /mockups/?style=fresh&device=desktop#home

### Purpose
- **The home page: what loads at postup.now/.** Two modes on one URL: Live and Building. [M1018b]

### Scenarios
- Live nearby: opens in Live mode: map + Live now. [M1018b] [R2] [F029]
- None live: opens in Building mode. Live mode shows the map with cafe pins and an invite to post up. [M1018b] [F044]
- Live nearby, while in Building: banner "Maya just posted up nearby · See map". [M1018b]
- Nothing this week: drop This week; projects in general. [F043] [R3]
- Signed out / in: same, except 🔒 and the header avatar (signed in only). [TK§1] [M1018]

### Behavior
- Live · Building switch at the top (phone: over the map or in the header; desktop: top of the panel or header). [M1018b]
- Live mode: live pins are avatar markers with a pulse ring and count badge; cafe pins are coffee icons. Panel: Live now, This week cafes. [FS]
- Live mode with nobody live: "Working somewhere today?" + Post up. No empty or "quiet" copy. [M1018b] [F035]
- Building mode: first-visit welcome line, "What people are building" (3 project cards, closest first) + See all projects → `#projects`, big Post up, This week cafes. A preview; it doesn't copy the Projects page. [M1018b]
- Desktop: Live mode is the map with the right panel; Building mode is a full page. [FS] [M1018b]
- Building projects: closest first; show the closest available even if none are local. Heading says "What people are building", never "nearby" unless they are. [M1018c]
- Your own live postup shows here (manage entry). [R22] [F057]
- Tiles: Stadia Maps, free plan, hard cap; prefer the map failing over surprise charges; worldwide. [F003] [F004] [F006] [F007]

### Links
- Live marker / row → `#postup`. Cafe → `#cafe`. Project card → `#project`. See all projects → `#projects`. Post up → `#post`. [FS] [M1018b]

### States
- New area → `#empty-area`. [FS]

### Decisions
- Stumblers (no idea what PostUp is): the only explainer is the Building-mode welcome line; Live mode has none. **Decision for Martin:** add a one-line explainer to Live mode too, or a fuller "How it works"? See flow `stumbled`. [M1025]
- First-time visitors split by intent: stumbled on it, curious about content, came to post up, opened a share link (flow map, Arrive box). [M1025]
- Replaces "Post up shows only when someone's live": Building mode has a big Post up. [M1018b] [FS]
- Overlay-on-map version drawn for comparison: `#home-overlay-alt`, not chosen. [M1018b]

### Unsourced
- Area label ("Near Westside, Los Angeles") and the change-area picker. [R7⚠]
- Launch area Playa Vista / Westside LA as fallback centre. [R8⚠]

### Gap fixes
- Gap fix (Oct 25): Live now includes an ask-to-join postup (Tess, marked "Ask to join") that opens `#postup-ask`; open-join rows unchanged. [M1025]

---

## Recent map · old no-live home (not /) (`quiet`)
URL: /mockups/?style=fresh&device=phone#quiet  ·  desktop: /mockups/?style=fresh&device=desktop#quiet

### Purpose
- Map of this week's cafes when nobody's live (drawn as the no-live home). [FS]

### Scenarios
- Same in all scenarios (this week's cafes; nobody live by design). [M1018]

### Overrides
- No longer the no-live home: with no live postups home shows no map and focuses on projects. [F044] [R1]

### Links
- Cafe → `#cafe`. Project → `#project`. Post up → `#post` with the cafe preset. [FS]

### Open
- Whether this map stays reachable at all once home is projects-first. [unsourced]

---

## Nearby (/nearby) · photos (A) (`quiet-feed`)
URL: /mockups/?style=fresh&device=phone#quiet-feed  ·  desktop: /mockups/?style=fresh&device=desktop#quiet-feed

### Purpose
- The Nearby tab (`/nearby`): photo-led feed of this week's postups and project updates. [FS] [F029]

### Scenarios
- Live nearby: postup feed, as drawn. [FS]
- None live: falls back to projects; project cards replace postup cards. Hero line "What people are building"; closest first, even if none are local; never call them nearby unless they are. [M1018] [F043] [M1018c]
- Signed out / in: same. [M1018]

### Behavior
- Hero "Good things happen at cafes" + "N postups nearby this week". [FS]
- Cards: avatar, name, when / how far, working on, project tag, cafe, "Post up here", "N joined"; project-update cards. [FS]
- First visit: one dismissable welcome line on top. [F063] [F098] [R5]
- Photos: user and project photos only. Google photos never. [F032] [F031] [R38]
- Root tab: no Back. [R13]
- Desktop: full-page grid with a sticky sidebar. No map behind it. [F051] [FS]

### Links
- Name → `#profile`. Cafe → `#cafe`. Project → `#project`. "Post up here" → `#post` with the cafe preset. [FS] [R40]

### States
- Nothing this week → projects in general. [F043] [R3]
- Loading → `#loading`. Offline → `#offline`. [FS]

### Copy
- Called "Nearby", never "Quiet right now". [F035] [FS]

### Unsourced
- Header avatar → `#me` on phone (still open in the build). [R15⚠]
- "Near …" location label. [R7⚠]

### Open
- Build still lacks the photo cards. [FS]

---

## Nearby (/nearby) · no photos (B) (`quiet-feed-b`)
URL: /mockups/?style=fresh&device=phone#quiet-feed-b  ·  desktop: /mockups/?style=fresh&device=desktop#quiet-feed-b

### Purpose
- Comparison variant of Nearby with colored bands instead of photos. [FS] [F030]

### Scenarios
- None live: falls back to projects, same as `#quiet-feed`. [M1018] [F043]
- Signed out / in: same. [M1018]

### Behavior
- Same content and links as `#quiet-feed`. [FS]
- A card with no photo uses a tinted tile, never a grey box. [R38]

### Open
- Which variant ships. Photo cards are listed as missing from the build, which implies A. [FS] [unsourced]

---

## Cafe (`cafe`)
URL: /mockups/?style=fresh&device=phone#cafe  ·  desktop: /mockups/?style=fresh&device=desktop#cafe

### Purpose
- One cafe: who's here now and the place details. [FS]

### Scenarios
- None live: no Here now section; this week's count stays. [M1018]
- Signed out / in: same, except 🔒. [TK§1]

### Behavior
- Google UI-Kit place card for photos, rating, hours. Only Google content on the page, only inside the widget; store only `place_id`. [FS] [R36] [F032]
- Google API cost is a concern; keep Google calls to the widget. [F085]
- Hero photo is a user photo ("Maya's photo"). [drawn] [F086]
- "Here now" people with Join; "Post up here"; the project that was here. [FS]
- Desktop: map + right panel. [FS] [F053]

### Links
- Join → `#postup`. "Post up here" → `#post` with the cafe preset. Share → share sheet. [FS] [R41⚠]

### States
- Place card fails → `#cafe-gfail`. [F060] [R37]

---

## Post up (`post`)
URL: /mockups/?style=fresh&device=phone#post  ·  desktop: /mockups/?style=fresh&device=desktop#post

### Purpose
- Post that you're working at a cafe. [FS]

### Scenarios
- Signed out: Post up 🔒 → sign-in sheet (`#post-signin`). [FS] [R9⚠]
- Signed in: Post up goes straight to `#posted`. [FS]
- Live / none: same. [M1018]

### Behavior
- Cafe preselected (nearest) with Change → `#where`. Not a map picker. [FS] [F058] [F062] [R17]
- Working on (text), project chip / + Project, Until (1h / 2h / 3h / time). [FS] [R17]
- Who can join: "Anyone can join" / "Ask to join", set per postup by the poster. Poster gets an alert when someone joins. [F055] [F095]
- Optional photo; never slows posting down. [F033] [R20]
- Signed out: Post up opens the sign-in sheet over this screen; URL stays `/post`. [R9⚠]
- Desktop: centered dialog. No tab bar on phone. [FS]

### Decisions
- Default "Anyone can join" is our default, not Martin's. [R18]

### Unsourced
- Sign-in required to post; anonymous posting off (D3). [R16⚠]
- Signed-out draft survives sign-in. [R11⚠]

### Not adopted
- "Where I'm sitting" note/photo: todo. [F056]

---

## You're posted up (`posted`)
URL: /mockups/?style=fresh&device=phone#posted  ·  desktop: /mockups/?style=fresh&device=desktop#posted

### Purpose
- Confirmation that your postup is live. [FS]

### Scenarios
- Same in all scenarios; reached only after signing in. [M1018]

### Behavior
- Share link with Copy; Invite friends → share sheet. [FS]
- "Add a photo of your spot": optional, asked here after posting. [F033] [R20]
- Manage postup → `#live`. Map → home. Close → home. [FS]
- The flow must not just stop after posting. [F110]

### Overrides
- Home is called Home; the "Map" link label wasn't decided. [F046] [unsourced]

---

## Postup · anyone can join (`postup`)
URL: /mockups/?style=fresh&device=phone#postup  ·  desktop: /mockups/?style=fresh&device=desktop#postup

### Purpose
- Someone's live postup you can join. [FS]

### Scenarios
- Signed out: Join 🔒 → sign-in sheet (`#join-signin`). [FS]
- Signed in: Join goes straight to `#joined`. [FS]
- Live / none: no effect; this postup is live. [M1018]

### Behavior
- Person, project, cafe, time, "Anyone can join", Join 🔒. [FS] [drawn]
- Share; ⋯ → profile / share / report / block. [FS] [F059]
- Poster gets an alert when you join. [F055]
- Desktop: map + right panel. [FS] [F053]

### Links
- Person → `#profile`. Project → `#project`. Cafe → `#cafe`. Join → sign-in → `#joined`. [FS] [R40]

### States
- `#postup-ended`, `#postup-full`, `#postup-cancelled`. [F060]

### Unsourced
- Explain what Join means ("Let Maya know you're coming, then say hi at the cafe"). [R24⚠]

---

## You're joining (`joined`)
URL: /mockups/?style=fresh&device=phone#joined  ·  desktop: /mockups/?style=fresh&device=desktop#joined

### Purpose
- Confirmation after joining. [FS]

### Scenarios
- Same in all scenarios; reached only after signing in. [M1018]

### Behavior
- Group chat → `#chat`. Directions → Apple / Google Maps sheet. Cafe, Project links. Leave → confirm sheet. [FS]
- The poster has been told you're coming. [F055]
- The flow must not just stop after joining. [F110]

### Unsourced
- Directions open Apple/Google Maps (ledger item). [R25⚠]

---

## Project (`project`)
URL: /mockups/?style=fresh&device=phone#project  ·  desktop: /mockups/?style=fresh&device=desktop#project

### Purpose
- One project: cover, owner, updates, live postups. [FS]

### Scenarios
- None live: no Live section. [M1018]
- Signed in: 🔒 gone; Update / Post up go straight through. [TK§1] [FS]

### Behavior
- Post update, Post up (for this project), Follow; all need sign-in. [FS]
- Updates timeline with images; the owner posts updates. [R35] [F052]
- No map. Desktop: full page. [F052] [FS]

### Links
- Owner → `#profile`. Live row → `#postup`. Cafe → `#cafe`. [drawn] [R40]

### Unsourced
- Test or hidden projects never show. [R34⚠]

### Open
- Image storage for projects (Vercel Blob?). [TK§4]

---

## Projects (`projects`)
URL: /mockups/?style=fresh&device=phone#projects  ·  desktop: /mockups/?style=fresh&device=desktop#projects

### Purpose
- What people are building. Built first so new users don't land on an empty map. [F024] [FS] [M1018c]
- Sorted closest first; shows the closest projects available even if none are local. Never claim "nearby" unless they are. [M1018c]

### Scenarios
- Same in all scenarios (🔒 hidden when signed in). [M1018] [TK§1]

### Behavior
- Grid with Nearby / Following / Mine filters that work; "+" for a new project. [FS] [R32]
- First visit: one dismissable line ("See what people are building…"). [F067] [R6] [M1018c]
- No map. Grid on desktop, list on phone. Root tab: no Back. [F052] [TK§1] [R13]

### States
- Each filter has a friendly empty state. [R32]

### Copy
- Drawn empty heading "No projects yet" reads like the banned empty copy; check against the no-empty-copy rule. [F035] [R4]

---

## New project (`project-new`)
URL: /mockups/?style=fresh&device=phone#project-new  ·  desktop: /mockups/?style=fresh&device=desktop#project-new

### Purpose
- Create a project: cover, name, kind, one line. [FS] [drawn]

### Scenarios
- Signed out: Create → sign-in sheet. [FS]
- Signed in: Create → `#project`. [FS]

### Behavior
- Needs sign-in (sheet at Create). Desktop: centered dialog. [FS]

---

## Project update (`project-update`)
URL: /mockups/?style=fresh&device=phone#project-update  ·  desktop: /mockups/?style=fresh&device=desktop#project-update

### Purpose
- Owner posts an update: title, notes, image. [FS] [R35]

### Scenarios
- Signed out: Post update → sign-in sheet. [unsourced]
- Signed in: Post update → `#project`. [R35]

### Behavior
- Desktop: centered dialog. [FS]

---

## Post up for a project (`project-attach`)
URL: /mockups/?style=fresh&device=phone#project-attach  ·  desktop: /mockups/?style=fresh&device=desktop#project-attach

### Purpose
- Post up tied to a project, now or "I was here earlier". [FS]

### Scenarios
- Signed out: Post up 🔒 → `#attach-signin`. [FS]
- Signed in: Post up → `#posted`. [FS]

### Behavior
- "I was here earlier" adds it to the cafe's recent activity. [drawn]
- Needs sign-in → `#attach-signin`. [FS]
- Desktop: centered dialog. [FS]

### Copy
- "I was here earlier", not "Earlier today". [TK§2] [R19⚠]

---

## Where are you? (`where`)
URL: /mockups/?style=fresh&device=phone#where  ·  desktop: /mockups/?style=fresh&device=desktop#where

### Purpose
- Cafe picker for posting: nearby cafes by distance plus search. [F062] [F097] [R17]

### Scenarios
- None live: no "· 2 live" on the cafe rows. [M1018]
- Signed out / in: same. [M1018]

### Behavior
- Not a map: a map only helps with curated cafes, which we don't have yet. [F058]
- Picking a cafe returns to the form with it set. [drawn]
- Desktop: centered dialog. [FS]

### Open
- Location-permission explainer / denied fallback: the ledger has it open, the final-screens list says not adopted. [R21] [FS]

### Gap fixes
- Gap fix (Oct 25): tapping the search box opens `#where-search`. [M1025]

---

## Cafe search (`where-search`)
URL: /mockups/?style=fresh&device=phone#where-search  ·  desktop: /mockups/?style=fresh&device=desktop#where-search

### Purpose
- Search results in the picker. [FS]

### Scenarios
- Same in all scenarios. [M1018]

### Behavior
- Google Places Autocomplete in our UI is fine; show "powered by Google" attribution. [F097] [FS]

---

## Edit postup (`post-edit`)
URL: /mockups/?style=fresh&device=phone#post-edit  ·  desktop: /mockups/?style=fresh&device=desktop#post-edit

### Purpose
- Change your live postup; Save → `#live`. [FS] [drawn]

### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]

### Decisions
- Managing your own postup is important. [F057]

---

## You're live (`live`)
URL: /mockups/?style=fresh&device=phone#live  ·  desktop: /mockups/?style=fresh&device=desktop#live

### Purpose
- Manage your live postup. [FS] [F057]

### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. Live toggle: no effect (your own postup). [M1018]

### Behavior
- Time-left ring, cafe, project, +30 min, Edit, Who can join. [FS]
- Requests with the joiner's reason: Approve / Decline. Joined list. Group chat. Share. End postup (confirm). [FS] [F061]
- Your live state also shows on home. [R22]
- Desktop: map + right panel. [FS]

### Decisions
- Before this screen, nothing showed you were live (review gap). [F112]

---

## Postup · ask to join (`postup-ask`)
URL: /mockups/?style=fresh&device=phone#postup-ask  ·  desktop: /mockups/?style=fresh&device=desktop#postup-ask

### Purpose
- A postup where the poster approves who joins. [FS] [F055]

### Scenarios
- Signed out: Ask to join 🔒 → `#ask-signin`. [FS]
- Signed in: Ask to join → `#ask`. [FS]
- Live / none: no effect. [M1018]

### Behavior
- "Tess approves who joins" → Ask to join → sign-in → `#ask` → `#requested`. [FS]

### Open
- Show the cafe name before approval? Martin never answered. Code hides it (D2); the mockup shows it. [F070] [R23]

---

## Ask to join (`ask`)
URL: /mockups/?style=fresh&device=phone#ask  ·  desktop: /mockups/?style=fresh&device=desktop#ask

### Purpose
- Write a short reason for joining. [F061] [F095]

### Scenarios
- Same in all scenarios; reached after signing in. [M1018]

### Behavior
- Poster gets an alert and approves or declines. [F095] [F055]

---

## Request sent (`requested`)
URL: /mockups/?style=fresh&device=phone#requested  ·  desktop: /mockups/?style=fresh&device=desktop#requested

### Purpose
- Confirmation after asking. [FS]

### Scenarios
- Same in all scenarios. [M1018]

### Behavior
- See who else is nearby; View postup; Cancel request. [drawn]

---

## Postup ended (`postup-ended`)
URL: /mockups/?style=fresh&device=phone#postup-ended  ·  desktop: /mockups/?style=fresh&device=desktop#postup-ended

### Purpose
- State: the postup is over. [F060] [R47]

### Scenarios
- Same in all scenarios. [M1018]

### Behavior
- See what's nearby; Follow the poster for next time. [drawn]

### Gap fixes
- Gap fix (Oct 25): "Follow Maya for next time" is a Follow button (sign-in sheet when signed out) plus a "Go to Home" link. [M1025]

---

## Postup full (`postup-full`)
URL: /mockups/?style=fresh&device=phone#postup-full  ·  desktop: /mockups/?style=fresh&device=desktop#postup-full

### Purpose
- State: the poster isn't taking more people. [F060] [R47]

### Scenarios
- Same in all scenarios. [M1018]

---

## Postup cancelled (`postup-cancelled`)
URL: /mockups/?style=fresh&device=phone#postup-cancelled  ·  desktop: /mockups/?style=fresh&device=desktop#postup-cancelled

### Purpose
- State: the poster cancelled. [F060] [R47]

### Scenarios
- Same in all scenarios. [M1018]

---

## Share link · live postup (`invite`)
URL: /mockups/?style=fresh&device=phone#invite  ·  desktop: /mockups/?style=fresh&device=desktop#invite

### Purpose
- Logged-out landing for a shared postup link. [FS] [R39] [F066]

### Scenarios
- Signed out: Join 🔒 → sign-in sheet. [FS]
- Signed in: Join → `#joined`. [FS]
- Live / none: no effect; the shared postup is live. [M1018]

### Copy
- "Maya is working at Bean Theory till 4. Join her?" plus one line on what PostUp is. [FS] [R39]

### Links
- Join → sign-in → `#joined`. Cafe → `#cafe`. [drawn]

---

## Share link · ended (`invite-ended`)
URL: /mockups/?style=fresh&device=phone#invite-ended  ·  desktop: /mockups/?style=fresh&device=desktop#invite-ended

### Purpose
- Shared link to a postup that ended → what's nearby. [FS] [R39]

### Scenarios
- Same in all scenarios. [M1018]

### Gap fixes
- Gap fix (Oct 25): adds "Follow Maya for next time" (sign-in sheet when signed out; signing in returns here, Following) and "Go to Home". [M1025]

### Was the flow "Share link to an ended postup"
- Now a single screen state, not a flow: an invite link whose postup has ended lands here (see the Share link to a live postup flow's edge cases). [M1032]
- Signed-out visitor opening an old link should not hit a dead end: see what's nearby and follow the poster. [M1024]
- "This postup ended" + See what's nearby, Follow Maya for next time, Go to Home. [FS] [R39]
- Follow → sign-in sheet; back on the page signed in, Follow shows Following; Go to Home opens Home in Building mode. [FS] [M1018] [M1025]
- Cancelled instead of ended: #postup-cancelled copy. No 404; a next step is always offered. [F060] [M1024]

---

## Empty area (`empty-area`)
URL: /mockups/?style=fresh&device=phone#empty-area  ·  desktop: /mockups/?style=fresh&device=desktop#empty-area

### Purpose
- Nobody is live nearby: show what happened here lately instead of an empty screen. Recently nearby (past postups: who, cafe, day, project) → `#profile`; Projects nearby → `#project`; then cafes to be the first today and Post up. [M1032]
- Was: an area with no postups yet, "Be the first here". [FS]

### Scenarios
- Same in all scenarios (the area has no postups by definition). [M1018]

### Behavior
- No fake activity. [TK§2]
- Recent activity is real past postups and project updates from the area (this week first, then older); if there is none at all, projects in general, then cafes. [M1032]

### Overrides
- No postups means no map on home; the drawing shows one. Focus on projects. [F044] [R1]
- Nothing this week → projects in general. [F043]

### Open
- A fallback list of good cafes for empty areas. [TK§4]

---

## Cafe · Google card failed (`cafe-gfail`)
URL: /mockups/?style=fresh&device=phone#cafe-gfail  ·  desktop: /mockups/?style=fresh&device=desktop#cafe-gfail

### Purpose
- Place card failed to load. [F060]

### Scenarios
- None live: no Here now section, same as `#cafe`. [M1018]

### Behavior
- "Details unavailable", Open in Maps, Retry. [FS] [R37]

---

## Loading (`loading`)
URL: /mockups/?style=fresh&device=phone#loading  ·  desktop: /mockups/?style=fresh&device=desktop#loading

### Purpose
- Skeleton while the feed loads. [FS] [F060] [TK§1]

### Scenarios
- Same in all scenarios. [M1018]

---

## Offline (`offline`)
URL: /mockups/?style=fresh&device=phone#offline  ·  desktop: /mockups/?style=fresh&device=desktop#offline

### Purpose
- Last loaded Nearby feed with an offline banner and Retry. Not a blank screen. [FS]

### Scenarios
- Same in all scenarios. [M1018]

### Open
- The ledger asks for a full offline screen, not just a banner; the final mockup is the cached feed + banner. [R46⚠] [FS]

---

## Group chat (`chat`)
URL: /mockups/?style=fresh&device=phone#chat  ·  desktop: /mockups/?style=fresh&device=desktop#chat

### Purpose
- One group chat per postup: the poster and joined/approved people. Needed at launch. [F061] [F096] [FS]

### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]

### Behavior
- "Only people in this postup can see this chat." [FS]
- Per-message ⋯: copy, report, block. [F096] [FS]
- Header → `#postup`. Desktop: full page. [drawn] [FS]

### Open
- Retention: code uses 24h; that's our default. [R31] [FS]

---

## Inbox · Chats (`inbox`)
URL: /mockups/?style=fresh&device=phone#inbox  ·  desktop: /mockups/?style=fresh&device=desktop#inbox

### Purpose
- Inbox tab: your postup chats. [FS] [F096]

### Scenarios
- Signed out: sign-in sheet over it; no unread dot. [unsourced]
- Signed in: as drawn. [drawn]

### Behavior
- Chats | Activity tabs. Ended chats dimmed. Unread dot on the tab. Root tab: no Back. [FS] [R13]

---

## Inbox · Activity (`activity`)
URL: /mockups/?style=fresh&device=phone#activity  ·  desktop: /mockups/?style=fresh&device=desktop#activity

### Purpose
- Requests, joins, "said yes", messages, follows. [FS]

### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]

### Behavior
- Each row opens the related screen (request → `#live`, message → `#chat`, follow → `#profile`). [drawn]

### Open
- Email alerts. [TK§4]

---

## Profile (`profile`)
URL: /mockups/?style=fresh&device=phone#profile  ·  desktop: /mockups/?style=fresh&device=desktop#profile

### Purpose
- Someone's public profile. [FS] [F065]

### Scenarios
- None live: no live card. [M1018]
- Signed out: Follow → sign-in sheet. [FS]
- Signed in: Follow toggles. [FS]

### Behavior
- Live card, avatar, bio, "N postups · since Sep", Follow, regular cafes, projects, past postups. [FS] [R76]
- ⋯ → report / block. [FS] [F059]

---

## My profile (`me`)
URL: /mockups/?style=fresh&device=phone#me  ·  desktop: /mockups/?style=fresh&device=desktop#me

### Purpose
- Your own profile. [FS] [F065]

### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]

### Behavior
- Live card → `#live`, Edit profile, gear → `#settings`. [FS]
- Desktop rail avatar opens this. [FS]

---

## Settings (`settings`)
URL: /mockups/?style=fresh&device=phone#settings  ·  desktop: /mockups/?style=fresh&device=desktop#settings

### Purpose
- Notification toggles; Account: Blocked people, Sign out, Delete account. [FS] [F065]

### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]

### Unsourced
- Account deletion in the app (store guideline 5.1.1). [R43⚠]

### Open
- Email alerts. [TK§4]

### Gap fixes
- Gap fix (Oct 25): Sign out signs you out and lands on Home (was the share-link page); Delete account also lands on Home, signed out. [M1025]

---

## Report (`report`)
URL: /mockups/?style=fresh&device=phone#report  ·  desktop: /mockups/?style=fresh&device=desktop#report

### Purpose
- Report a person, postup or message: reason + optional details. [F059] [drawn]

### Scenarios
- Same in all scenarios. [M1018]

### Unsourced
- Admin reports page for Martin only. [R30⚠]

### Open
- No user ban system yet. [TK§4]

---

## Reported (`reported`)
URL: /mockups/?style=fresh&device=phone#reported  ·  desktop: /mockups/?style=fresh&device=desktop#reported

### Purpose
- Thanks; offer to block too. [FS]

### Scenarios
- Same in all scenarios. [M1018]

### Copy
- "They won't know you reported them." No safety tips. [FS] [F059]

---

## Share link · project (`invite-project`)
URL: /mockups/?style=fresh&device=phone#invite-project  ·  desktop: /mockups/?style=fresh&device=desktop#invite-project

### Purpose
- Logged-out landing for a shared project link. [F067] [R39]

### Scenarios
- Signed out: Follow 🔒 → sign-in sheet. [FS]
- Signed in: Follow toggles to Following. [FS]

### Copy
- "Maya is building Star Fox 64 mod" — see updates, follow, or join her next postup. [FS]

### Behavior
- Follow needs sign-in. [FS]

---

## Home overlay · alternative, not chosen (`home-overlay-alt`)
URL: /mockups/?style=fresh&device=phone#home-overlay-alt  ·  desktop: /mockups/?style=fresh&device=desktop#home-overlay-alt

### Purpose
- Comparison only: a projects card floating over a dimmed map. **Alternative, not chosen**; Home uses the Live · Building switch instead. [M1018b]

### Scenarios
- Same in all scenarios. [M1018]

### Behavior
- Card: 3 projects, See all projects, Post up, Show map (hides the card). [M1018b] [drawn]
- Heading "What people are building". [M1018c]

---

## Sheet · Block (`ov-block`)
URL: /mockups/?style=fresh&device=phone&ov=block#postup  ·  desktop: /mockups/?style=fresh&device=desktop&ov=block#postup · shown over #postup

### Purpose
- Block: you won't see each other's postups or messages; they aren't told. [FS] [F059]

### Scenarios
- Same in all scenarios. [M1018]

### Gap fixes
- Gap fix (Oct 25): the sheet links to Settings (Blocked people) to manage or undo blocks. [M1025]

---

## Sheet · Delete account (`ov-delacct`)
URL: /mockups/?style=fresh&device=phone&ov=delacct#settings  ·  desktop: /mockups/?style=fresh&device=desktop&ov=delacct#settings · shown over #settings

### Purpose
- Confirm deleting profile, postups and projects; can't be undone. [FS] [drawn]

### Scenarios
- Same in all scenarios. [M1018]

### Gap fixes
- Gap fix (Oct 25): Delete account signs you out and lands on Home. [M1025]

---

## Sheet · Directions (`ov-dirs`)
URL: /mockups/?style=fresh&device=phone&ov=dirs#joined  ·  desktop: /mockups/?style=fresh&device=desktop&ov=dirs#joined · shown over #joined

### Purpose
- Open in Apple Maps / Google Maps. [FS]

### Scenarios
- Same in all scenarios. [M1018]

### Unsourced
- Ledger item for directions. [R25⚠]

---

## Sheet · End postup (`ov-endlive`)
URL: /mockups/?style=fresh&device=phone&ov=endlive#live  ·  desktop: /mockups/?style=fresh&device=desktop&ov=endlive#live · shown over #live

### Purpose
- Confirm ending; joiners and anyone waiting get an alert. [FS] [drawn]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · Leave (`ov-leave`)
URL: /mockups/?style=fresh&device=phone&ov=leave#joined  ·  desktop: /mockups/?style=fresh&device=desktop&ov=leave#joined · shown over #joined

### Purpose
- Confirm leaving; the poster gets an alert. [FS] [drawn]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · More (`ov-more`)
URL: /mockups/?style=fresh&device=phone&ov=more#postup  ·  desktop: /mockups/?style=fresh&device=desktop&ov=more#postup · shown over #postup

### Purpose
- View profile, Share, Report, Block. [FS] [F059]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · Message options (`ov-msg`)
URL: /mockups/?style=fresh&device=phone&ov=msg#chat  ·  desktop: /mockups/?style=fresh&device=desktop&ov=msg#chat · shown over #chat

### Purpose
- Copy, Report message, Block sender. [F096] [FS]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · Share (`ov-share`)
URL: /mockups/?style=fresh&device=phone&ov=share#posted  ·  desktop: /mockups/?style=fresh&device=desktop&ov=share#posted · shown over #posted

### Purpose
- Share sheet: link with Copy, then Messages / WhatsApp / Email / More. [drawn]

### Scenarios
- Same in all scenarios. [M1018]

### Unsourced
- Share opens this sheet, never the poster's success screen. [R41⚠]

---

## Sheet · Sign in (join, ask, post, follow, create, update) (`ov-signin`)
URL: /mockups/?style=fresh&device=phone&ov=signin#profile  ·  desktop: /mockups/?style=fresh&device=desktop&ov=signin#profile · shown over #profile

### Folded pages
- `#join-signin`, `#ask-signin`, `#post-signin` and `#attach-signin` are no longer pages: their button opens this sheet over the same page (`act`), and signing in continues to the action. Old links redirect here. [M1031-draft]

### Purpose
- Sign-in sheet for Follow, Create project and Post update when signed out. Signing in switches the toggle to Signed in and continues. [FS] [M1018]

### Scenarios
- Signed out only; signed in never shows it. [FS]

### Was #join-signin (over #postup): Purpose
- Sign-in sheet over the postup when you tap Join (also used by Follow on `#invite-project`). [FS] [drawn]

### Was #join-signin (over #postup): Scenarios
- Signed out: the sheet. [FS]
- Signed in: no sheet; shows `#postup`. [FS] [M1018]

### Was #join-signin (over #postup): Behavior
- Success → `#joined`. [FS]

### Was #ask-signin (over #postup-ask): Purpose
- Sign-in sheet before asking to join. Success → `#ask`. [FS] [drawn]

### Was #ask-signin (over #postup-ask): Scenarios
- Signed in: no sheet; shows `#postup-ask`. [FS] [M1018]

### Was #post-signin (over #post): Purpose
- The global sign-in sheet, shown at the moment of action. Variants: join, ask, attach. [FS]

### Was #post-signin (over #post): Scenarios
- Signed out: the sheet, as drawn. [FS]
- Signed in: no sheet; shows `#post`. [FS] [M1018]

### Was #post-signin (over #post): Behavior
- Continue with Apple / Google, "Not now". The build also adds a dev sign-in and "Use a PostUp username" (→ /login). [FS]
- Only at post, join, follow, new project. [FS]
- Success → `#posted`. [drawn]

### Was #post-signin (over #post): Unsourced
- Every "Log in" link opens this sheet, not the /login page. [R10⚠]

### Was #attach-signin (over #project-attach): Purpose
- Sign-in sheet when posting up for a project. Success → `#posted`. [FS] [drawn]

### Was #attach-signin (over #project-attach): Scenarios
- Signed in: no sheet; shows `#project-attach`. [FS] [M1018]

---

## Sources cited
- **F003** — Map provider must have a hard cap; prefer failing over surprise charges. (Martin, S03 t63u): “I'd like to find a map provider that has some limit cap so I don't get charged a bunch if we get lots of traffic, I'd rather the site jsut fail”
- **F004** — Tile coverage: the whole world. (Martin, S03 t70u): “the whole world”
- **F006** — Rejected paid Workers plan; go back to free tile plan. (Martin, S04 t90u): “ok let's switch back to one of those free plans”
- **F007** — Map tiles: Stadia Maps. (Martin, S04 t92u): “ok cool let's do stadia”
- **F013** — General UX rule: little on screen at a time; drill-down with back button. (Martin, S05 t119u): “In general I want to stick to there is always not much on the screen at at time”
- **F024** — Build in order of need; projects first because an empty map would greet users. (Martin, S08-mockups-1 t192u): “I want to develop features int he order that we will need them. It sounds liek the proejct section of postup is more important since an empty map woudl await users otherwise”
- **F026** — Mockups link to each other. (Martin, S08-mockups-1 t194u): “can you make the mockups link to each other?”
- **F029** — Proposal (accepted in later work): feed when no one live, map when live. (PostUp PM (assistant), S08-mockups-1): “When no one is live, I'd open on a feed instead, with recent postups, project updates and a big "Post up" button, and keep the map one tap away for picking a cafe. Once there are live postups, open on the map, since that's when it's exciting.”
- **F030** — Alternate feed-first mock; think about appeal. (Martin, S08-mockups-1 t197u): “yeah make it an alternate mock so I can compare. And think deep about what will be appeaing to people”
- **F031** — Consider images in feed. (Martin, S08-mockups-1 t198u): “(like do w eneed images, etc)”
- **F032** — Google photos never in feed. (PostUp PM (assistant), S08-mockups-1): “**Google photos stay out of the feed.** Their terms only allow them inside the Google card on a cafe's page.”
- **F033** — Optional photo ask after posting. (PostUp PM (assistant), S08-mockups-1): “after someone posts, ask "Add a photo of your spot?" as an optional step, so it doesn't slow posting down.”
- **F035** — Never say it's quiet. (Martin, S08-mockups-1 t200u): “I don't think we even need to say it's quiet right now btw”
- **F036** — Keep current style; try other fundamental styles. (Martin, S08-mockups-1 t201u): “this looks great! are there other fundamental styles we can try (keep this even if we make another style)”
- **F043** — First-visit experience required; fall back to projects in general when nothing this week. (Martin, S11 t244u): “the final site doesn't seem like it has the first experience liek we talked about? If there aren't things from this week, we should just show projects in general”
- **F044** — No map when no postups; focus on projects. (Martin, S11 t247u): “We weren't supposed to show the map when there's no post ups, we were going to focus on projects.”
- **F046** — Tab always called Home. (Martin, S11 t252u): “I think we just always call the map tab home btw”
- **F051** — Nearby feed on desktop should not show the map. (Martin, S08-mockups-2 t207u): “huh, but nearby feed with photos on desktop still shows the map?”
- **F052** — Projects must not show the map. (Martin, S08-mockups-2 t208u): “why does clicking on projects shwo the map?”
- **F053** — Map only on map, cafe and postup screens. (PostUp PM (assistant), S08-mockups-2): “The map now only shows on the map, cafe and postup screens.”
- **F055** — Join mode is a per-postup setting by the poster; poster is alerted. (Martin, S08-mockups-2 t210u): “1. That can be a setting on the postup by whoever started it. I did have in mind we'd alert the person starting it.”
- **F056** — Where-I'm-sitting note/picture: to-do. (Martin, S08-mockups-2 t210u): “2. You should be able to put a description of where you are or a picture.. let's leave this on the todo list for now”
- **F057** — Managing your own postup is important. (Martin, S08-mockups-2 t210u): “3. This is an important one, we should mock it up.”
- **F058** — Doubts the map as cafe picker. (Martin, S08-mockups-2 t210u): “idk if a map is the best way? A map is more useful when there is a list of curated good cafes to go to, but we don't have that starting out.”
- **F059** — Report and block yes; no safety tips. (Martin, S08-mockups-2 t210u): “5. Reporting and blocking woudl be good to have. Idk about safety tips, this site is for adults and they should be smart enough to understand the risks.”
- **F060** — Profile/account needed; fix wrong links; add ended/failed states. (Martin, S08-mockups-2 t210u): “8. yeah we need this, any ideas? 9. sure fix those 10. sure we can add those.”
- **F061** — Chat at launch; reason when requesting to join. (Martin, S08-mockups-2 t210u): “and yes, we need chat at launch. I think you can leave a reason why you want to join when requesting to join a postup where approval is required, and there is a chat for people in the postup”
- **F062** — Cafe picking via search sheet (agreed). (PostUp PM (assistant), S08-mockups-2): “Posting up opens a "Where are you?" sheet that lists nearby cafes by distance, with a search box.”
- **F063** — Dismissable first-visit welcome. (PostUp PM (assistant), S08-mockups-2): “A one-line welcome at the top of the feed the first time ("Post up at a cafe and see who's working nearby"), which you can dismiss.”
- **F064** — Phone and desktop menus match. (PostUp PM (assistant), S08-mockups-2): “**7. What I meant:** the phone and desktop layouts disagree. Desktop has a Nearby tab and phone doesn't, so I'll make the menus match.”
- **F065** — Profile contents. (PostUp PM (assistant), S08-mockups-2): “**8. Profile:** your photo and name, a short bio, and your regular cafes.”
- **F066** — Agreed to search picker, welcome/share pages (plus projects), menus, profile. (Martin, S08-mockups-2 t211u): “4 - ok sounds good. 6. sure that sounds good - thoguh that doesn't cover the project updates section of the site. 7. ok good yeah choose whatever you think is best. 8. Cool yeah that works”
- **F067** — Projects first-visit line and project share landing. (PostUp PM (assistant), S08-mockups-2): “The Projects page gets its own first-visit line”
- **F070** — Cafe visibility asked; no Martin answer in transcript. (PostUp PM (assistant), S08-mockups-2): “the mockups show a postup's cafe name before anyone joins, but older copy said the exact spot stays hidden until the poster approves. Which do you want?”
- **F076** — All mockup styles via dev-only setting. (Martin, S08-mockups-3 t231u): “it'd be cool if we supported all the styling choices you did in the mockups, it can be a dev only setting that I can adjust in these mockups”
- **F085** — Google Photos/Places API cost concern — easy to overcharge. (Martin, S07 t164u): “My main concern there is the Google Photos api being heavy and easy to get overcharged”
- **F086** — App will encourage users to take photos. (Martin, S07 t165u): “So my app will encourage you to take photos”
- **F095** — Builder brief: join mode per-postup; ask-to-join with reason (parent→builder brief, S08-mockups-builder-2): “Join mode is a per-postup setting chosen by the poster: 'Anyone can join' or 'Ask to join'. Ask-to-join: joiner writes a short reason; poster gets an alert and approves/declines”
- **F096** — Builder brief: chat at launch (parent→builder brief, S08-mockups-builder-2): “Chat at launch: group chat per postup for joined people + poster; inbox listing chats; chat has report/block per message”
- **F097** — Builder brief: Where are you? cafe search sheet (parent→builder brief, S08-mockups-builder-2): “Where are you?' sheet: nearby cafes list by distance + search box (Google Places Autocomplete in our UI is fine; note attribution)”
- **F098** — Builder brief: dismissable first-visit welcome (parent→builder brief, S08-mockups-builder-2): “one-line welcome atop feed ('Post up at a cafe”
- **F110** — UX review: first-time visitor not told what PostUp is (UX-review subagent, S08-mockups-ux-review): “first-time visitor isn't told what PostUp is, there's no reason to trust a stranger, and after you post up or join, the flow just stops”
- **F112** — UX review gap: manage live postup (UX-review subagent, S08-mockups-ux-review): “Managing your own postup:** once posted, nothing shows you're live”
- **R1** — requirements.md item 1: No live postups means no map on home. Home focuses on projects instead; the map appears only when postups exist.
- **R2** — requirements.md item 2: When postups are live, home is the map with "Live now" (side panel on desktop).
- **R3** — requirements.md item 3: With no activity this week, home and the feed fall back to recent projects of any age. Never empty or "quiet" copy.
- **R4** — requirements.md item 4: No empty or "quiet" copy anywhere ("No posts yet", "Nothing yet", "Nobody.", "quiet").
- **R5** — requirements.md item 5: First-visit explainer: what PostUp is (cafes, postups, join), dismissable.
- **R6** — requirements.md item 6: First-visit guidance on Projects.
- **R7** — requirements.md item 7: Location context, e.g. "Near Westside, Los Angeles".
- **R8** — requirements.md item 8: Launch area is Playa Vista / Westside LA as the fallback centre (D1).
- **R9** — requirements.md item 9: Sign-in only at the moment of action, as a sheet over the current screen (Apple + Google).
- **R10** — requirements.md item 10: Every "Log in" link opens the sheet, not the /login page.
- **R11** — requirements.md item 11: Signed-out drafts survive sign-in.
- **R12** — requirements.md item 12: Phone tab bar: Map, Nearby, Post up, Projects, Inbox. Desktop left rail with the same items. Consistent across devices.
- **R13** — requirements.md item 13: Root tabs have no Back button.
- **R14** — requirements.md item 14: No "Mockups" link in the real nav.
- **R15** — requirements.md item 15: Avatar in nav and a visible signed-in vs signed-out difference.
- **R16** — requirements.md item 16: Sign in required to post; anonymous posting is off (D3).
- **R17** — requirements.md item 17: Post form: cafe preselected, a real "Change" picker ("Where are you?" with nearby list and search), "Working on" text, project chips, Until 1h/2h/3h/time, Who can join.
- **R18** — requirements.md item 18: Default join mode is "Anyone can join" (D5).
- **R19** — requirements.md item 19: Attach-to-project requires sign-in, and the past option reads "I was here earlier".
- **R20** — requirements.md item 20: Optional "Add a photo of your spot", asked after posting on the confirmation screen; never required.
- **R21** — requirements.md item 21: Location permission explainer, plus a denied state that falls back to search/pick.
- **R22** — requirements.md item 22: Manage your live postup: time left, Extend, Edit, End, shown on home.
- **R23** — requirements.md item 23: Ask-to-join hides the cafe (neighborhood only) until approved (D2).
- **R24** — requirements.md item 24: Explain what Join means ("Let Maya know you're coming, then say hi at the cafe").
- **R25** — requirements.md item 25: Directions open Apple/Google Maps.
- **R30** — requirements.md item 30: Admin reports page for Martin only.
- **R31** — requirements.md item 31: Chat for poster and approved joiners, readable 24h after end (D6).
- **R32** — requirements.md item 32: Projects grid with Nearby / Following / Mine tabs that work, each with a friendly empty state.
- **R34** — requirements.md item 34: Test or hidden projects never show.
- **R35** — requirements.md item 35: Project page, updates timeline with images, owner posts updates.
- **R36** — requirements.md item 36: Google Places content only inside UI Kit widgets, never in the feed; we store only `place_id`.
- **R37** — requirements.md item 37: Google card failure falls back ("Details unavailable", Open in Maps, Retry).
- **R38** — requirements.md item 38: Feed photos come from users and projects only; fallback is a tinted tile, never a grey box.
- **R39** — requirements.md item 39: Share landings: live postup ("X is working at Y till Z. Join?"), ended postup (→ what's nearby), project ("X is building Y").
- **R40** — requirements.md item 40: Feed items link person → profile, cafe → cafe, project → project.
- **R41** — requirements.md item 41: Share opens a share sheet (not the poster's success screen).
- **R43** — requirements.md item 43: Account deletion in the app (store guideline 5.1.1).
- **R46** — requirements.md item 46: Offline: a full offline screen (mockup), not just a banner.
- **R47** — requirements.md item 47: Ended / full / cancelled states.
- **R53** — requirements.md item 53: Nav tab for / is always labeled "Home" (never "Map").
- **R69** — requirements.md item 69: The map shows only on map, cafe and postup screens; Projects and the Nearby feed never show it.
- **R76** — requirements.md item 76: Profile: photo, name, bio, regular cafes, projects, past postups, follow button, settings and sign out.
- **FS** — final-screens.md (final screens answer, Oct 2026)
- **M1018** — Martin, Oct 18 2026 (relayed by the PM): every page gets a scenario toggle (signed out/in × live nearby/none) and renders that scenario; pages that do not differ say "same in all scenarios"; mark the home page (/) clearly
- **M1018b** — Martin, Oct 18 2026 (relayed by the PM): Home (/) has two modes on one URL, Live (map + Live now) and Building (projects preview, See all projects, Post up, This week); default by whether anyone is live; Live · Building switch; banner when someone goes live in Building; draw the overlay-on-map version as #home-overlay-alt, alternative, not chosen
- **M1018c** — Martin, Oct 18 2026 (relayed by the PM): the Building heading is "What people are building" (not "nearby"); the list is sorted closest-first and shows the closest projects available even if none are local; never claim "nearby" unless they are
- **M1024** — Martin, Oct 24 2026 (relayed by the PM): keep tracking user types/scenarios and also track critical flows: a type of user arrives in a certain situation and goes through a scenario step by step; draft all important MVP flows
- **M1025** — Martin, Oct 25 2026 (relayed by the PM): a flow map, a state machine from a first-time visitor (not registered) showing how users reach the starting point of each flow
- **M1031-draft** — PM draft decision, Oct 31 2026 (model phase 2, approved scope; each one listed for Martin to confirm)
- **M1032** — Martin, Oct 28 2026: phase scope decisions (phase 2 = MVP; ask/approve in phase 2; merged flows; empty area shows recent activity and projects)
- **drawn** — the mockup drawing itself
- **unsourced** — no source; confirm with Martin
- **TK§1** — mockup-takeaways.md (mockup session takeaways) §1
- **TK§2** — mockup-takeaways.md (mockup session takeaways) §2
- **TK§4** — mockup-takeaways.md (mockup session takeaways) §4

---

# Critical flows
Critical flows (Martin, Oct 24 2026 [M1024]): a type of user arrives in a certain situation and goes through a scenario step by step. Each step names the screen and the scenario params (auth, live, Home mode, sheet). Flows marked Draft were inferred from the screen notes; confirm with Martin.

## Flow: Newcomer looks around, then joins (`look-around`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/look-around.html

### Persona
- First-time visitor, signed out: curious what PostUp is, or has no idea and arrived from search, a social post or a link.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- Understand PostUp from the first screen, see live and past content, and join someone; sign in only at Join. [M1024] [M1025] [M1032]

### Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: postup@out.live (M 2), postup-ask@out.live (T), cafe@out.live (cafe), **home@out.live.building** (Building), quiet@out.live (Locate), project@out.live (Star Fox 64 mod), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), me@out.live (S), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: none
2. **home@out.live.building** · user: What is this, really? · action: switches to Building · edge: tap: Building
   - Building: the welcome line "Post up at a cafe. See who's working nearby." and projects first. [M1018b] [drawn] [M1025]
   - next site states: home@out.live.live (Live), cafe@out.live (Lantern Tea A D M 3 postups), me@out.live (S), projects@out.live (See all projects), **project@out.live** (Star Fox 64 mod M Maya · Yesterday), post@out.live (Post up), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), cafe-gfail@out.live (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
3. **project@out.live** · user: Gets it: people work on projects at cafes · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Opens a project: updates and past postups. [FS] [M1025]
   - next site states: back (Back), project-new@out.live (New), **profile@out.live** (Maya), project-update@out.live (Update), project-attach@out.live (Post up), cafe@out.live (Bean Theory), postup@out.live (M Maya Bean Theory · till 4pm Live), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), me@out.live (S), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **profile@out.live** · user: Who is behind it? · action: taps the owner · edge: tap: Maya
   - Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025]
   - next site states: back (Back), profile+more@out.live (More), **postup@out.live** (Live at Bean Theory Till 4pm · Sta), profile+signin@out.live (Follow), cafe@out.live (Bean Theory), project@out.live (Star Fox 64 mod Updated yesterday), home@out.live.live (home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
5. **postup@out.live** · user: She's live right now · action: taps Live at Bean Theory · edge: tap: Live at Bean Theory Till 4pm · Sta
   - Her live postup; Join shows 🔒. [FS] [M1024]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **postup+signin@out.live** (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: none
6. **postup+signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: postup@out.live (close), postup@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
7. **joined@in.live** · user: Signed in; committed · action: signs in · edge: tap: Continue with Apple
   - Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)

### Connected flows [M1025]
- `join`: branch out at step 7→3; merge in at step 7 (from its step 3)
- `invite-live`: branch out at step 7→3; merge in at step 7 (from its step 3)
- `leave`: branch out at step 7→1; merge in at —

### Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#home` · auth=out live=live mode=building — Building: the welcome line "Post up at a cafe. See who's working nearby." and projects first. [M1018b] [drawn] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
3. `#project` · auth=out live=live — Opens a project: updates and past postups. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)
4. `#profile` · auth=out live=live — Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#profile)
5. `#postup` · auth=out live=live — Her live postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
6. `#postup` + sheet `signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#postup)
7. `#joined` · auth=in live=live — Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)

### Branches and edge cases
- Joins straight from Live now: taps a live row, Join 🔒, sign-in sheet, joined in one go (was Curious visitor joins someone live). [FS] [M1018] [M1024]
- Follows the maker instead of joining: Follow 🔒 → sign-in sheet → signed in and following (was Curious browser). [FS] [M1025]
- No idea what PostUp is: taps the first live person, then the cafe, to understand by example (was Stumbled on it). [FS] [M1025]
- Nobody live: Home opens in Building, so the flow starts at the projects (merged from the old first-visit-none flow). [M1018b] [M1025]
- Taps Post up instead: see Came to post up. [M1025]
- Not now on the sheet: stays signed out, nothing lost. [drawn] [M1025]
- Never empty or "quiet" copy when nothing is live. [F035] [R4]
- Nobody live: Home opens in Building, where the welcome line shows first. [M1018b] [drawn] [M1025]
- Dismisses the welcome (×): it should stay dismissed. [drawn] [unsourced]
- Leaves after the first screen: the value has to be clear without scrolling. [M1025]
- Not now on the sheet: stays on the postup, still signed out. [drawn] [M1024]
- Switches to Building to look at projects first. [M1018b] [M1024]

### Success criteria
- No sign-in before an action. [FS]
- After sign-in the original action completes. [M1018] [M1024]
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

### Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

---

## Flow: Nobody live nearby (newcomer) (`empty-area-newcomer`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area-newcomer.html

### Persona
- First-time visitor, signed out, in an area where nobody is live right now.

### Starting state
- auth=out · live=none · device=phone · entry URL `/`

### Goal
- With nobody live nearby, see what happened here lately and projects nearby, then join in later or be the first. [M1032]

### Steps
1. **home@out.none.building** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home in Building mode: closest projects. [M1018c]
   - next site states: home@out.none.live (Live), cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), **empty-area@out.none** (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: first-post step 1 (if Came to post up right now)
2. **empty-area@out.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups) and Projects nearby, then cafes to be the first. [M1032]
   - next site states: cafe@out.none (cafe), me@out.none (S), post@out.none (Stories Cafe 0.3 mi), **profile@out.none** (Maya posted up at Bean Theory), project@out.none (Star Fox 64 mod), home@out.none.building (Home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: none
3. **profile@out.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@out.none (More), profile+signin@out.none (Follow), cafe@out.none (Bean Theory), project@out.none (Star Fox 64 mod Updated yesterday), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), post@out.none (Post up), me@out.none (S), cafe-gfail@out.none (Bean Theory (Google card fails))
   - enterable flows: none
4. **empty-area@out.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@out.none (cafe), me@out.none (S), post@out.none (Stories Cafe 0.3 mi), profile@out.none (Maya posted up at Bean Theory), **project@out.none** (Star Fox 64 mod), home@out.none.building (Home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: none
5. **project@out.none** · user: What are people making? · action: taps a project nearby · edge: tap: Star Fox 64 mod
   - A project nearby: updates and past postups. [FS] [M1032]
   - next site states: back (Back), project-new@out.none (New), profile@out.none (Maya), project-update@out.none (Update), project-attach@out.none (Post up), cafe@out.none (Bean Theory), home@out.none.building (Home), quiet-feed@out.none (Nearby), post@out.none (Post up), projects@out.none (Projects), inbox@out.none (Inbox), me@out.none (S), cafe-gfail@out.none (Bean Theory (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- `first-post`: branch out at step 1→1; merge in at —

### Screens
1. `#home` · auth=out live=none mode=building — Home in Building mode: closest projects. [M1018c] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#empty-area` · auth=out live=none — Nobody's live nearby: Recently nearby (past postups) and Projects nearby, then cafes to be the first. [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none#empty-area)
3. `#profile` · auth=out live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none#profile)
4. `#empty-area` · auth=out live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none#empty-area)
5. `#project` · auth=out live=none — A project nearby: updates and past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none#project)

### Branches and edge cases
- No past activity at all in the area: projects in general, then good cafes to be the first. [M1032]

### Success criteria
- Never an empty or "quiet" screen: recent postups and projects nearby are shown. [F035] [R4] [M1032]

### Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

---

## Flow: Join someone live (`join`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/join.html

### Persona
- Registered user, signed in, who wants company now.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Join a live postup and get there; checking the person first is optional. [M1024] [M1032]

### Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Found someone · action: taps a live row · edge: tap: M 2
   - Who, project, cafe, who else is joining. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: desktop-browse step 2 (if Checking one postup)
3. **joined@in.live** · user: Decides to join · action: taps Join · edge: tap: Join
   - You're joining; the poster is told. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), **joined+dirs@in.live** (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
4. **joined+dirs@in.live** · user: Needs the route · action: taps Directions · edge: tap: Directions
   - Directions sheet: Apple / Google Maps. [FS] [M1024]
   - next site states: **joined@in.live** (close)
   - enterable flows: none
5. **joined@in.live** · user: Knows the way · action: closes Directions · edge: tap: Cancel
   - Back on the joined screen. [M1031-draft]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **chat@in.live** (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
6. **chat@in.live** · user: Says they're coming · action: opens the group chat · edge: tap: Group chat
   - Says "on my way" in the postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `invite-live`: branch out at step 3→3; merge in at step 3 (from its step 3), step 5 (from its step 3)
- `leave`: branch out at step 3→1, step 5→1; merge in at —
- `chat`: branch out at step 6→2; merge in at step 6 (from its step 2)
- `catch-up`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Who, project, cafe, who else is joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#joined` · auth=in live=live — You're joining; the poster is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)
5. `#joined` · auth=in live=live — Back on the joined screen. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
6. `#chat` · auth=in live=live — Says "on my way" in the postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Optional check first (was Cautious joiner): from the postup, the project tag → project, the owner → profile (postup count, regular cafes, past postups), the cafe → cafe; Back returns each time. [FS] [F065] [M1024]
- Compares with an Ask to join postup (Tess): phase 2, see Ask to join. [M1032]
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

### Success criteria
- Home → joined in 2 taps. [M1024]
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

---

## Flow: Share link to a live postup (`invite-live`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-live.html

### Persona
- Friend of a poster, signed out, opened postup.now/p/… from a message.

### Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

### Goal
- Join the friend who shared the link. [M1024]

### Steps
1. **invite@out.live** · user: A friend sent this; knows the context · action: opens the share link · edge: entry
   - Landing for the shared postup. [FS] [R39]
   - next site states: project@out.live (Star Fox 64 mod), **invite+signin@out.live** (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: none
2. **invite+signin@out.live** · user: Wants to join the friend · action: taps Join 🔒 · edge: tap: Join Maya
   - Join → sign-in sheet. [FS] [M1024]
   - next site states: invite@out.live (close), invite@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
3. **joined@in.live** · user: Signed in; going · action: signs in · edge: tap: Continue with Apple
   - Joined. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **chat@in.live** (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), leave step 1 (if Plans changed)
4. **chat@in.live** · user: Wants to say hi before going · action: opens chat · edge: tap: Group chat
   - Postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `join`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `chat`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `leave`: branch out at step 3→1; merge in at —

### Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite)
2. `#invite` + sheet `signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#chat` · auth=in live=live — Postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- The postup has ended by the time the link is opened: lands on `#invite-ended` (This postup ended; See what's nearby, Follow Maya for next time, Go to Home). Was its own flow. [M1032]
- Link is to an ask-to-join postup → Ask to join flow. [FS] [M1024]
- Already signed in: Join goes straight to joined. [TK§1] [M1024]

### Success criteria
- The link works without an account until Join. [R39] [M1024]

---

## Flow: Nobody live nearby (signed in) (`empty-area`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area.html

### Persona
- Signed-in user in an area where nobody is live right now.

### Starting state
- auth=in · live=none · device=phone · entry URL `/`

### Goal
- With nobody live nearby, see what happened here lately and projects nearby, then join in later or be the first. [M1032]

### Steps
1. **home@in.none.building** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home in Building mode: closest projects. [M1018c]
   - next site states: home@in.none.live (Live), cafe@in.none (Lantern Tea A D M 3 postups), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), **empty-area@in.none** (area has no postups), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
2. **empty-area@in.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups) and Projects nearby, then cafes to be the first. [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), **profile@in.none** (Maya posted up at Bean Theory), project@in.none (Star Fox 64 mod), home@in.none.building (Home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none
3. **profile@in.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), project@in.none (Star Fox 64 mod Updated yesterday), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 1 (if Likes someone's work)
4. **empty-area@in.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), profile@in.none (Maya posted up at Bean Theory), **project@in.none** (Star Fox 64 mod), home@in.none.building (Home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none
5. **project@in.none** · user: What are people making? · action: taps a project nearby · edge: tap: Star Fox 64 mod
   - A project nearby: updates and past postups. [FS] [M1032]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: project-builder step 3 (if Project exists), following step 2 (if Wants to see what else is being built)

### Connected flows [M1025]
- `following`: branch out at step 3→1, step 5→2; merge in at step 5 (from its step 2)
- `project-builder`: branch out at step 5→3; merge in at step 5 (from its step 3)

### Screens
1. `#home` · auth=in live=none mode=building — Home in Building mode: closest projects. [M1018c] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)
2. `#empty-area` · auth=in live=none — Nobody's live nearby: Recently nearby (past postups) and Projects nearby, then cafes to be the first. [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)
3. `#profile` · auth=in live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
4. `#empty-area` · auth=in live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)
5. `#project` · auth=in live=none — A project nearby: updates and past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)

### Branches and edge cases
- No past activity at all in the area: projects in general, then good cafes to be the first. [M1032]

### Success criteria
- Never an empty or "quiet" screen: recent postups and projects nearby are shown. [F035] [R4] [M1032]

### Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

---

## Flow: Came to post up: first post with sign-in (`first-post`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post.html

### Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

### Starting state
- auth=out · live=none · device=phone · entry URL `/`

### Goal
- Go live in about ten seconds. [M1024]

### Steps
1. **home@out.none.building** · user: Came to post up right now · action: arrives at / · edge: entry
   - Taps Post up. [M1018b]
   - next site states: home@out.none.live (Live), cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), **post@out.none** (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: empty-area-newcomer step 1 (if Nobody around right now)
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), post+signin@out.none (Post up), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), me@out.none (S)
   - enterable flows: none
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), project-new@out.none (Project), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), post@out.none (Post up), me@out.none (S)
   - enterable flows: none
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), **where-search+signin@out.none** (Post up), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), post@out.none (Post up), me@out.none (S)
   - enterable flows: none
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), **posted@in.none** (signs in → continues)
   - enterable flows: none
6. **posted@in.none** · user: Live; wants company · action: signs in · edge: tap: Continue with Apple
   - Posted; link to copy. [FS]
   - next site states: home@in.none.building (Close), project@in.none (Star Fox 64 mod), **posted+share@in.none** (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: returning-post step 2 (if Posted; now live for others)
7. **posted+share@in.none** · user: Wants friends to come too · action: taps Invite friends · edge: tap: Invite friends
   - Invite friends: share sheet. [drawn] [M1024]
   - next site states: posted@in.none (close)
   - enterable flows: none

### Connected flows [M1025]
- `returning-post`: branch out at step 6→2; merge in at step 6 (from its step 2)
- `empty-area-newcomer`: branch out at step 1→1; merge in at —

### Screens
1. `#home` · auth=out live=none mode=building — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#where-search)
6. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)
7. `#posted` + sheet `share` · auth=in live=none — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=share#posted)

### Branches and edge cases
- Location denied: picker falls back to search. [R21] [unsourced]
- Cafe search fails without a Maps key → error state. [unsourced]

### Success criteria
- The form is not lost through sign-in. [M1018] [M1024]

### Needs Martin's decision
- Location-permission explainer: in or out? (ledger open, final list says not adopted) [R21] [FS]

---

## Flow: Returning poster (`returning-post`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/returning-post.html

### Persona
- Signed-in regular.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Post up with defaults, then see you're live. [M1024]

### Steps
1. **post@in.live** · user: Regular; working at a cafe today · action: taps Post up · edge: entry
   - Last project and nearest cafe preselected; no 🔒. [FS] [M1024]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: desktop-browse step 3 (if Wants to post too)
2. **posted@in.live** · user: Posted; now live for others · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), project@in.live (Star Fox 64 mod), posted+share@in.live (Invite friends), **live@in.live** (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company)
3. **live@in.live** · user: Managing their postup · action: opens their live postup · edge: tap: Manage postup
   - You're live: time left, requests, chat. [FS] [F057]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), **home@in.live.live** (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: hosting step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)
4. **home@in.live.live** · user: Checks they show up on Home · action: goes Home · edge: tap: Home
   - Your live state shows on home. [R22]
   - next site states: postup@in.live (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)

### Connected flows [M1025]
- `first-post`: branch out at step 2→6; merge in at step 2 (from its step 6)
- `host-approve`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `desktop-browse`: branch out at step 4→1; merge in at step 1 (from its step 3)
- `hosting`: branch out at step 3→1; merge in at —
- `join`: branch out at step 4→1; merge in at —
- `catch-up`: branch out at step 4→1; merge in at —

### Screens
1. `#post` · auth=in live=live — Last project and nearest cafe preselected; no 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#post)
2. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#posted)
3. `#live` · auth=in live=live — You're live: time left, requests, chat. [FS] [F057] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#home` · auth=in live=live mode=live — Your live state shows on home. [R22] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)

### Branches and edge cases
- Already live: Post up opens #live instead of a second postup. [unsourced] [M1024]

### Success criteria
- Home → live in 2 taps. [M1024]

### Needs Martin's decision
- Can someone have two postups at once? [unsourced]

---

## Flow: Hosting live: extend, edit, end (`hosting`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/hosting.html

### Persona
- Signed-in poster who is live.

### Starting state
- auth=in · live=live · device=phone · entry URL `/live`

### Goal
- Manage time and end cleanly. [M1024]

### Steps
1. **live@in.live** · user: Live; wants more time · action: opens their live postup · edge: entry
   - +30 min extends. [FS]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), **post-edit@in.live** (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: returning-post step 3 (if Managing their postup), host-approve step 2 (if Deciding on the request)
2. **post-edit@in.live** · user: Plans changed: different time · action: taps Edit · edge: tap: Edit
   - Edit cafe/what/until; Save → #live. [FS] [drawn]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **live@in.live** (Save), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: none
3. **live@in.live** · user: Saved · action: taps Save · edge: back
   - Back on live. [FS]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), **live+endlive@in.live** (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: returning-post step 3 (if Managing their postup), host-approve step 2 (if Deciding on the request)
4. **live+endlive@in.live** · user: Wrapping up · action: taps End postup · edge: tap: End postup
   - End postup → confirm; joiners and waiters alerted. [FS] [drawn]
   - next site states: live@in.live (close), **me@in.live** (End now)
   - enterable flows: none
5. **me@in.live** · user: Done for today · action: confirms End now · edge: tap: End now
   - Back home. [M1024] Ending your own postup doesn't change who else is live nearby (live = nearby, not this postup). [M1031-draft]
   - next site states: back (Back), settings@in.live (Settings), live@in.live (1:42 You're live at Bean Theory Ti), cafe@in.live (Lantern Tea), project-new@in.live (Tide Clock Updated Sun), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), cafe-gfail@in.live (Lantern Tea (Google card fails))
   - enterable flows: delete-account step 1 (if Leaving PostUp)

### Connected flows [M1025]
- `returning-post`: branch out at step 1→3, step 3→3; merge in at step 1 (from its step 3), step 3 (from its step 3)
- `host-approve`: branch out at step 1→2, step 3→2; merge in at step 1 (from its step 2), step 3 (from its step 2)
- `delete-account`: branch out at step 5→1; merge in at —

### Screens
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
2. `#post-edit` · auth=in live=live — Edit cafe/what/until; Save → #live. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#post-edit)
3. `#live` · auth=in live=live — Back on live. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup → confirm; joiners and waiters alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive#live)
5. `#me` · auth=in live=live — Back home. [M1024] Ending your own postup doesn't change who else is live nearby (live = nearby, not this postup). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#me)

### Branches and edge cases
- Time runs out: ends automatically, chat stays 24h. [R31] [FS]
- Closes "who can join" (full): new visitors see #postup-full. [F060] [R47]

### Success criteria
- Joiners always know the postup ended. [FS] [M1024]

---

## Flow: Postup chat (`chat`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/chat.html

### Persona
- Signed-in poster or joiner.

### Starting state
- auth=in · live=live · device=phone · entry URL `/inbox`

### Goal
- Coordinate in the group chat. [M1024]

### Steps
1. **inbox@in.live** · user: Wants to check messages · action: opens Inbox · edge: entry
   - Inbox · Chats. [FS] [F096]
   - next site states: activity@in.live (Activity 2), **chat@in.live** (M Maya's postup Maya: Grabbing ano), postup-ended@in.live (T Tess's postup Ended · Tue Tue), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: catch-up step 2 (if Checks messages first)
2. **chat@in.live** · user: Wants to sort out details in chat · action: opens a chat · edge: tap: M Maya's postup Maya: Grabbing ano
   - One chat per postup. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), **chat+msg@in.live** (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: none
3. **chat+msg@in.live** · user: Something off about a message · action: long-presses a message · edge: tap: Message options
   - Long-press: copy, report, block sender. [F096] [FS]
   - next site states: chat@in.live (close), report@in.live (Report message), chat+block@in.live (Block sender)
   - enterable flows: none

### Connected flows [M1025]
- `catch-up`: branch out at step 1→2; merge in at step 1 (from its step 2)

### Screens
1. `#inbox` · auth=in live=live — Inbox · Chats. [FS] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox)
2. `#chat` · auth=in live=live — One chat per postup. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)
3. `#chat` + sheet `msg` · auth=in live=live — Long-press: copy, report, block sender. [F096] [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=msg#chat)

### Branches and edge cases
- Signed out: sign-in sheet over Inbox. [unsourced]
- Chat closes 24h after the postup. [R31] [FS]

### Success criteria
- Only poster + joined/approved can read. [F061]

### Needs Martin's decision
- Chat retention (24h default). [R31] [FS]

---

## Flow: Report and block (`safety`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/safety.html

### Persona
- Signed-in user uncomfortable with someone.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Report and block quickly. [F059] [M1024]

### Steps
1. **postup+more@in.live** · user: Uncomfortable with someone · action: taps More · edge: entry
   - More: profile, share, report, block. [FS] [F059]
   - next site states: postup@in.live (close), profile@in.live (View profile), postup+share@in.live (Share), **report@in.live** (Report), postup+block@in.live (Block)
   - enterable flows: none
2. **report@in.live** · user: Wants to report · action: taps Report · edge: tap: Report
   - Reason + details. [F059] [drawn]
   - next site states: back (Back), **reported@in.live** (Send report), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: none
3. **reported@in.live** · user: Reported; still uneasy · action: sends the report · edge: tap: Send report
   - Thanks; offer to block. [FS]
   - next site states: home@in.live.live (Close), **reported+block@in.live** (Block Maya too), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: none
4. **reported+block@in.live** · user: Wants them gone · action: taps Block too · edge: tap: Block Maya too
   - Block: neither sees the other; they aren't told. [FS] [F059]
   - next site states: reported@in.live (close), home@in.live.live (Block), **settings@in.live** (Blocked people (Settings))
   - enterable flows: none
5. **settings@in.live** · user: Might undo later · action: opens Settings · edge: tap: Blocked people (Settings)
   - Blocked people list to undo. [FS] [F065]
   - next site states: back (Back), home@out.live.live (Sign out), settings+delacct@in.live (Delete account), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: delete-account step 2 (if Looking for the delete option), settings-notify step 1 (if Tuning alerts)

### Connected flows [M1025]
- `delete-account`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `settings-notify`: branch out at step 5→1; merge in at —

### Screens
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#reported)
4. `#reported` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block#reported)
5. `#settings` · auth=in live=live — Blocked people list to undo. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=live#settings)

### Branches and edge cases
- From a chat message: Message options → Report message. [F096]

### Success criteria
- No safety-tip screens. [F059] [FS]

### Needs Martin's decision
- No ban system yet: who reviews reports? [TK§4]

---

## Flow: Leave a postup you joined (`leave`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/leave.html

### Persona
- Signed-in joiner whose plans changed.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Back out politely. [M1024]

### Steps
1. **joined@in.live** · user: Plans changed · action: opens their joined postup · edge: entry
   - Leave link. [drawn]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), **joined+leave@in.live** (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), invite-live step 3 (if Signed in; going)
2. **joined+leave@in.live** · user: Backing out politely · action: taps Leave · edge: tap: Leave
   - Confirm; poster alerted. [FS] [drawn]
   - next site states: joined@in.live (close), **postup@in.live** (Leave)
   - enterable flows: none
3. **postup@in.live** · user: Out; back on the postup page · action: confirms Leave · edge: tap: Leave
   - Back home. [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)

### Connected flows [M1025]
- `join`: branch out at step 1→3, step 3→2; merge in at step 1 (from its step 3), step 3 (from its step 2)
- `invite-live`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `desktop-browse`: branch out at step 3→2; merge in at step 3 (from its step 2)

### Screens
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave#joined)
3. `#postup` · auth=in live=live — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

### Branches and edge cases
- The poster ended or cancelled first: #postup-cancelled. [F060]

### Success criteria
- Poster knows. [FS]

---

## Flow: Share link to a project (`invite-project`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-project.html

### Persona
- Signed-out visitor opening postup.now/project/… .

### Starting state
- auth=out · live=live · device=phone · entry URL `/project/…`

### Goal
- Follow the project to hear about the next postup. [M1024]

### Steps
1. **invite-project@out.live** · user: Friend's project link; curious about it · action: opens the project link · edge: entry
   - "Maya is building Star Fox 64 mod". [FS] [F067]
   - next site states: project@out.live (See updates), **invite-project+signin@out.live** (Follow), profile@out.live (Next postup: weekdays at Bean Theo), home@out.live.live (home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S)
   - enterable flows: none
2. **invite-project+signin@out.live** · user: Wants updates · action: taps Follow 🔒 · edge: tap: Follow
   - Follow 🔒 → sign-in sheet. [FS] [M1024]
   - next site states: invite-project@out.live (close), **invite-project@in.live** (Continue with Apple)
   - enterable flows: none
3. **invite-project@in.live** · user: Signed in; following · action: signs in · edge: tap: Continue with Apple
   - Sign-in returns to the same page, now following (Follow has no continuation). [M1031-draft]
   - next site states: **project@in.live** (See updates), profile@in.live (Next postup: weekdays at Bean Theo), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: none
4. **project@in.live** · user: Following · action: taps See updates · edge: tap: See updates
   - Following; live postups for the project shown. [FS] [M1024]
   - next site states: back (Back), project-new@in.live (New), profile@in.live (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#invite-project` · auth=out live=live — "Maya is building Star Fox 64 mod". [FS] [F067] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite-project)
2. `#invite-project` + sheet `signin` · auth=out live=live — Follow 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite-project)
3. `#invite-project` · auth=in live=live — Sign-in returns to the same page, now following (Follow has no continuation). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#invite-project)
4. `#project` · auth=in live=live — Following; live postups for the project shown. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)

### Branches and edge cases
- Project owner is live now: join from the project. [FS] [M1024]

### Success criteria
- Follow survives sign-in. [M1018] [M1024]

---

## Flow: Ask to join, then get approved (joiner side) (`ask-join`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/ask-join.html

### Persona
- Signed-in user; poster approves who joins.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Send a reason, get a yes, meet up. [M1024]

### Steps
1. **postup-ask@in.live** · user: Interested, but the host screens people · action: opens an ask-to-join postup · edge: entry
   - "Tess approves who joins". [FS] [F055]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **ask@in.live** (Ask to join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: catch-up step 4 (if My request was approved)
2. **ask@in.live** · user: Explaining why they want to join · action: taps Ask to join · edge: tap: Ask to join
   - Short reason. [F061] [F095]
   - next site states: back (Back), ask+share@in.live (Share), ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **requested@in.live** (Send request), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: none
3. **requested@in.live** · user: Waiting for an answer · action: sends the request · edge: tap: Send request
   - Request sent; can cancel. [FS] [drawn]
   - next site states: home@in.live.live (Close), quiet-feed@in.live (See who else is nearby), postup-ask@in.live (View postup), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
4. **activity@in.live** · user: Gets the yes · action: later: alert arrives · edge: event: alert arrives
   - Activity: "Tess said yes". [FS] [M1024]
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), **chat@in.live** (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: host-approve step 1 (if Hosting; someone wants in), following step 4 (if Hears that someone posted up), catch-up step 3 (if What else happened?)
5. **chat@in.live** · user: Now part of the group · action: opens the chat · edge: tap: M Maya: Hey! Here till 4 — come sa
   - Now in the postup chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `catch-up`: branch out at step 1→4, step 4→3; merge in at step 1 (from its step 4), step 4 (from its step 3)
- `following`: branch out at step 4→4; merge in at step 4 (from its step 4)
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

### Screens
1. `#postup-ask` · auth=in live=live — "Tess approves who joins". [FS] [F055] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
2. `#ask` · auth=in live=live — Short reason. [F061] [F095] (/mockups/?style=fresh&device=phone&auth=in&live=live#ask)
3. `#requested` · auth=in live=live — Request sent; can cancel. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#requested)
4. `#activity` · auth=in live=live — Activity: "Tess said yes". [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
5. `#chat` · auth=in live=live — Now in the postup chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Signed out: Ask to join → #ask-signin → #ask. [FS]
- Declined or no answer before the postup ends: shown in Activity, no chat. [unsourced] [M1024]
- Cafe name before approval: hidden or shown? [F070] [R23]

### Success criteria
- Joiner learns the outcome without refreshing. [F095] [M1024]

### Needs Martin's decision
- Show the cafe name before approval? (drawing shows it, code hides it) [F070] [R23]
- What the joiner sees if never answered. [unsourced]

---

## Flow: Host approves a request (`host-approve`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/host-approve.html

### Persona
- Signed-in poster with an ask-to-join postup.

### Starting state
- auth=in · live=live · device=phone · entry URL `/live`

### Goal
- Approve or decline with the joiner's reason in view. [M1024]

### Steps
1. **activity@in.live** · user: Hosting; someone wants in · action: later: alert arrives · edge: entry
   - Alert: "Ari asked to join". [FS]
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), **live@in.live** (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: ask-join step 4 (if Gets the yes), following step 4 (if Hears that someone posted up), catch-up step 3 (if What else happened?)
2. **live@in.live** · user: Deciding on the request · action: opens the request · edge: tap: D Dev asked to join your postup 2
   - Requests with reason: Approve / Decline. [FS] [F061]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), **profile@in.live** (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time)
3. **profile@in.live** · user: Wants to check the asker first · action: taps the asker · edge: tap: D Dev · 2 min ago
   - Optionally checks the asker's profile first. [FS] [M1024]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod Updated yesterday), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **live@in.live** · user: Asker looks fine; back to my postup · action: taps Back · edge: back
   - Back on your live postup; the profile has no chat link (as in the app). [M1031-draft]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), **chat@in.live** (Group chat), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time)
5. **chat@in.live** · user: Approved; welcoming them · action: opens the group chat · edge: tap: Group chat
   - Approved people are in the chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `returning-post`: branch out at step 2→3, step 4→3; merge in at step 2 (from its step 3), step 4 (from its step 3)
- `ask-join`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `following`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `catch-up`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `hosting`: branch out at step 2→1, step 4→1; merge in at —
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)

### Screens
1. `#activity` · auth=in live=live — Alert: "Ari asked to join". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
2. `#live` · auth=in live=live — Requests with reason: Approve / Decline. [FS] [F061] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
3. `#profile` · auth=in live=live — Optionally checks the asker's profile first. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
4. `#live` · auth=in live=live — Back on your live postup; the profile has no chat link (as in the app). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
5. `#chat` · auth=in live=live — Approved people are in the chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Decline: joiner is told politely. [F095] [unsourced]
- Block from the request via More. [F059] [M1024]

### Success criteria
- Approve in one tap from #live. [FS] [M1024]

---

## Flow: Project builder: create, update, post up for it (`project-builder`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/project-builder.html

### Persona
- Signed-in maker.

### Starting state
- auth=in · live=none · device=phone · entry URL `/projects`

### Goal
- Have a project page that collects updates and postups. [M1024]

### Steps
1. **projects@in.none** · user: Wants a home for their project · action: opens Projects · edge: entry
   - Projects, "+". [FS]
   - next site states: **project-new@in.none** (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S)
   - enterable flows: following step 3 (if Wants to see who they follow)
2. **project-new@in.none** · user: Starts a new project page · action: taps New project · edge: tap: New project
   - Cover, name, kind, one line. [FS] [drawn]
   - next site states: back (Back), **project@in.none** (Create), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S)
   - enterable flows: none
3. **project@in.none** · user: Project exists · action: taps Create · edge: tap: Create
   - New project page. [FS]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), **project-update@in.none** (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
4. **project-update@in.none** · user: Sharing progress · action: taps Update · edge: tap: Update
   - Post an update with image. [FS] [R35]
   - next site states: back (Back), **project@in.none** (Post update), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S)
   - enterable flows: none
5. **project@in.none** · user: Update can wait; post up first · action: taps Back · edge: back
   - Back on the project (Update has no Post up link, as in the app). [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), **project-attach@in.none** (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
6. **project-attach@in.none** · user: Working on it at a cafe · action: taps Post up for this · edge: tap: Post up for this
   - Post up for this project, now or earlier today. [FS]
   - next site states: back (Back), **posted@in.none** (Post up), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S)
   - enterable flows: none
7. **posted@in.none** · user: Live for the project · action: taps Post up · edge: tap: Post up
   - Posted, tied to the project. [FS]
   - next site states: home@in.none.building (Close), project@in.none (Star Fox 64 mod), posted+share@in.none (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

### Connected flows [M1025]
- `following`: branch out at step 1→3, step 3→2, step 5→2; merge in at step 1 (from its step 3), step 3 (from its step 2), step 5 (from its step 2)
- `first-post`: branch out at step 7→6; merge in at step 7 (from its step 6)
- `returning-post`: branch out at step 7→2; merge in at step 7 (from its step 2)

### Screens
1. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
2. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-new)
3. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
4. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-update)
5. `#project` · auth=in live=none — Back on the project (Update has no Post up link, as in the app). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
6. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-attach)
7. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)

### Branches and edge cases
- Signed out: Create / Post update open the sign-in sheet, form kept. [FS] [M1018]
- Signed out attach: #attach-signin. [FS]

### Success criteria
- Updates and postups show on the project timeline. [FS] [M1024]

### Needs Martin's decision
- Image storage for projects (Vercel Blob?). [TK§4]

---

## Flow: Follow a person or project (`following`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/following.html

### Persona
- Signed-in user who liked someone's work.

### Starting state
- auth=in · live=none · device=phone · entry URL `/u/maya`

### Goal
- Hear when they post up next. [M1024]

### Steps
1. **profile@in.none** · user: Likes someone's work · action: opens a profile · edge: entry
   - Follow → Following. [FS]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), **project@in.none** (Star Fox 64 mod Updated yesterday), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: empty-area step 3 (if Who comes here?)
2. **project@in.none** · user: Wants to see what else is being built · action: taps Maya's project · edge: tap: Star Fox 64 mod Updated yesterday
   - Profile has no tab bar (as in the app), so: project first, then the Projects tab. [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), **projects@in.none** (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: project-builder step 3 (if Project exists)
3. **projects@in.none** · user: Wants to see who they follow · action: taps Projects · edge: tap: Projects
   - Projects → Following filter. [FS] [R32]
   - next site states: project-new@in.none (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S)
   - enterable flows: project-builder step 1 (if Wants a home for their project)
4. **activity@in.live** · user: Hears that someone posted up · action: later: someone they follow posts up · edge: event: someone you follow posts up
   - Later: "Maya posted up" alert. [FS] [M1024] Event "someone you follow posts up": the alert lands in Activity and Nearby now has someone live. [M1031-draft]
   - next site states: inbox@in.live (Chats), **postup@in.live** (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), catch-up step 3 (if What else happened?)
5. **postup@in.live** · user: Wants to go · action: taps the alert · edge: tap: Maya posted up at Bean Theory
   - Opens and joins. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)

### Connected flows [M1025]
- `project-builder`: branch out at step 2→3, step 3→1; merge in at step 2 (from its step 3)
- `empty-area`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `ask-join`: branch out at step 4→4; merge in at step 4 (from its step 4)
- `catch-up`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `join`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `desktop-browse`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

### Screens
1. `#profile` · auth=in live=none — Follow → Following. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
2. `#project` · auth=in live=none — Profile has no tab bar (as in the app), so: project first, then the Projects tab. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
3. `#projects` · auth=in live=none — Projects → Following filter. [FS] [R32] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
4. `#activity` · auth=in live=live — Later: "Maya posted up" alert. [FS] [M1024] Event "someone you follow posts up": the alert lands in Activity and Nearby now has someone live. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
5. `#postup` · auth=in live=live — Opens and joins. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

### Branches and edge cases
- Signed out: Follow → sign-in sheet. [FS]

### Success criteria
- Follow alerts arrive. [M1024]

### Needs Martin's decision
- Alert for "people you follow post up" is saved but not sent yet in the build. [unsourced]

---

## Flow: Postup ends, fills or is cancelled while you look (`postup-states`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/postup-states.html

### Persona
- Anyone viewing a postup.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Clear state and a next step. [F060] [M1024]

### Steps
1. **postup-full@in.live** · user: Wanted to join; it's full · action: opens a full postup · edge: entry
   - Full. [F060] [R47]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
2. **postup-cancelled@in.live** · user: Host cancelled · action: later: postup cancelled · edge: event: postup is cancelled
   - Cancelled. [F060] [R47]
   - next site states: back (Back), postup-cancelled+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
3. **postup-full@in.live** · user: Checks the other postup · action: taps Back · edge: back
   - Back to the full postup (split: a cancelled postup doesn't later end). [M1031-draft]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
4. **postup-ended@in.live** · user: Too late; it ended · action: later: postup ended · edge: event: postup ends
   - Ended: see what's nearby, follow. [drawn] Ending is this postup's status; others may still be live nearby. [M1031-draft]
   - next site states: back (Back), postup-ended+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: catch-up step 7 (if That one's over)

### Connected flows [M1025]
- `catch-up`: branch out at step 4→7; merge in at step 4 (from its step 7)

### Screens
1. `#postup-full` · auth=in live=live — Full. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
2. `#postup-cancelled` · auth=in live=live — Cancelled. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-cancelled)
3. `#postup-full` · auth=in live=live — Back to the full postup (split: a cancelled postup doesn't later end). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
4. `#postup-ended` · auth=in live=live — Ended: see what's nearby, follow. [drawn] Ending is this postup's status; others may still be live nearby. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ended)

### Success criteria
- Never a blank page. [F060]

---

## Flow: Slow network and offline (`loading-offline`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/loading-offline.html

### Persona
- Anyone on bad wifi.

### Starting state
- auth=in · live=live · device=phone · entry URL `/nearby`

### Goal
- Keep showing something useful. [M1024]

### Steps
1. **loading@in.live** · user: Opened the feed on bad wifi · action: opens Nearby · edge: entry
   - Skeleton. [FS] [F060]
   - next site states: home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
2. **offline@in.live** · user: Connection dropped · action: later: network drops · edge: event: network drops
   - Cached feed + offline banner + Retry. [FS]
   - next site states: me@in.live (S), quiet@in.live (quiet), **quiet-feed@in.live** (Retry), post@in.live (Post up), cafe@in.live (Maya's photo), project@in.live (Star Fox 64 mod), home@in.live.live (Home), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: none
3. **quiet-feed@in.live** · user: Back online · action: taps Retry · edge: tap: Retry
   - Retry succeeds. [FS]
   - next site states: me@in.live (S), quiet@in.live (quiet), post@in.live (Post up), cafe@in.live (Maya's photo), project@in.live (Star Fox 64 mod), home@in.live.live (Home), projects@in.live (Projects), inbox@in.live (Inbox), **cafe-gfail@in.live** (Maya's photo (Google card fails))
   - enterable flows: none
4. **cafe-gfail@in.live** · user: Checking a cafe; Google is down · action: taps a cafe · edge: tap: Maya's photo (Google card fails)
   - Google card failed: rest of cafe still works. [F060]
   - next site states: back (Back), cafe-gfail+share@in.live (Share), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod), postup@in.live (Join), cafe-gfail+dirs@in.live (Open in Maps), post@in.live (Post up here), home@in.live.live (Home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#loading` · auth=in live=live — Skeleton. [FS] [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#loading)
2. `#offline` · auth=in live=live — Cached feed + offline banner + Retry. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#offline)
3. `#quiet-feed` · auth=in live=live — Retry succeeds. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#quiet-feed)
4. `#cafe-gfail` · auth=in live=live — Google card failed: rest of cafe still works. [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe-gfail)

### Branches and edge cases
- First visit while offline: nothing cached (fails in the build today). [unsourced]

### Success criteria
- No blank screens. [FS]

### Needs Martin's decision
- Full offline screen vs banner only. [R46⚠] [FS]

---

## Flow: Delete account (`delete-account`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/delete-account.html

### Persona
- Signed-in user leaving.

### Starting state
- auth=in · live=none · device=phone · entry URL `/me`

### Goal
- Remove profile, postups and projects. [M1024]

### Steps
1. **me@in.none** · user: Leaving PostUp · action: opens My profile · edge: entry
   - My profile → Settings. [FS]
   - next site states: back (Back), **settings@in.none** (Settings), live@in.none (1:42 You're live at Bean Theory Ti), cafe@in.none (Lantern Tea), project-new@in.none (Tide Clock Updated Sun), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), cafe-gfail@in.none (Lantern Tea (Google card fails))
   - enterable flows: none
2. **settings@in.none** · user: Looking for the delete option · action: taps Settings · edge: tap: Settings
   - Account section. [FS] [F065]
   - next site states: back (Back), home@out.none.building (Sign out), **settings+delacct@in.none** (Delete account), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S)
   - enterable flows: settings-notify step 1 (if Tuning alerts)
3. **settings+delacct@in.none** · user: Sure about it · action: taps Delete account · edge: tap: Delete account
   - Confirm; can't be undone. [FS] [drawn]
   - next site states: settings@in.none (close), **home@out.none.building** (Delete account)
   - enterable flows: none
4. **home@out.none.building** · user: Gone · action: confirms · edge: tap: Delete account
   - Signed out at Home. [M1024]
   - next site states: home@out.none.live (Live), cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: empty-area-newcomer step 1 (if Nobody around right now), first-post step 1 (if Came to post up right now)

### Connected flows [M1025]
- `settings-notify`: branch out at step 2→1; merge in at —
- `empty-area-newcomer`: branch out at step 4→1; merge in at —
- `first-post`: branch out at step 4→1; merge in at —

### Screens
1. `#me` · auth=in live=none — My profile → Settings. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#me)
2. `#settings` · auth=in live=none — Account section. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
3. `#settings` + sheet `delacct` · auth=in live=none — Confirm; can't be undone. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=delacct#settings)
4. `#home` · auth=out live=none mode=building — Signed out at Home. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

### Branches and edge cases
- Deleting while live: postup ends and joiners are alerted? [unsourced]

### Success criteria
- All their content gone. [FS]

### Needs Martin's decision
- What happens to a live postup and chats on delete. [unsourced]

---

## Flow: Desktop browse and post (`desktop-browse`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/desktop-browse.html

### Persona
- Signed-in user at a laptop.

### Starting state
- auth=in · live=live · device=desktop · entry URL `/`

### Goal
- Same flows with map + right panel. [FS] [M1024]

### Steps
1. **home@in.live.live** · user: At a laptop; browsing · action: arrives at / · edge: entry
   - Map with 440px panel. [FS]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Checking one postup · action: taps a live pin · edge: tap: M 2
   - Postup in the panel. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), **post@in.live** (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone)
3. **post@in.live** · user: Wants to post too · action: taps Post up · edge: tap: Post up
   - Post up as a centered dialog. [FS]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today)
4. **posted@in.live** · user: Posted; now live for others · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), project@in.live (Star Fox 64 mod), posted+share@in.live (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

### Connected flows [M1025]
- `first-post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `catch-up`: branch out at step 1→1; merge in at —
- `join`: branch out at step 2→2; merge in at —
- `returning-post`: branch out at step 4→2; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#postup)
3. `#post` · auth=in live=live — Post up as a centered dialog. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#post)
4. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#posted)

### Success criteria
- Rail and tab bar have the same items. [F064] [R12]

---

## Flow: Notification settings and sign out (`settings-notify`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/settings-notify.html

### Persona
- Signed-in user.

### Starting state
- auth=in · live=none · device=phone · entry URL `/settings`

### Goal
- Tune alerts, sign out. [M1024]

### Steps
1. **settings@in.none** · user: Tuning alerts · action: opens Settings · edge: entry
   - Toggles; Sign out. [FS] [F065]
   - next site states: back (Back), **home@out.none.building** (Sign out), settings+delacct@in.none (Delete account), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S)
   - enterable flows: delete-account step 2 (if Looking for the delete option)
2. **home@out.none.building** · user: Done for now · action: taps Sign out · edge: tap: Sign out
   - Signed out. [M1024]
   - next site states: home@out.none.live (Live), cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: empty-area-newcomer step 1 (if Nobody around right now), first-post step 1 (if Came to post up right now)

### Connected flows [M1025]
- `delete-account`: branch out at step 1→2; merge in at step 1 (from its step 2)
- `empty-area-newcomer`: branch out at step 2→1; merge in at —
- `first-post`: branch out at step 2→1; merge in at —

### Screens
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

### Success criteria
- Toggles actually change alerts. [M1024]

### Needs Martin's decision
- Email alerts at launch? [TK§4]

---

## Flow: Catch up on what happened (`catch-up`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/catch-up.html

### Persona
- Registered user coming back after a while away.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- See what happened since last time: replies, approvals, ended postups. [M1031-draft]

### Steps
1. **home@in.live.live** · user: What did I miss? · action: comes back and opens / · edge: entry
   - Home in Live mode; Inbox tab shows an unread dot. [drawn] [M1031-draft]
   - next site states: postup@in.live (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), **inbox@in.live** (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing)
2. **inbox@in.live** · user: Checks messages first · action: taps Inbox · edge: tap: Inbox
   - Chats: group chats, newest first, including an ended postup. [drawn] [M1031-draft]
   - next site states: **activity@in.live** (Activity 2), chat@in.live (M Maya's postup Maya: Grabbing ano), postup-ended@in.live (T Tess's postup Ended · Tue Tue), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: chat step 1 (if Wants to check messages)
3. **activity@in.live** · user: What else happened? · action: taps Activity · edge: tap: Activity 2
   - Activity: joins, requests, approvals, follows, messages. [drawn] [M1031-draft]
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), **postup-ask@in.live** (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), following step 4 (if Hears that someone posted up)
4. **postup-ask@in.live** · user: My request was approved · action: taps "Tess said yes to your request" · edge: tap: T Tess said yes to your request Ye
   - Tess's postup. [drawn] [M1031-draft]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), ask@in.live (Ask to join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: ask-join step 1 (if Interested, but the host screens people)
5. **activity@in.live** · user: Back to the list · action: taps Back · edge: back
   - Activity again. [drawn] [M1031-draft]
   - next site states: **inbox@in.live** (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), following step 4 (if Hears that someone posted up)
6. **inbox@in.live** · user: Any replies? · action: taps Chats · edge: tap: Chats
   - Chats list. [drawn] [M1031-draft]
   - next site states: activity@in.live (Activity 2), chat@in.live (M Maya's postup Maya: Grabbing ano), **postup-ended@in.live** (T Tess's postup Ended · Tue Tue), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: chat step 1 (if Wants to check messages)
7. **postup-ended@in.live** · user: That one's over · action: taps Tess's ended postup · edge: tap: T Tess's postup Ended · Tue Tue
   - Ended postup: see what's nearby, follow. [drawn] [M1031-draft]
   - next site states: back (Back), postup-ended+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), **inbox@in.live** (Inbox), me@in.live (S)
   - enterable flows: none
8. **inbox@in.live** · user: Back to chats · action: taps Back · edge: back
   - Chats list. [drawn] [M1031-draft]
   - next site states: activity@in.live (Activity 2), **chat@in.live** (M Maya's postup Maya: Grabbing ano), postup-ended@in.live (T Tess's postup Ended · Tue Tue), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: chat step 1 (if Wants to check messages)
9. **chat@in.live** · user: Reads the replies · action: opens Maya's postup chat · edge: tap: M Maya's postup Maya: Grabbing ano
   - Group chat with the latest replies. [drawn] [M1031-draft]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `ask-join`: branch out at step 3→4, step 4→1, step 5→4; merge in at step 3 (from its step 4), step 5 (from its step 4)
- `following`: branch out at step 3→4, step 5→4; merge in at step 3 (from its step 4), step 5 (from its step 4)
- `chat`: branch out at step 2→1, step 6→1, step 9→2; merge in at —
- `host-approve`: branch out at step 3→1, step 5→1; merge in at —
- `join`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 1→1; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Home in Live mode; Inbox tab shows an unread dot. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#inbox` · auth=in live=live — Chats: group chats, newest first, including an ended postup. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox)
3. `#activity` · auth=in live=live — Activity: joins, requests, approvals, follows, messages. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
4. `#postup-ask` · auth=in live=live — Tess's postup. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
5. `#activity` · auth=in live=live — Activity again. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
6. `#inbox` · auth=in live=live — Chats list. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox)
7. `#postup-ended` · auth=in live=live — Ended postup: see what's nearby, follow. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ended)
8. `#inbox` · auth=in live=live — Chats list. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox)
9. `#chat` · auth=in live=live — Group chat with the latest replies. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Nothing happened while away: Activity and Chats need a positive empty state, never "quiet". [F035] [M1031-draft]

### Success criteria
- From Home, the user reaches replies, an approval and an ended postup through the Inbox. [M1031-draft]

### Needs Martin's decision
- No "since you were away" summary exists; catching up means opening Inbox, then each item. [M1031-draft]
- No unread or new markers per item beyond the Activity count badge; there is no way to tell what is new since last visit. [M1031-draft]
- An approval ("Tess said yes") opens Tess's postup as Ask to join, not a joined/approved state. [M1031-draft]
- Ended postups appear only in Chats ("Tess's postup · Ended"), not as an Activity alert. [M1031-draft]
- Replies show as one Activity row per message linking to the group chat; there is no reply thread view. [M1031-draft]
