# Flow: Quick joiner (`quick-joiner`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/quick-joiner.html

## Persona
- Registered user who already knows someone nearby is live.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Join in two taps and get directions. [M1024]

## Steps
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps a row, then Join. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#joined` · auth=in live=live — Confirmation. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)
5. `#chat` · auth=in live=live — Says "on my way" in the postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

## Branches and edge cases
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]

## Success criteria
- Home → joined in 2 taps. [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
