# Flow: Postup chat (`chat`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/chat.html

## Persona
- Signed-in poster or joiner.

## Starting state
- auth=in · live=live · device=phone · entry URL `/inbox`

## Goal
- Coordinate in the group chat. [M1024]

## Steps
1. `#inbox` · auth=in live=live — Inbox · Chats. [FS] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox)
2. `#chat` · auth=in live=live — One chat per postup. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)
3. `#chat` + sheet `msg` · auth=in live=live — Long-press: copy, report, block sender. [F096] [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=msg#chat)

## Branches and edge cases
- Signed out: sign-in sheet over Inbox. [unsourced]
- Chat closes 24h after the postup. [R31] [FS]

## Success criteria
- Only poster + joined/approved can read. [F061]

## Needs Martin's decision
- Chat retention (24h default). [R31] [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
