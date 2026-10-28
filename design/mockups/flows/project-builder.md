# Flow: Project builder: create, update, post up for it (`project-builder`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: **project-new@in.none** (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox)
   - enterable flows: following step 2 (if Wants to see who they follow)
2. **project-new@in.none** · user: Starts a new project page · action: taps New project · edge: tap: New project
   - Cover, name, kind, one line. [FS] [drawn]
   - next site states: back (Back), **project@in.none** (Create)
   - enterable flows: none
3. **project@in.none** · user: Project exists · action: taps Create · edge: tap: Create
   - New project page. [FS]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), **project-update@in.none** (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: none
4. **project-update@in.none** · user: Sharing progress · action: taps Update · edge: tap: Update
   - Post an update with image. [FS] [R35]
   - next site states: back (Back), project@in.none (Post update)
   - enterable flows: none
5. **project-attach@in.none** · user: Working on it at a cafe · action: taps Post up for this · edge: back, then tap: Post up
   - Post up for this project, now or earlier today. [FS]
   - next site states: back (Back), **posted@in.none** (Post up)
   - enterable flows: none
6. **posted@in.none** · user: Live for the project · action: taps Post up · edge: tap: Post up
   - Posted, tied to the project. [FS]
   - next site states: home@in.none.building (Close), project@in.none (Star Fox 64 mod), posted+share@in.none (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

## Connected flows [M1025]
- `following`: branch out at step 1→2; merge in at step 1 (from its step 2)
- `first-post`: branch out at step 6→6; merge in at step 6 (from its step 6)
- `returning-post`: branch out at step 6→2; merge in at step 6 (from its step 2)

## Screens
1. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
2. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-new)
3. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
4. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-update)
5. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-attach)
6. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)

## Branches and edge cases
- Signed out: Create / Post update open the sign-in sheet, form kept. [FS] [M1018]
- Signed out attach: #attach-signin. [FS]

## Success criteria
- Updates and postups show on the project timeline. [FS] [M1024]

## Needs Martin's decision
- Image storage for projects (Vercel Blob?). [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
