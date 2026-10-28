# Flow: Empty area: be the first (`empty-area`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area.html

## Persona
- Signed-in user in a city with no postups yet.

## Starting state
- auth=in · live=none · device=phone · entry URL `/`

## Goal
- Seed the area. [M1024]

## Steps
1. **home@in.none.building** · user: Nobody around here yet · action: arrives at / · edge: entry
   - Closest projects even if far. [M1018c]
   - next site states: home@in.none.live (Live), cafe@in.none (Lantern Tea A D M 3 postups), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), **empty-area@in.none** (area has no postups), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
2. **empty-area@in.none** · user: Sees the area is empty · action: opens the empty area · edge: cond: area has no postups
   - "Be the first here". [FS]
   - next site states: cafe@in.none (cafe), me@in.none (S), **post@in.none** (Stories Cafe 0.3 mi), home@in.none.building (Home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none
3. **post@in.none** · user: Will be the first · action: taps Post up · edge: tap: Stories Cafe 0.3 mi
   - Post up. [FS]
   - next site states: back (Back), where@in.none (Bean Theory Nearest · 0.4 mi Chang), project-new@in.none (Project), posted@in.none (Post up), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today), desktop-browse step 3 (if Wants to post too)

## Connected flows [M1025]
- `desktop-browse`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `returning-post`: branch out at step 3→1; merge in at —

## Screens
1. `#home` · auth=in live=none mode=building — Closest projects even if far. [M1018c] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)
2. `#empty-area` · auth=in live=none — "Be the first here". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)
3. `#post` · auth=in live=none — Post up. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#post)

## Success criteria
- Positive copy, never "quiet". [F035] [R4]

## Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
