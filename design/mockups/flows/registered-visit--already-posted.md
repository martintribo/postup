# Flow: Registered visit → Already posted up (`registered-visit--already-posted`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--already-posted.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: postup@in.live (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), **post@in.live** (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: registered-visit step 1 (if Wants company now), registered-visit--cancelled step 1 (if Wants company now), registered-visit--ended step 1 (if Wants company now), registered-visit--full step 1 (if Wants company now), registered-visit--post step 1 (if Wants company now), registered-visit--report step 1 (if Wants company now), registered-visit--too-far step 1 (if Wants company now), registered-visit--follow-project step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **post@in.live** · user: At a cafe, wants company · action: taps Post up · edge: tap: Post up
   - Post up with the nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), posted@in.live (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), **post-already@in.live** (Post up (you already have a live postup)), post-far@in.live (Post up (the place is too far from you))
   - enterable flows: registered-visit--ended-post step 3 (if At a cafe, wants company), registered-visit--link-post step 3 (if At a cafe, wants company), registered-visit--nobody-post step 2 (if At a cafe, wants company), registered-visit--post step 2 (if At a cafe, wants company), registered-visit--too-far step 2 (if At a cafe, wants company), desktop-browse step 3 (if At a cafe, wants company)
3. **post-already@in.live** · user: Forgot they're already live at Lot 1 · action: posts · edge: tap: Post up (you already have a live postup)
   - You're already posted up at Lot 1 Coffee, with View your postup. [M1039]
   - next site states: back (Back), **live@in.live** (View your postup), home@in.live.live (Back to map), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: first-visit--already-posted step 6 (if Forgot they're already live at Lot 1), first-visit--live-already-posted step 6 (if Forgot they're already live at Lot 1)
4. **live@in.live** · user: Checks on the postup they have · action: taps View your postup · edge: tap: View your postup
   - Their live postup. [M1039]
   - next site states: back (Back), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), live+share@in.live (Share), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: registered-visit--hosting step 1 (if Live; wants more time), registered-visit--post step 4 (if Managing their postup), registered-visit--hosting-project step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)

## Connected flows [M1025]
- `desktop-browse`: branch out at step 1→1, step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--post`: branch out at step 2→2, step 4→4; merge in at step 4 (from its step 4)
- `registered-visit--ended-post`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--link-post`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--nobody-post`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `first-visit--already-posted`: branch out at step 3→6; merge in at step 3 (from its step 6)
- `host-approve`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `registered-visit`: branch out at step 1→1; merge in at —
- `registered-visit--cancelled`: branch out at step 1→1; merge in at —
- `registered-visit--ended`: branch out at step 1→1; merge in at —
- `registered-visit--full`: branch out at step 1→1; merge in at —
- `registered-visit--report`: branch out at step 1→1; merge in at —
- `registered-visit--follow-project`: branch out at step 1→1; merge in at —
- `catch-up`: branch out at step 1→1; merge in at —
- `registered-visit--too-far`: branch out at step 2→2; merge in at —
- `registered-visit--hosting`: branch out at step 4→1; merge in at —
- `registered-visit--hosting-project`: branch out at step 4→1; merge in at —
- `first-visit--live-already-posted`: branch out at —; merge in at step 3 (from its step 6)

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=0#home)
2. `#post` · auth=in live=live — Post up with the nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#post)
3. `#post-already` · auth=in live=live — You're already posted up at Lot 1 Coffee, with View your postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#post-already)
4. `#live` · auth=in live=live — Their live postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#live)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
