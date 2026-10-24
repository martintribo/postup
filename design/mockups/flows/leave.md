# Flow: Leave a postup you joined (`leave`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/leave.html

## Persona
- Signed-in joiner whose plans changed.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Back out politely. [M1024]

## Steps
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave#joined)
3. `#home` · auth=in live=live mode=live — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)

## Branches and edge cases
- The poster ended or cancelled first: #postup-cancelled. [F060]

## Success criteria
- Poster knows. [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
