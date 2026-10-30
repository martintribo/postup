# Report
Screen id: `report`
URL (phone): /mockups/?style=fresh&device=phone#report
URL (desktop): /mockups/?style=fresh&device=desktop#report
Styles: fresh (default), cozy, night, bold via ?style=
Scenario: ?auth=out|in&live=live|none (default out + live); see the Scenarios section

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing.

## Purpose
- Report a person, postup or message: reason + optional details. [F059] [drawn]

## Scenarios
- Same in all scenarios. [M1018]

## Unsourced
- Admin reports page for Martin only. [R30⚠]

## Open
- No user ban system yet. [TK§4]

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

### Chrome: Rail (desktop) · Phase versions
- Phase 1 version hides: projects (phase-2 screens or Building mode). [M1035]

### Chrome: Rail (desktop) · Phase 0
- Phase 0 version hides: inbox (no chat, so no Inbox). [M1037]

### Chrome: Tab bar (phone) · Purpose
- Phone tab bar: Map, Post up, Projects. Pages that show it declare a "nav" tab slot; its links are available on those pages when no sheet is open. [drawn] [M1031-draft]

### Chrome: Tab bar (phone) · Phase versions
- Phase 1 version hides: projects (phase-2 screens or Building mode). [M1035]

### Chrome: Tab bar (phone) · Phase 0
- Phase 0 version hides: inbox (no chat, so no Inbox); the tab bar is Map, Nearby, Post up. [M1037]

## Sources cited
- **F013** — General UX rule: little on screen at a time; drill-down with back button. (Martin, S05 t119u): “In general I want to stick to there is always not much on the screen at at time”
- **F026** — Mockups link to each other. (Martin, S08-mockups-1 t194u): “can you make the mockups link to each other?”
- **F032** — Google photos never in feed. (PostUp PM (assistant), S08-mockups-1): “**Google photos stay out of the feed.** Their terms only allow them inside the Google card on a cafe's page.”
- **F035** — Never say it's quiet. (Martin, S08-mockups-1 t200u): “I don't think we even need to say it's quiet right now btw”
- **F036** — Keep current style; try other fundamental styles. (Martin, S08-mockups-1 t201u): “this looks great! are there other fundamental styles we can try (keep this even if we make another style)”
- **F043** — First-visit experience required; fall back to projects in general when nothing this week. (Martin, S11 t244u): “the final site doesn't seem like it has the first experience liek we talked about? If there aren't things from this week, we should just show projects in general”
- **F044** — No map when no postups; focus on projects. (Martin, S11 t247u): “We weren't supposed to show the map when there's no post ups, we were going to focus on projects.”
- **F046** — Tab always called Home. (Martin, S11 t252u): “I think we just always call the map tab home btw”
- **F051** — Nearby feed on desktop should not show the map. (Martin, S08-mockups-2 t207u): “huh, but nearby feed with photos on desktop still shows the map?”
- **F052** — Projects must not show the map. (Martin, S08-mockups-2 t208u): “why does clicking on projects shwo the map?”
- **F053** — Map only on map, cafe and postup screens. (PostUp PM (assistant), S08-mockups-2): “The map now only shows on the map, cafe and postup screens.”
- **F056** — Where-I'm-sitting note/picture: to-do. (Martin, S08-mockups-2 t210u): “2. You should be able to put a description of where you are or a picture.. let's leave this on the todo list for now”
- **F059** — Report and block yes; no safety tips. (Martin, S08-mockups-2 t210u): “5. Reporting and blocking woudl be good to have. Idk about safety tips, this site is for adults and they should be smart enough to understand the risks.”
- **F064** — Phone and desktop menus match. (PostUp PM (assistant), S08-mockups-2): “**7. What I meant:** the phone and desktop layouts disagree. Desktop has a Nearby tab and phone doesn't, so I'll make the menus match.”
- **F066** — Agreed to search picker, welcome/share pages (plus projects), menus, profile. (Martin, S08-mockups-2 t211u): “4 - ok sounds good. 6. sure that sounds good - thoguh that doesn't cover the project updates section of the site. 7. ok good yeah choose whatever you think is best. 8. Cool yeah that works”
- **F076** — All mockup styles via dev-only setting. (Martin, S08-mockups-3 t231u): “it'd be cool if we supported all the styling choices you did in the mockups, it can be a dev only setting that I can adjust in these mockups”
- **F086** — App will encourage users to take photos. (Martin, S07 t165u): “So my app will encourage you to take photos”
- **R1** — requirements.md item 1: No live postups means no map on home. Home focuses on projects instead; the map appears only when postups exist.
- **R3** — requirements.md item 3: With no activity this week, home and the feed fall back to recent projects of any age. Never empty or "quiet" copy.
- **R4** — requirements.md item 4: No empty or "quiet" copy anywhere ("No posts yet", "Nothing yet", "Nobody.", "quiet").
- **R9** — requirements.md item 9: Sign-in only at the moment of action, as a sheet over the current screen (Apple + Google).
- **R12** — requirements.md item 12: Phone tab bar: Map, Nearby, Post up, Projects, Inbox. Desktop left rail with the same items. Consistent across devices.
- **R30** — requirements.md item 30: Admin reports page for Martin only.
- **R36** — requirements.md item 36: Google Places content only inside UI Kit widgets, never in the feed; we store only `place_id`.
- **R38** — requirements.md item 38: Feed photos come from users and projects only; fallback is a tinted tile, never a grey box.
- **R53** — requirements.md item 53: Nav tab for / is always labeled "Home" (never "Map").
- **R69** — requirements.md item 69: The map shows only on map, cafe and postup screens; Projects and the Nearby feed never show it.
- **FS** — final-screens.md (final screens answer, Oct 2026)
- **M1018** — Martin, Oct 18 2026 (relayed by the PM): every page gets a scenario toggle (signed out/in × live nearby/none) and renders that scenario; pages that do not differ say "same in all scenarios"; mark the home page (/) clearly
- **M1018b** — Martin, Oct 18 2026 (relayed by the PM): Home (/) has two modes on one URL, Live (map + Live now) and Building (projects preview, See all projects, Post up, This week); default by whether anyone is live; Live · Building switch; banner when someone goes live in Building; draw the overlay-on-map version as #home-overlay-alt, alternative, not chosen
- **M1018c** — Martin, Oct 18 2026 (relayed by the PM): the Building heading is "What people are building" (not "nearby"); the list is sorted closest-first and shows the closest projects available even if none are local; never claim "nearby" unless they are
- **M1024** — Martin, Oct 24 2026 (relayed by the PM): keep tracking user types/scenarios and also track critical flows: a type of user arrives in a certain situation and goes through a scenario step by step; draft all important MVP flows
- **M1025** — Martin, Oct 25 2026 (relayed by the PM): a flow map, a state machine from a first-time visitor (not registered) showing how users reach the starting point of each flow
- **M1031-draft** — PM draft decision, Oct 31 2026 (model phase 2, approved scope; each one listed for Martin to confirm)
- **M1035** — Martin, Oct 28 2026: per-phase screen versions
- **drawn** — the mockup drawing itself
- **unsourced** — no source; confirm with Martin
- **TK§1** — mockup-takeaways.md (mockup session takeaways) §1
- **TK§2** — mockup-takeaways.md (mockup session takeaways) §2
- **TK§4** — mockup-takeaways.md (mockup session takeaways) §4
