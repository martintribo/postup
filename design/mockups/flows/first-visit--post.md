# Flow: First visit → Posted up (`first-visit--post`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--post.html

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
   - enterable flows: first-visit--already-posted step 1 (if Nobody around right now), first-visit--nobody step 1 (if Nobody around right now), first-visit--too-far step 1 (if Nobody around right now), first-visit--nobody-project step 1 (if Nobody around right now)
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.none (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--already-posted step 2 (if Filling in the post), first-visit--ended-post step 3 (if Filling in the post), first-visit--link-post step 3 (if Filling in the post), first-visit--live-already-posted step 2 (if Filling in the post), first-visit--live-post step 2 (if Filling in the post), first-visit--live-too-far step 2 (if Filling in the post), first-visit--too-far step 2 (if Filling in the post)
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--already-posted step 3 (if Not at the nearest cafe), first-visit--too-far step 3 (if Not at the nearest cafe)
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.none** (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-visit--already-posted step 4 (if Looking for the right cafe), first-visit--ended-post step 5 (if Looking for the right cafe), first-visit--link-post step 5 (if Looking for the right cafe), first-visit--live-already-posted step 4 (if Looking for the right cafe), first-visit--live-post step 4 (if Looking for the right cafe), first-visit--live-too-far step 4 (if Looking for the right cafe), first-visit--too-far step 4 (if Looking for the right cafe)
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), **posted@in.none** (signs in → continues), post-already@in.none (signs in → continues (you already have a live postup)), post-far@in.none (signs in → continues (the place is too far from you))
   - enterable flows: first-visit--already-posted step 5 (if Ready; asked to sign in), first-visit--ended-post step 6 (if Ready; asked to sign in), first-visit--link-post step 6 (if Ready; asked to sign in), first-visit--live-already-posted step 5 (if Ready; asked to sign in), first-visit--live-post step 5 (if Ready; asked to sign in), first-visit--live-too-far step 5 (if Ready; asked to sign in), first-visit--too-far step 5 (if Ready; asked to sign in)
6. **posted@in.none** · user: Live; wants company · action: signs in · edge: tap: Continue with Apple
   - Posted; link to copy. [FS]
   - next site states: home@in.none.live (Close), **posted+share@in.none** (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Close), project@in.none (Star Fox 64 mod), projects@in.none (Projects), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-visit--ended-post step 7 (if Live; wants company), first-visit--link-post step 7 (if Live; wants company), first-visit--live-post step 6 (if Live; wants company), registered-visit--post step 3 (if Live)
7. **posted+share@in.none** · user: Wants friends to come too · action: taps Invite friends · edge: tap: Invite friends
   - Invite friends: share sheet. [drawn] [M1024]
   - next site states: posted@in.none (close), post-already@in.none (close (you already have a live postup)), post-far@in.none (close (the place is too far from you))
   - enterable flows: none

## Connected flows [M1025]
- `first-visit--ended-post`: branch out at step 2→3, step 4→5, step 5→6, step 6→7; merge in at step 2 (from its step 3), step 4 (from its step 5), step 5 (from its step 6), step 6 (from its step 7)
- `first-visit--link-post`: branch out at step 2→3, step 4→5, step 5→6, step 6→7; merge in at step 2 (from its step 3), step 4 (from its step 5), step 5 (from its step 6), step 6 (from its step 7)
- `first-visit--live-post`: branch out at step 2→2, step 4→4, step 5→5, step 6→6; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5), step 6 (from its step 6)
- `first-visit--live-already-posted`: branch out at step 2→2, step 4→4, step 5→5; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5)
- `first-visit--live-too-far`: branch out at step 2→2, step 4→4, step 5→5; merge in at step 2 (from its step 2), step 4 (from its step 4), step 5 (from its step 5)
- `registered-visit--post`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `first-visit--nobody`: branch out at step 1→1; merge in at —
- `first-visit--nobody-project`: branch out at step 1→1; merge in at —
- `first-visit--already-posted`: branch out at step 5→5; merge in at —
- `first-visit--too-far`: branch out at step 5→5; merge in at —

## Screens
1. `#home` · auth=out live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin&ph=0#where-search)
6. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#posted)
7. `#posted` + sheet `share` · auth=in live=none — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=share&ph=0#posted)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
