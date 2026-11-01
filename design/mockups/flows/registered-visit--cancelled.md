# Flow: Registered visit → Postup cancelled (`registered-visit--cancelled`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--cancelled.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: registered-visit step 1 (if Wants company now), registered-visit--already-posted step 1 (if Wants company now), registered-visit--ended step 1 (if Wants company now), registered-visit--full step 1 (if Wants company now), registered-visit--post step 1 (if Wants company now), registered-visit--report step 1 (if Wants company now), registered-visit--too-far step 1 (if Wants company now), registered-visit--follow-project step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Found someone · action: taps a live row · edge: tap: M 2
   - Who, project, cafe, who else is joining. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: registered-visit step 2 (if Found someone), registered-visit--ended step 2 (if Found someone), registered-visit--full step 2 (if Found someone), registered-visit--link-ended step 4 (if Could go to this one), registered-visit--report step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)
3. **postup-cancelled@in.live** · user: The host left · action: waits while reading · edge: event: postup is cancelled
   - Cancelled state replaces Join. [FS] [M1040]
   - next site states: back (Back), postup-cancelled+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none

## Connected flows [M1025]
- `registered-visit--link-ended`: branch out at step 2→4; merge in at step 2 (from its step 4)
- `registered-visit--already-posted`: branch out at step 1→1; merge in at —
- `registered-visit--post`: branch out at step 1→1; merge in at —
- `registered-visit--too-far`: branch out at step 1→1; merge in at —
- `registered-visit--follow-project`: branch out at step 1→1; merge in at —
- `catch-up`: branch out at step 1→1; merge in at —
- `registered-visit`: branch out at step 2→2; merge in at —
- `registered-visit--ended`: branch out at step 2→2; merge in at —
- `registered-visit--full`: branch out at step 2→2; merge in at —
- `registered-visit--report`: branch out at step 2→2; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=0#home)
2. `#postup` · auth=in live=live — Who, project, cafe, who else is joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#postup)
3. `#postup-cancelled` · auth=in live=live — Cancelled state replaces Join. [FS] [M1040] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#postup-cancelled)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
