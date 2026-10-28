# Flow: Delete account (`delete-account`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/delete-account.html

## Persona
- Signed-in user leaving.

## Starting state
- auth=in · live=none · device=phone · entry URL `/me`

## Goal
- Remove profile, postups and projects. [M1024]

## Steps
1. **me@in.none** · user: Leaving PostUp · action: opens My profile · edge: entry
   - My profile → Settings. [FS]
   - next site states: back (Back), **settings@in.none** (Settings), live@in.none (1:42 You're live at Bean Theory Ti), cafe@in.none (Lantern Tea), project-new@in.none (Tide Clock Updated Sun), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), cafe-gfail@in.none (Lantern Tea (Google card fails))
   - enterable flows: none
2. **settings@in.none** · user: Looking for the delete option · action: taps Settings · edge: tap: Settings
   - Account section. [FS] [F065]
   - next site states: back (Back), home@out.none.building (Sign out), **settings+delacct@in.none** (Delete account), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S)
   - enterable flows: settings-notify step 1 (if Tuning alerts)
3. **settings+delacct@in.none** · user: Sure about it · action: taps Delete account · edge: tap: Delete account
   - Confirm; can't be undone. [FS] [drawn]
   - next site states: settings@in.none (close), **home@out.none.building** (Delete account)
   - enterable flows: none
4. **home@out.none.building** · user: Gone · action: confirms · edge: tap: Delete account
   - Signed out at Home. [M1024]
   - next site states: home@out.none.live (Live), cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: first-post step 1 (if Came to post up right now)

## Connected flows [M1025]
- `settings-notify`: branch out at step 2→1; merge in at —
- `first-post`: branch out at step 4→1; merge in at —

## Screens
1. `#me` · auth=in live=none — My profile → Settings. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#me)
2. `#settings` · auth=in live=none — Account section. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
3. `#settings` + sheet `delacct` · auth=in live=none — Confirm; can't be undone. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=delacct#settings)
4. `#home` · auth=out live=none mode=building — Signed out at Home. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

## Branches and edge cases
- Deleting while live: postup ends and joiners are alerted? [unsourced]

## Success criteria
- All their content gone. [FS]

## Needs Martin's decision
- What happens to a live postup and chats on delete. [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
