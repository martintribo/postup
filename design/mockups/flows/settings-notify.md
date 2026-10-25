# Flow: Notification settings and sign out (`settings-notify`)
Priority: **nice** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/settings-notify.html

## Persona
- Signed-in user.

## Starting state
- auth=in · live=none · device=phone · entry URL `/settings`

## Goal
- Tune alerts, sign out. [M1024]

## Steps
1. **settings@in.none** · user: Tuning alerts · action: opens Settings · edge: entry
   - Toggles; Sign out. [FS] [F065]
   - next site states: back (Back), **home@out.none.building** (Sign out), settings+delacct@in.none (Delete account)
   - enterable flows: delete-account step 2 (if Looking for the delete option)
2. **home@out.none.building** · user: Done for now · action: taps Sign out · edge: tap: Sign out
   - Signed out. [M1024]
   - next site states: home@out.none.live (Live), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), cafe@out.none (Lantern Tea A D M 3 postups), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@out.none (area has no postups)
   - enterable flows: first-post step 1 (if Came to post up right now)

## Connected flows [M1025]
- `delete-account`: branch out at step 1→2; merge in at step 1 (from its step 2)
- `first-post`: branch out at step 2→1; merge in at —

## Screens
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

## Success criteria
- Toggles actually change alerts. [M1024]

## Needs Martin's decision
- Email alerts at launch? [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
