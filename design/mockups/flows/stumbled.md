# Flow: Stumbled on it: what is this? (`stumbled`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/stumbled.html

## Persona
- First-time visitor with no idea what PostUp is; arrived from search, a social post or a word-of-mouth link.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp within the first screen and reach something real before any sign-in. [M1025]

## Steps
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. No explainer line is drawn in Live mode, only the brand. [drawn] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Taps the first live person to see what a postup is. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#cafe` · auth=out live=live — Taps the cafe: who is here now, Post up here. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#cafe)
4. `#home` · auth=out live=live mode=building — Back on Home, flips to Building: the welcome line "Post up at a cafe. See who's working nearby." and "What people are building". [drawn] [M1018c] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
5. `#project` · auth=out live=live — Opens a project and gets the idea; Follow and Post up (🔒) are the next steps. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)

## Branches and edge cases
- Nobody live: Home opens in Building, where the welcome line shows first. [M1018b] [drawn] [M1025]
- Dismisses the welcome (×): it should stay dismissed. [drawn] [unsourced]
- Leaves after the first screen: the value has to be clear without scrolling. [M1025]

## Success criteria
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

## Needs Martin's decision
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
