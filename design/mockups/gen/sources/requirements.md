# PostUp requirements ledger (Martin's product decisions)
Rebuilt Oct 16, 2026 ~4:50 PM CT after gapfill-2 + Mockups group rebuild.
Facts: `/cursor/stores/store-f9d14309-8909-44c2-8159-471214b611f2/postup-excerpts/facts.jsonl` (F001–F091).
Mockups group sessions: S08-mockups-1, S08-mockups-2, S08-mockups-3 (full arc + artifacts on part 3).

## Quick index: fact tags
- **process**: 22 facts
- **dashboard**: 16 facts
- **home**: 12 facts
- **mockups**: 8 facts
- **styling**: 7 facts
- **infra**: 6 facts
- **map**: 6 facts
- **cafes**: 5 facts
- **projects**: 5 facts
- **photos**: 5 facts
- **google**: 4 facts
- **posting**: 4 facts
- **first-visit**: 4 facts
- **nav**: 4 facts
- **desktop**: 4 facts
- **join**: 4 facts
- **cost**: 3 facts
- **memory**: 3 facts
- **account**: 3 facts
- **plan**: 3 facts
- **data**: 2 facts
- **ux**: 2 facts
- **fidelity**: 2 facts
- **testing**: 2 facts
- **native**: 2 facts
- **copy**: 1 facts
- **todo**: 1 facts
- **safety**: 1 facts
- **states**: 1 facts
- **chat**: 1 facts
- **share**: 1 facts
- **open-decision**: 1 facts
- **hub**: 1 facts

## All facts (id → gist → session)
- **F001** (S02 pos 197): Worktree dev DBs use Docker/local Postgres; not PGlite, SQLite or a Neon copy. — quote verified.
- **F002** (S02 pos 213): Wants a working PostUp dev instance. — quote verified.
- **F003** (S03 pos 392): Map provider must have a hard cap; prefer failing over surprise charges. — quote verified.
- **F004** (S03 pos 428): Tile coverage: the whole world. — quote verified.
- **F005** (S03 pos 425): OK to use Martin's Cloudflare account. — quote verified.
- **F006** (S04 pos 577): Rejected paid Workers plan; go back to free tile plan. — quote verified.
- **F007** (S04 pos 588): Map tiles: Stadia Maps. — quote verified.
- **F008** (S04 pos 623): Approved merging Stadia tiles to main. — quote verified.
- **F009** (S04 pos 634): Remove the Stadia worker. — quote verified.
- **F010** (S05 pos 785): Site map: ~5 sections, 1-3 word titles, visual not text. — quote verified.
- **F011** (S05 pos 792): Site-map sections expandable to show low-level features. — quote verified.
- **F012** (S05 pos 819): Site map: branch view and branch-diff view. — quote verified.
- **F013** (S05 pos 819): General UX rule: little on screen at a time; drill-down with back button. — quote verified.
- **F014** (S05 pos 831): Each sitemap page has a how-to-reach blurb. — quote verified.
- **F015** (S06 pos 976): Lineage: no nodes for old versions, draw a line instead. — quote verified.
- **F016** (S06 pos 987): Dashboard top row half height. — quote verified.
- **F017** (S06 pos 997): Cards with no page changes skip the graph. — quote verified.
- **F018** (S06 pos 1008): Add code-architecture node map. — quote verified.
- **F019** (S06 pos 1018): Main code map on top row. — quote verified.
- **F020** (S07 pos 1187): Idea: places photos at side with leader lines to markers. — quote verified.
- **F021** (S07 pos 1204): Try UI Kit on a new branch off places. — quote verified.
- **F022** (S07 pos 1227): Hub should offer API for setting cloud keys. — quote verified.
- **F023** (S07 pos 1236): Remove legacy Places from the old server key. — quote verified.
- **F024** (S08-mockups-1 pos 1383): Build in order of need; projects first because an empty map would greet users. — quote verified.
- **F025** (S08-mockups-1 pos 1386): Planning section on dashboard; mockups before development. — quote verified.
- **F026** (S08-mockups-1 pos 1396): Mockups link to each other. — quote verified.
- **F027** (S08-mockups-1 pos 1406): Raised the no-live-postups state. — quote verified.
- **F028** (S08-mockups-1 pos 1409): Questioned showing the map when no one is live. — quote verified.
- **F029** (S08-mockups-1 pos 1410): Proposal (accepted in later work): feed when no one live, map when live. — quote verified.
- **F030** (S08-mockups-1 pos 1412): Alternate feed-first mock; think about appeal. — quote verified.
- **F031** (S08-mockups-1 pos 1415): Consider images in feed. — quote verified.
- **F032** (S08-mockups-1 pos 1423): Google photos never in feed. — quote verified.
- **F033** (S08-mockups-1 pos 1423): Optional photo ask after posting. — quote verified.
- **F034** (S08-mockups-1 pos 1425): Mockups must look like a real professional app. — quote verified.
- **F035** (S08-mockups-1 pos 1432): Never say it's quiet. — quote verified.
- **F036** (S08-mockups-1 pos 1442): Keep current style; try other fundamental styles. — quote verified.
- **F037** (S08-mockups-3 pos 1595): One branch + worktree site per phase, no merge to main; keep dashboard/graphs current. — quote verified.
- **F038** (S08-mockups-3 pos 1618): Always link live sites. — quote verified.
- **F039** (S08-mockups-3 pos 1637): Verify by running the branches. — quote verified.
- **F040** (S08-mockups-3 pos 1792): App should look exactly like the mockups. — quote verified.
- **F041** (S08-mockups-3 pos 1792): Real data from original project branch into worktrees. — quote verified.
- **F042** (S08-mockups-3 pos 1792): Checklist validation skill per worktree URL. — quote verified.
- **F043** (S11 pos 1808): First-visit experience required; fall back to projects in general when nothing this week. — quote verified.
- **F044** (S11 pos 1830): No map when no postups; focus on projects. — quote verified.
- **F045** (S11 pos 1850): Don't let tasks run long without check-ins. — quote verified.
- **F046** (S11 pos 1883): Tab always called Home. — quote verified.
- **F047** (S11 pos 1900): Keep a verbatim excerpt store. — quote verified.
- **F048** (S11 pos 1907): Two layers: sessions and facts. — quote verified.
- **F049** (S08-mockups-1 pos 1449): Desktop mockups required. — quote verified.
- **F050** (S08-mockups-1 pos 1464): Bold style on desktop too. — quote verified.
- **F051** (S08-mockups-2 pos 1489): Nearby feed on desktop should not show the map. — quote verified.
- **F052** (S08-mockups-2 pos 1499): Projects must not show the map. — quote verified.
- **F053** (S08-mockups-2 pos 1507): Map only on map, cafe and postup screens. — quote verified.
- **F054** (S08-mockups-2 pos 1509): Review from visitor perspectives. — quote verified.
- **F055** (S08-mockups-2 pos 1519): Join mode is a per-postup setting by the poster; poster is alerted. — quote verified.
- **F056** (S08-mockups-2 pos 1519): Where-I'm-sitting note/picture: to-do. — quote verified.
- **F057** (S08-mockups-2 pos 1519): Managing your own postup is important. — quote verified.
- **F058** (S08-mockups-2 pos 1519): Doubts the map as cafe picker. — quote verified.
- **F059** (S08-mockups-2 pos 1519): Report and block yes; no safety tips. — quote verified.
- **F060** (S08-mockups-2 pos 1519): Profile/account needed; fix wrong links; add ended/failed states. — quote verified.
- **F061** (S08-mockups-2 pos 1519): Chat at launch; reason when requesting to join. — quote verified.
- **F062** (S08-mockups-2 pos 1520): Cafe picking via search sheet (agreed). — quote verified.
- **F063** (S08-mockups-2 pos 1520): Dismissable first-visit welcome. — quote verified.
- **F064** (S08-mockups-2 pos 1520): Phone and desktop menus match. — quote verified.
- **F065** (S08-mockups-2 pos 1520): Profile contents. — quote verified.
- **F066** (S08-mockups-2 pos 1526): Agreed to search picker, welcome/share pages (plus projects), menus, profile. — quote verified.
- **F067** (S08-mockups-2 pos 1529): Projects first-visit line and project share landing. — quote verified.
- **F068** (S08-mockups-2 pos 1542): Some mockup gaps deferred to implementation. — quote verified.
- **F069** (S08-mockups-2 pos 1559): Iterative implementation plan for postup.now. — quote verified.
- **F070** (S08-mockups-2 pos 1564): Cafe visibility asked; no Martin answer in transcript. — quote verified.
- **F071** (S08-mockups-2 pos 1566): Wrapped native app suggested (Cordova). — quote verified.
- **F072** (S08-mockups-2 pos 1567): Capacitor proposed instead. — quote verified.
- **F073** (S08-mockups-2 pos 1574): Store review perspectives. — quote verified.
- **F074** (S08-mockups-3 pos 1649): Consider direct Hub access. — quote verified.
- **F075** (S08-mockups-3 pos 1694): Check all sites load. — quote verified.
- **F076** (S08-mockups-3 pos 1701): All mockup styles via dev-only setting. — quote verified.
- **F077** (S08-mockups-3 pos 1710): Styling baked into the first branch. — quote verified.
- **F078** (S08-mockups-3 pos 1718): Milestone progress updates. — quote verified.
- **F079** (S08-mockups-1 pos 1459): Fresh + Cozy/Night/Bold switcher live on mockups. — quote verified.
- **F080** (S08-mockups-1 pos 1462): Desktop mockups live in all four styles. — quote verified.
- **F081** (S08-mockups-2 pos 1555): Mockups grew to 44 screens after review batch. — quote verified.
- **F082** (S08-mockups-2 pos 1592): 13-phase iterative rollout plan. — quote verified.
- **F083** (S08-mockups-3 pos 1793): Fidelity gap acknowledged: colors match, layouts do not. — quote verified.
- **F084** (S07 pos 1377): Step back: identify core essential pieces to release. — quote verified.
- **F085** (S07 pos 1170): Google Photos/Places API cost concern — easy to overcharge. — quote verified.
- **F086** (S07 pos 1182): App will encourage users to take photos. — quote verified.
- **F087** (S08-mockups-2 pos 1486): Asked where the no-active-postups page is. — quote verified.
- **F088** (S04 pos 689): Dashboard focuses on important worktrees (photos/places/project tracking). — quote verified.
- **F089** (S05 pos 760): Need visual site map associated with features. — quote verified.
- **F090** (S06 pos 935): Top row: live site map + lineage overview. — quote verified.
- **F091** (S06 pos 940): Compare maps default to branch vs parent in lineage. — quote verified.

## Prior numbered requirements (1–80)
See previous ledger body retained below for verification checklists; citations to S08/S09/S10 now map to S08-mockups-*. Contradictions (hidden cafe D2, Westside D1, join default D5, chat 24h D6) still stand.

## Home and first visit
1. **No live postups means no map on home. Home focuses on projects instead; the map appears only when postups exist.** Applies on phone and desktop, for fresh and signed-in visitors. Source: conv (Martin, Oct 15). Verify: in the WK and Q states, `/` shows no `.leaflet-container` and does show project cards. [auto R01] ✅ **Facts: F044, F028, F029, F024, F051.**
2. **When postups are live, home is the map with "Live now" (side panel on desktop).** Source: plan M4, feed. Verify: in LIVE, `/` shows the map and the live-now list. [auto R02] ✅ **Facts: F029.**
3. **With no activity this week, home and the feed fall back to recent projects of any age. Never empty or "quiet" copy.** Source: conv (Martin, Oct 15). Verify: in Q, `/` and `/nearby` show project cards. [auto R03] ✅ **Facts: F043.**
4. **No empty or "quiet" copy anywhere ("No posts yet", "Nothing yet", "Nobody.", "quiet").** Source: conv (repeated). Verify: key routes in all three states contain none of those phrases. [auto R04] ✅ (fixed /activity and /settings) **Facts: F035.**
5. **First-visit explainer: what PostUp is (cafes, postups, join), dismissable.** Source: review 1/2 (blocker), conv. Verify: with fresh storage, `/` shows a welcome line about cafes and posting up or joining. [auto R05] ✅ **Facts: F043, F063, F066.**
6. **First-visit guidance on Projects.** Source: conv, plan M2 (welcome line on Projects). Verify: fresh `/projects` shows the welcome line. [auto R06] ✅ **Facts: F043, F067.**
7. **Location context, e.g. "Near Westside, Los Angeles".** Source: review 2. Verify: `/nearby` and the no-live home show "Near …". [auto R36] ✅ (fixed) The area picker ("▾", change area) is ❌ still open. **⚠ UNSOURCED.**
8. **Launch area is Playa Vista / Westside LA as the fallback centre (D1).** Source: plan D1, cfg. Verify: with location denied, the map centres on Westside, or "Near Westside, Los Angeles" shows. 🖐 (label passes) **⚠ UNSOURCED.**
9. **Sign-in only at the moment of action, as a sheet over the current screen (Apple + Google).** Source: plan M1, GAPS, review 1. Verify: signed out, submit `/post`: the sheet opens and the URL stays `/post`. [auto R08] ✅ **⚠ UNSOURCED.**
10. **Every "Log in" link opens the sheet, not the /login page.** Source: conv (shared shell). Verify: click a /login link: the sheet shows. [auto R09] ✅ (desktop fixed: capture-phase intercept) **⚠ UNSOURCED.**
11. **Signed-out drafts survive sign-in.** Source: conv (post flow). Verify: fill `/post`, sign in from the sheet, and the fields come back. Done once with Playwright (flow.mjs). 🖐 ✅ **⚠ UNSOURCED.**

## Navigation
12. **Phone tab bar: Map, Nearby, Post up, Projects, Inbox. Desktop left rail with the same items. Consistent across devices.** Source: review cross-cutting, GAPS. Verify: [auto R10] ✅ **Facts: F046, F064, F066 (label is Home, not Map).**
13. **Root tabs have no Back button.** Source: review 2/3. Verify: `/`, `/nearby`, `/projects`, `/inbox` have no Back. [auto R11] ✅ **Facts: F054 (perspective review only, weak).**
14. **No "Mockups" link in the real nav.** Source: review cross-cutting. [auto R32] ✅ **⚠ UNSOURCED.**
15. **Avatar in nav and a visible signed-in vs signed-out difference.** Source: review 7. Verify: the desktop rail shows the avatar when signed in. ✅ on desktop. On phone the Nearby header avatar from the mockup is ❌ open. **⚠ UNSOURCED.**

## Posting
16. **Sign in required to post; anonymous posting is off (D3).** Source: plan D3/M5. [auto R08] ✅ **⚠ UNSOURCED.**
17. **Post form: cafe preselected, a real "Change" picker ("Where are you?" with nearby list and search), "Working on" text, project chips, Until 1h/2h/3h/time, Who can join.** Source: review 4, plan M3. Verify: `/post`, tap Where: the sheet lists nearby cafes. ✅ (seen in flow.mjs and the sheets) **Facts: F062, F066, F058.**
18. **Default join mode is "Anyone can join" (D5).** Source: plan D5, cfg. [auto R14] ✅ (now read from config) **Facts: F055 (per-postup setting by poster; the 'Anyone' default is ours, not Martin's).**
19. **Attach-to-project requires sign-in, and the past option reads "I was here earlier".** Source: review 4. [auto R24, R25] ✅ **⚠ UNSOURCED.**
20. **Optional "Add a photo of your spot", asked after posting on the confirmation screen; never required.** Source: feed. ❌ open (there is no postup photo storage yet; "You're posted up" screen is in the next chunk) **Facts: F033.**
21. **Location permission explainer, plus a denied state that falls back to search/pick.** Source: review 4. ❌ open **Facts: F062 (weak).**
22. **Manage your live postup: time left, Extend, Edit, End, shown on home.** Source: plan M5, review 4. Partial: home shows "You're live" in LIVE. The m5 manage page still needs restyling. 🖐 **Facts: F057.**

## Joining and safety
23. **Ask-to-join hides the cafe (neighborhood only) until approved (D2).** Source: plan D2, cfg. Verify: `/p/8` (an ask postup) shows "a cafe in …", not the cafe name. [auto R13] ✅ **Facts: F070 (⚠ Martin never answered; the hidden cafe is our default and contradicts the mockups).**
24. **Explain what Join means ("Let Maya know you're coming, then say hi at the cafe").** Source: review 1. [auto R37] ✅ (fixed) **⚠ UNSOURCED.**
25. **Directions open Apple/Google Maps.** Source: review 5, plan M9. [auto R23] ✅ **⚠ UNSOURCED.**
26. **The poster is always alerted and approves or declines; joiners list.** Source: plan M6. 🖐 (m6 flow; not re-run here) **Facts: F055, F061.**
27. **Leave asks for confirmation.** Source: review 5. ❌ open (in the join-screens chunk) **Facts: F057 (weak).**
28. **Report and block on people and postups.** Source: plan M8 (launch blocker). [auto R18] ✅ present, but inline, not yet the mockup "…" menu (❌ in the report chunk) **Facts: F059.**
29. **No safety tips.** Source: plan M8 ("per Martin"). [auto R17] ✅ **Facts: F059.**
30. **Admin reports page for Martin only.** Source: plan M8. [auto R35] ✅ **⚠ UNSOURCED.**
31. **Chat for poster and approved joiners, readable 24h after end (D6).** Source: plan M7/D6, cfg. 🖐 (m7) **Facts: F061 (chat at launch; the 24h read window is our default).**

## Projects
32. **Projects grid with Nearby / Following / Mine tabs that work, each with a friendly empty state.** Source: review 3, GAPS. [auto R26] ✅ **Facts: F052, F053.**
33. **Follow a project.** Source: review 3. [auto R27] ✅ **Facts: F065 (follow button).**
34. **Test or hidden projects never show.** Source: plan M0. [auto R19] ✅ **⚠ UNSOURCED.**
35. **Project page, updates timeline with images, owner posts updates.** Source: plan M2. ✅ (sheets) **Facts: F052.**

## Cafes and Google
36. **Google Places content only inside UI Kit widgets, never in the feed; we store only `place_id`.** Source: plan rules, feed. 🖐 (code: GCard wraps the UI Kit only) **Facts: F032.**
37. **Google card failure falls back ("Details unavailable", Open in Maps, Retry).** Source: plan M12, review. [auto R28] ✅ **⚠ UNSOURCED.**
38. **Feed photos come from users and projects only; fallback is a tinted tile, never a grey box.** Source: feed. Partial: the project placeholder is a tinted tile. User photos are ❌ open (feed chunk). **Facts: F032, F031.**

## Share and links
39. **Share landings: live postup ("X is working at Y till Z. Join?"), ended postup (→ what's nearby), project ("X is building Y").** Source: plan M9, review 8, conv. [auto R07a/b/c] ✅ **Facts: F067, F063.**
40. **Feed items link person → profile, cafe → cafe, project → project.** Source: review 2. [auto R22] ✅ **Facts: F060 (fix wrong links).**
41. **Share opens a share sheet (not the poster's success screen).** Source: review 5. ❌ open (share-sheet chunk; native share or copy for now) **⚠ UNSOURCED.**

## Account
42. **Profile, settings, sign out reachable.** Source: review 7, plan M11. [auto R30] ✅ **Facts: F060, F065, F066.**
43. **Account deletion in the app (store guideline 5.1.1).** Source: plan M10/M11. [auto R29] ✅ **⚠ UNSOURCED.**
44. **Real title and meta/OG tags.** Source: plan M0. [auto R20] ✅ **⚠ UNSOURCED.**

## Look and platform
45. **Four styles (Fresh, Cozy, Night, Bold), each working on phone and desktop; components use tokens only.** Source: persp, conv. [auto R21] ✅ plus the token lint unit test **Facts: F076, F077, F036, F034, F040, F050.**
46. **Offline: a full offline screen (mockup), not just a banner.** Source: plan M10/M12, GAPS. [auto R42] ✅ for now: the check only looks for offline/connection wording, which the m10 banner passes. The mockup's full-screen state is still open (offline chunk). **⚠ UNSOURCED.**
47. **Ended / full / cancelled states.** Source: plan M12, review 5. 🖐 (ended landing is ✅; the postup page states are in the states chunk) **Facts: F060.**

## Process (Martin)
48. **No PRs. Martin approves merges to main. Prod deploys from main. Never touch the prod DB or prod Vercel env.** Source: plan, conv. ✅ (only fast-forward pushes to phase/*) **Facts: F037, F008.**
49. **Confirm by doing the work, never guess. Diagrams and feature maps only if verified.** Source: notes. 🖐 **Facts: F039.**
50. **Lineage and worktree-card display rules for the PM page.** Source: notes. 🖐 **Facts: F015, F017, F010-F014, F016, F018, F019.**
51. **Phase branches frozen as reference; the app is built on phase/final with all flags on.** Source: conv (Oct 15). ✅ **⚠ UNSOURCED.**
52. **`drizzle-kit push` must never offer to drop `import_map`.** Source: conv (Hub, Oct 15). Verify: push against a DB that has `import_map` → "No changes detected". ✅ (tablesFilter) **⚠ UNSOURCED.**
53. **Nav tab for / is always labeled "Home" (never "Map").** Verify: phone tab bar and desktop rail show Home. **Facts: F046.**


## Contradictions and decisions that are only our defaults (check with Martin)
- **#12:** the tab is labeled "Home", not "Map" (F046).
- **#23 (D2):** Martin never decided to hide the cafe. The question (F070) went unanswered, and the mockups show the cafe name.
- **#18 (D5):** Martin's rule is that join mode is a setting the poster picks (F055). "Anyone can join" as the default is ours.
- **#31 (D6):** chat at launch is Martin's (F061). The 24h read window is ours.
- **#8 (D1):** Westside LA is ours. Martin never chose it in the covered transcript.

## Decisions found in excerpts that weren't in the ledger before
54. **Map provider must have a hard usage cap; prefer the site failing over surprise charges. Free plan, Stadia tiles, worldwide coverage.** Facts: F003, F006, F007, F004, F008, F009.
55. **Worktree dev databases use Docker/local Postgres.** Facts: F001.
56. **Build in order of need; projects first because otherwise an empty map greets users.** Facts: F024.
57. **Mockups before development; the dashboard has a planning section.** Facts: F025.
58. **Professional-app quality; keep the chosen style when adding others.** Facts: F034, F036.
59. **No-live state designed for appeal: user photos first, Google photos never in the feed, optional photo ask after posting.** Facts: F030-F033.
60. **Always send live site links.** Facts: F038.
61. **One branch and one worktree site per phase, no merging to main, dashboard and graphs kept current.** Facts: F037.
62. **Real data goes into the worktrees.** Facts: F041.
63. **Checklist validation skill.** Facts: F042.
64. **Check in during long work and send milestone updates.** Facts: F045, F078.
65. **Dashboard UX rules.** Facts: F010-F019.
66. **Verbatim excerpt store.** Facts: F047, F048.
67. **Remove legacy Places from the old server key; the Hub should offer a key-setting API.** Facts: F023, F022.
68. **Every screen has a desktop design, and each style (including Bold) works on desktop.** Facts: F049, F050.
69. **The map shows only on map, cafe and postup screens; Projects and the Nearby feed never show it.** Facts: F051, F052, F053.
70. **Requesting to join an approval-required postup includes a reason.** Facts: F061.
71. **Chat for the people in a postup is required at launch.** Facts: F061.
72. **The poster is alerted when someone joins.** Facts: F055.
73. **To-do: a "where I'm sitting" description or picture.** Facts: F056.
74. **Picking a cafe uses search and a nearby list, not the map.** Facts: F058, F062, F066.
75. **Phone and desktop menus match.** Facts: F064, F066.
76. **Profile: photo, name, bio, regular cafes, projects, past postups, follow button, settings and sign out.** Facts: F065, F066.
77. **Projects first-visit line, plus a project share landing page.** Facts: F066, F067.
78. **Review from visitor perspectives (new, bored, wants to post up), and store those perspectives.** Facts: F054, F073.
79. **Native app wraps the same web rendering. Martin suggested Cordova; Capacitor was proposed instead, with no explicit OK from Martin in the transcript.** Facts: F071, F072.
80. **Styles are baked into the first branch; all mockup styles are switchable through a dev-only setting.** Facts: F076, F077.


## Newly sourced / added after gapfill-2 (Oct 16 afternoon)
81. **Google Places/Photos cost is a first-class concern; the app should encourage user photos.** Facts: F084, F085 (ids may vary — see facts.jsonl for Google cost + encourage photos).
82. **Dashboard top row: live site map + lineage; compare defaults to branch vs parent; focus on important worktrees.** Facts: F087–F090.
83. **Mockups: 44 screens after the review batch; desktop in all four styles; fidelity still incomplete (colors match, layouts do not).** Facts: F079–F082.
84. **Step back and identify the core essential pieces needed to release.** Facts: F083.


## From mockup builder / UX-review work logs (F092–F113)
- Builder briefs encode Martin decisions (join mode, chat at launch, Where-are-you sheet, first-visit welcome, Fresh+styles, feed-first, no quiet copy, desktop, Projects without map).
- UX review recorded first-visit/trust gaps, manage-live-postup gap, cafe-picker gap.
