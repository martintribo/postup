# Flow: Quick joiner (`quick-joiner`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/quick-joiner.html

## Persona
- Registered user who already knows someone nearby is live.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Join in two taps and get directions. [M1024]

## Steps
1. **home@in.live.live** · user: Knows a friend is live; wants to go now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: cautious-joiner step 1 (if Wants company today, but careful about who), desktop-browse step 1 (if At a laptop; browsing)
2. **postup@in.live** · user: Found them; joining · action: taps the row · edge: tap: M 2
   - Taps a row, then Join. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), desktop-browse step 2 (if Checking one postup)
3. **joined@in.live** · user: Decides to just join now · action: taps Join · edge: tap: Join
   - Confirmation. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), **joined+dirs@in.live** (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 9 (if Committed; needs to get there), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
4. **joined+dirs@in.live** · user: Needs the route · action: taps Directions · edge: sheet: Directions
   - Directions. [FS] [M1024]
   - next site states: joined@in.live (close)
   - enterable flows: none
5. **chat@in.live** · user: Wants to say they're coming · action: opens the group chat · edge: 2 taps: close, then Group chat
   - Says "on my way" in the postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

## Connected flows [M1025]
- `invite-live`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `cautious-joiner`: branch out at step 2→2; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —
- `leave`: branch out at step 3→1; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps a row, then Join. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#joined` · auth=in live=live — Confirmation. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)
5. `#chat` · auth=in live=live — Says "on my way" in the postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

## Branches and edge cases
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]

## Success criteria
- Home → joined in 2 taps. [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
