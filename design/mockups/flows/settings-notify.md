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
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

## Success criteria
- Toggles actually change alerts. [M1024]

## Needs Martin's decision
- Email alerts at launch? [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
