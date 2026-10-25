# Flow: Curious browser: live now, then past content (`curious-browser`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/curious-browser.html

## Persona
- First-time visitor, signed out, who has heard of PostUp and wants to see what is on it: who is live and what people have made.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- See live and past content, then follow someone, signing in only at Follow. [M1025]

## Steps
1. `#home` · auth=out live=live mode=live — Live now list: who is working where. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Peeks at a live postup, then Back. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#home` · auth=out live=live mode=building — Switches to Building for past content. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
4. `#projects` · auth=out live=live — See all projects, closest first. [M1018c] [FS] (/mockups/?style=fresh&device=phone&auth=out&live=live#projects)
5. `#project` · auth=out live=live — Opens a project: updates and past postups. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)
6. `#profile` · auth=out live=live — Opens the maker's profile: past postups, regular cafes. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#profile)
7. `#profile` + sheet `signin` · auth=out live=live — Taps Follow: soft sign-in sheet; Not now keeps browsing. [FS] [M1018] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#profile)
8. `#profile` · auth=in live=live — Signed in and following. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)

## Branches and edge cases
- Nobody live: Home opens in Building, so the flow starts at the projects (merged from the old first-visit-none flow). [M1018b] [M1025]
- Taps Post up instead: see Came to post up. [M1025]
- Not now on the sheet: stays signed out, nothing lost. [drawn] [M1025]
- Never empty or "quiet" copy when nothing is live. [F035] [R4]

## Success criteria
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]

## Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
