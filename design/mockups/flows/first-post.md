# Flow: Came to post up: first post with sign-in (`first-post`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post.html

## Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- Go live in about ten seconds. [M1024]

## Steps
1. `#home` · auth=out live=none mode=building — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none#where-search)
5. `#post-signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none#post-signin)
6. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)
7. `#posted` + sheet `share` · auth=in live=none — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=share#posted)

## Branches and edge cases
- Location denied: picker falls back to search. [R21] [unsourced]
- Cafe search fails without a Maps key → error state. [unsourced]

## Success criteria
- The form is not lost through sign-in. [M1018] [M1024]

## Needs Martin's decision
- Location-permission explainer: in or out? (ledger open, final list says not adopted) [R21] [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
