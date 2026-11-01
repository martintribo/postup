# Flow: First visit → Ended link, browses Nearby (`first-visit--link-ended`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--link-ended.html

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
   - enterable flows: none
2. **quiet-feed@out.live** · user: Who else is around? · action: taps See what's nearby · edge: tap: See what's nearby
   - Nearby list of postups. [FS] [M1041]
   - next site states: me@out.live (S), quiet@out.live (quiet), post@out.live (Post up), cafe@out.live (Maya's photo), home@out.live.live (Home), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Maya's photo (Google card fails))
   - enterable flows: none

## Connected flows [M1025]
- none

## Screens
1. `#invite-ended` · auth=out live=live — This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#invite-ended)
2. `#quiet-feed` · auth=out live=live — Nearby list of postups. [FS] [M1041] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#quiet-feed)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
