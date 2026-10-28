# Flow: Join someone live (`join`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox-one@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails)), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Found someone · action: taps a live row · edge: tap: M 2
   - Who, project, cafe, who else is joining. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox-one@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails)), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: desktop-browse step 2 (if Checking one postup)
3. **joined@in.live** · user: Decides to join · action: taps Join · edge: tap: Join
   - You're joining; the poster is told. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), **joined+dirs@in.live** (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox-one@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails)), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
4. **joined+dirs@in.live** · user: Needs the route · action: taps Directions · edge: tap: Directions
   - Directions sheet: Apple / Google Maps. [FS] [M1024]
   - next site states: **joined@in.live** (close)
   - enterable flows: none
5. **joined@in.live** · user: Knows the way · action: closes Directions · edge: tap: Cancel
   - Back on the joined screen. [M1031-draft]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **chat@in.live** (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox-one@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails)), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
6. **chat@in.live** · user: Says they're coming · action: opens the group chat · edge: tap: Group chat
   - Says "on my way" in the postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox-one@in.live (Inbox), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

## Connected flows [M1025]
- `invite-live`: branch out at step 3→3; merge in at step 3 (from its step 3), step 5 (from its step 3)
- `leave`: branch out at step 3→1, step 5→1; merge in at —
- `chat`: branch out at step 6→2; merge in at step 6 (from its step 2)
- `catch-up`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Who, project, cafe, who else is joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#joined` · auth=in live=live — You're joining; the poster is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)
5. `#joined` · auth=in live=live — Back on the joined screen. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
6. `#chat` · auth=in live=live — Says "on my way" in the postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

## Branches and edge cases
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
