# Flow: Follow a person or project (`following`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/following.html

## Persona
- Signed-in user who liked someone's work.

## Starting state
- auth=in · live=none · device=phone · entry URL `/u/maya`

## Goal
- Hear when they post up next. [M1024]

## Steps
1. `#profile` · auth=in live=none — Follow → Following. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
2. `#projects` · auth=in live=none — Projects → Following filter. [FS] [R32] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
3. `#activity` · auth=in live=live — Later: "Maya posted up" alert. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
4. `#postup` · auth=in live=live — Opens and joins. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

## Branches and edge cases
- Signed out: Follow → sign-in sheet. [FS]

## Success criteria
- Follow alerts arrive. [M1024]

## Needs Martin's decision
- Alert for "people you follow post up" is saved but not sent yet in the build. [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
