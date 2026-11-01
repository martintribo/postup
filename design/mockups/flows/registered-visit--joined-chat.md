# Flow: Registered visit → Chats with the group (`registered-visit--joined-chat`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/registered-visit--joined-chat.html

## Persona
- Signed-in user. Arrives at / (someone live nearby or not), from a link a friend sent, or back while hosting or joined.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Get to a postup, post up, or follow or post a project, from whichever way they arrive. [M1044]

## Steps
1. **joined@in.live** · user: Plans changed · action: opens their joined postup · edge: entry
   - Leave link. [drawn]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), **inbox@in.live** (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: registered-visit step 3 (if Decides to join), registered-visit--joined step 1 (if Plans changed), registered-visit--joined-project step 1 (if Plans changed)
2. **inbox@in.live** · user: Wants to check messages · action: opens Inbox · edge: tap: Inbox
   - Inbox: one list of postup chats, newest first, unread dots. [F096] [M1033]
   - next site states: **chat@in.live** (Maya's postup · Bean Theory), postup-ended@in.live (Tess's postup · Grindhouse), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), activity@in.live (Activity 2), projects@in.live (Projects)
   - enterable flows: catch-up step 2 (if Checks messages first)
3. **chat@in.live** · user: Wants to sort out details in chat · action: opens a chat · edge: tap: Maya's postup · Bean Theory
   - One chat per postup. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), **chat+msg@in.live** (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
4. **chat+msg@in.live** · user: Something off about a message · action: long-presses a message · edge: tap: Message options
   - Long-press: copy, report, block sender. [F096] [FS]
   - next site states: chat@in.live (close), report@in.live (Report message), chat+block@in.live (Block sender)
   - enterable flows: none

## Connected flows [M1025]
- `registered-visit`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `catch-up`: branch out at step 2→2; merge in at step 2 (from its step 2)
- `registered-visit--joined`: branch out at step 1→1; merge in at —
- `registered-visit--joined-project`: branch out at step 1→1; merge in at —

## Screens
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#joined)
2. `#inbox` · auth=in live=live — Inbox: one list of postup chats, newest first, unread dots. [F096] [M1033] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#inbox)
3. `#chat` · auth=in live=live — One chat per postup. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#chat)
4. `#chat` + sheet `msg` · auth=in live=live — Long-press: copy, report, block sender. [F096] [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=msg&ph=1#chat)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
