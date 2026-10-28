# Flow: Share link to a project (`invite-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-project.html

## Persona
- Signed-out visitor opening postup.now/project/… .

## Starting state
- auth=out · live=live · device=phone · entry URL `/project/…`

## Goal
- Follow the project to hear about the next postup. [M1024]

## Steps
1. **invite-project@out.live** · user: Friend's project link; curious about it · action: opens the project link · edge: entry
   - "Maya is building Star Fox 64 mod". [FS] [F067]
   - next site states: project@out.live (See updates), **invite-project+signin@out.live** (Follow), profile@out.live (Next postup: weekdays at Bean Theo), home@out.live.live (home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox-one@out.live (Inbox), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none
2. **invite-project+signin@out.live** · user: Wants updates · action: taps Follow 🔒 · edge: tap: Follow
   - Follow 🔒 → sign-in sheet. [FS] [M1024]
   - next site states: invite-project@out.live (close), **invite-project@in.live** (Continue with Apple)
   - enterable flows: none
3. **invite-project@in.live** · user: Signed in; following · action: signs in · edge: tap: Continue with Apple
   - Sign-in returns to the same page, now following (Follow has no continuation). [M1031-draft]
   - next site states: **project@in.live** (See updates), profile@in.live (Next postup: weekdays at Bean Theo), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox-one@in.live (Inbox), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none
4. **project@in.live** · user: Following · action: taps See updates · edge: tap: See updates
   - Following; live postups for the project shown. [FS] [M1024]
   - next site states: back (Back), project-new@in.live (New), profile@in.live (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox-one@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails)), inbox@in.live (Inbox (later design: two-tab Inbox (phase 2) [M1033]))
   - enterable flows: none

## Connected flows [M1025]
- none

## Screens
1. `#invite-project` · auth=out live=live — "Maya is building Star Fox 64 mod". [FS] [F067] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite-project)
2. `#invite-project` + sheet `signin` · auth=out live=live — Follow 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite-project)
3. `#invite-project` · auth=in live=live — Sign-in returns to the same page, now following (Follow has no continuation). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#invite-project)
4. `#project` · auth=in live=live — Following; live postups for the project shown. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)

## Branches and edge cases
- Project owner is live now: join from the project. [FS] [M1024]

## Success criteria
- Follow survives sign-in. [M1018] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
