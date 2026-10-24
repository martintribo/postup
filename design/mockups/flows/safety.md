# Flow: Report and block (`safety`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/safety.html

## Persona
- Signed-in user uncomfortable with someone.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Report and block quickly. [F059] [M1024]

## Steps
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#reported)
4. `#postup` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block#postup)
5. `#settings` · auth=in live=live — Blocked people list to undo. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=live#settings)

## Branches and edge cases
- From a chat message: Message options → Report message. [F096]

## Success criteria
- No safety-tip screens. [F059] [FS]

## Needs Martin's decision
- No ban system yet: who reviews reports? [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
