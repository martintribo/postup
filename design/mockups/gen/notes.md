<!--
PostUp mockup notes: the source of truth that sits beside each mockup screen.
Edit here, then run: python3 gen/build.py
Format: "## <screen-id> | <Title>", optional "host: <screen>" (overlays), then "### <Section>" with "- " bullets.
Every bullet ends with source tags:
  [F046]   fact id in sources/facts.jsonl (Martin's words or an agreed answer)
  [FS]     sources/final-screens.md      [TK§n] sources/mockup-takeaways.md section n
  [R12]    sources/requirements.md item  [R12⚠] ledger marks that item UNSOURCED
  [drawn]  shown in the mockup itself     [unsourced] nothing backs it; confirm with Martin
  [M1018]  Martin, Oct 18 2026 (relayed): scenario toggle on every page, '/' clearly marked
  [M1018b] Martin, Oct 18 2026 (relayed): Home (/) has two modes, Live and Building, on one URL
  [M1025]  Martin, Oct 25 2026 (relayed): flow map, state machine from a first-time visitor (gen/flowmap.py)
  [M1024]  Martin, Oct 24 2026 (relayed): track critical flows (gen/flowdata.py)
  [M1018c] Martin, Oct 18 2026 (relayed): heading "What people are building"; closest-first, never claim nearby unless they are
Each screen has a "### Scenarios" section. Bullets starting "Signed out:", "Signed in:", "Live nearby:", "None live:" are highlighted for the current scenario.
New decisions go here, on the screen they affect. Not just in chat.
-->

## _global | Global rules
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

## index | Mockup index
### Purpose
- Mockup switcher (screens, style, device). Not a product screen. [FS]
### Scenarios
- Same in all scenarios. The 2×2 scenario matrix lives here. [M1018]
### Decisions
- No "Mockups" link in the real nav. [R14⚠]

## home | Home page (/)
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
- Replaces "Post up shows only when someone's live": Building mode has a big Post up. [M1018b] [FS]
- Overlay-on-map version drawn for comparison: `#home-overlay-alt`, not chosen. [M1018b]
### Unsourced
- Area label ("Near Westside, Los Angeles") and the change-area picker. [R7⚠]
- Launch area Playa Vista / Westside LA as fallback centre. [R8⚠]

## home-overlay-alt | Home overlay · alternative, not chosen
### Purpose
- Comparison only: a projects card floating over a dimmed map. **Alternative, not chosen**; Home uses the Live · Building switch instead. [M1018b]
### Scenarios
- Same in all scenarios. [M1018]
### Behavior
- Card: 3 projects, See all projects, Post up, Show map (hides the card). [M1018b] [drawn]
- Heading "What people are building". [M1018c]

## quiet | Recent map · old no-live home (not /)
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

## quiet-feed | Nearby (/nearby) · photos (A)
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

## quiet-feed-b | Nearby (/nearby) · no photos (B)
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

## cafe | Cafe
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

## post | Post up
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

## post-signin | Sign-in sheet · post
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

## posted | You're posted up
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

## postup | Postup · anyone can join
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

## join-signin | Sign-in sheet · join
### Purpose
- Sign-in sheet over the postup when you tap Join (also used by Follow on `#invite-project`). [FS] [drawn]
### Scenarios
- Signed out: the sheet. [FS]
- Signed in: no sheet; shows `#postup`. [FS] [M1018]
### Behavior
- Success → `#joined`. [FS]

## joined | You're joining
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

## project | Project
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

## projects | Projects
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

## project-new | New project
### Purpose
- Create a project: cover, name, kind, one line. [FS] [drawn]
### Scenarios
- Signed out: Create → sign-in sheet. [FS]
- Signed in: Create → `#project`. [FS]
### Behavior
- Needs sign-in (sheet at Create). Desktop: centered dialog. [FS]

## project-update | Project update
### Purpose
- Owner posts an update: title, notes, image. [FS] [R35]
### Scenarios
- Signed out: Post update → sign-in sheet. [unsourced]
- Signed in: Post update → `#project`. [R35]
### Behavior
- Desktop: centered dialog. [FS]

## project-attach | Post up for a project
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

## attach-signin | Sign-in sheet · attach
### Purpose
- Sign-in sheet when posting up for a project. Success → `#posted`. [FS] [drawn]
### Scenarios
- Signed in: no sheet; shows `#project-attach`. [FS] [M1018]


## where | Where are you?
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

## where-search | Cafe search
### Purpose
- Search results in the picker. [FS]
### Scenarios
- Same in all scenarios. [M1018]
### Behavior
- Google Places Autocomplete in our UI is fine; show "powered by Google" attribution. [F097] [FS]

## post-edit | Edit postup
### Purpose
- Change your live postup; Save → `#live`. [FS] [drawn]
### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]
### Decisions
- Managing your own postup is important. [F057]

## live | You're live
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

## postup-ask | Postup · ask to join
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

## ask-signin | Sign-in sheet · ask
### Purpose
- Sign-in sheet before asking to join. Success → `#ask`. [FS] [drawn]
### Scenarios
- Signed in: no sheet; shows `#postup-ask`. [FS] [M1018]


## ask | Ask to join
### Purpose
- Write a short reason for joining. [F061] [F095]
### Scenarios
- Same in all scenarios; reached after signing in. [M1018]
### Behavior
- Poster gets an alert and approves or declines. [F095] [F055]

## requested | Request sent
### Purpose
- Confirmation after asking. [FS]
### Scenarios
- Same in all scenarios. [M1018]
### Behavior
- See who else is nearby; View postup; Cancel request. [drawn]

## postup-ended | Postup ended
### Purpose
- State: the postup is over. [F060] [R47]
### Scenarios
- Same in all scenarios. [M1018]
### Behavior
- See what's nearby; Follow the poster for next time. [drawn]

## postup-full | Postup full
### Purpose
- State: the poster isn't taking more people. [F060] [R47]
### Scenarios
- Same in all scenarios. [M1018]


## postup-cancelled | Postup cancelled
### Purpose
- State: the poster cancelled. [F060] [R47]
### Scenarios
- Same in all scenarios. [M1018]


## invite | Share link · live postup
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

## invite-ended | Share link · ended
### Purpose
- Shared link to a postup that ended → what's nearby. [FS] [R39]
### Scenarios
- Same in all scenarios. [M1018]


## invite-project | Share link · project
### Purpose
- Logged-out landing for a shared project link. [F067] [R39]
### Scenarios
- Signed out: Follow 🔒 → sign-in sheet. [FS]
- Signed in: Follow toggles to Following. [FS]
### Copy
- "Maya is building Star Fox 64 mod" — see updates, follow, or join her next postup. [FS]
### Behavior
- Follow needs sign-in. [FS]

## empty-area | Empty area
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

## cafe-gfail | Cafe · Google card failed
### Purpose
- Place card failed to load. [F060]
### Scenarios
- None live: no Here now section, same as `#cafe`. [M1018]
### Behavior
- "Details unavailable", Open in Maps, Retry. [FS] [R37]

## loading | Loading
### Purpose
- Skeleton while the feed loads. [FS] [F060] [TK§1]
### Scenarios
- Same in all scenarios. [M1018]


## offline | Offline
### Purpose
- Last loaded Nearby feed with an offline banner and Retry. Not a blank screen. [FS]
### Scenarios
- Same in all scenarios. [M1018]
### Open
- The ledger asks for a full offline screen, not just a banner; the final mockup is the cached feed + banner. [R46⚠] [FS]

## chat | Group chat
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

## inbox | Inbox · Chats
### Purpose
- Inbox tab: your postup chats. [FS] [F096]
### Scenarios
- Signed out: sign-in sheet over it; no unread dot. [unsourced]
- Signed in: as drawn. [drawn]
### Behavior
- Chats | Activity tabs. Ended chats dimmed. Unread dot on the tab. Root tab: no Back. [FS] [R13]

## activity | Inbox · Activity
### Purpose
- Requests, joins, "said yes", messages, follows. [FS]
### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]
### Behavior
- Each row opens the related screen (request → `#live`, message → `#chat`, follow → `#profile`). [drawn]
### Open
- Email alerts. [TK§4]

## profile | Profile
### Purpose
- Someone's public profile. [FS] [F065]
### Scenarios
- None live: no live card. [M1018]
- Signed out: Follow → sign-in sheet. [FS]
- Signed in: Follow toggles. [FS]
### Behavior
- Live card, avatar, bio, "N postups · since Sep", Follow, regular cafes, projects, past postups. [FS] [R76]
- ⋯ → report / block. [FS] [F059]

## me | My profile
### Purpose
- Your own profile. [FS] [F065]
### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]
### Behavior
- Live card → `#live`, Edit profile, gear → `#settings`. [FS]
- Desktop rail avatar opens this. [FS]

## settings | Settings
### Purpose
- Notification toggles; Account: Blocked people, Sign out, Delete account. [FS] [F065]
### Scenarios
- Signed out: sign-in sheet over it. [unsourced]
- Signed in: as drawn. [drawn]
### Unsourced
- Account deletion in the app (store guideline 5.1.1). [R43⚠]
### Open
- Email alerts. [TK§4]

## report | Report
### Purpose
- Report a person, postup or message: reason + optional details. [F059] [drawn]
### Scenarios
- Same in all scenarios. [M1018]
### Unsourced
- Admin reports page for Martin only. [R30⚠]
### Open
- No user ban system yet. [TK§4]

## reported | Reported
### Purpose
- Thanks; offer to block too. [FS]
### Scenarios
- Same in all scenarios. [M1018]
### Copy
- "They won't know you reported them." No safety tips. [FS] [F059]

## ov-share | Sheet · Share
host: posted
### Purpose
- Share sheet: link with Copy, then Messages / WhatsApp / Email / More. [drawn]
### Scenarios
- Same in all scenarios. [M1018]
### Unsourced
- Share opens this sheet, never the poster's success screen. [R41⚠]

## ov-dirs | Sheet · Directions
host: joined
### Purpose
- Open in Apple Maps / Google Maps. [FS]
### Scenarios
- Same in all scenarios. [M1018]
### Unsourced
- Ledger item for directions. [R25⚠]

## ov-leave | Sheet · Leave
host: joined
### Purpose
- Confirm leaving; the poster gets an alert. [FS] [drawn]
### Scenarios
- Same in all scenarios. [M1018]


## ov-endlive | Sheet · End postup
host: live
### Purpose
- Confirm ending; joiners and anyone waiting get an alert. [FS] [drawn]
### Scenarios
- Same in all scenarios. [M1018]


## ov-more | Sheet · More
host: postup
### Purpose
- View profile, Share, Report, Block. [FS] [F059]
### Scenarios
- Same in all scenarios. [M1018]


## ov-msg | Sheet · Message options
host: chat
### Purpose
- Copy, Report message, Block sender. [F096] [FS]
### Scenarios
- Same in all scenarios. [M1018]


## ov-block | Sheet · Block
host: postup
### Purpose
- Block: you won't see each other's postups or messages; they aren't told. [FS] [F059]
### Scenarios
- Same in all scenarios. [M1018]


## ov-delacct | Sheet · Delete account
host: settings
### Purpose
- Confirm deleting profile, postups and projects; can't be undone. [FS] [drawn]
### Scenarios
- Same in all scenarios. [M1018]


## ov-signin | Sheet · Sign in (follow, create, update)
host: profile
### Purpose
- Sign-in sheet for Follow, Create project and Post update when signed out. Signing in switches the toggle to Signed in and continues. [FS] [M1018]
### Scenarios
- Signed out only; signed in never shows it. [FS]
