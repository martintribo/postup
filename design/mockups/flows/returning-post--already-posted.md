# Flow: Returning poster → Already posted up (`returning-post--already-posted`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/returning-post--already-posted.html

## Persona
- Signed-in regular.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Post up with defaults, then see you're live. [M1024]

## Steps
1. **post@in.live** · user: Regular; working at a cafe today · action: taps Post up · edge: entry
   - Last project and nearest cafe preselected; no 🔒. [FS] [M1024]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), posted@in.live (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects), **post-already@in.live** (Post up (you already have a live postup)), post-far@in.live (Post up (the place is too far from you))
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today), returning-post--too-far step 1 (if Regular; working at a cafe today), desktop-browse step 3 (if Wants to post too)
2. **post-already@in.live** · user: Forgot they're still live from earlier · action: taps Post up · edge: tap: Post up (you already have a live postup)
   - You're already posted up at Lot 1 Coffee. [M1039]
   - next site states: back (Back), **live@in.live** (View your postup), home@in.live.live (Back to map), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: first-visit--already-posted step 6 (if Forgot they're already live at Lot 1)
3. **live@in.live** · user: Ends or edits that one instead · action: taps View your postup · edge: tap: View your postup
   - Their live postup. [M1039]
   - next site states: back (Back), live+share@in.live (Share), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)

## Connected flows [M1025]
- `returning-post`: branch out at step 1→1, step 3→3; merge in at step 3 (from its step 3)
- `desktop-browse`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `first-visit--already-posted`: branch out at step 2→6; merge in at step 2 (from its step 6)
- `host-approve`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `returning-post--too-far`: branch out at step 1→1; merge in at —
- `hosting`: branch out at step 3→1; merge in at —

## Screens
1. `#post` · auth=in live=live — Last project and nearest cafe preselected; no 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post)
2. `#post-already` · auth=in live=live — You're already posted up at Lot 1 Coffee. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post-already)
3. `#live` · auth=in live=live — Their live postup. [M1039] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
