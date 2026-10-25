# Flow: Desktop browse and post (`desktop-browse`)
Priority: **nice** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: **postup@in.live** (M 2), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: cautious-joiner step 1 (if Wants company today, but careful about who), quick-joiner step 1 (if Knows a friend is live; wants to go now)
2. **postup@in.live** · user: Checking one postup · action: taps a live pin · edge: tap: M 2
   - Postup in the panel. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), quick-joiner step 2 (if Found them; joining)
3. **post@in.live** · user: Wants to post too · action: taps Post up · edge: back, then tap: Post up
   - Post up as a centered dialog. [FS]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **posted@in.live** (Post up)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today)
4. **posted@in.live** · user: Live · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), project@in.live (Star Fox 64 mod), posted+share@in.live (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Live)

## Connected flows [M1025]
- `first-post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `cautious-joiner`: branch out at step 2→2; merge in at —
- `quick-joiner`: branch out at step 2→2; merge in at —
- `returning-post`: branch out at step 4→2; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#postup)
3. `#post` · auth=in live=live — Post up as a centered dialog. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#post)
4. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#posted)

## Success criteria
- Rail and tab bar have the same items. [F064] [R12]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
