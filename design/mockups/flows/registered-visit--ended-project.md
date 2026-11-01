# Flow: Registered visit → Follows a maker (`registered-visit--ended-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--ended-project.html

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
   - enterable flows: registered-visit--ended-post step 1 (if Too late for this one), registered-visit--link-ended step 1 (if Too late for this one)
2. **quiet-feed@in.live** · user: Who else is around? · action: taps See what's nearby · edge: tap: See what's nearby
   - Nearby list of postups. [FS] [M1041]
   - next site states: me@in.live (S), quiet@in.live (quiet), post@in.live (Post up), cafe@in.live (Maya's photo), home@in.live.live (Home), inbox@in.live (Inbox), **project@in.live** (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: registered-visit--ended-post step 2 (if Who else is around?), registered-visit--link-ended step 2 (if Who else is around?), loading-offline step 3 (if Back online)
3. **project@in.live** · user: What's this? · action: taps Star Fox 64 mod · edge: tap: Star Fox 64 mod
   - Project page from Nearby. [FS] [M1043]
   - next site states: back (Back), project-new@in.live (New), **profile@in.live** (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--follow-project step 3 (if A Star Fox 64 mod, nice), registered-visit--hosting-project step 2 (if What's Maya making?), registered-visit--joined-project step 2 (if What are they working on?), registered-visit--link-project step 2 (if So that's what Maya is working on)
4. **profile@in.live** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--follow-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)
5. **profile@in.live** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Following Maya. [FS] [M1044]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--follow-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `host-approve`: branch out at step 4→3, step 5→3; merge in at step 4 (from its step 3), step 5 (from its step 3)
- `registered-visit--follow-project`: branch out at step 5→4; merge in at step 3 (from its step 3), step 5 (from its step 4)
- `registered-visit--hosting-project`: branch out at step 5→3; merge in at step 3 (from its step 2), step 5 (from its step 3)
- `registered-visit--joined-project`: branch out at step 5→3; merge in at step 3 (from its step 2), step 5 (from its step 3)
- `registered-visit--link-project`: branch out at step 5→3; merge in at step 3 (from its step 2), step 5 (from its step 3)
- `loading-offline`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `registered-visit--ended-post`: branch out at step 2→2; merge in at —
- `registered-visit--link-ended`: branch out at step 2→2; merge in at —

## Screens
1. `#invite-ended` · auth=in live=live — This postup ended; See what's nearby, Follow Maya for next time, Go to Home. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#invite-ended)
2. `#quiet-feed` · auth=in live=live — Nearby list of postups. [FS] [M1041] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#quiet-feed)
3. `#project` · auth=in live=live — Project page from Nearby. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#project)
4. `#profile` · auth=in live=live — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)
5. `#profile` · auth=in live=live — Following Maya. [FS] [M1044] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
