# Flow: Catch up on what happened (`catch-up`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/catch-up.html

## Persona
- Registered user coming back after a while away.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- See what happened since last time: replies, approvals, ended postups. [M1031-draft]

## Steps
1. **home@in.live.live** · user: What did I miss? · action: comes back and opens / · edge: entry
   - Home in Live mode; Inbox tab shows an unread dot. [drawn] [M1031-draft]
   - next site states: postup@in.live (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), **inbox@in.live** (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing)
2. **inbox@in.live** · user: Checks messages first · action: taps Inbox · edge: tap: Inbox
   - Chats: group chats, newest first, including an ended postup. [drawn] [M1031-draft]
   - next site states: chat@in.live (Maya's postup · Bean Theory), postup-ended@in.live (Tess's postup · Grindhouse), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), **activity@in.live** (Activity 2), projects@in.live (Projects)
   - enterable flows: chat step 1 (if Wants to check messages)
3. **activity@in.live** · user: What else happened? · action: taps Activity · edge: tap: Activity 2
   - Activity: joins, requests, approvals, follows, messages. [drawn] [M1031-draft]
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), **postup-ask@in.live** (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), following step 4 (if Hears that someone posted up)
4. **postup-ask@in.live** · user: My request was approved · action: taps "Tess said yes to your request" · edge: tap: T Tess said yes to your request Ye
   - Tess's postup. [drawn] [M1031-draft]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), ask@in.live (Ask to join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: ask-join step 1 (if Interested, but the host screens people)
5. **activity@in.live** · user: Back to the list · action: taps Back · edge: back
   - Activity again. [drawn] [M1031-draft]
   - next site states: **inbox@in.live** (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), following step 4 (if Hears that someone posted up)
6. **inbox@in.live** · user: Any replies? · action: taps Chats · edge: tap: Chats
   - Chats list. [drawn] [M1031-draft]
   - next site states: chat@in.live (Maya's postup · Bean Theory), **postup-ended@in.live** (Tess's postup · Grindhouse), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), activity@in.live (Activity 2), projects@in.live (Projects)
   - enterable flows: chat step 1 (if Wants to check messages)
7. **postup-ended@in.live** · user: That one's over · action: taps Tess's ended postup · edge: tap: T Tess's postup Ended · Tue Tue
   - Ended postup: see what's nearby, follow. [drawn] [M1031-draft]
   - next site states: back (Back), postup-ended+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), **inbox@in.live** (Inbox), projects@in.live (Projects)
   - enterable flows: none
8. **inbox@in.live** · user: Back to chats · action: taps Back · edge: back
   - Chats list. [drawn] [M1031-draft]
   - next site states: **chat@in.live** (Maya's postup · Bean Theory), postup-ended@in.live (Tess's postup · Grindhouse), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), activity@in.live (Activity 2), projects@in.live (Projects)
   - enterable flows: chat step 1 (if Wants to check messages)
9. **chat@in.live** · user: Reads the replies · action: opens Maya's postup chat · edge: tap: M Maya's postup Maya: Grabbing ano
   - Group chat with the latest replies. [drawn] [M1031-draft]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

## Connected flows [M1025]
- `ask-join`: branch out at step 3→4, step 4→1, step 5→4; merge in at step 3 (from its step 4), step 5 (from its step 4)
- `following`: branch out at step 3→4, step 5→4; merge in at step 3 (from its step 4), step 5 (from its step 4)
- `chat`: branch out at step 2→1, step 6→1, step 9→2; merge in at —
- `host-approve`: branch out at step 3→1, step 5→1; merge in at —
- `join`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Home in Live mode; Inbox tab shows an unread dot. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=2#home)
2. `#inbox` · auth=in live=live — Chats: group chats, newest first, including an ended postup. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#inbox)
3. `#activity` · auth=in live=live — Activity: joins, requests, approvals, follows, messages. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
4. `#postup-ask` · auth=in live=live — Tess's postup. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-ask)
5. `#activity` · auth=in live=live — Activity again. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
6. `#inbox` · auth=in live=live — Chats list. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#inbox)
7. `#postup-ended` · auth=in live=live — Ended postup: see what's nearby, follow. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-ended)
8. `#inbox` · auth=in live=live — Chats list. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#inbox)
9. `#chat` · auth=in live=live — Group chat with the latest replies. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#chat)

## Branches and edge cases
- Nothing happened while away: Activity and Chats need a positive empty state, never "quiet". [F035] [M1031-draft]

## Success criteria
- From Home, the user reaches replies, an approval and an ended postup through the Inbox. [M1031-draft]

## Needs Martin's decision
- No "since you were away" summary exists; catching up means opening Inbox, then each item. [M1031-draft]
- No unread or new markers per item beyond the Activity count badge; there is no way to tell what is new since last visit. [M1031-draft]
- An approval ("Tess said yes") opens Tess's postup as Ask to join, not a joined/approved state. [M1031-draft]
- Ended postups appear only in Chats ("Tess's postup · Ended"), not as an Activity alert. [M1031-draft]
- Replies show as one Activity row per message linking to the group chat; there is no reply thread view. [M1031-draft]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
