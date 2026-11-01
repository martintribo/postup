# Flow: First visit → Too far away (`first-visit--live-too-far`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--live-too-far.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: postup@out.live (M 2), cafe@out.live (cafe), quiet@out.live (Locate), quiet-feed@out.live (Nearby), **post@out.live** (Post up), me@out.live (S), inbox@out.live (Inbox), postup-ask@out.live (T), home@out.live.building (Building), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: first-visit step 1 (if Curious what this is; sees people live), first-visit--browse step 1 (if Curious what this is; sees people live), first-visit--live-already-posted step 1 (if Curious what this is; sees people live), first-visit--live-post step 1 (if Curious what this is; sees people live), first-visit--not-now step 1 (if Curious what this is; sees people live), first-visit--follow-project step 1 (if Curious what this is; sees people live)
2. **post@out.live** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.live** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.live (Post up), home@out.live.live (home), quiet-feed@out.live (Nearby), me@out.live (S), inbox@out.live (Inbox), project-new@out.live (Project), projects@out.live (Projects)
   - enterable flows: first-visit--already-posted step 2 (if Filling in the post), first-visit--ended-post step 3 (if Filling in the post), first-visit--link-post step 3 (if Filling in the post), first-visit--live-already-posted step 2 (if Filling in the post), first-visit--live-post step 2 (if Filling in the post), first-visit--post step 2 (if Filling in the post), first-visit--too-far step 2 (if Filling in the post)
3. **where@out.live** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.live (Post up), **where-search@out.live** (Search cafes), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project-new@out.live (Project), projects@out.live (Projects)
   - enterable flows: first-visit--ended-post step 4 (if Not at the nearest cafe), first-visit--link-post step 4 (if Not at the nearest cafe), first-visit--live-already-posted step 3 (if Not at the nearest cafe), first-visit--live-post step 3 (if Not at the nearest cafe)
4. **where-search@out.live** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.live (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.live** (Post up), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project-new@out.live (Project), projects@out.live (Projects)
   - enterable flows: first-visit--already-posted step 4 (if Looking for the right cafe), first-visit--ended-post step 5 (if Looking for the right cafe), first-visit--link-post step 5 (if Looking for the right cafe), first-visit--live-already-posted step 4 (if Looking for the right cafe), first-visit--live-post step 4 (if Looking for the right cafe), first-visit--post step 4 (if Looking for the right cafe), first-visit--too-far step 4 (if Looking for the right cafe)
5. **where-search+signin@out.live** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.live (close), where-search@in.live (Continue with Apple), posted@in.live (signs in → continues), post-already@in.live (signs in → continues (you already have a live postup)), **post-far@in.live** (signs in → continues (the place is too far from you))
   - enterable flows: first-visit--already-posted step 5 (if Ready; asked to sign in), first-visit--ended-post step 6 (if Ready; asked to sign in), first-visit--link-post step 6 (if Ready; asked to sign in), first-visit--live-already-posted step 5 (if Ready; asked to sign in), first-visit--live-post step 5 (if Ready; asked to sign in), first-visit--post step 5 (if Ready; asked to sign in), first-visit--too-far step 5 (if Ready; asked to sign in)
6. **post-far@in.live** · user: The cafe they picked is 2 mi away · action: posts · edge: tap: Continue with Apple (the place is too far from you)
   - You're too far away: you can only post up where you are. Best effort in the browser. [M1039]
   - next site states: back (Back), **where@in.live** (Pick a cafe near you), home@in.live.live (Back to map), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: first-visit--too-far step 6 (if The cafe they picked is 2 mi away), registered-visit--too-far step 3 (if The cafe they picked is 2 mi away)
7. **where@in.live** · user: Picks the cafe they're actually at · action: taps Pick a cafe near you · edge: tap: Pick a cafe near you
   - Where are you? list, nearest first. [FS] [M1039]
   - next site states: back (Back), where-search@in.live (Search cafes), posted@in.live (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), post-already@in.live (Post up (you already have a live postup)), post-far@in.live (Post up (the place is too far from you))
   - enterable flows: none

## Connected flows [M1025]
- `first-visit--too-far`: branch out at step 2→2, step 4→4, step 5→5, step 6→6; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5), step 6 (from its step 6)
- `first-visit--already-posted`: branch out at step 2→2, step 4→4, step 5→5; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5)
- `first-visit--post`: branch out at step 2→2, step 4→4, step 5→5; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5)
- `first-visit--ended-post`: branch out at step 5→6; merge in at step 2 (from its step 3)
- `first-visit--link-post`: branch out at step 5→6; merge in at step 2 (from its step 3)
- `first-visit`: branch out at step 1→1; merge in at —
- `first-visit--browse`: branch out at step 1→1; merge in at —
- `first-visit--not-now`: branch out at step 1→1; merge in at —
- `first-visit--follow-project`: branch out at step 1→1; merge in at —
- `first-visit--live-already-posted`: branch out at step 5→5; merge in at —
- `first-visit--live-post`: branch out at step 5→5; merge in at —
- `registered-visit--too-far`: branch out at —; merge in at step 6 (from its step 3)

## Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live&ph=0#home)
2. `#post` · auth=out live=live — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#post)
3. `#where` · auth=out live=live — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#where)
4. `#where-search` · auth=out live=live — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#where-search)
5. `#where-search` + sheet `signin` · auth=out live=live — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#where-search)
6. `#post-far` · auth=in live=live — You're too far away: you can only post up where you are. Best effort in the browser. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#post-far)
7. `#where` · auth=in live=live — Where are you? list, nearest first. [FS] [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#where)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
