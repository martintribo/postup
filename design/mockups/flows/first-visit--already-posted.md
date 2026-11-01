# Flow: First visit → Already posted up (`first-visit--already-posted`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--already-posted.html

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
   - enterable flows: first-visit--nobody step 1 (if Nobody around right now), first-visit--post step 1 (if Nobody around right now), first-visit--too-far step 1 (if Nobody around right now), first-visit--nobody-project step 1 (if Nobody around right now)
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.none (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--ended-post step 3 (if Filling in the post), first-visit--link-post step 3 (if Filling in the post), first-visit--live-already-posted step 2 (if Filling in the post), first-visit--live-post step 2 (if Filling in the post), first-visit--live-too-far step 2 (if Filling in the post), first-visit--post step 2 (if Filling in the post), first-visit--too-far step 2 (if Filling in the post)
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--post step 3 (if Not at the nearest cafe), first-visit--too-far step 3 (if Not at the nearest cafe)
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.none** (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--ended-post step 5 (if Looking for the right cafe), first-visit--link-post step 5 (if Looking for the right cafe), first-visit--live-already-posted step 4 (if Looking for the right cafe), first-visit--live-post step 4 (if Looking for the right cafe), first-visit--live-too-far step 4 (if Looking for the right cafe), first-visit--post step 4 (if Looking for the right cafe), first-visit--too-far step 4 (if Looking for the right cafe)
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), posted@in.none (signs in → continues), **post-already@in.none** (signs in → continues (you already have a live postup)), post-far@in.none (signs in → continues (the place is too far from you))
   - enterable flows: first-visit--ended-post step 6 (if Ready; asked to sign in), first-visit--link-post step 6 (if Ready; asked to sign in), first-visit--live-already-posted step 5 (if Ready; asked to sign in), first-visit--live-post step 5 (if Ready; asked to sign in), first-visit--live-too-far step 5 (if Ready; asked to sign in), first-visit--post step 5 (if Ready; asked to sign in), first-visit--too-far step 5 (if Ready; asked to sign in)
6. **post-already@in.none** · user: Forgot they're already live at Lot 1 · action: posts · edge: tap: Continue with Apple (you already have a live postup)
   - You're already posted up at Lot 1 Coffee, with View your postup. [M1039]
   - next site states: back (Back), **live@in.none** (View your postup), home@in.none.live (Back to map), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Back to map), projects@in.none (Projects)
   - enterable flows: first-visit--live-already-posted step 6 (if Forgot they're already live at Lot 1), registered-visit--already-posted step 3 (if Forgot they're already live at Lot 1)
7. **live@in.none** · user: Checks on the postup they have · action: taps View your postup · edge: tap: View your postup
   - Their live postup. [M1039]
   - next site states: back (Back), live+share@in.none (Share), post-edit@in.none (Edit), profile@in.none (J Jon On the way · 10 min), live+endlive@in.none (End postup), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), chat@in.none (Group chat), inbox@in.none (Inbox), project@in.none (Star Fox 64 mod), home@in.none.building (Home), projects@in.none (Projects)
   - enterable flows: registered-visit--hosting step 1 (if Live; wants more time), registered-visit--post step 4 (if Managing their postup), registered-visit--hosting-project step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)

## Connected flows [M1025]
- `first-visit--live-already-posted`: branch out at step 2→2, step 4→4, step 5→5, step 6→6; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5), step 6 (from its step 6)
- `first-visit--ended-post`: branch out at step 2→3, step 4→5, step 5→6; merge in at step 2 (from its step 3), step 4 (from its step 5), step 5 (from its step 6)
- `first-visit--link-post`: branch out at step 2→3, step 4→5, step 5→6; merge in at step 2 (from its step 3), step 4 (from its step 5), step 5 (from its step 6)
- `first-visit--live-post`: branch out at step 2→2, step 4→4, step 5→5; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5)
- `first-visit--live-too-far`: branch out at step 2→2, step 4→4, step 5→5; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5)
- `registered-visit--already-posted`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `registered-visit--post`: branch out at step 7→4; merge in at step 7 (from its step 4)
- `host-approve`: branch out at step 7→2; merge in at step 7 (from its step 2)
- `first-visit--nobody`: branch out at step 1→1; merge in at —
- `first-visit--nobody-project`: branch out at step 1→1; merge in at —
- `first-visit--post`: branch out at step 5→5; merge in at —
- `first-visit--too-far`: branch out at step 5→5; merge in at —
- `registered-visit--hosting`: branch out at step 7→1; merge in at —
- `registered-visit--hosting-project`: branch out at step 7→1; merge in at —

## Screens
1. `#home` · auth=out live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin&ph=0#where-search)
6. `#post-already` · auth=in live=none — You're already posted up at Lot 1 Coffee, with View your postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#post-already)
7. `#live` · auth=in live=none — Their live postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#live)

## Success criteria
- One live postup per account; they land on a way to view the one they have. [M1039]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
