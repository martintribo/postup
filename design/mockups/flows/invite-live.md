# Flow: Share link to a live postup (`invite-live`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-live.html

## Persona
- Friend of a poster, signed out, opened postup.now/p/… from a message.

## Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Join the friend who shared the link. [M1024]

## Steps
1. **invite@out.live** · user: A friend sent this; knows the context · action: opens the share link · edge: entry
   - Landing for the shared postup. [FS] [R39]
   - next site states: **invite+signin@out.live** (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: none
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
- `leave`: branch out at step 3→1; merge in at —

## Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#invite)
2. `#invite` + sheet `signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#invite)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)

## Branches and edge cases
- Phase 0: ends at Joined; no chat step (chat is phase 1, see the Chat flow). [M1037]
- The postup has ended by the time the link is opened: lands on `#invite-ended` (This postup ended; See what's nearby, Follow Maya for next time, Go to Home). Was its own flow. [M1032]
- Link is to an ask-to-join postup → Ask to join flow. [FS] [M1024]
- Already signed in: Join goes straight to joined. [TK§1] [M1024]

## Success criteria
- The link works without an account until Join. [R39] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
