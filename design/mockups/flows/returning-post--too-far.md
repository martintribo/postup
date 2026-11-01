# Flow: Returning poster → Too far away (`returning-post--too-far`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/returning-post--too-far.html

## Persona
- Signed-in regular.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Post up with defaults, then see you're live. [M1024]

## Steps
1. **post@in.live** · user: Regular; working at a cafe today · action: taps Post up · edge: entry
   - Last project and nearest cafe preselected; no 🔒. [FS] [M1024]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), posted@in.live (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), post-already@in.live (Post up (you already have a live postup)), **post-far@in.live** (Post up (the place is too far from you))
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today), returning-post--already-posted step 1 (if Regular; working at a cafe today), desktop-browse step 3 (if Wants to post too)
2. **post-far@in.live** · user: Picked the cafe from yesterday by habit · action: taps Post up · edge: tap: Post up (the place is too far from you)
   - You're too far away. [M1039]
   - next site states: back (Back), **where@in.live** (Pick a cafe near you), home@in.live.live (Back to map), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: first-post--too-far step 6 (if The cafe they picked is 2 mi away)
3. **where@in.live** · user: Picks today's cafe · action: taps Pick a cafe near you · edge: tap: Pick a cafe near you
   - Where are you? list, nearest first. [FS] [M1039]
   - next site states: back (Back), where-search@in.live (Search cafes), posted@in.live (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), post-already@in.live (Post up (you already have a live postup)), post-far@in.live (Post up (the place is too far from you))
   - enterable flows: none

## Connected flows [M1025]
- `desktop-browse`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `first-post--too-far`: branch out at step 2→6; merge in at step 2 (from its step 6)
- `returning-post`: branch out at step 1→1; merge in at —
- `returning-post--already-posted`: branch out at step 1→1; merge in at —

## Screens
1. `#post` · auth=in live=live — Last project and nearest cafe preselected; no 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post)
2. `#post-far` · auth=in live=live — You're too far away. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post-far)
3. `#where` · auth=in live=live — Where are you? list, nearest first. [FS] [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#where)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
