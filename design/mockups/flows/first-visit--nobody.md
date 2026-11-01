# Flow: First visit → Looks at past postups (`first-visit--nobody`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--nobody.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@out.none (cafe), quiet@out.none (Locate), post@out.none (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), home@out.none.building (Building), projects@out.none (Projects), **empty-area@out.none** (area has no postups), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: first-visit--already-posted step 1 (if Nobody around right now), first-visit--post step 1 (if Nobody around right now), first-visit--too-far step 1 (if Nobody around right now)
2. **empty-area@out.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032]
   - next site states: cafe@out.none (cafe), me@out.none (S), post@out.none (Stories Cafe 0.3 mi), **profile@out.none** (Maya posted up at Bean Theory), home@out.none.live (Home), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.building (Home), projects@out.none (Projects), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: none
3. **profile@out.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@out.none (More), profile+signin@out.none (Follow), cafe@out.none (Bean Theory), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project@out.none (Star Fox 64 mod Updated yesterday), home@out.none.building (home), projects@out.none (Projects), cafe-gfail@out.none (Bean Theory (Google card fails))
   - enterable flows: none
4. **empty-area@out.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@out.none (cafe), me@out.none (S), post@out.none (Stories Cafe 0.3 mi), profile@out.none (Maya posted up at Bean Theory), home@out.none.live (Home), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.building (Home), projects@out.none (Projects), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: none

## Connected flows [M1025]
- `first-visit--already-posted`: branch out at step 1→1; merge in at —
- `first-visit--post`: branch out at step 1→1; merge in at —
- `first-visit--too-far`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=out live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#empty-area` · auth=out live=none — Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#empty-area)
3. `#profile` · auth=out live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#profile)
4. `#empty-area` · auth=out live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#empty-area)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
