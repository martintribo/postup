# Flow: Join someone live → Postup full (`join--full`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/join--full.html

## Persona
- Registered user, signed in, who wants company now.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Join a live postup and get there; checking the person first is optional. [M1024] [M1032]

## Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), join--cancelled step 1 (if Wants company now), join--ended step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Found someone · action: taps a live row · edge: tap: M 2
   - Who, project, cafe, who else is joining. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone), join--cancelled step 2 (if Found someone), join--ended step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)
3. **postup-full@in.live** · user: No room left · action: waits while reading · edge: event: postup fills
   - Full state replaces Join. [FS] [M1040]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none

## Connected flows [M1025]
- `catch-up`: branch out at step 1→1; merge in at —
- `join`: branch out at step 2→2; merge in at —
- `join--cancelled`: branch out at step 2→2; merge in at —
- `join--ended`: branch out at step 2→2; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=1#home)
2. `#postup` · auth=in live=live — Who, project, cafe, who else is joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#postup)
3. `#postup-full` · auth=in live=live — Full state replaces Join. [FS] [M1040] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#postup-full)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
