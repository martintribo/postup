# Flow: First visit → Browses Nearby (`first-visit--browse`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--browse.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: postup@out.live (M 2), cafe@out.live (cafe), quiet@out.live (Locate), **quiet-feed@out.live** (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), postup-ask@out.live (T), home@out.live.building (Building), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: first-visit step 1 (if Curious what this is; sees people live), first-visit--live-already-posted step 1 (if Curious what this is; sees people live), first-visit--live-post step 1 (if Curious what this is; sees people live), first-visit--live-too-far step 1 (if Curious what this is; sees people live), first-visit--not-now step 1 (if Curious what this is; sees people live), first-visit--follow-project step 1 (if Curious what this is; sees people live)
2. **quiet-feed@out.live** · user: Wants to see everyone around · action: taps Nearby · edge: tap: Nearby
   - Nearby list of postups. [FS] [M1041]
   - next site states: me@out.live (S), quiet@out.live (quiet), post@out.live (Post up), cafe@out.live (Maya's photo), home@out.live.live (Home), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Maya's photo (Google card fails))
   - enterable flows: first-visit--ended-not-now step 2 (if Who else is around?), first-visit--ended-post step 2 (if Who else is around?), first-visit--link-ended step 2 (if Who else is around?), first-visit--ended-project step 2 (if Who else is around?)

## Connected flows [M1025]
- `first-visit--ended-not-now`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `first-visit--ended-post`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `first-visit--link-ended`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `first-visit--ended-project`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `first-visit`: branch out at step 1→1; merge in at —
- `first-visit--live-already-posted`: branch out at step 1→1; merge in at —
- `first-visit--live-post`: branch out at step 1→1; merge in at —
- `first-visit--live-too-far`: branch out at step 1→1; merge in at —
- `first-visit--not-now`: branch out at step 1→1; merge in at —
- `first-visit--follow-project`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live&ph=0#home)
2. `#quiet-feed` · auth=out live=live — Nearby list of postups. [FS] [M1041] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#quiet-feed)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
