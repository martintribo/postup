# Flow: Registered visit → Posts up instead (`registered-visit--ended-post`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--ended-post.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **invite-ended@in.live** · user: Too late for this one · action: opens the share link · edge: entry
   - This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032]
   - next site states: **quiet-feed@in.live** (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: registered-visit--link-ended step 1 (if Too late for this one), registered-visit--ended-project step 1 (if Too late for this one)
2. **quiet-feed@in.live** · user: Who else is around? · action: taps See what's nearby · edge: tap: See what's nearby
   - Nearby list of postups. [FS] [M1041]
   - next site states: me@in.live (S), quiet@in.live (quiet), **post@in.live** (Post up), cafe@in.live (Maya's photo), home@in.live.live (Home), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: registered-visit--link-ended step 2 (if Who else is around?), registered-visit--ended-project step 2 (if Who else is around?), loading-offline step 3 (if Back online)
3. **post@in.live** · user: At a cafe, wants company · action: taps Post up · edge: tap: Post up
   - Post up with the nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), post-already@in.live (Post up (you already have a live postup)), post-far@in.live (Post up (the place is too far from you))
   - enterable flows: registered-visit--already-posted step 2 (if At a cafe, wants company), registered-visit--link-post step 3 (if At a cafe, wants company), registered-visit--nobody-post step 2 (if At a cafe, wants company), registered-visit--post step 2 (if At a cafe, wants company), registered-visit--too-far step 2 (if At a cafe, wants company), desktop-browse step 3 (if At a cafe, wants company)
4. **posted@in.live** · user: Live · action: taps Post up · edge: tap: Post up
   - Posted; link to copy. [FS]
   - next site states: home@in.live.live (Close), posted+share@in.live (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-visit--ended-post step 7 (if Live; wants company), first-visit--link-post step 7 (if Live; wants company), first-visit--live-post step 6 (if Live; wants company), first-visit--post step 6 (if Live; wants company), registered-visit--post step 3 (if Live)

## Connected flows [M1025]
- `loading-offline`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--already-posted`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--nobody-post`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `registered-visit--too-far`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `first-visit--ended-post`: branch out at step 4→7; merge in at step 4 (from its step 7)
- `first-visit--link-post`: branch out at step 4→7; merge in at step 4 (from its step 7)
- `first-visit--live-post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `first-visit--post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `registered-visit--post`: branch out at step 4→3; merge in at step 3 (from its step 2)
- `registered-visit--link-ended`: branch out at step 2→2; merge in at —
- `registered-visit--ended-project`: branch out at step 2→2; merge in at —
- `registered-visit--link-post`: branch out at —; merge in at step 3 (from its step 3)
- `desktop-browse`: branch out at —; merge in at step 3 (from its step 3)

## Screens
1. `#invite-ended` · auth=in live=live — This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#invite-ended)
2. `#quiet-feed` · auth=in live=live — Nearby list of postups. [FS] [M1041] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#quiet-feed)
3. `#post` · auth=in live=live — Post up with the nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#post)
4. `#posted` · auth=in live=live — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#posted)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
