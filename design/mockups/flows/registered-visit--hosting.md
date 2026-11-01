# Flow: Registered visit → Extends, then ends (`registered-visit--hosting`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--hosting.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/live`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **live@in.live** · user: Live; wants more time · action: opens their live postup · edge: entry
   - +30 min extends. [FS]
   - next site states: back (Back), **post-edit@in.live** (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), live+share@in.live (Share), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: registered-visit--post step 4 (if Managing their postup), registered-visit--hosting-project step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)
2. **post-edit@in.live** · user: Staying longer · action: taps Edit · edge: tap: Edit
   - Edit the postup: extend the end time. [FS] [M1024]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **live@in.live** (Save), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects)
   - enterable flows: none
3. **live@in.live** · user: Extended · action: saves · edge: back
   - Hosting page with the new end time. [FS]
   - next site states: back (Back), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), **live+endlive@in.live** (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), live+share@in.live (Share), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: registered-visit--post step 4 (if Managing their postup), registered-visit--hosting-project step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)
4. **live+endlive@in.live** · user: Heading out · action: taps End postup · edge: tap: End postup
   - End postup? confirm sheet. [FS]
   - next site states: live@in.live (close), **me@in.live** (End now)
   - enterable flows: none
5. **me@in.live** · user: Done for today · action: taps End now · edge: tap: End now
   - Ended; back on Me. [FS]
   - next site states: back (Back), settings@in.live (Settings), live@in.live (1:42 You're live at Bean Theory Ti), cafe@in.live (Lantern Tea), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), project-new@in.live (Tide Clock Updated Sun), projects@in.live (Projects), cafe-gfail@in.live (Lantern Tea (Google card fails))
   - enterable flows: delete-account step 1 (if Leaving PostUp)

## Connected flows [M1025]
- `registered-visit--post`: branch out at step 1→4, step 3→4; merge in at step 1 (from its step 4), step 3 (from its step 4)
- `host-approve`: branch out at step 1→2, step 3→2; merge in at step 1 (from its step 2), step 3 (from its step 2)
- `registered-visit--hosting-project`: branch out at step 1→1, step 3→1; merge in at —
- `delete-account`: branch out at step 5→1; merge in at —

## Screens
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)
2. `#post-edit` · auth=in live=live — Edit the postup: extend the end time. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post-edit)
3. `#live` · auth=in live=live — Hosting page with the new end time. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup? confirm sheet. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive&ph=1#live)
5. `#me` · auth=in live=live — Ended; back on Me. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#me)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
