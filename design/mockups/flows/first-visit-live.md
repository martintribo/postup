# Flow: First-time visitor, someone is live (`first-visit-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit-live.html

## Persona
- New visitor, signed out, curious; lands on / with live postups nearby.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand the site and join someone; sign in only at Join. [M1024]

## Steps
1. `#home` · auth=out live=live mode=live — Home opens in Live mode with a one-line welcome. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Opens a postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#join-signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#join-signin)
4. `#joined` · auth=in live=live — Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)

## Branches and edge cases
- Not now on the sheet: stays on the postup, still signed out. [drawn] [M1024]
- Switches to Building to look at projects first. [M1018b] [M1024]

## Success criteria
- No sign-in before an action. [FS]
- After sign-in the original action completes. [M1018] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
