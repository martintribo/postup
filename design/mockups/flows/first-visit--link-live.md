# Flow: First visit → Joined from a shared link (`first-visit--link-live`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--link-live.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **invite@out.live** · user: A friend sent this; knows the context · action: opens the share link · edge: entry
   - Landing for the shared postup. [FS] [R39]
   - next site states: **invite+signin@out.live** (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: first-visit--link-post step 1 (if A friend sent this; knows the context), first-visit--link-project step 1 (if A friend sent this; knows the context)
2. **invite+signin@out.live** · user: Wants to join the friend · action: taps Join 🔒 · edge: tap: Join Maya
   - Join → sign-in sheet. [FS] [M1024]
   - next site states: invite@out.live (close), invite@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
3. **joined@in.live** · user: Signed in; going · action: signs in · edge: tap: Continue with Apple
   - Joined. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), leave step 1 (if Plans changed)

## Connected flows [M1025]
- `join`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `first-visit--link-post`: branch out at step 1→1; merge in at —
- `first-visit--link-project`: branch out at step 1→1; merge in at —
- `leave`: branch out at step 3→1; merge in at —

## Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#invite)
2. `#invite` + sheet `signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#invite)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
