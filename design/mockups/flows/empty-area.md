# Flow: Nobody live nearby (signed in) (`empty-area`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area.html

## Persona
- Signed-in user in an area where nobody is live right now.

## Starting state
- auth=in · live=none · device=phone · entry URL `/`

## Goal
- With nobody live nearby, see who posted up here lately, then be the first today. [M1032]

## Steps
1. **home@in.none.building** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home in Building mode: closest projects. [M1018c]
   - next site states: home@in.none.live (Live), cafe@in.none (Lantern Tea A D M 3 postups), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), quiet-feed@in.none (Nearby), inbox-one@in.none (Inbox), **empty-area@in.none** (area has no postups), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails)), inbox@in.none (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none
2. **empty-area@in.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), **profile@in.none** (Maya posted up at Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox-one@in.none (Inbox), cafe-gfail@in.none (cafe (Google card fails)), inbox@in.none (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none
3. **profile@in.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), project@in.none (Star Fox 64 mod Updated yesterday), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox-one@in.none (Inbox), post@in.none (Post up), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails)), inbox@in.none (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: following step 1 (if Likes someone's work)
4. **empty-area@in.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), profile@in.none (Maya posted up at Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox-one@in.none (Inbox), cafe-gfail@in.none (cafe (Google card fails)), inbox@in.none (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none

## Connected flows [M1025]
- `following`: branch out at step 3→1; merge in at —

## Screens
1. `#home` · auth=in live=none mode=building — Home in Building mode: closest projects. [M1018c] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)
2. `#empty-area` · auth=in live=none — Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)
3. `#profile` · auth=in live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
4. `#empty-area` · auth=in live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)

## Branches and edge cases
- No past activity at all in the area: good cafes to be the first. [M1032] [M1034]

## Success criteria
- Never an empty or "quiet" screen: recent postups and projects nearby are shown. [F035] [R4] [M1032]

## Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
