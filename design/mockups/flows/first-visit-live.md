# Flow: Curious visitor joins someone live (`first-visit-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit-live.html

## Persona
- New visitor, signed out, curious; lands on / with live postups nearby.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand the site and join someone; sign in only at Join. [M1024]

## Steps
1. **home@out.live.live** · user: Curious; sees people live right now · action: arrives at / · edge: entry
   - Home opens in Live mode with a one-line welcome. [M1018b] [M1024]
   - next site states: **postup@out.live** (M 2), cafe@out.live (tap), home@out.live.building (Building), quiet@out.live (Locate), project@out.live (Star Fox 64 mod), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live ( (Google card fails))
   - enterable flows: curious-browser step 1 (if Curious what is on the site), stumbled step 1 (if No idea what PostUp is)
2. **postup@out.live** · user: Tempted by one postup · action: taps a live row · edge: tap: M 2
   - Opens a postup; Join shows 🔒. [FS] [M1024]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **join-signin@out.live** (Join), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: curious-browser step 2 (if Peeking at who is live), stumbled step 2 (if Trying to understand by example)
3. **join-signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: back (Back), join-signin+share@out.live (Share), join-signin+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (signs in), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: invite-live step 2 (if Wants to join the friend)
4. **joined@in.live** · user: Signed in; committed · action: signs in · edge: sign-in: signs in
   - Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 8 (if Committed; needs to get there), quick-joiner step 3 (if Committed), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)

## Connected flows [M1025]
- `cautious-joiner`: branch out at step 4→8; merge in at step 4 (from its step 8)
- `quick-joiner`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `invite-live`: branch out at step 4→3; merge in at step 3 (from its step 2)
- `curious-browser`: branch out at step 2→2; merge in at —
- `stumbled`: branch out at step 2→2; merge in at —
- `leave`: branch out at step 4→1; merge in at —

## Screens
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
