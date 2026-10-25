# Flow: Share link to a project (`invite-project`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: project@out.live (See updates), **invite-project+signin@out.live** (Follow), profile@out.live (Next postup: weekdays at Bean Theo)
   - enterable flows: none
2. **invite-project+signin@out.live** · user: Wants updates · action: taps Follow 🔒 · edge: sheet: Follow
   - Follow 🔒 → sign-in sheet. [FS] [M1024]
   - next site states: invite-project@out.live (close), invite-project@in.live (signs in)
   - enterable flows: none
3. **project@in.live** · user: Following · action: signs in · edge: 2 taps: signs in, then See updates
   - Following; live postups for the project shown. [FS] [M1024]
   - next site states: back (Back), project-new@in.live (New), profile@in.live (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 3 (if Wants proof Maya is legit: what is she building?)

## Connected flows [M1025]
- `cautious-joiner`: branch out at step 3→3; merge in at step 3 (from its step 3)

## Screens
1. `#invite-project` · auth=out live=live — "Maya is building Star Fox 64 mod". [FS] [F067] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite-project)
2. `#invite-project` + sheet `signin` · auth=out live=live — Follow 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite-project)
3. `#project` · auth=in live=live — Following; live postups for the project shown. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)

## Branches and edge cases
- Project owner is live now: join from the project. [FS] [M1024]

## Success criteria
- Follow survives sign-in. [M1018] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
