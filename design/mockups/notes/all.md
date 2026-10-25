# PostUp mockups — implementation notes (all screens)
Source of truth for building PostUp: the v1034 mockups plus these notes. Where a note says "Overrides", the note beats the drawing.
Mockup: /mockups/?style=<fresh|cozy|night|bold>&device=<phone|desktop>&auth=<out|in>&live=<live|none>#<screen>  (overlay sheets: &ov=<sheet>)
The home page (/) is `#home`, called Home: two modes on one URL, Live and Building (`?mode=live|building`); default by whether anyone's live. `#home-overlay-alt` is an alternative, not chosen. `#quiet` is the old no-live home drawing (not /); `#quiet-feed` / `#quiet-feed-b` are Nearby (/nearby).
Screens: 45 + 9 overlay sheets.

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

## Sign-in sheet · post (`post-signin`)
URL: /mockups/?style=fresh&device=phone#post-signin  ·  desktop: /mockups/?style=fresh&device=desktop#post-signin

### Purpose
- The global sign-in sheet, shown at the moment of action. Variants: join, ask, attach. [FS]

### Scenarios
- Signed out: the sheet, as drawn. [FS]
- Signed in: no sheet; shows `#post`. [FS] [M1018]

### Behavior
- Continue with Apple / Google, "Not now". The build also adds a dev sign-in and "Use a PostUp username" (→ /login). [FS]
- Only at post, join, follow, new project. [FS]
- Success → `#posted`. [drawn]

### Unsourced
- Every "Log in" link opens this sheet, not the /login page. [R10⚠]

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

## Sign-in sheet · join (`join-signin`)
URL: /mockups/?style=fresh&device=phone#join-signin  ·  desktop: /mockups/?style=fresh&device=desktop#join-signin

### Purpose
- Sign-in sheet over the postup when you tap Join (also used by Follow on `#invite-project`). [FS] [drawn]

### Scenarios
- Signed out: the sheet. [FS]
- Signed in: no sheet; shows `#postup`. [FS] [M1018]

### Behavior
- Success → `#joined`. [FS]

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

## Sign-in sheet · attach (`attach-signin`)
URL: /mockups/?style=fresh&device=phone#attach-signin  ·  desktop: /mockups/?style=fresh&device=desktop#attach-signin

### Purpose
- Sign-in sheet when posting up for a project. Success → `#posted`. [FS] [drawn]

### Scenarios
- Signed in: no sheet; shows `#project-attach`. [FS] [M1018]

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

## Sign-in sheet · ask (`ask-signin`)
URL: /mockups/?style=fresh&device=phone#ask-signin  ·  desktop: /mockups/?style=fresh&device=desktop#ask-signin

### Purpose
- Sign-in sheet before asking to join. Success → `#ask`. [FS] [drawn]

### Scenarios
- Signed in: no sheet; shows `#postup-ask`. [FS] [M1018]

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

## Empty area (`empty-area`)
URL: /mockups/?style=fresh&device=phone#empty-area  ·  desktop: /mockups/?style=fresh&device=desktop#empty-area

### Purpose
- An area with no postups yet: "Be the first here". [FS]

### Scenarios
- Same in all scenarios (the area has no postups by definition). [M1018]

### Behavior
- No fake activity. [TK§2]

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

## Sheet · Share (`ov-share`)
URL: /mockups/?style=fresh&device=phone&ov=share#posted  ·  desktop: /mockups/?style=fresh&device=desktop&ov=share#posted · shown over #posted

### Purpose
- Share sheet: link with Copy, then Messages / WhatsApp / Email / More. [drawn]

### Scenarios
- Same in all scenarios. [M1018]

### Unsourced
- Share opens this sheet, never the poster's success screen. [R41⚠]

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

## Sheet · Leave (`ov-leave`)
URL: /mockups/?style=fresh&device=phone&ov=leave#joined  ·  desktop: /mockups/?style=fresh&device=desktop&ov=leave#joined · shown over #joined

### Purpose
- Confirm leaving; the poster gets an alert. [FS] [drawn]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · End postup (`ov-endlive`)
URL: /mockups/?style=fresh&device=phone&ov=endlive#live  ·  desktop: /mockups/?style=fresh&device=desktop&ov=endlive#live · shown over #live

### Purpose
- Confirm ending; joiners and anyone waiting get an alert. [FS] [drawn]

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

## Sheet · Block (`ov-block`)
URL: /mockups/?style=fresh&device=phone&ov=block#postup  ·  desktop: /mockups/?style=fresh&device=desktop&ov=block#postup · shown over #postup

### Purpose
- Block: you won't see each other's postups or messages; they aren't told. [FS] [F059]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · Delete account (`ov-delacct`)
URL: /mockups/?style=fresh&device=phone&ov=delacct#settings  ·  desktop: /mockups/?style=fresh&device=desktop&ov=delacct#settings · shown over #settings

### Purpose
- Confirm deleting profile, postups and projects; can't be undone. [FS] [drawn]

### Scenarios
- Same in all scenarios. [M1018]

---

## Sheet · Sign in (follow, create, update) (`ov-signin`)
URL: /mockups/?style=fresh&device=phone&ov=signin#profile  ·  desktop: /mockups/?style=fresh&device=desktop&ov=signin#profile · shown over #profile

### Purpose
- Sign-in sheet for Follow, Create project and Post update when signed out. Signing in switches the toggle to Signed in and continues. [FS] [M1018]

### Scenarios
- Signed out only; signed in never shows it. [FS]

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
- **drawn** — the mockup drawing itself
- **unsourced** — no source; confirm with Martin
- **TK§1** — mockup-takeaways.md (mockup session takeaways) §1
- **TK§2** — mockup-takeaways.md (mockup session takeaways) §2
- **TK§4** — mockup-takeaways.md (mockup session takeaways) §4

---

# Critical flows
Critical flows (Martin, Oct 24 2026 [M1024]): a type of user arrives in a certain situation and goes through a scenario step by step. Each step names the screen and the scenario params (auth, live, Home mode, sheet). Flows marked Draft were inferred from the screen notes; confirm with Martin.

## Flow: Cautious joiner checks a few postups, then joins (`cautious-joiner`)
Priority: **MVP must** · Status: Martin's example (Oct 24) [M1024]
Player: /mockups/flows/cautious-joiner.html

### Persona
- Registered user, signed in, wants company but checks people out first.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Join a live postup after comparing a few. [M1024]

### Steps
1. `#home` · auth=in live=live mode=live — Opens / in Live mode: map + Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#project` · auth=in live=live — Opens Maya's project to see what she's working on, then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)
4. `#profile` · auth=in live=live — Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
5. `#cafe` · auth=in live=live — Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe)
6. `#postup-ask` · auth=in live=live — Compares a second postup (Tess approves who joins), then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
7. `#postup` · auth=in live=live — Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
8. `#joined` · auth=in live=live — You're joining Maya; Maya is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
9. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)

### Branches and edge cases
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

### Success criteria
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

---

## Flow: Quick joiner (`quick-joiner`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/quick-joiner.html

### Persona
- Registered user who already knows someone nearby is live.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Join in two taps and get directions. [M1024]

### Steps
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps a row, then Join. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#joined` · auth=in live=live — Confirmation. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)
5. `#chat` · auth=in live=live — Says "on my way" in the postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]

### Success criteria
- Home → joined in 2 taps. [M1024]

---

## Flow: Curious visitor joins someone live (`first-visit-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit-live.html

### Persona
- New visitor, signed out, curious; lands on / with live postups nearby.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- Understand the site and join someone; sign in only at Join. [M1024]

### Steps
1. `#home` · auth=out live=live mode=live — Home opens in Live mode with a one-line welcome. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Opens a postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#join-signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#join-signin)
4. `#joined` · auth=in live=live — Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)

### Branches and edge cases
- Not now on the sheet: stays on the postup, still signed out. [drawn] [M1024]
- Switches to Building to look at projects first. [M1018b] [M1024]

### Success criteria
- No sign-in before an action. [FS]
- After sign-in the original action completes. [M1018] [M1024]

---

## Flow: Curious browser: live now, then past content (`curious-browser`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/curious-browser.html

### Persona
- First-time visitor, signed out, who has heard of PostUp and wants to see what is on it: who is live and what people have made.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- See live and past content, then follow someone, signing in only at Follow. [M1025]

### Steps
1. `#home` · auth=out live=live mode=live — Live now list: who is working where. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Peeks at a live postup, then Back. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#home` · auth=out live=live mode=building — Switches to Building for past content. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
4. `#projects` · auth=out live=live — See all projects, closest first. [M1018c] [FS] (/mockups/?style=fresh&device=phone&auth=out&live=live#projects)
5. `#project` · auth=out live=live — Opens a project: updates and past postups. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)
6. `#profile` · auth=out live=live — Opens the maker's profile: past postups, regular cafes. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#profile)
7. `#profile` + sheet `signin` · auth=out live=live — Taps Follow: soft sign-in sheet; Not now keeps browsing. [FS] [M1018] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#profile)
8. `#profile` · auth=in live=live — Signed in and following. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)

### Branches and edge cases
- Nobody live: Home opens in Building, so the flow starts at the projects (merged from the old first-visit-none flow). [M1018b] [M1025]
- Taps Post up instead: see Came to post up. [M1025]
- Not now on the sheet: stays signed out, nothing lost. [drawn] [M1025]
- Never empty or "quiet" copy when nothing is live. [F035] [R4]

### Success criteria
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]

### Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]

---

## Flow: Stumbled on it: what is this? (`stumbled`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/stumbled.html

### Persona
- First-time visitor with no idea what PostUp is; arrived from search, a social post or a word-of-mouth link.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- Understand PostUp within the first screen and reach something real before any sign-in. [M1025]

### Steps
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. No explainer line is drawn in Live mode, only the brand. [drawn] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Taps the first live person to see what a postup is. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#cafe` · auth=out live=live — Taps the cafe: who is here now, Post up here. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#cafe)
4. `#home` · auth=out live=live mode=building — Back on Home, flips to Building: the welcome line "Post up at a cafe. See who's working nearby." and "What people are building". [drawn] [M1018c] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
5. `#project` · auth=out live=live — Opens a project and gets the idea; Follow and Post up (🔒) are the next steps. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)

### Branches and edge cases
- Nobody live: Home opens in Building, where the welcome line shows first. [M1018b] [drawn] [M1025]
- Dismisses the welcome (×): it should stay dismissed. [drawn] [unsourced]
- Leaves after the first screen: the value has to be clear without scrolling. [M1025]

### Success criteria
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

### Needs Martin's decision
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

---

## Flow: Share link to a live postup (`invite-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-live.html

### Persona
- Friend of a poster, signed out, opened postup.now/p/… from a message.

### Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

### Goal
- Join the friend who shared the link. [M1024]

### Steps
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite)
2. `#join-signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#join-signin)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#chat` · auth=in live=live — Postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Link is to an ask-to-join postup → Ask to join flow. [FS] [M1024]
- Already signed in: Join goes straight to joined. [TK§1] [M1024]

### Success criteria
- The link works without an account until Join. [R39] [M1024]

---

## Flow: Share link to an ended postup (`invite-ended`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-ended.html

### Persona
- Signed-out visitor opening an old link.

### Starting state
- auth=out · live=none · device=phone · entry URL `/p/7xk2 (ended)`

### Goal
- Not hit a dead end: see what's around and follow the poster. [M1024]

### Steps
1. `#invite-ended` · auth=out live=none — "This postup ended" + what's around. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=none#invite-ended)
2. `#profile` + sheet `signin` · auth=out live=none — Follow the poster → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#profile)
3. `#home` · auth=in live=none mode=building — Continues to Home. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

### Branches and edge cases
- Cancelled instead of ended: #postup-cancelled copy. [F060] [M1024]

### Success criteria
- No 404, a next step is always offered. [F060] [M1024]

---

## Flow: Share link to a project (`invite-project`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-project.html

### Persona
- Signed-out visitor opening postup.now/project/… .

### Starting state
- auth=out · live=live · device=phone · entry URL `/project/…`

### Goal
- Follow the project to hear about the next postup. [M1024]

### Steps
1. `#invite-project` · auth=out live=live — "Maya is building Star Fox 64 mod". [FS] [F067] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite-project)
2. `#invite-project` + sheet `signin` · auth=out live=live — Follow 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite-project)
3. `#project` · auth=in live=live — Following; live postups for the project shown. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)

### Branches and edge cases
- Project owner is live now: join from the project. [FS] [M1024]

### Success criteria
- Follow survives sign-in. [M1018] [M1024]

---

## Flow: Ask to join, then get approved (joiner side) (`ask-join`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/ask-join.html

### Persona
- Signed-in user; poster approves who joins.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Send a reason, get a yes, meet up. [M1024]

### Steps
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
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/host-approve.html

### Persona
- Signed-in poster with an ask-to-join postup.

### Starting state
- auth=in · live=live · device=phone · entry URL `/live`

### Goal
- Approve or decline with the joiner's reason in view. [M1024]

### Steps
1. `#activity` · auth=in live=live — Alert: "Ari asked to join". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
2. `#live` · auth=in live=live — Requests with reason: Approve / Decline. [FS] [F061] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
3. `#profile` · auth=in live=live — Optionally checks the asker's profile first. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
4. `#chat` · auth=in live=live — Approved people are in the chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Decline: joiner is told politely. [F095] [unsourced]
- Block from the request via More. [F059] [M1024]

### Success criteria
- Approve in one tap from #live. [FS] [M1024]

---

## Flow: Came to post up: first post with sign-in (`first-post`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post.html

### Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

### Starting state
- auth=out · live=none · device=phone · entry URL `/`

### Goal
- Go live in about ten seconds. [M1024]

### Steps
1. `#home` · auth=out live=none mode=building — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none#where-search)
5. `#post-signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none#post-signin)
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
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/returning-post.html

### Persona
- Signed-in regular.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Post up with defaults, then see you're live. [M1024]

### Steps
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
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/hosting.html

### Persona
- Signed-in poster who is live.

### Starting state
- auth=in · live=live · device=phone · entry URL `/live`

### Goal
- Manage time and end cleanly. [M1024]

### Steps
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
2. `#post-edit` · auth=in live=live — Edit cafe/what/until; Save → #live. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#post-edit)
3. `#live` · auth=in live=live — Back on live. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup → confirm; joiners and waiters alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive#live)
5. `#home` · auth=in live=none mode=building — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

### Branches and edge cases
- Time runs out: ends automatically, chat stays 24h. [R31] [FS]
- Closes "who can join" (full): new visitors see #postup-full. [F060] [R47]

### Success criteria
- Joiners always know the postup ended. [FS] [M1024]

---

## Flow: Project builder: create, update, post up for it (`project-builder`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/project-builder.html

### Persona
- Signed-in maker.

### Starting state
- auth=in · live=none · device=phone · entry URL `/projects`

### Goal
- Have a project page that collects updates and postups. [M1024]

### Steps
1. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
2. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-new)
3. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
4. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-update)
5. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-attach)
6. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)

### Branches and edge cases
- Signed out: Create / Post update open the sign-in sheet, form kept. [FS] [M1018]
- Signed out attach: #attach-signin. [FS]

### Success criteria
- Updates and postups show on the project timeline. [FS] [M1024]

### Needs Martin's decision
- Image storage for projects (Vercel Blob?). [TK§4]

---

## Flow: Follow a person or project (`following`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/following.html

### Persona
- Signed-in user who liked someone's work.

### Starting state
- auth=in · live=none · device=phone · entry URL `/u/maya`

### Goal
- Hear when they post up next. [M1024]

### Steps
1. `#profile` · auth=in live=none — Follow → Following. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
2. `#projects` · auth=in live=none — Projects → Following filter. [FS] [R32] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
3. `#activity` · auth=in live=live — Later: "Maya posted up" alert. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
4. `#postup` · auth=in live=live — Opens and joins. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

### Branches and edge cases
- Signed out: Follow → sign-in sheet. [FS]

### Success criteria
- Follow alerts arrive. [M1024]

### Needs Martin's decision
- Alert for "people you follow post up" is saved but not sent yet in the build. [unsourced]

---

## Flow: Postup chat (`chat`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/chat.html

### Persona
- Signed-in poster or joiner.

### Starting state
- auth=in · live=live · device=phone · entry URL `/inbox`

### Goal
- Coordinate in the group chat. [M1024]

### Steps
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
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/safety.html

### Persona
- Signed-in user uncomfortable with someone.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Report and block quickly. [F059] [M1024]

### Steps
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#reported)
4. `#postup` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block#postup)
5. `#settings` · auth=in live=live — Blocked people list to undo. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=live#settings)

### Branches and edge cases
- From a chat message: Message options → Report message. [F096]

### Success criteria
- No safety-tip screens. [F059] [FS]

### Needs Martin's decision
- No ban system yet: who reviews reports? [TK§4]

---

## Flow: Leave a postup you joined (`leave`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/leave.html

### Persona
- Signed-in joiner whose plans changed.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Back out politely. [M1024]

### Steps
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave#joined)
3. `#home` · auth=in live=live mode=live — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)

### Branches and edge cases
- The poster ended or cancelled first: #postup-cancelled. [F060]

### Success criteria
- Poster knows. [FS]

---

## Flow: Postup ends, fills or is cancelled while you look (`postup-states`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/postup-states.html

### Persona
- Anyone viewing a postup.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Clear state and a next step. [F060] [M1024]

### Steps
1. `#postup-full` · auth=in live=live — Full. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
2. `#postup-cancelled` · auth=in live=live — Cancelled. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-cancelled)
3. `#postup-ended` · auth=in live=none — Ended: see what's nearby, follow. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#postup-ended)

### Success criteria
- Never a blank page. [F060]

---

## Flow: Empty area: be the first (`empty-area`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area.html

### Persona
- Signed-in user in a city with no postups yet.

### Starting state
- auth=in · live=none · device=phone · entry URL `/`

### Goal
- Seed the area. [M1024]

### Steps
1. `#home` · auth=in live=none mode=building — Closest projects even if far. [M1018c] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)
2. `#empty-area` · auth=in live=none — "Be the first here". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)
3. `#post` · auth=in live=none — Post up. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#post)

### Success criteria
- Positive copy, never "quiet". [F035] [R4]

### Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

---

## Flow: Slow network and offline (`loading-offline`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/loading-offline.html

### Persona
- Anyone on bad wifi.

### Starting state
- auth=in · live=live · device=phone · entry URL `/nearby`

### Goal
- Keep showing something useful. [M1024]

### Steps
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
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/delete-account.html

### Persona
- Signed-in user leaving.

### Starting state
- auth=in · live=none · device=phone · entry URL `/me`

### Goal
- Remove profile, postups and projects. [M1024]

### Steps
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
Priority: **nice** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/desktop-browse.html

### Persona
- Signed-in user at a laptop.

### Starting state
- auth=in · live=live · device=desktop · entry URL `/`

### Goal
- Same flows with map + right panel. [FS] [M1024]

### Steps
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#postup)
3. `#post` · auth=in live=live — Post up as a centered dialog. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#post)
4. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#posted)

### Success criteria
- Rail and tab bar have the same items. [F064] [R12]

---

## Flow: Notification settings and sign out (`settings-notify`)
Priority: **nice** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/settings-notify.html

### Persona
- Signed-in user.

### Starting state
- auth=in · live=none · device=phone · entry URL `/settings`

### Goal
- Tune alerts, sign out. [M1024]

### Steps
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

### Success criteria
- Toggles actually change alerts. [M1024]

### Needs Martin's decision
- Email alerts at launch? [TK§4]
