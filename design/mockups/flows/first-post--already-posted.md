# Flow: Came to post up: first post with sign-in → Already posted up (`first-post--already-posted`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post--already-posted.html

## Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- Go live in about ten seconds. [M1024]

## Steps
1. **home@out.none.live** · user: Came to post up right now · action: arrives at / · edge: entry
   - Taps Post up. [M1018b]
   - next site states: cafe@out.none (cafe), quiet@out.none (Locate), **post@out.none** (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), home@out.none.building (Building), projects@out.none (Projects), empty-area@out.none (area has no postups), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: empty-area-newcomer step 1 (if Nobody around right now), first-post step 1 (if Came to post up right now), first-post--too-far step 1 (if Came to post up right now)
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.none (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-post step 2 (if Filling in the post), first-post--too-far step 2 (if Filling in the post)
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-post step 3 (if Not at the nearest cafe), first-post--too-far step 3 (if Not at the nearest cafe)
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.none** (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: first-post step 4 (if Looking for the right cafe), first-post--too-far step 4 (if Looking for the right cafe)
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), posted@in.none (signs in → continues), **post-already@in.none** (signs in → continues (you already have a live postup)), post-far@in.none (signs in → continues (the place is too far from you))
   - enterable flows: first-post step 5 (if Ready; asked to sign in), first-post--too-far step 5 (if Ready; asked to sign in)
6. **post-already@in.none** · user: Forgot they're already live at Lot 1 · action: signs in · edge: tap: Continue with Apple (you already have a live postup)
   - You're already posted up at Lot 1 Coffee, with View your postup. [M1039]
   - next site states: back (Back), **live@in.none** (View your postup), home@in.none.live (Back to map), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Back to map), projects@in.none (Projects)
   - enterable flows: returning-post--already-posted step 2 (if Forgot they're still live from earlier)
7. **live@in.none** · user: Checks on the postup they have · action: taps View your postup · edge: tap: View your postup
   - Their live postup. [M1039]
   - next site states: back (Back), live+share@in.none (Share), post-edit@in.none (Edit), profile@in.none (J Jon On the way · 10 min), live+endlive@in.none (End postup), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), chat@in.none (Group chat), inbox@in.none (Inbox), project@in.none (Star Fox 64 mod), home@in.none.building (Home), projects@in.none (Projects)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)

## Connected flows [M1025]
- `returning-post--already-posted`: branch out at step 6→2; merge in at step 6 (from its step 2)
- `returning-post`: branch out at step 7→3; merge in at step 7 (from its step 3)
- `host-approve`: branch out at step 7→2; merge in at step 7 (from its step 2)
- `empty-area-newcomer`: branch out at step 1→1; merge in at —
- `first-post`: branch out at step 5→5; merge in at —
- `first-post--too-far`: branch out at step 5→5; merge in at —
- `hosting`: branch out at step 7→1; merge in at —

## Screens
1. `#home` · auth=out live=none mode=live — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin&ph=0#where-search)
6. `#post-already` · auth=in live=none — You're already posted up at Lot 1 Coffee, with View your postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#post-already)
7. `#live` · auth=in live=none — Their live postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#live)

## Success criteria
- One live postup per account; they land on a way to view the one they have. [M1039]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
