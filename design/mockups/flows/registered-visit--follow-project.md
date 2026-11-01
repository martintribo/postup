# Flow: Registered visit → Follows a maker (`registered-visit--follow-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--follow-project.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: postup@in.live (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), **home@in.live.building** (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: registered-visit step 1 (if Wants company now), registered-visit--already-posted step 1 (if Wants company now), registered-visit--cancelled step 1 (if Wants company now), registered-visit--ended step 1 (if Wants company now), registered-visit--full step 1 (if Wants company now), registered-visit--post step 1 (if Wants company now), registered-visit--report step 1 (if Wants company now), registered-visit--too-far step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **home@in.live.building** · user: What are people making? · action: taps Building · edge: tap: Building
   - What people are building: project cards. [M1018b] [M1018c]
   - next site states: cafe@in.live (Lantern Tea A D M 3 postups), me@in.live (S), post@in.live (Post up), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), home@in.live.live (Live), projects@in.live (See all projects), **project@in.live** (Star Fox 64 mod M Maya · Yesterday), cafe-gfail@in.live (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
3. **project@in.live** · user: A Star Fox 64 mod, nice · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Project page: updates and who's behind it. [FS] [M1042]
   - next site states: back (Back), project-new@in.live (New), **profile@in.live** (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 3 (if What's this?), registered-visit--hosting-project step 2 (if What's Maya making?), registered-visit--joined-project step 2 (if What are they working on?), registered-visit--link-project step 2 (if So that's what Maya is working on)
4. **profile@in.live** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)
5. **profile@in.live** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Following Maya. [FS] [M1044]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `host-approve`: branch out at step 4→3, step 5→3; merge in at step 4 (from its step 3), step 5 (from its step 3)
- `registered-visit--ended-project`: branch out at step 5→4; merge in at step 3 (from its step 3), step 5 (from its step 4)
- `registered-visit--hosting-project`: branch out at step 5→3; merge in at step 3 (from its step 2), step 5 (from its step 3)
- `registered-visit--joined-project`: branch out at step 5→3; merge in at step 3 (from its step 2), step 5 (from its step 3)
- `registered-visit--link-project`: branch out at step 5→3; merge in at step 3 (from its step 2), step 5 (from its step 3)
- `registered-visit`: branch out at step 1→1; merge in at —
- `registered-visit--already-posted`: branch out at step 1→1; merge in at —
- `registered-visit--cancelled`: branch out at step 1→1; merge in at —
- `registered-visit--ended`: branch out at step 1→1; merge in at —
- `registered-visit--full`: branch out at step 1→1; merge in at —
- `registered-visit--post`: branch out at step 1→1; merge in at —
- `registered-visit--report`: branch out at step 1→1; merge in at —
- `registered-visit--too-far`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 1→1; merge in at —
- `catch-up`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=2#home)
2. `#home` · auth=in live=live mode=building — What people are building: project cards. [M1018b] [M1018c] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=building&ph=2#home)
3. `#project` · auth=in live=live — Project page: updates and who's behind it. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#project)
4. `#profile` · auth=in live=live — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)
5. `#profile` · auth=in live=live — Following Maya. [FS] [M1044] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
