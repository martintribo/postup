# Flow: Share link to a live postup (`invite-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: project@out.live (Star Fox 64 mod), **invite+signin@out.live** (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: none
2. **invite+signin@out.live** · user: Wants to join the friend · action: taps Join 🔒 · edge: tap: Join Maya
   - Join → sign-in sheet. [FS] [M1024]
   - next site states: invite@out.live (close), invite@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
3. **joined@in.live** · user: Signed in; going · action: signs in · edge: tap: Continue with Apple
   - Joined. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **chat@in.live** (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 10 (if Committed; needs to get there), quick-joiner step 3 (if Decides to just join now), leave step 1 (if Plans changed)
4. **chat@in.live** · user: Wants to say hi before going · action: opens chat · edge: tap: Group chat
   - Postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

## Connected flows [M1025]
- `cautious-joiner`: branch out at step 3→10; merge in at step 3 (from its step 10)
- `quick-joiner`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `chat`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `leave`: branch out at step 3→1; merge in at —

## Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite)
2. `#invite` + sheet `signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#chat` · auth=in live=live — Postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

## Branches and edge cases
- Link is to an ask-to-join postup → Ask to join flow. [FS] [M1024]
- Already signed in: Join goes straight to joined. [TK§1] [M1024]

## Success criteria
- The link works without an account until Join. [R39] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
