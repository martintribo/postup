# Flow: Registered visit → Starts a project (`registered-visit--builds-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--builds-project.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=none · device=phone · entry URL `/`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **home@in.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@in.none (cafe), quiet@in.none (Locate), post@in.none (Post up), quiet-feed@in.none (Nearby), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Building), **projects@in.none** (Projects), empty-area@in.none (area has no postups), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: registered-visit--nobody step 1 (if Nobody around right now), registered-visit--nobody-post step 1 (if Nobody around right now)
2. **projects@in.none** · user: Wants a home for their project · action: opens Projects · edge: tap: Projects
   - Projects, "+". [FS]
   - next site states: **project-new@in.none** (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home)
   - enterable flows: following step 3 (if Wants to see who they follow)
3. **project-new@in.none** · user: Starts a new project page · action: taps New project · edge: tap: New project
   - Cover, name, kind, one line. [FS] [drawn]
   - next site states: back (Back), **project@in.none** (Create), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
4. **project@in.none** · user: Project exists · action: taps Create · edge: tap: Create
   - New project page. [FS]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), **project-update@in.none** (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
5. **project-update@in.none** · user: Sharing progress · action: taps Update · edge: tap: Update
   - Post an update with image. [FS] [R35]
   - next site states: back (Back), **project@in.none** (Post update), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
6. **project@in.none** · user: Update can wait; post up first · action: taps Back · edge: back
   - Back on the project (Update has no Post up link, as in the app). [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), **project-attach@in.none** (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
7. **project-attach@in.none** · user: Working on it at a cafe · action: taps Post up for this · edge: tap: Post up for this
   - Post up for this project, now or earlier today. [FS]
   - next site states: back (Back), **posted@in.none** (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (home), projects@in.none (Projects), post-already@in.none (Post up (you already have a live postup)), post-far@in.none (Post up (the place is too far from you))
   - enterable flows: none
8. **posted@in.none** · user: Live for the project · action: taps Post up · edge: tap: Post up
   - Posted, tied to the project. [FS]
   - next site states: home@in.none.live (Close), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), posted+share@in.none (Invite friends), inbox@in.none (Inbox), home@in.none.building (Close), project@in.none (Star Fox 64 mod), projects@in.none (Projects), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: registered-visit--post step 3 (if Live)

## Connected flows [M1025]
- `following`: branch out at step 2→3, step 4→2, step 6→2; merge in at step 2 (from its step 3), step 4 (from its step 2), step 6 (from its step 2)
- `registered-visit--post`: branch out at step 8→3; merge in at step 8 (from its step 3)
- `registered-visit--nobody`: branch out at step 1→1; merge in at —
- `registered-visit--nobody-post`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=in live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=live&ph=2#home)
2. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#projects)
3. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-new)
4. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
5. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-update)
6. `#project` · auth=in live=none — Back on the project (Update has no Post up link, as in the app). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
7. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-attach)
8. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#posted)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
