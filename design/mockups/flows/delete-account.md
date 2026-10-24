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
