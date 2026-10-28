# Flow: Slow network and offline (`loading-offline`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/loading-offline.html

## Persona
- Anyone on bad wifi.

## Starting state
- auth=in · live=live · device=phone · entry URL `/nearby`

## Goal
- Keep showing something useful. [M1024]

## Steps
1. **loading@in.live** · user: Opened the feed on bad wifi · action: opens Nearby · edge: entry
   - Skeleton. [FS] [F060]
   - next site states: home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none
2. **offline@in.live** · user: Connection dropped · action: later: network drops · edge: event: network drops
   - Cached feed + offline banner + Retry. [FS]
   - next site states: me@in.live (S), quiet@in.live (quiet), **quiet-feed@in.live** (Retry), post@in.live (Post up), cafe@in.live (Maya's photo), project@in.live (Star Fox 64 mod), home@in.live.live (Home), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: none
3. **quiet-feed@in.live** · user: Back online · action: taps Retry · edge: tap: Retry
   - Retry succeeds. [FS]
   - next site states: me@in.live (S), quiet@in.live (quiet), post@in.live (Post up), cafe@in.live (Maya's photo), project@in.live (Star Fox 64 mod), home@in.live.live (Home), projects@in.live (Projects), inbox@in.live (Inbox), **cafe-gfail@in.live** (Maya's photo (Google card fails))
   - enterable flows: none
4. **cafe-gfail@in.live** · user: Checking a cafe; Google is down · action: taps a cafe · edge: tap: Maya's photo (Google card fails)
   - Google card failed: rest of cafe still works. [F060]
   - next site states: back (Back), cafe-gfail+share@in.live (Share), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod), postup@in.live (Join), cafe-gfail+dirs@in.live (Open in Maps), post@in.live (Post up here), home@in.live.live (Home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S)
   - enterable flows: none

## Connected flows [M1025]
- none

## Screens
1. `#loading` · auth=in live=live — Skeleton. [FS] [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#loading)
2. `#offline` · auth=in live=live — Cached feed + offline banner + Retry. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#offline)
3. `#quiet-feed` · auth=in live=live — Retry succeeds. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#quiet-feed)
4. `#cafe-gfail` · auth=in live=live — Google card failed: rest of cafe still works. [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe-gfail)

## Branches and edge cases
- First visit while offline: nothing cached (fails in the build today). [unsourced]

## Success criteria
- No blank screens. [FS]

## Needs Martin's decision
- Full offline screen vs banner only. [R46⚠] [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
