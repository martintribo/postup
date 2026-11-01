# Flow: First visit → Follows a maker (`first-visit--follow-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--follow-project.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: postup@out.live (M 2), cafe@out.live (cafe), quiet@out.live (Locate), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), postup-ask@out.live (T), **home@out.live.building** (Building), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: first-visit step 1 (if Curious what this is; sees people live), first-visit--browse step 1 (if Curious what this is; sees people live), first-visit--live-already-posted step 1 (if Curious what this is; sees people live), first-visit--live-post step 1 (if Curious what this is; sees people live), first-visit--live-too-far step 1 (if Curious what this is; sees people live), first-visit--not-now step 1 (if Curious what this is; sees people live)
2. **home@out.live.building** · user: What are people making? · action: taps Building · edge: tap: Building
   - What people are building: project cards. [M1018b] [M1018c]
   - next site states: cafe@out.live (Lantern Tea A D M 3 postups), post@out.live (Post up), quiet-feed@out.live (Nearby), me@out.live (S), inbox@out.live (Inbox), home@out.live.live (Live), projects@out.live (See all projects), **project@out.live** (Star Fox 64 mod M Maya · Yesterday), cafe-gfail@out.live (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
3. **project@out.live** · user: A Star Fox 64 mod, nice · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Project page: updates and who's behind it. [FS] [M1042]
   - next site states: back (Back), project-new@out.live (New), **profile@out.live** (Maya), project-update@out.live (Update), project-attach@out.live (Post up), cafe@out.live (Bean Theory), postup@out.live (M Maya Bean Theory · till 4pm Live), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit--ended-project step 3 (if What's this?), first-visit--link-project step 2 (if So that's what Maya is working on)
4. **profile@out.live** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@out.live (More), postup@out.live (Live at Bean Theory Till 4pm · Sta), **profile+signin@out.live** (Follow), cafe@out.live (Bean Theory), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Updated yesterday), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit step 3 (if Who is behind it?), first-visit--not-now step 3 (if Who is behind it?), first-visit--ended-project step 4 (if Who makes this?), first-visit--link-project step 3 (if Who makes this?)
5. **profile+signin@out.live** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Follow 🔒 opens the sign-in sheet. [FS] [M1025]
   - next site states: profile@out.live (close), **profile@in.live** (Continue with Apple)
   - enterable flows: first-visit--ended-project step 5 (if Wants to see what Maya makes next), first-visit--link-project step 4 (if Wants to see what Maya makes next), first-visit--nobody-project step 5 (if Wants to see what Maya makes next)
6. **profile@in.live** · user: Signed up; following Maya · action: signs in · edge: tap: Continue with Apple
   - Signed in and following Maya. [FS] [M1042]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--follow-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `first-visit`: branch out at step 1→1, step 4→3; merge in at step 4 (from its step 3)
- `first-visit--not-now`: branch out at step 1→1, step 4→3; merge in at step 4 (from its step 3)
- `first-visit--nobody-project`: branch out at step 5→5; merge in at step 5 (from its step 5)
- `registered-visit--ended-project`: branch out at step 6→4; merge in at step 6 (from its step 4)
- `registered-visit--follow-project`: branch out at step 6→4; merge in at step 6 (from its step 4)
- `registered-visit--hosting-project`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `registered-visit--joined-project`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `registered-visit--link-project`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `host-approve`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `first-visit--browse`: branch out at step 1→1; merge in at —
- `first-visit--live-already-posted`: branch out at step 1→1; merge in at —
- `first-visit--live-post`: branch out at step 1→1; merge in at —
- `first-visit--live-too-far`: branch out at step 1→1; merge in at —
- `first-visit--ended-project`: branch out at —; merge in at step 3 (from its step 3)
- `first-visit--link-project`: branch out at —; merge in at step 3 (from its step 2)

## Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live&ph=2#home)
2. `#home` · auth=out live=live mode=building — What people are building: project cards. [M1018b] [M1018c] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building&ph=2#home)
3. `#project` · auth=out live=live — Project page: updates and who's behind it. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=2#project)
4. `#profile` · auth=out live=live — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=2#profile)
5. `#profile` + sheet `signin` · auth=out live=live — Follow 🔒 opens the sign-in sheet. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=2#profile)
6. `#profile` · auth=in live=live — Signed in and following Maya. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
