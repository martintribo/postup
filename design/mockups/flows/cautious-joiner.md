# Flow: Cautious joiner checks a few postups, then joins (`cautious-joiner`)
Priority: **MVP must** · Status: Martin's example (Oct 24) [M1024]
Player: /mockups/flows/cautious-joiner.html

## Persona
- Registered user, signed in, wants company but checks people out first.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Join a live postup after comparing a few. [M1024]

## Steps
1. **home@in.live.live** · user: Wants company today, but careful about who · action: arrives at / · edge: entry
   - Opens / in Live mode: map + Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: quick-joiner step 1 (if Knows a friend is live; wants to go now), desktop-browse step 1 (if At a laptop; browsing)
2. **postup@in.live** · user: Interested in Maya, not sure yet · action: taps Maya's row · edge: tap: M 2
   - Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), **project@in.live** (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)
3. **project@in.live** · user: Wants proof Maya is legit: what is she building? · action: taps the project tag · edge: tap: Star Fox 64 mod Adding a new Corne
   - Opens Maya's project to see what she's working on, then Back. [FS] [M1024]
   - next site states: back (Back), project-new@in.live (New), **profile@in.live** (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **profile@in.live** · user: Checking Maya's track record · action: taps Maya (owner) · edge: tap: Maya
   - Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), **cafe@in.live** (Bean Theory), project@in.live (Star Fox 64 mod Updated yesterday), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: host-approve step 3 (if Wants to check the asker first)
5. **cafe@in.live** · user: Is the place itself OK? · action: taps the cafe · edge: tap: Bean Theory
   - Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024]
   - next site states: back (Back), cafe+share@in.live (Share), project@in.live (Star Fox 64 mod), postup@in.live (Join), post@in.live (Post up here), **home@in.live.live** (Home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none
6. **home@in.live.live** · user: Wants to compare with someone else · action: taps Home · edge: tap: Home
   - Back on Home: Live now shows Tess, marked Ask to join. [M1025]
   - next site states: postup@in.live (M 2), **postup-ask@in.live** (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: quick-joiner step 1 (if Knows a friend is live; wants to go now), desktop-browse step 1 (if At a laptop; browsing)
7. **postup-ask@in.live** · user: Comparing with another option · action: taps Tess (Ask to join) · edge: tap: T
   - Compares a second postup (Tess approves who joins), then Back. [FS] [M1024]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), ask@in.live (Ask to join), **home@in.live.live** (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: ask-join step 1 (if Interested, but the host screens people)
8. **home@in.live.live** · user: Done comparing; back to the list · action: taps Back · edge: back
   - Back from Tess's postup lands on Home, not on Maya's postup (split from one "back to Maya's postup" step). [M1031-draft]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (cafe), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: quick-joiner step 1 (if Knows a friend is live; wants to go now), desktop-browse step 1 (if At a laptop; browsing)
9. **postup@in.live** · user: Decided: Maya it is · action: taps Maya's row again · edge: tap: M 2
   - Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)
10. **joined@in.live** · user: Committed; needs to get there · action: taps Join · edge: tap: Join
   - You're joining Maya; Maya is told. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), **joined+dirs@in.live** (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), me@in.live (S), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: quick-joiner step 3 (if Decides to just join now), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
11. **joined+dirs@in.live** · user: On the way · action: taps Directions · edge: tap: Directions
   - Directions sheet: Apple / Google Maps. [FS] [M1024]
   - next site states: joined@in.live (close)
   - enterable flows: quick-joiner step 4 (if Needs the route)

## Connected flows [M1025]
- `quick-joiner`: branch out at step 2→2, step 6→1, step 11→4; merge in at —
- `desktop-browse`: branch out at step 2→2, step 6→1, step 9→2; merge in at —
- `host-approve`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `invite-live`: branch out at step 10→3; merge in at step 10 (from its step 3)
- `ask-join`: branch out at step 7→1; merge in at —
- `leave`: branch out at step 10→1; merge in at —

## Screens
1. `#home` · auth=in live=live mode=live — Opens / in Live mode: map + Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#project` · auth=in live=live — Opens Maya's project to see what she's working on, then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)
4. `#profile` · auth=in live=live — Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
5. `#cafe` · auth=in live=live — Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe)
6. `#home` · auth=in live=live mode=live — Back on Home: Live now shows Tess, marked Ask to join. [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
7. `#postup-ask` · auth=in live=live — Compares a second postup (Tess approves who joins), then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
8. `#home` · auth=in live=live mode=live — Back from Tess's postup lands on Home, not on Maya's postup (split from one "back to Maya's postup" step). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
9. `#postup` · auth=in live=live — Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
10. `#joined` · auth=in live=live — You're joining Maya; Maya is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
11. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)

## Branches and edge cases
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

## Success criteria
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
