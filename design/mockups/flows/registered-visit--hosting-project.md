# Flow: Registered visit → Follows a maker while hosting (`registered-visit--hosting-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--hosting-project.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/live`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **live@in.live** · user: Live; wants more time · action: opens their live postup · edge: entry
   - +30 min extends. [FS]
   - next site states: back (Back), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), live+share@in.live (Share), chat@in.live (Group chat), inbox@in.live (Inbox), **project@in.live** (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: registered-visit--hosting step 1 (if Live; wants more time), registered-visit--post step 4 (if Managing their postup), host-approve step 2 (if Deciding on the request)
2. **project@in.live** · user: What's Maya making? · action: taps Star Fox 64 mod · edge: tap: Star Fox 64 mod
   - Project page. [FS] [M1044]
   - next site states: back (Back), project-new@in.live (New), **profile@in.live** (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 3 (if What's this?), registered-visit--follow-project step 3 (if A Star Fox 64 mod, nice), registered-visit--joined-project step 2 (if What are they working on?), registered-visit--link-project step 2 (if So that's what Maya is working on)
3. **profile@in.live** · user: Who makes this? · action: taps Maya · edge: tap: Maya
   - Maya's profile with Follow. [FS] [M1042]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--follow-project step 4 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)
4. **profile@in.live** · user: Wants to see what Maya makes next · action: taps Follow · edge: tap: Follow
   - Following Maya. [FS] [M1044]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit--ended-project step 4 (if Who makes this?), registered-visit--follow-project step 4 (if Who makes this?), registered-visit--joined-project step 3 (if Who makes this?), registered-visit--link-project step 3 (if Who makes this?), host-approve step 3 (if Wants to check the asker first)

## Connected flows [M1025]
- `host-approve`: branch out at step 1→2, step 3→3, step 4→3; merge in at step 1 (from its step 2), step 3 (from its step 3), step 4 (from its step 3)
- `registered-visit--ended-project`: branch out at step 4→4; merge in at step 2 (from its step 3), step 4 (from its step 4)
- `registered-visit--follow-project`: branch out at step 4→4; merge in at step 2 (from its step 3), step 4 (from its step 4)
- `registered-visit--joined-project`: branch out at step 4→3; merge in at step 2 (from its step 2), step 4 (from its step 3)
- `registered-visit--link-project`: branch out at step 4→3; merge in at step 2 (from its step 2), step 4 (from its step 3)
- `registered-visit--post`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `registered-visit--hosting`: branch out at step 1→1; merge in at —

## Screens
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#live)
2. `#project` · auth=in live=live — Project page. [FS] [M1044] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#project)
3. `#profile` · auth=in live=live — Maya's profile with Follow. [FS] [M1042] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)
4. `#profile` · auth=in live=live — Following Maya. [FS] [M1044] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
