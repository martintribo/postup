# Flow: Registered visit → Ended link, joins someone nearby (`registered-visit--link-ended`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--link-ended.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **invite-ended@in.live** · user: Too late for this one · action: opens the share link · edge: entry
   - This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032]
   - next site states: **quiet-feed@in.live** (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: registered-visit--ended-post step 1 (if Too late for this one), registered-visit--ended-project step 1 (if Too late for this one)
2. **quiet-feed@in.live** · user: Who else is around? · action: taps See what's nearby · edge: tap: See what's nearby
   - Nearby list of postups. [FS] [M1041]
   - next site states: me@in.live (S), quiet@in.live (quiet), post@in.live (Post up), **cafe@in.live** (Maya's photo), home@in.live.live (Home), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: registered-visit--ended-post step 2 (if Who else is around?), registered-visit--ended-project step 2 (if Who else is around?), loading-offline step 3 (if Back online)
3. **cafe@in.live** · user: Someone's at Bean Theory now · action: taps a live postup's photo · edge: tap: Maya's photo
   - The cafe with who's live there. [FS] [M1043]
   - next site states: back (Back), **postup@in.live** (Join), post@in.live (Post up here), home@in.live.live (Home), quiet-feed@in.live (Nearby), me@in.live (S), cafe+share@in.live (Share), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--link-post step 2 (if What's this cafe like?)
4. **postup@in.live** · user: Could go to this one · action: taps the live postup · edge: tap: Join
   - The live postup. [FS] [M1043]
   - next site states: back (Back), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), postup+share@in.live (Share), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: registered-visit step 2 (if Found someone), registered-visit--cancelled step 2 (if Found someone), registered-visit--ended step 2 (if Found someone), registered-visit--full step 2 (if Found someone), registered-visit--report step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)
5. **joined@in.live** · user: Going to this one instead · action: taps Join · edge: tap: Join
   - You're joining. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit step 3 (if Decides to join), registered-visit--joined step 1 (if Plans changed), registered-visit--joined-chat step 1 (if Plans changed), registered-visit--joined-project step 1 (if Plans changed)

## Connected flows [M1025]
- `loading-offline`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--link-post`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--cancelled`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `registered-visit--ended`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `registered-visit--full`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `registered-visit--report`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `desktop-browse`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `registered-visit`: branch out at step 5→3; merge in at step 4 (from its step 2)
- `registered-visit--ended-post`: branch out at step 2→2; merge in at —
- `registered-visit--ended-project`: branch out at step 2→2; merge in at —
- `registered-visit--joined`: branch out at step 5→1; merge in at —
- `registered-visit--joined-chat`: branch out at step 5→1; merge in at —
- `registered-visit--joined-project`: branch out at step 5→1; merge in at —

## Screens
1. `#invite-ended` · auth=in live=live — This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#invite-ended)
2. `#quiet-feed` · auth=in live=live — Nearby list of postups. [FS] [M1041] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#quiet-feed)
3. `#cafe` · auth=in live=live — The cafe with who's live there. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#cafe)
4. `#postup` · auth=in live=live — The live postup. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#postup)
5. `#joined` · auth=in live=live — You're joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#joined)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
