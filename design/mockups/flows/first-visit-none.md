# Flow: First-time visitor, nobody live (`first-visit-none`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit-none.html

## Persona
- New visitor, signed out, early launch: nobody live nearby.

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- See that people build things at cafes, and post up first. [M1024]

## Steps
1. `#home` · auth=out live=none mode=building — Home opens in Building: "What people are building", closest first. [M1018b] [M1018c] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#projects` · auth=out live=none — See all projects. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none#projects)
3. `#project` · auth=out live=none — Opens a project; Follow / Post up show 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none#project)
4. `#post` · auth=out live=none — Taps Post up. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none#post)
5. `#post-signin` · auth=out live=none — Post up 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none#post-signin)
6. `#posted` · auth=in live=none — You're posted up; invite friends. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)

## Branches and edge cases
- Flips to Live mode: empty map with an invite to post up, never "quiet" copy. [M1018b] [F035] [M1024]
- Someone goes live meanwhile: banner, no switch under them. [M1018b]

## Success criteria
- Never an empty screen. [F035] [R4]
- Projects shown even if none are local. [M1018c]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
