# Flow: Project builder: create, update, post up for it (`project-builder`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/project-builder.html

## Persona
- Signed-in maker.

## Starting state
- auth=in · live=none · device=phone · entry URL `/projects`

## Goal
- Have a project page that collects updates and postups. [M1024]

## Steps
1. **projects@in.none** · user: Wants a home for their project · action: opens Projects · edge: entry
   - Projects, "+". [FS]
   - next site states: **project-new@in.none** (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S), home@in.none.building (Home)
   - enterable flows: following step 3 (if Wants to see who they follow)
2. **project-new@in.none** · user: Starts a new project page · action: taps New project · edge: tap: New project
   - Cover, name, kind, one line. [FS] [drawn]
   - next site states: back (Back), **project@in.none** (Create), home@in.none.live (home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
3. **project@in.none** · user: Project exists · action: taps Create · edge: tap: Create
   - New project page. [FS]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), **project-update@in.none** (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
4. **project-update@in.none** · user: Sharing progress · action: taps Update · edge: tap: Update
   - Post an update with image. [FS] [R35]
   - next site states: back (Back), **project@in.none** (Post update), home@in.none.live (home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
5. **project@in.none** · user: Update can wait; post up first · action: taps Back · edge: back
   - Back on the project (Update has no Post up link, as in the app). [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), **project-attach@in.none** (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
6. **project-attach@in.none** · user: Working on it at a cafe · action: taps Post up for this · edge: tap: Post up for this
   - Post up for this project, now or earlier today. [FS]
   - next site states: back (Back), **posted@in.none** (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
7. **posted@in.none** · user: Live for the project · action: taps Post up · edge: tap: Post up
   - Posted, tied to the project. [FS]
   - next site states: home@in.none.live (Close), posted+share@in.none (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S), home@in.none.building (Close), project@in.none (Star Fox 64 mod), projects@in.none (Projects), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

## Connected flows [M1025]
- `following`: branch out at step 1→3, step 3→2, step 5→2; merge in at step 1 (from its step 3), step 3 (from its step 2), step 5 (from its step 2)
- `first-post`: branch out at step 7→6; merge in at step 7 (from its step 6)
- `returning-post`: branch out at step 7→2; merge in at step 7 (from its step 2)

## Screens
1. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#projects)
2. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-new)
3. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
4. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-update)
5. `#project` · auth=in live=none — Back on the project (Update has no Post up link, as in the app). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
6. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-attach)
7. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#posted)

## Branches and edge cases
- Signed out: Create / Post update open the sign-in sheet, form kept. [FS] [M1018]
- Signed out attach: #attach-signin. [FS]

## Success criteria
- Updates and postups show on the project timeline. [FS] [M1024]

## Needs Martin's decision
- Image storage for projects (Vercel Blob?). [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
