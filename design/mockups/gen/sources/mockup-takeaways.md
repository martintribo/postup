# Takeaways: PostUp mockup design session (S08-mockups-all)

**Question:** What are the takeaways from the PostUp mockup design session?
**Source:** excerpt group S08-mockups-all (2,869,252 chars), 17 overlapping chunks, all 17 reported. Chunks 03–12, 14 and 15 contain no Martin dialogue (commit diffs, mockup source, review artifacts), so findings from them are ranked below what Martin said. Generated 2026-10-16.

## Direct answer
Martin had the important flows mocked up before any development. He then pushed the mockups toward a professional, sparse, linked prototype: 44 screens, four styles, phone and desktop. He approved them on Oct 15 and asked for an iterative, branch-per-phase plan. The build that followed copied the mockups' **styles** (tokens, fonts, colours) but not their **layouts**. When he asked "Does this look exactly like the mockups?", the answer was no. The gap audit put the work left to match at 3–4 weeks. The main reasons: verification only checked styling, the worktree databases had no data, and the design history lived only in chat. The two fixes were the excerpt store and the requirements file.

## 1. Decisions Martin stated (newest wins)
**Later decisions that replace the mockups**
- The nav tab is always labeled **"Home"**, never "Map". The mockup index labels it "Map".
- With **no live postups, home shows no map** and focuses on projects. The mockup "Open map" card and the `?view=map` option in the M4 code don't follow this.
- With **no activity this week**, home and Nearby fall back to projects in general.

**Order and process**
- "develop features in the order that we will need them": projects come first, so new users don't land on an empty map (t192u). The order agreed: content tools → map shows content → join/post up (sign-in only at that moment) → sharing → polish.
- Mock up the important parts and flows first, then develop. The dashboard gets a project-planning section (t193u).
- The mockups must link to each other like a real app, and everything that looks tappable must go somewhere (t194u).
- "make these mockups look like a real professional app" (t199u). Keep his taste: sparse, 1–3 word labels, warm copy, drill-down with Back, 🔒 only on pages that need login.
- Mockups were approved: "this looks good.. can you come up with a plan to iteratively implement all of this on the live postup.now site?" (t215u).
- One branch per phase, no merges to main, each phase reviewable on its own worktree site. Keep the worktree and graph pages up to date (t218u).
- Store the review perspectives so he can later check what was missed (t217u).
- Problems on the live site (test projects, Clarksville default, SEO) get fixed "naturally … when we make these mockups real" (t214u).

**Home, feed and copy**
- "is it worth showing the map if no one is live?" He asked for a feed-first alternate to compare and to "think deep about what will be appealing … (like do we need images)" (t196u–t198u).
- "I don't think we even need to say it's quiet": no empty or quiet copy. The feed is called "Nearby" ("Good things happen at cafes") (t200u).
- On desktop, the Nearby feed must not show the map behind it (t207u). Projects must not open the map: it's a real Projects page, a grid on desktop and a list on phone (t208u). The map appears only on map-centric screens.
- Images: user photos are the main source and replace Google photos over time (his goal). Google photos appear only inside the Google card on a cafe page.

**Styles and devices**
- Keep the current style as **Fresh** (the default) and explore other styles (t201u). That produced Cozy, Night and Bold.
- "we also need desktop mockups" (t202u). Bold "looks very cool, can we get it for desktop?" (t203u).

**Answers to the gap review (t210u/t211u, items 1–10)**
1. Join approval is a per-postup setting chosen by the poster ("Anyone can join" or "Ask to join"). An ask includes a reason, and the poster is always alerted.
2. "Where I'm sitting" (a description or photo) stays on the todo list and isn't mocked.
3. Managing your own live postup is important and must be mocked (time left, requests, extend, end, edit, share).
4. Picking a cafe: a map isn't the best way without curated cafes. Use a "Where are you?" sheet with nearby cafes plus search instead.
5. Report and block yes. No safety tips: "this site is for adults."
6. A first-visit welcome line plus a share-link landing, extended to Projects: a Projects welcome line and a project share landing.
7. Phone and desktop nav must match. He left the details to the PM.
8. Profile: photo, name, bio, regular cafes, projects, past postups, follow, and settings or sign out.
9. Fix the dead and wrong links. 10. Add the ended, full and cancelled states, plus the failed-load, loading and offline states.
- Chat is needed at launch: a group chat per postup for the poster and approved joiners, an inbox, and an activity list.
- Native app idea: wrap the same rendering (he suggested Cordova; the PM recommended Capacitor after share links).

**After approval (feedback on the build)**
- "you haven't linked me live sites … links!!" Always link sites (t221u/t223u).
- "how can you know you did the work without running the branches": verify on the real worktree sites (t224u). He also flagged "there's an error on load" (t230u).
- Styling wasn't applied everywhere. Support all the mockup styles as a dev-only switcher, built into the first branch (m0) so every phase has it (t231u/t232u).
- Give progress updates while working (t234u).
- "Does this look exactly like the the mockups?" Add the real data from his original branch, and add a checklist skill that validates a worktree or URL (t239u).

## 2. Design system and screens (from mockup source and code; inferred)
- **Styles:** Fresh (the default, deeper green), Cozy (warm editorial, Fraunces serif), Night (dark neon) and Bold ("playful brutalist", Archivo Black, hard shadows). They switch via `?style=` or localStorage. The app uses design tokens with one theme file per style and a `/style` picker. D8 says Fresh is the default and Bold the front-runner, with the final pick deferred to M12. Only Fresh and Bold were eye-checked on the 44 final screens.
- **Shell:** a phone tab bar (Home/Map, Nearby, Post up in the centre, Projects, Inbox) and a desktop left rail. No Back on root tabs. On desktop, the cafe, postup and project pages open as side panels, and the post and sign-in screens open as centred dialogs. Sign-in is an Apple/Google **sheet** that appears only at the moment of action.
- **Home:** a map with a "Live now / This week" sheet when someone is live, and the photo-led Nearby feed when nobody is (later replaced by the no-map, projects-focused home above). An area label ("Near Venice, LA ▾") and an empty-area state ("Be the first here"), with no fake activity.
- **Post flow:** the "Where are you?" cafe sheet (Google attribution) → what you're working on (+ optional project) → until when → who can join → posted confirmation, with an optional "Add a photo of your spot" after it goes live. A live/manage screen with a timer ring, +30 min, Edit, Approve/Decline requests, and an End confirm.
- **Join:** open join or ask with a reason → "Request sent" → the cafe stays hidden until approved (D2: neighborhood plus a ~1.5 km fuzzed circle). Joined screen: group chat, Directions (opens Maps), and Leave with a confirm.
- **Other screens:** the invite landing ("Maya is working at Bean Theory till 4. Join her?"), the ended and project landings, the share sheet, a "…" more sheet with Report (reasons) and Block, profiles and settings (notification toggles, blocked people, delete account), the ended/full/cancelled states, the Google-card failure state, a loading skeleton, and offline (a banner plus a full screen).
- **Copy rule:** positive invites instead of empty states ("Working somewhere good today?", "Building something? Share a project"). "I was here earlier" replaces "Earlier today".
- **Plan:** M0 hygiene+tokens → M1 OAuth → M2 projects → M3 cafes → M4 feed/map → M5 post/manage → M6 join → M7 chat → M8 report/block → M9 share → M10 Capacitor → M11 profiles → M12 states+style. M7 and M8 block launch, and features sit behind flags. Rules: Google Places data appears only in UI Kit widgets (store only place_id), and JSON /api stays ready for the app.

## 3. Process lessons (why the app drifted from the mockups)
1. **Only the style was checked.** "The colors and fonts match now, but the layouts still use the old page structure." The phases were reskins of the old layout, not ports of the mockup screens.
2. **There was no data to compare.** "the worktree DBs have almost no postups/places, so most data screens show 'no live screen'." Import dev data before checking fidelity.
3. **The mockups themselves missed a decision.** The review found "The decision was feed-first when no one's live, but home is always the map." Decisions made in chat didn't always reach the mockups or the code.
4. **The design history lived only in the conversation.** The building agents didn't have Martin's decisions, which led to the excerpt store, `requirements.md`, and checking each build against it before reporting.
5. **Verify for real.** Run the branch sites in a browser and give links. Tests missed bugs (for example, a default style was never tested). Use at most 1–2 headless browsers: a parallel screenshot run once started 200+ Chromes and hung the box.
6. **Review like a person.** "it seems there were obvious issues here … Think like a normal human would." Use the 8 visitor journeys plus cross-cutting checks (every style on both devices, missing states, plain labels).
7. **Communication:** give milestone updates, don't let work run long, and add guards so Hub relays can't stall silently.

## 4. Open questions (not resolved in the group)
- D2: should the cafe name show before approval on ask-to-join postups? The code hides it by default.
- D1 launch area (the code defaults to Playa Vista / Westside LA), D3 requiring sign-in to post, seeded past postups, the default join mode and capacity (the code defaults to "open"), chat lifetime (24h), email alerts, and merge order.
- Final style choice: Fresh or Bold. Should Cozy and Night stay, and should the OS dark mode switch to Night automatically?
- Cordova vs Capacitor was never explicitly settled by Martin.
- A fallback list of good cafes for empty areas, and a separate mockups site vs exposing them through the dashboard.
- Image storage for projects (Vercel Blob?), and there's no user ban system yet.
- Whether to delete the stray public postup-pm Vercel project.
- The transcript has small gaps (the UX review and a builder report are cut off mid-text).
