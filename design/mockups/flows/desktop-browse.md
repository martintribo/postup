# Flow: Desktop browse and post (`desktop-browse`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/desktop-browse.html

## Persona
- Signed-in user at a laptop.

## Starting state
- auth=in · live=live · device=desktop · entry URL `/`

## Goal
- Same flows with map + right panel. [FS] [M1024]

## Steps
1. **home@in.live.live** · user: At a laptop; browsing · action: arrives at / · edge: entry
   - Map with 440px panel. [FS]
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: registered-visit step 1 (if Wants company now), registered-visit--already-posted step 1 (if Wants company now), registered-visit--cancelled step 1 (if Wants company now), registered-visit--ended step 1 (if Wants company now), registered-visit--full step 1 (if Wants company now), registered-visit--post step 1 (if Wants company now), registered-visit--report step 1 (if Wants company now), registered-visit--too-far step 1 (if Wants company now), registered-visit--follow-project step 1 (if Wants company now), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Checking one postup · action: taps a live pin · edge: tap: M 2
   - Postup in the panel. [FS]
   - next site states: back (Back), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), **post@in.live** (Post up), me@in.live (S), postup+share@in.live (Share), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: registered-visit step 2 (if Found someone), registered-visit--cancelled step 2 (if Found someone), registered-visit--ended step 2 (if Found someone), registered-visit--full step 2 (if Found someone), registered-visit--link-ended step 4 (if Could go to this one), registered-visit--report step 2 (if Found someone)
3. **post@in.live** · user: At a cafe, wants company · action: taps Post up · edge: tap: Post up
   - Post up with the nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), post-already@in.live (Post up (you already have a live postup)), post-far@in.live (Post up (the place is too far from you))
   - enterable flows: registered-visit--already-posted step 2 (if At a cafe, wants company), registered-visit--ended-post step 3 (if At a cafe, wants company), registered-visit--link-post step 3 (if At a cafe, wants company), registered-visit--nobody-post step 2 (if At a cafe, wants company), registered-visit--post step 2 (if At a cafe, wants company), registered-visit--too-far step 2 (if At a cafe, wants company)
4. **posted@in.live** · user: Live · action: taps Post up · edge: tap: Post up
   - Posted; link to copy. [FS]
   - next site states: home@in.live.live (Close), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), posted+share@in.live (Invite friends), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: registered-visit--post step 3 (if Live)

## Connected flows [M1025]
- `registered-visit--already-posted`: branch out at step 1→1, step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--post`: branch out at step 1→1, step 4→3; merge in at step 3 (from its step 2)
- `registered-visit--too-far`: branch out at step 1→1, step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--link-ended`: branch out at step 2→4; merge in at step 2 (from its step 4)
- `registered-visit--nobody-post`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--follow-project`: branch out at step 1→1; merge in at —
- `catch-up`: branch out at step 1→1; merge in at —
- `registered-visit`: branch out at step 2→2; merge in at —
- `registered-visit--cancelled`: branch out at step 2→2; merge in at —
- `registered-visit--ended`: branch out at step 2→2; merge in at —
- `registered-visit--full`: branch out at step 2→2; merge in at —
- `registered-visit--report`: branch out at step 2→2; merge in at —
- `registered-visit--ended-post`: branch out at —; merge in at step 3 (from its step 3)
- `registered-visit--link-post`: branch out at —; merge in at step 3 (from its step 3)

## Screens
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live&ph=2#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#postup)
3. `#post` · auth=in live=live — Post up with the nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#post)
4. `#posted` · auth=in live=live — Posted; link to copy. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#posted)

## Success criteria
- Rail and tab bar have the same items. [F064] [R12]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
