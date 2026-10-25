# Flow: Curious browser: live now, then past content (`curious-browser`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/curious-browser.html

## Persona
- First-time visitor, signed out, who has heard of PostUp and wants to see what is on it: who is live and what people have made.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- See live and past content, then follow someone, signing in only at Follow. [M1025]

## Steps
1. **home@out.live.live** · user: Curious what is on the site · action: arrives at / · edge: entry
   - Live now list: who is working where. [M1018b] [M1025]
   - next site states: **postup@out.live** (M 2), postup-ask@out.live (T), cafe@out.live (tap), home@out.live.building (Building), quiet@out.live (Locate), project@out.live (Star Fox 64 mod), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live ( (Google card fails))
   - enterable flows: first-visit-live step 1 (if Curious; sees people live right now), stumbled step 1 (if No idea what PostUp is)
2. **postup@out.live** · user: Peeking at who is live · action: taps a live row · edge: tap: M 2
   - Peeks at a live postup, then Back. [FS] [M1025]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), join-signin@out.live (Join), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit-live step 2 (if Tempted by one postup), stumbled step 2 (if Trying to understand by example)
3. **home@out.live.building** · user: Wants past content too · action: back, switches to Building · edge: back, then mode: Building
   - Switches to Building for past content. [M1018b] [M1025]
   - next site states: home@out.live.live (Live), me@out.live (S), **projects@out.live** (See all projects), project@out.live (Star Fox 64 mod M Maya · Yesterday), post@out.live (Post up), cafe@out.live (Lantern Tea A D M 3 postups), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), cafe-gfail@out.live (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: stumbled step 4 (if Still unsure; looks around)
4. **projects@out.live** · user: Browsing what people build · action: taps See all projects · edge: tap: See all projects
   - See all projects, closest first. [M1018c] [FS]
   - next site states: project-new@out.live (New project), **project@out.live** (Star Fox 64 mod M Maya · Yesterday), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), inbox@out.live (Inbox)
   - enterable flows: none
5. **project@out.live** · user: Interested in one project · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Opens a project: updates and past postups. [FS] [M1025]
   - next site states: back (Back), project-new@out.live (New), **profile@out.live** (Maya), project-update@out.live (Update), project-attach@out.live (Post up), cafe@out.live (Bean Theory), postup@out.live (M Maya Bean Theory · till 4pm Live), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
6. **profile@out.live** · user: Who is behind it? · action: taps the owner · edge: tap: Maya
   - Opens the maker's profile: past postups, regular cafes. [FS] [F065] [M1025]
   - next site states: back (Back), profile+more@out.live (More), postup@out.live (Live at Bean Theory Till 4pm · Sta), **profile+signin@out.live** (Follow), cafe@out.live (Bean Theory), project@out.live (Star Fox 64 mod Updated yesterday), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
7. **profile+signin@out.live** · user: Wants to keep up with them · action: taps Follow 🔒 · edge: sheet: Follow
   - Taps Follow: soft sign-in sheet; Not now keeps browsing. [FS] [M1018] [M1025]
   - next site states: profile@out.live (close), **profile@in.live** (signs in)
   - enterable flows: none
8. **profile@in.live** · user: Convinced enough to sign in · action: signs in · edge: sign-in: signs in
   - Signed in and following. [FS] [M1025]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod Updated yesterday), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 4 (if Checking Maya's track record), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `stumbled`: branch out at step 2→2, step 3→4; merge in at step 3 (from its step 4)
- `cautious-joiner`: branch out at step 8→4; merge in at step 8 (from its step 4)
- `host-approve`: branch out at step 8→3; merge in at step 8 (from its step 3)
- `first-visit-live`: branch out at step 2→2; merge in at —

## Screens
1. `#home` · auth=out live=live mode=live — Live now list: who is working where. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Peeks at a live postup, then Back. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#home` · auth=out live=live mode=building — Switches to Building for past content. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
4. `#projects` · auth=out live=live — See all projects, closest first. [M1018c] [FS] (/mockups/?style=fresh&device=phone&auth=out&live=live#projects)
5. `#project` · auth=out live=live — Opens a project: updates and past postups. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)
6. `#profile` · auth=out live=live — Opens the maker's profile: past postups, regular cafes. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#profile)
7. `#profile` + sheet `signin` · auth=out live=live — Taps Follow: soft sign-in sheet; Not now keeps browsing. [FS] [M1018] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#profile)
8. `#profile` · auth=in live=live — Signed in and following. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)

## Branches and edge cases
- Nobody live: Home opens in Building, so the flow starts at the projects (merged from the old first-visit-none flow). [M1018b] [M1025]
- Taps Post up instead: see Came to post up. [M1025]
- Not now on the sheet: stays signed out, nothing lost. [drawn] [M1025]
- Never empty or "quiet" copy when nothing is live. [F035] [R4]

## Success criteria
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]

## Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
