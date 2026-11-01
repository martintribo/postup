# Flow: First visit → Too far away (`first-visit--too-far`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--too-far.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@out.none (cafe), quiet@out.none (Locate), **post@out.none** (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), home@out.none.building (Building), projects@out.none (Projects), empty-area@out.none (area has no postups), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: first-visit--already-posted step 1 (if Nobody around right now), first-visit--nobody step 1 (if Nobody around right now), first-visit--post step 1 (if Nobody around right now)
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.none (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--already-posted step 2 (if Filling in the post), first-visit--post step 2 (if Filling in the post)
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--already-posted step 3 (if Not at the nearest cafe), first-visit--post step 3 (if Not at the nearest cafe)
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.none** (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--already-posted step 4 (if Looking for the right cafe), first-visit--post step 4 (if Looking for the right cafe)
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), posted@in.none (signs in → continues), post-already@in.none (signs in → continues (you already have a live postup)), **post-far@in.none** (signs in → continues (the place is too far from you))
   - enterable flows: first-visit--already-posted step 5 (if Ready; asked to sign in), first-visit--post step 5 (if Ready; asked to sign in)
6. **post-far@in.none** · user: The cafe they picked is 2 mi away · action: signs in · edge: tap: Continue with Apple (the place is too far from you)
   - You're too far away: you can only post up where you are. Best effort in the browser. [M1039]
   - next site states: back (Back), **where@in.none** (Pick a cafe near you), home@in.none.live (Back to map), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Back to map), projects@in.none (Projects)
   - enterable flows: returning-post--too-far step 2 (if Picked the cafe from yesterday by habit)
7. **where@in.none** · user: Picks the cafe they're actually at · action: taps Pick a cafe near you · edge: tap: Pick a cafe near you
   - Where are you? list, nearest first. [FS] [M1039]
   - next site states: back (Back), where-search@in.none (Search cafes), posted@in.none (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), project-new@in.none (Project), home@in.none.building (home), projects@in.none (Projects), post-already@in.none (Post up (you already have a live postup)), post-far@in.none (Post up (the place is too far from you))
   - enterable flows: none

## Connected flows [M1025]
- `returning-post--too-far`: branch out at step 6→2; merge in at step 6 (from its step 2)
- `first-visit--nobody`: branch out at step 1→1; merge in at —
- `first-visit--already-posted`: branch out at step 5→5; merge in at —
- `first-visit--post`: branch out at step 5→5; merge in at —

## Screens
1. `#home` · auth=out live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin&ph=0#where-search)
6. `#post-far` · auth=in live=none — You're too far away: you can only post up where you are. Best effort in the browser. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#post-far)
7. `#where` · auth=in live=none — Where are you? list, nearest first. [FS] [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#where)

## Success criteria
- They can't post up somewhere they're not, and are sent to pick a cafe near them. [M1039]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
