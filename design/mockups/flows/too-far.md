# Flow: Post up from too far away (`too-far`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/too-far.html

## Persona
- Signed-in user who isn't at the cafe they pick.

## Starting state
- auth=in · live=none · device=phone · entry URL `/`

## Goal
- Try to post up at a far-away cafe and get sent back to pick a nearby one. [M1039]

## Steps
1. **post@in.none** · user: Wants to post at Stories Cafe · action: opens Post up · edge: entry
   - Post up form. [FS]
   - next site states: back (Back), where@in.none (Bean Theory Nearest · 0.4 mi Chang), posted@in.none (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), me@in.none (S), inbox@in.none (Inbox), project-new@in.none (Project), home@in.none.building (home), projects@in.none (Projects), post-already@in.none (Post up (you already have a live postup)), **post-far@in.none** (Post up (the place is too far from you))
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today), desktop-browse step 3 (if Wants to post too)
2. **post-far@in.none** · user: The cafe is 2 mi away · action: taps Post up · edge: tap: Post up (Google card fails)
   - You're too far away: you can only post up where you are. [M1039]
   - next site states: back (Back), **where@in.none** (Pick a cafe near you), home@in.none.live (Back to map), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Back to map), projects@in.none (Projects), post-already@in.none (Post up (you already have a live postup))
   - enterable flows: none
3. **where@in.none** · user: Picks the cafe they're actually at · action: taps Pick a cafe near you · edge: tap: Pick a cafe near you
   - Where are you? list, nearest first. [FS] [M1039]
   - next site states: back (Back), where-search@in.none (Search cafes), posted@in.none (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), project-new@in.none (Project), home@in.none.building (home), projects@in.none (Projects), post-already@in.none (Post up (you already have a live postup)), post-far@in.none (Post up (the place is too far from you))
   - enterable flows: none

## Connected flows [M1025]
- `desktop-browse`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `returning-post`: branch out at step 1→1; merge in at —

## Screens
1. `#post` · auth=in live=none — Post up form. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#post)
2. `#post-far` · auth=in live=none — You're too far away: you can only post up where you are. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#post-far)
3. `#where` · auth=in live=none — Where are you? list, nearest first. [FS] [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#where)

## Branches and edge cases
- The check is best effort in the browser: location can be denied or faked. Denied location blocks posting with the same message. [M1039]

## Success criteria
- A friend can't post up as being somewhere they're not, at least without effort. [M1039]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
