# Flow: Report and block (`safety`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/safety.html

## Persona
- Signed-in user uncomfortable with someone.

## Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

## Goal
- Report and block quickly. [F059] [M1024]

## Steps
1. **postup+more@in.live** · user: Uncomfortable with someone · action: taps More · edge: entry
   - More: profile, share, report, block. [FS] [F059]
   - next site states: postup@in.live (close), profile@in.live (View profile), postup+share@in.live (Share), **report@in.live** (Report), postup+block@in.live (Block)
   - enterable flows: none
2. **report@in.live** · user: Wants to report · action: taps Report · edge: tap: Report
   - Reason + details. [F059] [drawn]
   - next site states: back (Back), **reported@in.live** (Send report), home@in.live.live (home), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: none
3. **reported@in.live** · user: Reported; still uneasy · action: sends the report · edge: tap: Send report
   - Thanks; offer to block. [FS]
   - next site states: home@in.live.live (Close), **reported+block@in.live** (Block Maya too), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: none
4. **reported+block@in.live** · user: Wants them gone · action: taps Block too · edge: tap: Block Maya too
   - Block: neither sees the other; they aren't told. [FS] [F059]
   - next site states: reported@in.live (close), home@in.live.live (Block), **settings@in.live** (Blocked people (Settings))
   - enterable flows: none
5. **settings@in.live** · user: Might undo later · action: opens Settings · edge: tap: Blocked people (Settings)
   - Blocked people list to undo. [FS] [F065]
   - next site states: back (Back), home@out.live.live (Sign out), settings+delacct@in.live (Delete account), home@in.live.live (home), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: delete-account step 2 (if Looking for the delete option), settings-notify step 1 (if Tuning alerts)

## Connected flows [M1025]
- `delete-account`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `settings-notify`: branch out at step 5→1; merge in at —

## Screens
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more&ph=1#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#reported)
4. `#reported` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block&ph=1#reported)
5. `#settings` · auth=in live=live — Blocked people list to undo. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#settings)

## Branches and edge cases
- From a chat message: Message options → Report message. [F096]

## Success criteria
- No safety-tip screens. [F059] [FS]

## Needs Martin's decision
- No ban system yet: who reviews reports? [TK§4]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
