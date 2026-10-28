# Flow: Ask to join, then get approved (joiner side) (`ask-join`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/ask-join.html

## Persona
- Signed-in user; poster approves who joins.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Send a reason, get a yes, meet up. [M1024]

## Steps
1. **postup-ask@in.live** · user: Interested, but the host screens people · action: opens an ask-to-join postup · edge: entry
   - "Tess approves who joins". [FS] [F055]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **ask@in.live** (Ask to join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: cautious-joiner step 7 (if Comparing with another option), catch-up step 4 (if My request was approved)
2. **ask@in.live** · user: Explaining why they want to join · action: taps Ask to join · edge: tap: Ask to join
   - Short reason. [F061] [F095]
   - next site states: back (Back), ask+share@in.live (Share), ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **requested@in.live** (Send request), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: none
3. **requested@in.live** · user: Waiting for an answer · action: sends the request · edge: tap: Send request
   - Request sent; can cancel. [FS] [drawn]
   - next site states: home@in.live.live (Close), quiet-feed@in.live (See who else is nearby), postup-ask@in.live (View postup), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
4. **activity@in.live** · user: Gets the yes · action: later: alert arrives · edge: event: alert arrives
   - Activity: "Tess said yes". [FS] [M1024]
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), **chat@in.live** (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: host-approve step 1 (if Hosting; someone wants in), catch-up step 3 (if What else happened?), following step 4 (if Hears that someone posted up)
5. **chat@in.live** · user: Now part of the group · action: opens the chat · edge: tap: M Maya: Hey! Here till 4 — come sa
   - Now in the postup chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

## Connected flows [M1025]
- `catch-up`: branch out at step 1→4, step 4→3; merge in at step 1 (from its step 4), step 4 (from its step 3)
- `cautious-joiner`: branch out at step 1→7; merge in at step 1 (from its step 7)
- `following`: branch out at step 4→4; merge in at step 4 (from its step 4)
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

## Screens
1. `#postup-ask` · auth=in live=live — "Tess approves who joins". [FS] [F055] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
2. `#ask` · auth=in live=live — Short reason. [F061] [F095] (/mockups/?style=fresh&device=phone&auth=in&live=live#ask)
3. `#requested` · auth=in live=live — Request sent; can cancel. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#requested)
4. `#activity` · auth=in live=live — Activity: "Tess said yes". [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
5. `#chat` · auth=in live=live — Now in the postup chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

## Branches and edge cases
- Signed out: Ask to join → #ask-signin → #ask. [FS]
- Declined or no answer before the postup ends: shown in Activity, no chat. [unsourced] [M1024]
- Cafe name before approval: hidden or shown? [F070] [R23]

## Success criteria
- Joiner learns the outcome without refreshing. [F095] [M1024]

## Needs Martin's decision
- Show the cafe name before approval? (drawing shows it, code hides it) [F070] [R23]
- What the joiner sees if never answered. [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
