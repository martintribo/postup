# Flow: Postup chat (`chat`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/chat.html

## Persona
- Signed-in poster or joiner.

## Starting state
- auth=in · live=live · device=phone · entry URL `/inbox`

## Goal
- Coordinate in the group chat. [M1024]

## Steps
1. **inbox-one@in.live** · user: Wants to check messages · action: opens Inbox · edge: entry
   - Inbox: one list of postup chats, newest first, unread dots. [F096] [M1033]
   - next site states: **chat@in.live** (Maya's postup · Bean Theory), profile@in.live (Ari followed you), postup-ended@in.live (Tess's postup · Grindhouse), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none
2. **chat@in.live** · user: Wants to sort out details in chat · action: opens a chat · edge: tap: Maya's postup · Bean Theory
   - One chat per postup. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), **chat+msg@in.live** (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox-one@in.live (Inbox), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none
3. **chat+msg@in.live** · user: Something off about a message · action: long-presses a message · edge: tap: Message options
   - Long-press: copy, report, block sender. [F096] [FS]
   - next site states: chat@in.live (close), report@in.live (Report message), chat+block@in.live (Block sender)
   - enterable flows: none

## Connected flows [M1025]
- none

## Screens
1. `#inbox-one` · auth=in live=live — Inbox: one list of postup chats, newest first, unread dots. [F096] [M1033] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox-one)
2. `#chat` · auth=in live=live — One chat per postup. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)
3. `#chat` + sheet `msg` · auth=in live=live — Long-press: copy, report, block sender. [F096] [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=msg#chat)

## Branches and edge cases
- Signed out: sign-in sheet over Inbox. [unsourced]
- Chat closes 24h after the postup. [R31] [FS]

## Success criteria
- Only poster + joined/approved can read. [F061]

## Needs Martin's decision
- Chat retention (24h default). [R31] [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
