# Flow: First visit → Posts up at that cafe (`first-visit--link-post`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--link-post.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **invite@out.live** · user: A friend sent this; knows the context · action: opens the share link · edge: entry
   - Landing for the shared postup. [FS] [R39]
   - next site states: invite+signin@out.live (Join Maya), **cafe@out.live** (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: first-visit--link-live step 1 (if A friend sent this; knows the context), first-visit--link-project step 1 (if A friend sent this; knows the context)
2. **cafe@out.live** · user: What's this cafe like? · action: taps Bean Theory · edge: tap: Bean Theory · 0.4 mi
   - The cafe page, with Post up here and the tab bar. [FS] [M1043]
   - next site states: back (Back), cafe+share@out.live (Share), postup@out.live (Join), **post@out.live** (Post up here), home@out.live.live (Home), quiet-feed@out.live (Nearby), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit--ended-not-now step 3 (if Someone's at Bean Theory now), first-visit--link-ended step 3 (if Someone's at Bean Theory now)
3. **post@out.live** · user: Filling in the post · action: taps Post up · edge: tap: Post up here
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.live** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.live (Post up), home@out.live.live (home), quiet-feed@out.live (Nearby), me@out.live (S), inbox@out.live (Inbox), project-new@out.live (Project), projects@out.live (Projects)
   - enterable flows: first-visit--already-posted step 2 (if Filling in the post), first-visit--ended-post step 3 (if Filling in the post), first-visit--live-already-posted step 2 (if Filling in the post), first-visit--live-post step 2 (if Filling in the post), first-visit--live-too-far step 2 (if Filling in the post), first-visit--post step 2 (if Filling in the post), first-visit--too-far step 2 (if Filling in the post)
4. **where@out.live** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.live (Post up), **where-search@out.live** (Search cafes), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project-new@out.live (Project), projects@out.live (Projects)
   - enterable flows: first-visit--ended-post step 4 (if Not at the nearest cafe), first-visit--live-already-posted step 3 (if Not at the nearest cafe), first-visit--live-post step 3 (if Not at the nearest cafe), first-visit--live-too-far step 3 (if Not at the nearest cafe)
5. **where-search@out.live** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.live (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.live** (Post up), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project-new@out.live (Project), projects@out.live (Projects)
   - enterable flows: first-visit--already-posted step 4 (if Looking for the right cafe), first-visit--ended-post step 5 (if Looking for the right cafe), first-visit--live-already-posted step 4 (if Looking for the right cafe), first-visit--live-post step 4 (if Looking for the right cafe), first-visit--live-too-far step 4 (if Looking for the right cafe), first-visit--post step 4 (if Looking for the right cafe), first-visit--too-far step 4 (if Looking for the right cafe)
6. **where-search+signin@out.live** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.live (close), where-search@in.live (Continue with Apple), **posted@in.live** (signs in → continues), post-already@in.live (signs in → continues (you already have a live postup)), post-far@in.live (signs in → continues (the place is too far from you))
   - enterable flows: first-visit--already-posted step 5 (if Ready; asked to sign in), first-visit--ended-post step 6 (if Ready; asked to sign in), first-visit--live-already-posted step 5 (if Ready; asked to sign in), first-visit--live-post step 5 (if Ready; asked to sign in), first-visit--live-too-far step 5 (if Ready; asked to sign in), first-visit--post step 5 (if Ready; asked to sign in), first-visit--too-far step 5 (if Ready; asked to sign in)
7. **posted@in.live** · user: Live; wants company · action: signs in · edge: tap: Continue with Apple
   - Posted; link to copy. [FS]
   - next site states: home@in.live.live (Close), **posted+share@in.live** (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-visit--ended-post step 7 (if Live; wants company), first-visit--live-post step 6 (if Live; wants company), first-visit--post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)
8. **posted+share@in.live** · user: Wants friends to come too · action: taps Invite friends · edge: tap: Invite friends
   - Invite friends: share sheet. [drawn] [M1024]
   - next site states: posted@in.live (close), post-already@in.live (close (you already have a live postup)), post-far@in.live (close (the place is too far from you))
   - enterable flows: none

## Connected flows [M1025]
- `first-visit--post`: branch out at step 3→2, step 5→4, step 6→5, step 7→6; merge in at step 3 (from its step 2), step 5 (from its step 4), step 6 (from its step 5), step 7 (from its step 6)
- `first-visit--already-posted`: branch out at step 3→2, step 5→4, step 6→5; merge in at step 3 (from its step 2), step 5 (from its step 4), step 6 (from its step 5)
- `first-visit--too-far`: branch out at step 3→2, step 5→4, step 6→5; merge in at step 3 (from its step 2), step 5 (from its step 4), step 6 (from its step 5)
- `first-visit--ended-not-now`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `first-visit--link-ended`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `first-visit--live-already-posted`: branch out at step 6→5; merge in at step 3 (from its step 2)
- `first-visit--live-too-far`: branch out at step 6→5; merge in at step 3 (from its step 2)
- `returning-post`: branch out at step 7→2; merge in at step 7 (from its step 2)
- `first-visit--link-live`: branch out at step 1→1; merge in at —
- `first-visit--link-project`: branch out at step 1→1; merge in at —
- `first-visit--ended-post`: branch out at —; merge in at step 3 (from its step 3)
- `first-visit--live-post`: branch out at —; merge in at step 3 (from its step 2)

## Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#invite)
2. `#cafe` · auth=out live=live — The cafe page, with Post up here and the tab bar. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#cafe)
3. `#post` · auth=out live=live — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#post)
4. `#where` · auth=out live=live — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#where)
5. `#where-search` · auth=out live=live — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#where-search)
6. `#where-search` + sheet `signin` · auth=out live=live — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#where-search)
7. `#posted` · auth=in live=live — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#posted)
8. `#posted` + sheet `share` · auth=in live=live — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=share&ph=0#posted)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
