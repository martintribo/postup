# Flow: Registered visit → Looks at past postups (`registered-visit--nobody`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--nobody.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=none · device=phone · entry URL `/`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **home@in.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@in.none (cafe), quiet@in.none (Locate), post@in.none (Post up), quiet-feed@in.none (Nearby), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Building), projects@in.none (Projects), **empty-area@in.none** (area has no postups), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: registered-visit--nobody-post step 1 (if Nobody around right now), registered-visit--builds-project step 1 (if Nobody around right now)
2. **empty-area@in.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), **profile@in.none** (Maya posted up at Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none
3. **profile@in.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), project@in.none (Star Fox 64 mod Updated yesterday), home@in.none.building (home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 1 (if Likes someone's work)
4. **empty-area@in.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), profile@in.none (Maya posted up at Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none

## Connected flows [M1025]
- `registered-visit--nobody-post`: branch out at step 1→1; merge in at —
- `registered-visit--builds-project`: branch out at step 1→1; merge in at —
- `following`: branch out at step 3→1; merge in at —

## Screens
1. `#home` · auth=in live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=live&ph=0#home)
2. `#empty-area` · auth=in live=none — Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#empty-area)
3. `#profile` · auth=in live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#profile)
4. `#empty-area` · auth=in live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#empty-area)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
