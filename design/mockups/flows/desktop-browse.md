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
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), me@in.live (S), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Checking one postup · action: taps a live pin · edge: tap: M 2
   - Postup in the panel. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), **post@in.live** (Post up), me@in.live (S), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone)
3. **post@in.live** · user: Wants to post too · action: taps Post up · edge: tap: Post up
   - Post up as a centered dialog. [FS]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), me@in.live (S), project-new@in.live (Project), projects@in.live (Projects)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today)
4. **posted@in.live** · user: Posted; now live for others · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), posted+share@in.live (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), me@in.live (S), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

## Connected flows [M1025]
- `first-post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `catch-up`: branch out at step 1→1; merge in at —
- `join`: branch out at step 2→2; merge in at —
- `returning-post`: branch out at step 4→2; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live&ph=2#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#postup)
3. `#post` · auth=in live=live — Post up as a centered dialog. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#post)
4. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#posted)

## Success criteria
- Rail and tab bar have the same items. [F064] [R12]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
