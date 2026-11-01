# Flow: First visit → Follows the friend's project (`first-visit--link-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--link-project.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **invite@out.live** · user: A friend sent this; knows the context · action: opens the share link · edge: entry
   - Landing for the shared postup. [FS] [R39]
   - next site states: invite+signin@out.live (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), **project@out.live** (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: first-visit--link-live step 1 (if A friend sent this; knows the context), first-visit--link-post step 1 (if A friend sent this; knows the context)
2. **project@out.live** · user: So that's what Maya is working on · action: taps Star Fox 64 mod · edge: tap: Star Fox 64 mod
   - Project page from the shared postup. [FS] [M1043]
   - next site states: back (Back), project-new@out.live (New), **profile@out.live** (Maya), project-update@out.live (Update), project-attach@out.live (Post up), cafe@out.live (Bean Theory), postup@out.live (M Maya Bean Theory · till 4pm Live), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit--ended-project step 3 (if What's this?), first-visit--follow-project step 3 (if A Star Fox 64 mod, nice)
3. **profile@out.live** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@out.live (More), postup@out.live (Live at Bean Theory Till 4pm · Sta), **profile+signin@out.live** (Follow), cafe@out.live (Bean Theory), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Updated yesterday), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit step 3 (if Who is behind it?), first-visit--not-now step 3 (if Who is behind it?), first-visit--ended-project step 4 (if Who makes this?), first-visit--follow-project step 4 (if Who makes this?)
4. **profile+signin@out.live** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Follow 🔒 opens the sign-in sheet. [FS] [M1025]
   - next site states: profile@out.live (close), **profile@in.live** (Continue with Apple)
   - enterable flows: first-visit--ended-project step 5 (if Wants to see what Maya makes next), first-visit--follow-project step 5 (if Wants to see what Maya makes next), first-visit--nobody-project step 5 (if Wants to see what Maya makes next)
5. **profile@in.live** · user: Signed up; following Maya · action: signs in · edge: tap: Continue with Apple
   - Signed in and following Maya. [FS] [M1042]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--follow-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `first-visit`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `first-visit--not-now`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `first-visit--nobody-project`: branch out at step 4→5; merge in at step 4 (from its step 5)
- `registered-visit--ended-project`: branch out at step 5→4; merge in at step 5 (from its step 4)
- `registered-visit--follow-project`: branch out at step 5→4; merge in at step 5 (from its step 4)
- `registered-visit--hosting-project`: branch out at step 5→3; merge in at step 5 (from its step 3)
- `registered-visit--joined-project`: branch out at step 5→3; merge in at step 5 (from its step 3)
- `registered-visit--link-project`: branch out at step 5→3; merge in at step 5 (from its step 3)
- `host-approve`: branch out at step 5→3; merge in at step 5 (from its step 3)
- `first-visit--link-live`: branch out at step 1→1; merge in at —
- `first-visit--link-post`: branch out at step 1→1; merge in at —
- `first-visit--ended-project`: branch out at —; merge in at step 2 (from its step 3)
- `first-visit--follow-project`: branch out at —; merge in at step 2 (from its step 3)

## Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=2#invite)
2. `#project` · auth=out live=live — Project page from the shared postup. [FS] [M1043] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=2#project)
3. `#profile` · auth=out live=live — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=2#profile)
4. `#profile` + sheet `signin` · auth=out live=live — Follow 🔒 opens the sign-in sheet. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=2#profile)
5. `#profile` · auth=in live=live — Signed in and following Maya. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
