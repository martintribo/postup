# Flow: Share link to an ended postup (`invite-ended`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-ended.html

## Persona
- Signed-out visitor opening an old link.

## Starting state
- auth=out · live=none · device=phone · entry URL `/p/7xk2 (ended)`

## Goal
- Not hit a dead end: see what's around and follow the poster. [M1024]

## Steps
1. **invite-ended@out.none** · user: Arrived too late · action: opens an old share link · edge: entry
   - "This postup ended" + See what's nearby, Follow Maya for next time, Go to Home. [FS] [R39] [M1025]
   - next site states: quiet-feed@out.none (See what's nearby), **invite-ended+signin@out.none** (Follow Maya for next time), home@out.none.building (Go to Home)
   - enterable flows: none
2. **invite-ended+signin@out.none** · user: Wants to catch the next one · action: taps Follow Maya for next time 🔒 · edge: sheet: Follow Maya for next time
   - Follow → sign-in sheet. [FS] [M1025]
   - next site states: invite-ended@out.none (close), **invite-ended@in.none** (signs in)
   - enterable flows: none
3. **invite-ended@in.none** · user: Following Maya now · action: signs in · edge: sign-in: signs in
   - Back on the page, signed in; Follow shows Following. [M1018] [M1025]
   - next site states: quiet-feed@in.none (See what's nearby), **home@in.none.building** (Go to Home)
   - enterable flows: none
4. **home@in.none.building** · user: Signed in; looks around · action: taps Go to Home · edge: tap: Go to Home
   - Home in Building mode. [M1018b] [M1025]
   - next site states: home@in.none.live (Live), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), cafe@in.none (Lantern Tea A D M 3 postups), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@in.none (area has no postups)
   - enterable flows: empty-area step 1 (if Nobody around here yet)

## Connected flows [M1025]
- `empty-area`: branch out at step 4→1; merge in at —

## Screens
1. `#invite-ended` · auth=out live=none — "This postup ended" + See what's nearby, Follow Maya for next time, Go to Home. [FS] [R39] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=none#invite-ended)
2. `#invite-ended` + sheet `signin` · auth=out live=none — Follow → sign-in sheet. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#invite-ended)
3. `#invite-ended` · auth=in live=none — Back on the page, signed in; Follow shows Following. [M1018] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=none#invite-ended)
4. `#home` · auth=in live=none mode=building — Home in Building mode. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

## Branches and edge cases
- Cancelled instead of ended: #postup-cancelled copy. [F060] [M1024]

## Success criteria
- No 404, a next step is always offered. [F060] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
