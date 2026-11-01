# Flow: First visit → Follows a maker (`first-visit--nobody-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--nobody-project.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@out.none (cafe), quiet@out.none (Locate), post@out.none (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), **home@out.none.building** (Building), projects@out.none (Projects), empty-area@out.none (area has no postups), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: first-visit--already-posted step 1 (if Nobody around right now), first-visit--nobody step 1 (if Nobody around right now), first-visit--post step 1 (if Nobody around right now), first-visit--too-far step 1 (if Nobody around right now)
2. **home@out.none.building** · user: What are people making? · action: taps Building · edge: tap: Building
   - What people are building: project cards. [M1018b] [M1018c]
   - next site states: cafe@out.none (Lantern Tea A D M 3 postups), post@out.none (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), home@out.none.live (Live), projects@out.none (See all projects), **project@out.none** (Star Fox 64 mod M Maya · Yesterday), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
3. **project@out.none** · user: A Star Fox 64 mod, nice · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Project page: updates and who's behind it. [FS] [M1042]
   - next site states: back (Back), project-new@out.none (New), **profile@out.none** (Maya), project-update@out.none (Update), project-attach@out.none (Post up), cafe@out.none (Bean Theory), home@out.none.live (Home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), home@out.none.building (Home), projects@out.none (Projects), cafe-gfail@out.none (Bean Theory (Google card fails))
   - enterable flows: none
4. **profile@out.none** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@out.none (More), **profile+signin@out.none** (Follow), cafe@out.none (Bean Theory), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project@out.none (Star Fox 64 mod Updated yesterday), home@out.none.building (home), projects@out.none (Projects), cafe-gfail@out.none (Bean Theory (Google card fails))
   - enterable flows: first-visit--nobody step 3 (if Who comes here?)
5. **profile+signin@out.none** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Follow 🔒 opens the sign-in sheet. [FS] [M1025]
   - next site states: profile@out.none (close), **profile@in.none** (Continue with Apple)
   - enterable flows: first-visit--ended-project step 5 (if Wants to see what Maya makes next), first-visit--follow-project step 5 (if Wants to see what Maya makes next), first-visit--link-project step 4 (if Wants to see what Maya makes next)
6. **profile@in.none** · user: Signed up; following Maya · action: signs in · edge: tap: Continue with Apple
   - Signed in and following Maya. [FS] [M1042]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), project@in.none (Star Fox 64 mod Updated yesterday), home@in.none.building (home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: registered-visit--nobody step 3 (if Who comes here?), following step 1 (if Likes someone's work)

## Connected flows [M1025]
- `first-visit--nobody`: branch out at step 1→1, step 4→3; merge in at step 4 (from its step 3)
- `first-visit--ended-project`: branch out at step 5→5; merge in at step 5 (from its step 5)
- `first-visit--follow-project`: branch out at step 5→5; merge in at step 5 (from its step 5)
- `first-visit--link-project`: branch out at step 5→4; merge in at step 5 (from its step 4)
- `registered-visit--nobody`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `first-visit--already-posted`: branch out at step 1→1; merge in at —
- `first-visit--post`: branch out at step 1→1; merge in at —
- `first-visit--too-far`: branch out at step 1→1; merge in at —
- `following`: branch out at step 6→1; merge in at —

## Screens
1. `#home` · auth=out live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=2#home)
2. `#home` · auth=out live=none mode=building — What people are building: project cards. [M1018b] [M1018c] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building&ph=2#home)
3. `#project` · auth=out live=none — Project page: updates and who's behind it. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=2#project)
4. `#profile` · auth=out live=none — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=2#profile)
5. `#profile` + sheet `signin` · auth=out live=none — Follow 🔒 opens the sign-in sheet. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin&ph=2#profile)
6. `#profile` · auth=in live=none — Signed in and following Maya. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
