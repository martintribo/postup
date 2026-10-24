# Flow: Slow network and offline (`loading-offline`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/loading-offline.html

## Persona
- Anyone on bad wifi.

## Starting state
- auth=in · live=live · device=phone · entry URL `/nearby`

## Goal
- Keep showing something useful. [M1024]

## Steps
1. `#loading` · auth=in live=live — Skeleton. [FS] [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#loading)
2. `#offline` · auth=in live=live — Cached feed + offline banner + Retry. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#offline)
3. `#quiet-feed` · auth=in live=live — Retry succeeds. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#quiet-feed)
4. `#cafe-gfail` · auth=in live=live — Google card failed: rest of cafe still works. [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe-gfail)

## Branches and edge cases
- First visit while offline: nothing cached (fails in the build today). [unsourced]

## Success criteria
- No blank screens. [FS]

## Needs Martin's decision
- Full offline screen vs banner only. [R46⚠] [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
