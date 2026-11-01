# Flow: First visit → Ended link, leaves without signing in (`first-visit--ended-not-now`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--ended-not-now.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **invite-ended@out.live** · user: Too late for this one · action: opens the share link · edge: entry
   - This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032]
   - next site states: **quiet-feed@out.live** (See what's nearby), invite-ended+signin@out.live (Follow Maya for next time), home@out.live.live (Go to Home), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), projects@out.live (Projects)
   - enterable flows: first-visit--ended-post step 1 (if Too late for this one), first-visit--link-ended step 1 (if Too late for this one), first-visit--ended-project step 1 (if Too late for this one)
2. **quiet-feed@out.live** · user: Who else is around? · action: taps See what's nearby · edge: tap: See what's nearby
   - Nearby list of postups. [FS] [M1041]
   - next site states: me@out.live (S), quiet@out.live (quiet), post@out.live (Post up), **cafe@out.live** (Maya's photo), home@out.live.live (Home), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Maya's photo (Google card fails))
   - enterable flows: first-visit--ended-post step 2 (if Who else is around?), first-visit--link-ended step 2 (if Who else is around?), first-visit--ended-project step 2 (if Who else is around?)
3. **cafe@out.live** · user: Someone's at Bean Theory now · action: taps a live postup's photo · edge: tap: Maya's photo
   - The cafe with who's live there. [FS] [M1043]
   - next site states: back (Back), **postup@out.live** (Join), post@out.live (Post up here), home@out.live.live (Home), quiet-feed@out.live (Nearby), me@out.live (S), cafe+share@out.live (Share), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit--link-ended step 3 (if Someone's at Bean Theory now), first-visit--link-post step 2 (if What's this cafe like?)
4. **postup@out.live** · user: Could go to this one · action: taps the live postup · edge: tap: Join
   - The live postup. [FS] [M1043]
   - next site states: back (Back), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **postup+signin@out.live** (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), postup+share@out.live (Share), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit step 2 (if What is she doing?), first-visit--link-ended step 4 (if Could go to this one), first-visit--not-now step 2 (if What is she doing?)
5. **postup+signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: **postup@out.live** (close), postup@in.live (Continue with Apple), joined@in.live (signs in → continues)
   - enterable flows: first-visit step 5 (if Wants to join; asked to sign in), first-visit--link-ended step 5 (if Wants to join; asked to sign in), first-visit--not-now step 5 (if Wants to join; asked to sign in)
6. **postup@out.live** · user: Was only going for the friend · action: taps Not now · edge: tap: Not now
   - Back on the postup, still signed out. [drawn] [M1043]
   - next site states: back (Back), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), postup+signin@out.live (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), postup+share@out.live (Share), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit step 2 (if What is she doing?), first-visit--link-ended step 4 (if Could go to this one), first-visit--not-now step 2 (if What is she doing?)

## Connected flows [M1025]
- `first-visit`: branch out at step 4→2, step 5→5, step 6→2; merge in at step 4 (from its step 2), step 6 (from its step 2)
- `first-visit--not-now`: branch out at step 4→2, step 6→2; merge in at step 4 (from its step 2), step 6 (from its step 2)
- `first-visit--link-ended`: branch out at step 5→5, step 6→4; merge in at step 6 (from its step 4)
- `first-visit--link-post`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `first-visit--ended-post`: branch out at step 2→2; merge in at —
- `first-visit--ended-project`: branch out at step 2→2; merge in at —

## Screens
1. `#invite-ended` · auth=out live=live — This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#invite-ended)
2. `#quiet-feed` · auth=out live=live — Nearby list of postups. [FS] [M1041] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#quiet-feed)
3. `#cafe` · auth=out live=live — The cafe with who's live there. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#cafe)
4. `#postup` · auth=out live=live — The live postup. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#postup)
5. `#postup` + sheet `signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=1#postup)
6. `#postup` · auth=out live=live — Back on the postup, still signed out. [drawn] [M1043] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#postup)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
