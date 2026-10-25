# Flow: Postup ends, fills or is cancelled while you look (`postup-states`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/postup-states.html

## Persona
- Anyone viewing a postup.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Clear state and a next step. [F060] [M1024]

## Steps
1. **postup-full@in.live** · user: Wanted to join; it's full · action: opens a full postup · edge: entry
   - Full. [F060] [R47]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none
2. **postup-cancelled@in.live** · user: Host cancelled · action: later: postup cancelled · edge: event: postup fills / is cancelled / ends
   - Cancelled. [F060] [R47]
   - next site states: back (Back), postup-cancelled+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none
3. **postup-ended@in.none** · user: Too late; it ended · action: later: postup ended · edge: 2 taps: Inbox, then T Tess's postup Ended · Tue Tue
   - Ended: see what's nearby, follow. [drawn]
   - next site states: back (Back), postup-ended+more@in.none (More), profile@in.none (M Maya Bean Theory), quiet-feed@in.none (See what's nearby), home@in.none.building (Home), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox)
   - enterable flows: none

## Connected flows [M1025]
- none

## Screens
1. `#postup-full` · auth=in live=live — Full. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
2. `#postup-cancelled` · auth=in live=live — Cancelled. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-cancelled)
3. `#postup-ended` · auth=in live=none — Ended: see what's nearby, follow. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#postup-ended)

## Success criteria
- Never a blank page. [F060]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
