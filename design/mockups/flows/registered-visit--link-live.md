# Flow: Registered visit → Joins from a shared link (`registered-visit--link-live`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--link-live.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **invite@in.live** · user: A friend sent this · action: opens the share link · edge: entry
   - Landing for the shared postup; already signed in, so Join is one tap. [FS] [R39]
   - next site states: cafe@in.live (Bean Theory · 0.4 mi), **joined@in.live** (Join Maya), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: registered-visit--link-post step 1 (if A friend sent this), registered-visit--link-project step 1 (if A friend sent this)
2. **joined@in.live** · user: Going · action: taps Join · edge: tap: Join Maya
   - Joined. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit step 3 (if Decides to join), registered-visit--joined step 1 (if Plans changed), registered-visit--joined-chat step 1 (if Plans changed), registered-visit--joined-project step 1 (if Plans changed)

## Connected flows [M1025]
- `registered-visit`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--link-post`: branch out at step 1→1; merge in at —
- `registered-visit--link-project`: branch out at step 1→1; merge in at —
- `registered-visit--joined`: branch out at step 2→1; merge in at —
- `registered-visit--joined-chat`: branch out at step 2→1; merge in at —
- `registered-visit--joined-project`: branch out at step 2→1; merge in at —

## Screens
1. `#invite` · auth=in live=live — Landing for the shared postup; already signed in, so Join is one tap. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#invite)
2. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#joined)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
