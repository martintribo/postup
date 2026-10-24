# Flow: Cautious joiner checks a few postups, then joins (`cautious-joiner`)
Priority: **MVP must** · Status: Martin's example (Oct 24) [M1024]
Player: /mockups/flows/cautious-joiner.html

## Persona
- Registered user, signed in, wants company but checks people out first.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Join a live postup after comparing a few. [M1024]

## Steps
1. `#home` · auth=in live=live mode=live — Opens / in Live mode: map + Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#project` · auth=in live=live — Opens Maya's project to see what she's working on, then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)
4. `#profile` · auth=in live=live — Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
5. `#cafe` · auth=in live=live — Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe)
6. `#postup-ask` · auth=in live=live — Compares a second postup (Tess approves who joins), then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
7. `#postup` · auth=in live=live — Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
8. `#joined` · auth=in live=live — You're joining Maya; Maya is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
9. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)

## Branches and edge cases
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

## Success criteria
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
