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
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
2. **postup-cancelled@in.live** · user: Host cancelled · action: later: postup cancelled · edge: event: postup is cancelled
   - Cancelled. [F060] [R47]
   - next site states: back (Back), postup-cancelled+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
3. **postup-full@in.live** · user: Checks the other postup · action: taps Back · edge: back
   - Back to the full postup (split: a cancelled postup doesn't later end). [M1031-draft]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
4. **postup-ended@in.live** · user: Too late; it ended · action: later: postup ended · edge: event: postup ends
   - Ended: see what's nearby, follow. [drawn] Ending is this postup's status; others may still be live nearby. [M1031-draft]
   - next site states: back (Back), postup-ended+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none

## Connected flows [M1025]
- none

## Screens
1. `#postup-full` · auth=in live=live — Full. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
2. `#postup-cancelled` · auth=in live=live — Cancelled. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-cancelled)
3. `#postup-full` · auth=in live=live — Back to the full postup (split: a cancelled postup doesn't later end). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
4. `#postup-ended` · auth=in live=live — Ended: see what's nearby, follow. [drawn] Ending is this postup's status; others may still be live nearby. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ended)

## Success criteria
- Never a blank page. [F060]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
