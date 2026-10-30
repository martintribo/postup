# Flow: Join someone live (`join`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/join.html

## Persona
- Registered user, signed in, who wants company now.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Join a live postup and get there; checking the person first is optional. [M1024] [M1032]

## Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Found someone · action: taps a live row · edge: tap: M 2
   - Who, project, cafe, who else is joining. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: desktop-browse step 2 (if Checking one postup)
3. **joined@in.live** · user: Decides to join · action: taps Join · edge: tap: Join
   - You're joining; the poster is told. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **joined+dirs@in.live** (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: leave step 1 (if Plans changed)
4. **joined+dirs@in.live** · user: Needs the route · action: taps Directions · edge: tap: Directions
   - Directions sheet: Apple / Google Maps. [FS] [M1024]
   - next site states: **joined@in.live** (close)
   - enterable flows: none
5. **joined@in.live** · user: Knows the way · action: closes Directions · edge: tap: Cancel
   - Back on the joined screen. [M1031-draft]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: leave step 1 (if Plans changed)

## Connected flows [M1025]
- `leave`: branch out at step 3→1, step 5→1; merge in at —
- `catch-up`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=0#home)
2. `#postup` · auth=in live=live — Who, project, cafe, who else is joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#postup)
3. `#joined` · auth=in live=live — You're joining; the poster is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs&ph=0#joined)
5. `#joined` · auth=in live=live — Back on the joined screen. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)

## Branches and edge cases
- Phase 0: no group chat; joining means you're coming in person. The chat step moved to the Chat flow (phase 1). [M1037]
- Optional check first (was Cautious joiner): from the postup, the project tag → project, the owner → profile (postup count, regular cafes, past postups), the cafe → cafe; Back returns each time. [FS] [F065] [M1024]
- Compares with an Ask to join postup (Tess): phase 2, see Ask to join. [M1032]
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

## Success criteria
- Home → joined in 2 taps. [M1024]
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
