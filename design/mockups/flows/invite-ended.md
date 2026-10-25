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
   - "This postup ended" + what's around. [FS] [R39]
   - next site states: quiet-feed@out.none (See what's nearby)
   - enterable flows: none
2. **profile+signin@out.none** · user: Wants to catch the next one · action: taps Follow 🔒 · edge: gap
   - Follow the poster → sign-in sheet. [FS] [M1024]
   - next site states: profile@out.none (close), profile@in.none (signs in)
   - enterable flows: curious-browser step 7 (if Wants to keep up with them)
3. **home@in.none.building** · user: Signed in; looks around · action: signs in, continues to Home · edge: gap
   - Continues to Home. [M1018b] [M1024]
   - next site states: home@in.none.live (Live), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), cafe@in.none (Lantern Tea A D M 3 postups), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@in.none (area has no postups)
   - enterable flows: empty-area step 1 (if Nobody around here yet)

## Connected flows [M1025]
- `curious-browser`: branch out at step 2→7; merge in at step 2 (from its step 7)
- `empty-area`: branch out at step 3→1; merge in at —

## Screens
1. `#invite-ended` · auth=out live=none — "This postup ended" + what's around. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=none#invite-ended)
2. `#profile` + sheet `signin` · auth=out live=none — Follow the poster → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#profile)
3. `#home` · auth=in live=none mode=building — Continues to Home. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

## Branches and edge cases
- Cancelled instead of ended: #postup-cancelled copy. [F060] [M1024]

## Success criteria
- No 404, a next step is always offered. [F060] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
