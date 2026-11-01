# Flow: Notification settings and sign out (`settings-notify`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), home@out.none.live (Sign out), settings+delacct@in.none (Delete account), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), **home@out.none.building** (Sign out), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: delete-account step 2 (if Looking for the delete option)
2. **home@out.none.building** · user: Done for now · action: taps Sign out · edge: tap: Sign out
   - Signed out. [M1024]
   - next site states: cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.live (Live), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none

## Connected flows [M1025]
- `delete-account`: branch out at step 1→2; merge in at step 1 (from its step 2)

## Screens
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building&ph=2#home)

## Success criteria
- Toggles actually change alerts. [M1024]

## Needs Martin's decision
- Email alerts at launch? [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
