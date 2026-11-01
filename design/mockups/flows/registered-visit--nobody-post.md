# Flow: Registered visit → Is the first today (`registered-visit--nobody-post`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--nobody-post.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=none · device=phone · entry URL `/`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **home@in.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@in.none (cafe), quiet@in.none (Locate), **post@in.none** (Post up), quiet-feed@in.none (Nearby), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Building), projects@in.none (Projects), empty-area@in.none (area has no postups), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: registered-visit--nobody step 1 (if Nobody around right now), registered-visit--builds-project step 1 (if Nobody around right now)
2. **post@in.none** · user: At a cafe, wants company · action: taps Post up · edge: tap: Post up
   - Post up with the nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), where@in.none (Bean Theory Nearest · 0.4 mi Chang), **posted@in.none** (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), me@in.none (S), inbox@in.none (Inbox), project-new@in.none (Project), home@in.none.building (home), projects@in.none (Projects), post-already@in.none (Post up (you already have a live postup)), post-far@in.none (Post up (the place is too far from you))
   - enterable flows: registered-visit--already-posted step 2 (if At a cafe, wants company), registered-visit--ended-post step 3 (if At a cafe, wants company), registered-visit--link-post step 3 (if At a cafe, wants company), registered-visit--post step 2 (if At a cafe, wants company), registered-visit--too-far step 2 (if At a cafe, wants company), desktop-browse step 3 (if At a cafe, wants company)
3. **posted@in.none** · user: Live · action: taps Post up · edge: tap: Post up
   - Posted; link to copy. [FS]
   - next site states: home@in.none.live (Close), posted+share@in.none (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Close), project@in.none (Star Fox 64 mod), projects@in.none (Projects), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-visit--ended-post step 7 (if Live; wants company), first-visit--link-post step 7 (if Live; wants company), first-visit--live-post step 6 (if Live; wants company), first-visit--post step 6 (if Live; wants company), registered-visit--post step 3 (if Live)

## Connected flows [M1025]
- `registered-visit--post`: branch out at step 2→2, step 3→3; merge in at step 2 (from its step 2), step 3 (from its step 3)
- `registered-visit--already-posted`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `registered-visit--ended-post`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--link-post`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--too-far`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `desktop-browse`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `first-visit--ended-post`: branch out at step 3→7; merge in at step 3 (from its step 7)
- `first-visit--link-post`: branch out at step 3→7; merge in at step 3 (from its step 7)
- `first-visit--live-post`: branch out at step 3→6; merge in at step 3 (from its step 6)
- `first-visit--post`: branch out at step 3→6; merge in at step 3 (from its step 6)
- `registered-visit--nobody`: branch out at step 1→1; merge in at —
- `registered-visit--builds-project`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=in live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=live&ph=0#home)
2. `#post` · auth=in live=none — Post up with the nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#post)
3. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#posted)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
