# Flow: Host approves a request (`host-approve`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/host-approve.html

## Persona
- Signed-in poster with an ask-to-join postup.

## Starting state
- auth=in · live=live · device=phone · entry URL `/live`

## Goal
- Approve or decline with the joiner's reason in view. [M1024]

## Steps
1. **activity@in.live** · user: Hosting; someone wants in · action: later: alert arrives · edge: entry
   - Alert: "Ari asked to join". [FS]
   - next site states: inbox@in.live (Chats), **live@in.live** (D Dev asked to join your postup 2 ), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects)
   - enterable flows: ask-join step 4 (if Gets the yes), following step 3 (if Hears that someone posted up)
2. **live@in.live** · user: Deciding on the request · action: opens the request · edge: tap: D Dev asked to join your postup 2 
   - Requests with reason: Approve / Decline. [FS] [F061]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), **profile@in.live** (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time)
3. **profile@in.live** · user: Wants to check the asker first · action: taps the asker · edge: tap: D Dev · 2 min ago
   - Optionally checks the asker's profile first. [FS] [M1024]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod Updated yesterday), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 4 (if Checking Maya's track record)
4. **chat@in.live** · user: Approved; welcoming them · action: opens the chat · edge: back, then tap: M Maya: Hey! Here till 4 — come sa
   - Approved people are in the chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options)
   - enterable flows: chat step 2 (if Coordinating)

## Connected flows [M1025]
- `ask-join`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `following`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `returning-post`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `cautious-joiner`: branch out at step 3→4; merge in at step 3 (from its step 4)
- `chat`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `hosting`: branch out at step 2→1; merge in at —

## Screens
1. `#activity` · auth=in live=live — Alert: "Ari asked to join". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
2. `#live` · auth=in live=live — Requests with reason: Approve / Decline. [FS] [F061] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
3. `#profile` · auth=in live=live — Optionally checks the asker's profile first. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
4. `#chat` · auth=in live=live — Approved people are in the chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

## Branches and edge cases
- Decline: joiner is told politely. [F095] [unsourced]
- Block from the request via More. [F059] [M1024]

## Success criteria
- Approve in one tap from #live. [FS] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
