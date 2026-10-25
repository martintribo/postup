# Flow: Hosting live: extend, edit, end (`hosting`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/hosting.html

## Persona
- Signed-in poster who is live.

## Starting state
- auth=in · live=live · device=phone · entry URL `/live`

## Goal
- Manage time and end cleanly. [M1024]

## Steps
1. **live@in.live** · user: Live; wants more time · action: opens their live postup · edge: entry
   - +30 min extends. [FS]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), **post-edit@in.live** (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: host-approve step 2 (if Deciding on the request), returning-post step 3 (if Managing their postup)
2. **post-edit@in.live** · user: Plans changed: different time · action: taps Edit · edge: tap: Edit
   - Edit cafe/what/until; Save → #live. [FS] [drawn]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **live@in.live** (Save)
   - enterable flows: none
3. **live@in.live** · user: Saved · action: taps Save · edge: tap: Save
   - Back on live. [FS]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), **live+endlive@in.live** (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: host-approve step 2 (if Deciding on the request), returning-post step 3 (if Managing their postup)
4. **live+endlive@in.live** · user: Wrapping up · action: taps End postup · edge: sheet: End postup
   - End postup → confirm; joiners and waiters alerted. [FS] [drawn]
   - next site states: live@in.live (close), me@in.live (End now)
   - enterable flows: none
5. **me@in.none** · user: Done for today · action: confirms End now · edge: tap: End now (then live changes)
   - Back home. [M1024]
   - next site states: back (Back), settings@in.none (Settings), live@in.none (1:42 You're live at Bean Theory Ti), cafe@in.none (Lantern Tea), project-new@in.none (Tide Clock Updated Sun), cafe-gfail@in.none (Lantern Tea (Google card fails))
   - enterable flows: delete-account step 1 (if Leaving PostUp)

## Connected flows [M1025]
- `host-approve`: branch out at step 1→2, step 3→2; merge in at step 1 (from its step 2), step 3 (from its step 2)
- `returning-post`: branch out at step 1→3, step 3→3; merge in at step 1 (from its step 3), step 3 (from its step 3)
- `delete-account`: branch out at step 5→1; merge in at —

## Screens
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
2. `#post-edit` · auth=in live=live — Edit cafe/what/until; Save → #live. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#post-edit)
3. `#live` · auth=in live=live — Back on live. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup → confirm; joiners and waiters alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive#live)
5. `#me` · auth=in live=none — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none#me)

## Branches and edge cases
- Time runs out: ends automatically, chat stays 24h. [R31] [FS]
- Closes "who can join" (full): new visitors see #postup-full. [F060] [R47]

## Success criteria
- Joiners always know the postup ended. [FS] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
