# Flow: Registered visit → Follows the host's project (`registered-visit--joined-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--joined-project.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **joined@in.live** · user: Plans changed · action: opens their joined postup · edge: entry
   - Leave link. [drawn]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), **project@in.live** (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit step 3 (if Decides to join), registered-visit--joined step 1 (if Plans changed), registered-visit--joined-chat step 1 (if Plans changed)
2. **project@in.live** · user: What are they working on? · action: taps the project · edge: tap: Project
   - Project page. [FS] [M1044]
   - next site states: back (Back), project-new@in.live (New), **profile@in.live** (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 3 (if What's this?), registered-visit--follow-project step 3 (if A Star Fox 64 mod, nice), registered-visit--hosting-project step 2 (if What's Maya making?), registered-visit--link-project step 2 (if So that's what Maya is working on)
3. **profile@in.live** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--follow-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)
4. **profile@in.live** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Following Maya. [FS] [M1044]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--follow-project step 4 (if Who makes this?), registered-visit--hosting-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `host-approve`: branch out at step 3→3, step 4→3; merge in at step 3 (from its step 3), step 4 (from its step 3)
- `registered-visit--ended-project`: branch out at step 4→4; merge in at step 2 (from its step 3), step 4 (from its step 4)
- `registered-visit--follow-project`: branch out at step 4→4; merge in at step 2 (from its step 3), step 4 (from its step 4)
- `registered-visit--hosting-project`: branch out at step 4→3; merge in at step 2 (from its step 2), step 4 (from its step 3)
- `registered-visit--link-project`: branch out at step 4→3; merge in at step 2 (from its step 2), step 4 (from its step 3)
- `registered-visit`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `registered-visit--joined`: branch out at step 1→1; merge in at —
- `registered-visit--joined-chat`: branch out at step 1→1; merge in at —

## Screens
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#joined)
2. `#project` · auth=in live=live — Project page. [FS] [M1044] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#project)
3. `#profile` · auth=in live=live — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)
4. `#profile` · auth=in live=live — Following Maya. [FS] [M1044] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
