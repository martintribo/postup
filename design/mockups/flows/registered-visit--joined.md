# Flow: Registered visit → Leaves the postup (`registered-visit--joined`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--joined.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **joined@in.live** · user: Plans changed · action: opens their joined postup · edge: entry
   - Leave link. [drawn]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), **joined+leave@in.live** (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit step 3 (if Decides to join), registered-visit--joined-chat step 1 (if Plans changed), registered-visit--joined-project step 1 (if Plans changed)
2. **joined+leave@in.live** · user: Backing out politely · action: taps Leave · edge: tap: Leave
   - Confirm; poster alerted. [FS] [drawn]
   - next site states: joined@in.live (close), **postup@in.live** (Leave)
   - enterable flows: none
3. **postup@in.live** · user: Out; back on the postup page · action: confirms Leave · edge: tap: Leave
   - Back on the postup. [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: registered-visit step 2 (if Found someone), registered-visit--cancelled step 2 (if Found someone), registered-visit--ended step 2 (if Found someone), registered-visit--full step 2 (if Found someone), registered-visit--link-ended step 4 (if Could go to this one), registered-visit--report step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)

## Connected flows [M1025]
- `registered-visit`: branch out at step 1→3, step 3→2; merge in at step 1 (from its step 3), step 3 (from its step 2)
- `registered-visit--cancelled`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--ended`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--full`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--link-ended`: branch out at step 3→4; merge in at step 3 (from its step 4)
- `registered-visit--report`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `desktop-browse`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--joined-chat`: branch out at step 1→1; merge in at —
- `registered-visit--joined-project`: branch out at step 1→1; merge in at —

## Screens
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave&ph=1#joined)
3. `#postup` · auth=in live=live — Back on the postup. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#postup)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
