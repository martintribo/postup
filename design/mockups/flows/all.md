# PostUp critical flows
Critical flows (Martin, Oct 24 2026 [M1024]): a type of user arrives in a certain situation and goes through a scenario step by step. Each step names the screen and the scenario params (auth, live, Home mode, sheet). Flows marked Draft were inferred from the screen notes; confirm with Martin.

- [cautious-joiner](cautious-joiner.md) · MVP must · Cautious joiner checks a few postups, then joins
- [quick-joiner](quick-joiner.md) · MVP must · Quick joiner
- [first-visit-live](first-visit-live.md) · MVP must · Curious visitor joins someone live
- [curious-browser](curious-browser.md) · MVP must · Curious browser: live now, then past content
- [stumbled](stumbled.md) · MVP must · Stumbled on it: what is this?
- [invite-live](invite-live.md) · MVP must · Share link to a live postup
- [invite-ended](invite-ended.md) · MVP must · Share link to an ended postup
- [invite-project](invite-project.md) · MVP must · Share link to a project
- [ask-join](ask-join.md) · MVP must · Ask to join, then get approved (joiner side)
- [host-approve](host-approve.md) · MVP must · Host approves a request
- [first-post](first-post.md) · MVP must · Came to post up: first post with sign-in
- [returning-post](returning-post.md) · MVP must · Returning poster
- [hosting](hosting.md) · MVP must · Hosting live: extend, edit, end
- [project-builder](project-builder.md) · MVP must · Project builder: create, update, post up for it
- [following](following.md) · MVP must · Follow a person or project
- [chat](chat.md) · MVP must · Postup chat
- [safety](safety.md) · MVP must · Report and block
- [leave](leave.md) · MVP must · Leave a postup you joined
- [postup-states](postup-states.md) · MVP must · Postup ends, fills or is cancelled while you look
- [empty-area](empty-area.md) · MVP must · Empty area: be the first
- [loading-offline](loading-offline.md) · MVP must · Slow network and offline
- [delete-account](delete-account.md) · MVP must · Delete account
- [desktop-browse](desktop-browse.md) · nice · Desktop browse and post
- [settings-notify](settings-notify.md) · nice · Notification settings and sign out

## Flow: Cautious joiner checks a few postups, then joins (`cautious-joiner`)
Priority: **MVP must** · Status: Martin's example (Oct 24) [M1024]
Player: /mockups/flows/cautious-joiner.html

### Persona
- Registered user, signed in, wants company but checks people out first.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Join a live postup after comparing a few. [M1024]

### Steps
1. **home@in.live.live** · user: Wants company today, but careful about who · action: arrives at / · edge: entry
   - Opens / in Live mode: map + Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: quick-joiner step 1 (if Knows a friend is live; wants to go now), desktop-browse step 1 (if At a laptop; browsing)
2. **postup@in.live** · user: Interested in Maya, not sure yet · action: taps Maya's row · edge: tap: M 2
   - Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), **project@in.live** (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)
3. **project@in.live** · user: Wants proof Maya is legit: what is she building? · action: taps the project tag · edge: tap: Star Fox 64 mod Adding a new Corne
   - Opens Maya's project to see what she's working on, then Back. [FS] [M1024]
   - next site states: back (Back), project-new@in.live (New), **profile@in.live** (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **profile@in.live** · user: Checking Maya's track record · action: taps Maya (owner) · edge: tap: Maya
   - Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), **cafe@in.live** (Bean Theory), project@in.live (Star Fox 64 mod Updated yesterday), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: host-approve step 3 (if Wants to check the asker first)
5. **cafe@in.live** · user: Is the place itself OK? · action: taps the cafe · edge: tap: Bean Theory
   - Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024]
   - next site states: back (Back), cafe+share@in.live (Share), project@in.live (Star Fox 64 mod), postup@in.live (Join), post@in.live (Post up here), **home@in.live.live** (Home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails)), cafe-gfail@in.none (postups end (Google card fails))
   - enterable flows: none
6. **home@in.live.live** · user: Wants to compare with someone else · action: taps Home · edge: tap: Home
   - Back on Home: Live now shows Tess, marked Ask to join. [M1025]
   - next site states: postup@in.live (M 2), **postup-ask@in.live** (T), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: quick-joiner step 1 (if Knows a friend is live; wants to go now), desktop-browse step 1 (if At a laptop; browsing)
7. **postup-ask@in.live** · user: Comparing with another option · action: taps Tess (Ask to join) · edge: tap: T
   - Compares a second postup (Tess approves who joins), then Back. [FS] [M1024]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), ask@in.live (Ask to join), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: ask-join step 1 (if Interested, but the host screens people)
8. **postup@in.live** · user: Decided: Maya it is · action: back to Maya's postup · edge: back
   - Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)
9. **joined@in.live** · user: Committed; needs to get there · action: taps Join · edge: tap: Join
   - You're joining Maya; Maya is told. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), **joined+dirs@in.live** (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: quick-joiner step 3 (if Committed), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
10. **joined+dirs@in.live** · user: On the way · action: taps Directions · edge: sheet: Directions
   - Directions sheet: Apple / Google Maps. [FS] [M1024]
   - next site states: joined@in.live (close)
   - enterable flows: quick-joiner step 4 (if Needs the route)

### Connected flows [M1025]
- `quick-joiner`: branch out at step 2→2, step 6→1, step 10→4; merge in at step 8 (from its step 2)
- `desktop-browse`: branch out at step 2→2, step 6→1, step 8→2; merge in at step 8 (from its step 2)
- `host-approve`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `invite-live`: branch out at step 9→3; merge in at step 9 (from its step 3)
- `ask-join`: branch out at step 7→1; merge in at —
- `leave`: branch out at step 9→1; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Opens / in Live mode: map + Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#project` · auth=in live=live — Opens Maya's project to see what she's working on, then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)
4. `#profile` · auth=in live=live — Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
5. `#cafe` · auth=in live=live — Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe)
6. `#home` · auth=in live=live mode=live — Back on Home: Live now shows Tess, marked Ask to join. [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
7. `#postup-ask` · auth=in live=live — Compares a second postup (Tess approves who joins), then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
8. `#postup` · auth=in live=live — Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
9. `#joined` · auth=in live=live — You're joining Maya; Maya is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
10. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)

### Branches and edge cases
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

### Success criteria
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

---

## Flow: Quick joiner (`quick-joiner`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/quick-joiner.html

### Persona
- Registered user who already knows someone nearby is live.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Join in two taps and get directions. [M1024]

### Steps
1. **home@in.live.live** · user: Knows a friend is live; wants to go now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: cautious-joiner step 1 (if Wants company today, but careful about who), desktop-browse step 1 (if At a laptop; browsing)
2. **postup@in.live** · user: Found them; joining · action: taps the row · edge: tap: M 2
   - Taps a row, then Join. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), desktop-browse step 2 (if Checking one postup)
3. **joined@in.live** · user: Committed · action: taps Join · edge: tap: Join
   - Confirmation. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), **joined+dirs@in.live** (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 9 (if Committed; needs to get there), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)
4. **joined+dirs@in.live** · user: Needs the route · action: taps Directions · edge: sheet: Directions
   - Directions. [FS] [M1024]
   - next site states: joined@in.live (close)
   - enterable flows: none
5. **chat@in.live** · user: Wants to say they're coming · action: opens the group chat · edge: 2 taps: close, then Group chat
   - Says "on my way" in the postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options)
   - enterable flows: chat step 2 (if Coordinating)

### Connected flows [M1025]
- `invite-live`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `cautious-joiner`: branch out at step 2→2; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —
- `leave`: branch out at step 3→1; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps a row, then Join. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#joined` · auth=in live=live — Confirmation. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)
5. `#chat` · auth=in live=live — Says "on my way" in the postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]

### Success criteria
- Home → joined in 2 taps. [M1024]

---

## Flow: Curious visitor joins someone live (`first-visit-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit-live.html

### Persona
- New visitor, signed out, curious; lands on / with live postups nearby.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- Understand the site and join someone; sign in only at Join. [M1024]

### Steps
1. **home@out.live.live** · user: Curious; sees people live right now · action: arrives at / · edge: entry
   - Home opens in Live mode with a one-line welcome. [M1018b] [M1024]
   - next site states: **postup@out.live** (M 2), postup-ask@out.live (T), cafe@out.live (tap), home@out.live.building (Building), quiet@out.live (Locate), project@out.live (Star Fox 64 mod), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live ( (Google card fails))
   - enterable flows: curious-browser step 1 (if Curious what is on the site), stumbled step 1 (if No idea what PostUp is)
2. **postup@out.live** · user: Tempted by one postup · action: taps a live row · edge: tap: M 2
   - Opens a postup; Join shows 🔒. [FS] [M1024]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **join-signin@out.live** (Join), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: curious-browser step 2 (if Peeking at who is live), stumbled step 2 (if Trying to understand by example)
3. **join-signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: back (Back), join-signin+share@out.live (Share), join-signin+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (signs in), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: invite-live step 2 (if Wants to join the friend)
4. **joined@in.live** · user: Signed in; committed · action: signs in · edge: sign-in: signs in
   - Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 9 (if Committed; needs to get there), quick-joiner step 3 (if Committed), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)

### Connected flows [M1025]
- `cautious-joiner`: branch out at step 4→9; merge in at step 4 (from its step 9)
- `quick-joiner`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `invite-live`: branch out at step 4→3; merge in at step 3 (from its step 2)
- `curious-browser`: branch out at step 2→2; merge in at —
- `stumbled`: branch out at step 2→2; merge in at —
- `leave`: branch out at step 4→1; merge in at —

### Screens
1. `#home` · auth=out live=live mode=live — Home opens in Live mode with a one-line welcome. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Opens a postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#join-signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#join-signin)
4. `#joined` · auth=in live=live — Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)

### Branches and edge cases
- Not now on the sheet: stays on the postup, still signed out. [drawn] [M1024]
- Switches to Building to look at projects first. [M1018b] [M1024]

### Success criteria
- No sign-in before an action. [FS]
- After sign-in the original action completes. [M1018] [M1024]

---

## Flow: Curious browser: live now, then past content (`curious-browser`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/curious-browser.html

### Persona
- First-time visitor, signed out, who has heard of PostUp and wants to see what is on it: who is live and what people have made.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- See live and past content, then follow someone, signing in only at Follow. [M1025]

### Steps
1. **home@out.live.live** · user: Curious what is on the site · action: arrives at / · edge: entry
   - Live now list: who is working where. [M1018b] [M1025]
   - next site states: **postup@out.live** (M 2), postup-ask@out.live (T), cafe@out.live (tap), home@out.live.building (Building), quiet@out.live (Locate), project@out.live (Star Fox 64 mod), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live ( (Google card fails))
   - enterable flows: first-visit-live step 1 (if Curious; sees people live right now), stumbled step 1 (if No idea what PostUp is)
2. **postup@out.live** · user: Peeking at who is live · action: taps a live row · edge: tap: M 2
   - Peeks at a live postup, then Back. [FS] [M1025]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), join-signin@out.live (Join), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit-live step 2 (if Tempted by one postup), stumbled step 2 (if Trying to understand by example)
3. **home@out.live.building** · user: Wants past content too · action: back, switches to Building · edge: back, then mode: Building
   - Switches to Building for past content. [M1018b] [M1025]
   - next site states: home@out.live.live (Live), me@out.live (S), **projects@out.live** (See all projects), project@out.live (Star Fox 64 mod M Maya · Yesterday), post@out.live (Post up), cafe@out.live (Lantern Tea A D M 3 postups), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), cafe-gfail@out.live (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: stumbled step 4 (if Still unsure; looks around)
4. **projects@out.live** · user: Browsing what people build · action: taps See all projects · edge: tap: See all projects
   - See all projects, closest first. [M1018c] [FS]
   - next site states: project-new@out.live (New project), **project@out.live** (Star Fox 64 mod M Maya · Yesterday), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), inbox@out.live (Inbox)
   - enterable flows: none
5. **project@out.live** · user: Interested in one project · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Opens a project: updates and past postups. [FS] [M1025]
   - next site states: back (Back), project-new@out.live (New), **profile@out.live** (Maya), project-update@out.live (Update), project-attach@out.live (Post up), cafe@out.live (Bean Theory), postup@out.live (M Maya Bean Theory · till 4pm Live), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
6. **profile@out.live** · user: Who is behind it? · action: taps the owner · edge: tap: Maya
   - Opens the maker's profile: past postups, regular cafes. [FS] [F065] [M1025]
   - next site states: back (Back), profile+more@out.live (More), postup@out.live (Live at Bean Theory Till 4pm · Sta), **profile+signin@out.live** (Follow), cafe@out.live (Bean Theory), project@out.live (Star Fox 64 mod Updated yesterday), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
7. **profile+signin@out.live** · user: Wants to keep up with them · action: taps Follow 🔒 · edge: sheet: Follow
   - Taps Follow: soft sign-in sheet; Not now keeps browsing. [FS] [M1018] [M1025]
   - next site states: profile@out.live (close), **profile@in.live** (signs in)
   - enterable flows: none
8. **profile@in.live** · user: Convinced enough to sign in · action: signs in · edge: sign-in: signs in
   - Signed in and following. [FS] [M1025]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod Updated yesterday), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 4 (if Checking Maya's track record), host-approve step 3 (if Wants to check the asker first)

### Connected flows [M1025]
- `stumbled`: branch out at step 2→2, step 3→4; merge in at step 3 (from its step 4)
- `cautious-joiner`: branch out at step 8→4; merge in at step 8 (from its step 4)
- `host-approve`: branch out at step 8→3; merge in at step 8 (from its step 3)
- `first-visit-live`: branch out at step 2→2; merge in at —

### Screens
1. `#home` · auth=out live=live mode=live — Live now list: who is working where. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Peeks at a live postup, then Back. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#home` · auth=out live=live mode=building — Switches to Building for past content. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
4. `#projects` · auth=out live=live — See all projects, closest first. [M1018c] [FS] (/mockups/?style=fresh&device=phone&auth=out&live=live#projects)
5. `#project` · auth=out live=live — Opens a project: updates and past postups. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)
6. `#profile` · auth=out live=live — Opens the maker's profile: past postups, regular cafes. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#profile)
7. `#profile` + sheet `signin` · auth=out live=live — Taps Follow: soft sign-in sheet; Not now keeps browsing. [FS] [M1018] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#profile)
8. `#profile` · auth=in live=live — Signed in and following. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)

### Branches and edge cases
- Nobody live: Home opens in Building, so the flow starts at the projects (merged from the old first-visit-none flow). [M1018b] [M1025]
- Taps Post up instead: see Came to post up. [M1025]
- Not now on the sheet: stays signed out, nothing lost. [drawn] [M1025]
- Never empty or "quiet" copy when nothing is live. [F035] [R4]

### Success criteria
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]

### Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]

---

## Flow: Stumbled on it: what is this? (`stumbled`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/stumbled.html

### Persona
- First-time visitor with no idea what PostUp is; arrived from search, a social post or a word-of-mouth link.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- Understand PostUp within the first screen and reach something real before any sign-in. [M1025]

### Steps
1. **home@out.live.live** · user: No idea what PostUp is · action: arrives from search or a link · edge: entry
   - Home in Live mode: map + Live now. No explainer line is drawn in Live mode, only the brand. [drawn] [M1025]
   - next site states: **postup@out.live** (M 2), postup-ask@out.live (T), cafe@out.live (tap), home@out.live.building (Building), quiet@out.live (Locate), project@out.live (Star Fox 64 mod), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live ( (Google card fails))
   - enterable flows: first-visit-live step 1 (if Curious; sees people live right now), curious-browser step 1 (if Curious what is on the site)
2. **postup@out.live** · user: Trying to understand by example · action: taps the first live person · edge: tap: M 2
   - Taps the first live person to see what a postup is. [FS] [M1025]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), **cafe@out.live** (Bean Theory 0.4 mi · 8 min walk), join-signin@out.live (Join), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit-live step 2 (if Tempted by one postup), curious-browser step 2 (if Peeking at who is live)
3. **cafe@out.live** · user: What is this place? · action: taps the cafe · edge: tap: Bean Theory 0.4 mi · 8 min walk
   - Taps the cafe: who is here now, Post up here. [FS] [M1025]
   - next site states: back (Back), cafe+share@out.live (Share), project@out.live (Star Fox 64 mod), postup@out.live (Join), post@out.live (Post up here), home@out.live.live (Home), quiet-feed@out.live (Nearby), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live (Bean Theory (Google card fails)), cafe-gfail@out.none (postups end (Google card fails))
   - enterable flows: none
4. **home@out.live.building** · user: Still unsure; looks around · action: back to Home, flips to Building · edge: back, then mode: Building
   - Back on Home, flips to Building: the welcome line "Post up at a cafe. See who's working nearby." and "What people are building". [drawn] [M1018c] [M1025]
   - next site states: home@out.live.live (Live), me@out.live (S), projects@out.live (See all projects), **project@out.live** (Star Fox 64 mod M Maya · Yesterday), post@out.live (Post up), cafe@out.live (Lantern Tea A D M 3 postups), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), cafe-gfail@out.live (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: curious-browser step 3 (if Wants past content too)
5. **project@out.live** · user: Gets it: people work on projects at cafes · action: taps a project · edge: tap: Star Fox 64 mod M Maya · Yesterday
   - Opens a project and gets the idea; Follow and Post up (🔒) are the next steps. [FS] [M1025]
   - next site states: back (Back), project-new@out.live (New), profile@out.live (Maya), project-update@out.live (Update), project-attach@out.live (Post up), cafe@out.live (Bean Theory), postup@out.live (M Maya Bean Theory · till 4pm Live), home@out.live.live (Home), quiet-feed@out.live (Nearby), post@out.live (Post up), projects@out.live (Projects), inbox@out.live (Inbox), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: curious-browser step 5 (if Interested in one project)

### Connected flows [M1025]
- `curious-browser`: branch out at step 2→2, step 4→3, step 5→5; merge in at step 4 (from its step 3), step 5 (from its step 5)
- `first-visit-live`: branch out at step 2→2; merge in at —

### Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. No explainer line is drawn in Live mode, only the brand. [drawn] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Taps the first live person to see what a postup is. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#cafe` · auth=out live=live — Taps the cafe: who is here now, Post up here. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#cafe)
4. `#home` · auth=out live=live mode=building — Back on Home, flips to Building: the welcome line "Post up at a cafe. See who's working nearby." and "What people are building". [drawn] [M1018c] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
5. `#project` · auth=out live=live — Opens a project and gets the idea; Follow and Post up (🔒) are the next steps. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)

### Branches and edge cases
- Nobody live: Home opens in Building, where the welcome line shows first. [M1018b] [drawn] [M1025]
- Dismisses the welcome (×): it should stay dismissed. [drawn] [unsourced]
- Leaves after the first screen: the value has to be clear without scrolling. [M1025]

### Success criteria
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

### Needs Martin's decision
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

---

## Flow: Share link to a live postup (`invite-live`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-live.html

### Persona
- Friend of a poster, signed out, opened postup.now/p/… from a message.

### Starting state
- auth=out · live=live · device=phone · entry URL `/p/7xk2`

### Goal
- Join the friend who shared the link. [M1024]

### Steps
1. **invite@out.live** · user: A friend sent this; knows the context · action: opens the share link · edge: entry
   - Landing for the shared postup. [FS] [R39]
   - next site states: project@out.live (Star Fox 64 mod), **join-signin@out.live** (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: none
2. **join-signin@out.live** · user: Wants to join the friend · action: taps Join 🔒 · edge: tap: Join Maya
   - Join → sign-in sheet. [FS] [M1024]
   - next site states: back (Back), join-signin+share@out.live (Share), join-signin+more@out.live (More), profile@out.live (M Maya Live · till 4pm), project@out.live (Star Fox 64 mod Adding a new Corne), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (signs in), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit-live step 3 (if Wants to join; asked to sign in)
3. **joined@in.live** · user: Signed in; going · action: signs in · edge: sign-in: signs in
   - Joined. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **chat@in.live** (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 9 (if Committed; needs to get there), quick-joiner step 3 (if Committed), leave step 1 (if Plans changed)
4. **chat@in.live** · user: Coordinating · action: opens chat · edge: tap: Group chat
   - Postup chat. [F096] [M1024]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options)
   - enterable flows: chat step 2 (if Coordinating)

### Connected flows [M1025]
- `cautious-joiner`: branch out at step 3→9; merge in at step 3 (from its step 9)
- `quick-joiner`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `chat`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `leave`: branch out at step 3→1; merge in at —
- `first-visit-live`: branch out at —; merge in at step 2 (from its step 3)

### Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite)
2. `#join-signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live#join-signin)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
4. `#chat` · auth=in live=live — Postup chat. [F096] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Link is to an ask-to-join postup → Ask to join flow. [FS] [M1024]
- Already signed in: Join goes straight to joined. [TK§1] [M1024]

### Success criteria
- The link works without an account until Join. [R39] [M1024]

---

## Flow: Share link to an ended postup (`invite-ended`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-ended.html

### Persona
- Signed-out visitor opening an old link.

### Starting state
- auth=out · live=none · device=phone · entry URL `/p/7xk2 (ended)`

### Goal
- Not hit a dead end: see what's around and follow the poster. [M1024]

### Steps
1. **invite-ended@out.none** · user: Arrived too late · action: opens an old share link · edge: entry
   - "This postup ended" + See what's nearby, Follow Maya for next time, Go to Home. [FS] [R39] [M1025]
   - next site states: quiet-feed@out.none (See what's nearby), **invite-ended+signin@out.none** (Follow Maya for next time), home@out.none.building (Go to Home)
   - enterable flows: none
2. **invite-ended+signin@out.none** · user: Wants to catch the next one · action: taps Follow Maya for next time 🔒 · edge: sheet: Follow Maya for next time
   - Follow → sign-in sheet. [FS] [M1025]
   - next site states: invite-ended@out.none (close), **invite-ended@in.none** (signs in)
   - enterable flows: none
3. **invite-ended@in.none** · user: Following Maya now · action: signs in · edge: sign-in: signs in
   - Back on the page, signed in; Follow shows Following. [M1018] [M1025]
   - next site states: quiet-feed@in.none (See what's nearby), **home@in.none.building** (Go to Home)
   - enterable flows: none
4. **home@in.none.building** · user: Signed in; looks around · action: taps Go to Home · edge: tap: Go to Home
   - Home in Building mode. [M1018b] [M1025]
   - next site states: home@in.none.live (Live), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), cafe@in.none (Lantern Tea A D M 3 postups), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@in.none (area has no postups)
   - enterable flows: empty-area step 1 (if Nobody around here yet)

### Connected flows [M1025]
- `empty-area`: branch out at step 4→1; merge in at —

### Screens
1. `#invite-ended` · auth=out live=none — "This postup ended" + See what's nearby, Follow Maya for next time, Go to Home. [FS] [R39] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=none#invite-ended)
2. `#invite-ended` + sheet `signin` · auth=out live=none — Follow → sign-in sheet. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#invite-ended)
3. `#invite-ended` · auth=in live=none — Back on the page, signed in; Follow shows Following. [M1018] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=none#invite-ended)
4. `#home` · auth=in live=none mode=building — Home in Building mode. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

### Branches and edge cases
- Cancelled instead of ended: #postup-cancelled copy. [F060] [M1024]

### Success criteria
- No 404, a next step is always offered. [F060] [M1024]

---

## Flow: Share link to a project (`invite-project`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/invite-project.html

### Persona
- Signed-out visitor opening postup.now/project/… .

### Starting state
- auth=out · live=live · device=phone · entry URL `/project/…`

### Goal
- Follow the project to hear about the next postup. [M1024]

### Steps
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

### Connected flows [M1025]
- `cautious-joiner`: branch out at step 3→3; merge in at step 3 (from its step 3)

### Screens
1. `#invite-project` · auth=out live=live — "Maya is building Star Fox 64 mod". [FS] [F067] (/mockups/?style=fresh&device=phone&auth=out&live=live#invite-project)
2. `#invite-project` + sheet `signin` · auth=out live=live — Follow 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin#invite-project)
3. `#project` · auth=in live=live — Following; live postups for the project shown. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)

### Branches and edge cases
- Project owner is live now: join from the project. [FS] [M1024]

### Success criteria
- Follow survives sign-in. [M1018] [M1024]

---

## Flow: Ask to join, then get approved (joiner side) (`ask-join`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/ask-join.html

### Persona
- Signed-in user; poster approves who joins.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Send a reason, get a yes, meet up. [M1024]

### Steps
1. **postup-ask@in.live** · user: Interested, but the host screens people · action: opens an ask-to-join postup · edge: entry
   - "Tess approves who joins". [FS] [F055]
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **ask@in.live** (Ask to join), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: cautious-joiner step 7 (if Comparing with another option)
2. **ask@in.live** · user: Explaining why they want to join · action: taps Ask to join · edge: tap: Ask to join
   - Short reason. [F061] [F095]
   - next site states: back (Back), ask+share@in.live (Share), ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **requested@in.live** (Send request), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: none
3. **requested@in.live** · user: Waiting for an answer · action: sends the request · edge: tap: Send request
   - Request sent; can cancel. [FS] [drawn]
   - next site states: home@in.live.live (Close), quiet-feed@in.live (See who else is nearby), postup-ask@in.live (View postup), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none
4. **activity@in.live** · user: Gets the yes · action: later: alert arrives · edge: event: alert arrives
   - Activity: "Tess said yes". [FS] [M1024]
   - next site states: inbox@in.live (Chats), live@in.live (D Dev asked to join your postup 2 ), **chat@in.live** (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects)
   - enterable flows: host-approve step 1 (if Hosting; someone wants in), following step 3 (if Hears that someone posted up)
5. **chat@in.live** · user: Now part of the group · action: opens the chat · edge: tap: M Maya: Hey! Here till 4 — come sa
   - Now in the postup chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options)
   - enterable flows: chat step 2 (if Coordinating)

### Connected flows [M1025]
- `cautious-joiner`: branch out at step 1→7; merge in at step 1 (from its step 7)
- `following`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

### Screens
1. `#postup-ask` · auth=in live=live — "Tess approves who joins". [FS] [F055] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
2. `#ask` · auth=in live=live — Short reason. [F061] [F095] (/mockups/?style=fresh&device=phone&auth=in&live=live#ask)
3. `#requested` · auth=in live=live — Request sent; can cancel. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#requested)
4. `#activity` · auth=in live=live — Activity: "Tess said yes". [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
5. `#chat` · auth=in live=live — Now in the postup chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Signed out: Ask to join → #ask-signin → #ask. [FS]
- Declined or no answer before the postup ends: shown in Activity, no chat. [unsourced] [M1024]
- Cafe name before approval: hidden or shown? [F070] [R23]

### Success criteria
- Joiner learns the outcome without refreshing. [F095] [M1024]

### Needs Martin's decision
- Show the cafe name before approval? (drawing shows it, code hides it) [F070] [R23]
- What the joiner sees if never answered. [unsourced]

---

## Flow: Host approves a request (`host-approve`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/host-approve.html

### Persona
- Signed-in poster with an ask-to-join postup.

### Starting state
- auth=in · live=live · device=phone · entry URL `/live`

### Goal
- Approve or decline with the joiner's reason in view. [M1024]

### Steps
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

### Connected flows [M1025]
- `ask-join`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `following`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `returning-post`: branch out at step 2→3; merge in at step 2 (from its step 3)
- `cautious-joiner`: branch out at step 3→4; merge in at step 3 (from its step 4)
- `chat`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `hosting`: branch out at step 2→1; merge in at —

### Screens
1. `#activity` · auth=in live=live — Alert: "Ari asked to join". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
2. `#live` · auth=in live=live — Requests with reason: Approve / Decline. [FS] [F061] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
3. `#profile` · auth=in live=live — Optionally checks the asker's profile first. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
4. `#chat` · auth=in live=live — Approved people are in the chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)

### Branches and edge cases
- Decline: joiner is told politely. [F095] [unsourced]
- Block from the request via More. [F059] [M1024]

### Success criteria
- Approve in one tap from #live. [FS] [M1024]

---

## Flow: Came to post up: first post with sign-in (`first-post`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post.html

### Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

### Starting state
- auth=out · live=none · device=phone · entry URL `/`

### Goal
- Go live in about ten seconds. [M1024]

### Steps
1. **home@out.none.building** · user: Came to post up right now · action: arrives at / · edge: entry
   - Taps Post up. [M1018b]
   - next site states: home@out.none.live (Live), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), **post@out.none** (Post up), cafe@out.none (Lantern Tea A D M 3 postups), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@out.none (area has no postups)
   - enterable flows: none
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), post-signin@out.none (Post up)
   - enterable flows: none
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), project-new@out.none (Project), post-signin@out.none (Post up), **where-search@out.none** (Search cafes)
   - enterable flows: none
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), **post-signin@out.none** (Post up)
   - enterable flows: none
5. **post-signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), **posted@in.none** (signs in)
   - enterable flows: none
6. **posted@in.none** · user: Live; wants company · action: signs in · edge: sign-in: signs in
   - Posted; link to copy. [FS]
   - next site states: home@in.none.building (Close), project@in.none (Star Fox 64 mod), **posted+share@in.none** (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: returning-post step 2 (if Live)
7. **posted+share@in.none** · user: Inviting friends · action: taps Invite friends · edge: sheet: Invite friends
   - Invite friends: share sheet. [drawn] [M1024]
   - next site states: posted@in.none (close)
   - enterable flows: none

### Connected flows [M1025]
- `returning-post`: branch out at step 6→2; merge in at step 6 (from its step 2)

### Screens
1. `#home` · auth=out live=none mode=building — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none#where-search)
5. `#post-signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none#post-signin)
6. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)
7. `#posted` + sheet `share` · auth=in live=none — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=share#posted)

### Branches and edge cases
- Location denied: picker falls back to search. [R21] [unsourced]
- Cafe search fails without a Maps key → error state. [unsourced]

### Success criteria
- The form is not lost through sign-in. [M1018] [M1024]

### Needs Martin's decision
- Location-permission explainer: in or out? (ledger open, final list says not adopted) [R21] [FS]

---

## Flow: Returning poster (`returning-post`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/returning-post.html

### Persona
- Signed-in regular.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Post up with defaults, then see you're live. [M1024]

### Steps
1. **post@in.live** · user: Regular; working at a cafe today · action: taps Post up · edge: entry
   - Last project and nearest cafe preselected; no 🔒. [FS] [M1024]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **posted@in.live** (Post up)
   - enterable flows: desktop-browse step 3 (if Wants to post too)
2. **posted@in.live** · user: Live · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), project@in.live (Star Fox 64 mod), posted+share@in.live (Invite friends), **live@in.live** (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company)
3. **live@in.live** · user: Managing their postup · action: opens their live postup · edge: tap: Manage postup
   - You're live: time left, requests, chat. [FS] [F057]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), **home@in.live.live** (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: host-approve step 2 (if Deciding on the request), hosting step 1 (if Live; wants more time)
4. **home@in.live.live** · user: Checking Home · action: goes Home · edge: tap: Home
   - Your live state shows on home. [R22]
   - next site states: postup@in.live (M 2), postup-ask@in.live (T), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: cautious-joiner step 1 (if Wants company today, but careful about who), quick-joiner step 1 (if Knows a friend is live; wants to go now), desktop-browse step 1 (if At a laptop; browsing)

### Connected flows [M1025]
- `first-post`: branch out at step 2→6; merge in at step 2 (from its step 6)
- `host-approve`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `desktop-browse`: branch out at step 4→1; merge in at step 1 (from its step 3)
- `hosting`: branch out at step 3→1; merge in at —
- `cautious-joiner`: branch out at step 4→1; merge in at —
- `quick-joiner`: branch out at step 4→1; merge in at —

### Screens
1. `#post` · auth=in live=live — Last project and nearest cafe preselected; no 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#post)
2. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#posted)
3. `#live` · auth=in live=live — You're live: time left, requests, chat. [FS] [F057] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#home` · auth=in live=live mode=live — Your live state shows on home. [R22] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)

### Branches and edge cases
- Already live: Post up opens #live instead of a second postup. [unsourced] [M1024]

### Success criteria
- Home → live in 2 taps. [M1024]

### Needs Martin's decision
- Can someone have two postups at once? [unsourced]

---

## Flow: Hosting live: extend, edit, end (`hosting`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/hosting.html

### Persona
- Signed-in poster who is live.

### Starting state
- auth=in · live=live · device=phone · entry URL `/live`

### Goal
- Manage time and end cleanly. [M1024]

### Steps
1. **live@in.live** · user: Live; wants more time · action: opens their live postup · edge: entry
   - +30 min extends. [FS]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), **post-edit@in.live** (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: host-approve step 2 (if Deciding on the request), returning-post step 3 (if Managing their postup)
2. **post-edit@in.live** · user: Plans changed: different time · action: taps Edit · edge: tap: Edit
   - Edit cafe/what/until; Save → #live. [FS] [drawn]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **live@in.live** (Save)
   - enterable flows: none
3. **live@in.live** · user: Saved · action: taps Save · edge: tap: Save
   - Back on live. [FS]
   - next site states: back (Back), live+share@in.live (Share), project@in.live (Star Fox 64 mod), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), **live+endlive@in.live** (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: host-approve step 2 (if Deciding on the request), returning-post step 3 (if Managing their postup)
4. **live+endlive@in.live** · user: Wrapping up · action: taps End postup · edge: sheet: End postup
   - End postup → confirm; joiners and waiters alerted. [FS] [drawn]
   - next site states: live@in.live (close), me@in.live (End now)
   - enterable flows: none
5. **me@in.none** · user: Done for today · action: confirms End now · edge: tap: End now (then live changes)
   - Back home. [M1024]
   - next site states: back (Back), settings@in.none (Settings), live@in.none (1:42 You're live at Bean Theory Ti), cafe@in.none (Lantern Tea), project-new@in.none (Tide Clock Updated Sun), cafe-gfail@in.none (Lantern Tea (Google card fails))
   - enterable flows: delete-account step 1 (if Leaving PostUp)

### Connected flows [M1025]
- `host-approve`: branch out at step 1→2, step 3→2; merge in at step 1 (from its step 2), step 3 (from its step 2)
- `returning-post`: branch out at step 1→3, step 3→3; merge in at step 1 (from its step 3), step 3 (from its step 3)
- `delete-account`: branch out at step 5→1; merge in at —

### Screens
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
2. `#post-edit` · auth=in live=live — Edit cafe/what/until; Save → #live. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#post-edit)
3. `#live` · auth=in live=live — Back on live. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup → confirm; joiners and waiters alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive#live)
5. `#me` · auth=in live=none — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none#me)

### Branches and edge cases
- Time runs out: ends automatically, chat stays 24h. [R31] [FS]
- Closes "who can join" (full): new visitors see #postup-full. [F060] [R47]

### Success criteria
- Joiners always know the postup ended. [FS] [M1024]

---

## Flow: Project builder: create, update, post up for it (`project-builder`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/project-builder.html

### Persona
- Signed-in maker.

### Starting state
- auth=in · live=none · device=phone · entry URL `/projects`

### Goal
- Have a project page that collects updates and postups. [M1024]

### Steps
1. **projects@in.none** · user: Wants a home for their project · action: opens Projects · edge: entry
   - Projects, "+". [FS]
   - next site states: **project-new@in.none** (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox)
   - enterable flows: following step 2 (if Wants to see who they follow)
2. **project-new@in.none** · user: Creating it · action: taps New project · edge: tap: New project
   - Cover, name, kind, one line. [FS] [drawn]
   - next site states: back (Back), **project@in.none** (Create)
   - enterable flows: none
3. **project@in.none** · user: Project exists · action: taps Create · edge: tap: Create
   - New project page. [FS]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), **project-update@in.none** (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: none
4. **project-update@in.none** · user: Sharing progress · action: taps Update · edge: tap: Update
   - Post an update with image. [FS] [R35]
   - next site states: back (Back), project@in.none (Post update)
   - enterable flows: none
5. **project-attach@in.none** · user: Working on it at a cafe · action: taps Post up for this · edge: back, then tap: Post up
   - Post up for this project, now or earlier today. [FS]
   - next site states: back (Back), **posted@in.none** (Post up)
   - enterable flows: none
6. **posted@in.none** · user: Live for the project · action: taps Post up · edge: tap: Post up
   - Posted, tied to the project. [FS]
   - next site states: home@in.none.building (Close), project@in.none (Star Fox 64 mod), posted+share@in.none (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Live)

### Connected flows [M1025]
- `following`: branch out at step 1→2; merge in at step 1 (from its step 2)
- `first-post`: branch out at step 6→6; merge in at step 6 (from its step 6)
- `returning-post`: branch out at step 6→2; merge in at step 6 (from its step 2)

### Screens
1. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
2. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-new)
3. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
4. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-update)
5. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#project-attach)
6. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)

### Branches and edge cases
- Signed out: Create / Post update open the sign-in sheet, form kept. [FS] [M1018]
- Signed out attach: #attach-signin. [FS]

### Success criteria
- Updates and postups show on the project timeline. [FS] [M1024]

### Needs Martin's decision
- Image storage for projects (Vercel Blob?). [TK§4]

---

## Flow: Follow a person or project (`following`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/following.html

### Persona
- Signed-in user who liked someone's work.

### Starting state
- auth=in · live=none · device=phone · entry URL `/u/maya`

### Goal
- Hear when they post up next. [M1024]

### Steps
1. **profile@in.none** · user: Likes someone's work · action: opens a profile · edge: entry
   - Follow → Following. [FS]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), project@in.none (Star Fox 64 mod Updated yesterday), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: none
2. **projects@in.none** · user: Wants to see who they follow · action: opens Projects · edge: 2 taps: Bean Theory, then Projects
   - Projects → Following filter. [FS] [R32]
   - next site states: project-new@in.none (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox)
   - enterable flows: project-builder step 1 (if Wants a home for their project)
3. **activity@in.live** · user: Hears that someone posted up · action: later: alert arrives · edge: event: alert arrives
   - Later: "Maya posted up" alert. [FS] [M1024]
   - next site states: inbox@in.live (Chats), live@in.live (D Dev asked to join your postup 2 ), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in)
4. **postup@in.live** · user: Wants to go · action: taps the alert · edge: 2 taps: M Maya: Hey! Here till 4 — come sa, then M J S Bean Theory · till 4pm · 3 p
   - Opens and joins. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)

### Connected flows [M1025]
- `ask-join`: branch out at step 3→4; merge in at step 3 (from its step 4)
- `cautious-joiner`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `quick-joiner`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `desktop-browse`: branch out at step 4→2; merge in at step 4 (from its step 2)
- `project-builder`: branch out at step 2→1; merge in at —
- `host-approve`: branch out at step 3→1; merge in at —

### Screens
1. `#profile` · auth=in live=none — Follow → Following. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
2. `#projects` · auth=in live=none — Projects → Following filter. [FS] [R32] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
3. `#activity` · auth=in live=live — Later: "Maya posted up" alert. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
4. `#postup` · auth=in live=live — Opens and joins. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

### Branches and edge cases
- Signed out: Follow → sign-in sheet. [FS]

### Success criteria
- Follow alerts arrive. [M1024]

### Needs Martin's decision
- Alert for "people you follow post up" is saved but not sent yet in the build. [unsourced]

---

## Flow: Postup chat (`chat`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/chat.html

### Persona
- Signed-in poster or joiner.

### Starting state
- auth=in · live=live · device=phone · entry URL `/inbox`

### Goal
- Coordinate in the group chat. [M1024]

### Steps
1. **inbox@in.live** · user: Wants to check messages · action: opens Inbox · edge: entry
   - Inbox · Chats. [FS] [F096]
   - next site states: activity@in.live (Activity 2), **chat@in.live** (M Maya's postup Maya: Grabbing ano), postup-ended@in.live (T Tess's postup Ended · Tue Tue), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects)
   - enterable flows: none
2. **chat@in.live** · user: Coordinating · action: opens a chat · edge: tap: M Maya's postup Maya: Grabbing ano
   - One chat per postup. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), **chat+msg@in.live** (Message options)
   - enterable flows: none
3. **chat+msg@in.live** · user: Something off about a message · action: long-presses a message · edge: sheet: Message options
   - Long-press: copy, report, block sender. [F096] [FS]
   - next site states: chat@in.live (close), report@in.live (Report message)
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#inbox` · auth=in live=live — Inbox · Chats. [FS] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#inbox)
2. `#chat` · auth=in live=live — One chat per postup. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live#chat)
3. `#chat` + sheet `msg` · auth=in live=live — Long-press: copy, report, block sender. [F096] [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=msg#chat)

### Branches and edge cases
- Signed out: sign-in sheet over Inbox. [unsourced]
- Chat closes 24h after the postup. [R31] [FS]

### Success criteria
- Only poster + joined/approved can read. [F061]

### Needs Martin's decision
- Chat retention (24h default). [R31] [FS]

---

## Flow: Report and block (`safety`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/safety.html

### Persona
- Signed-in user uncomfortable with someone.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Report and block quickly. [F059] [M1024]

### Steps
1. **postup+more@in.live** · user: Uncomfortable with someone · action: taps More · edge: entry
   - More: profile, share, report, block. [FS] [F059]
   - next site states: postup@in.live (close), profile@in.live (View profile), postup+share@in.live (Share), **report@in.live** (Report), postup+block@in.live (Block Maya)
   - enterable flows: none
2. **report@in.live** · user: Wants to report · action: taps Report · edge: tap: Report
   - Reason + details. [F059] [drawn]
   - next site states: back (Back), **reported@in.live** (Send report)
   - enterable flows: none
3. **reported@in.live** · user: Reported; still uneasy · action: sends the report · edge: tap: Send report
   - Thanks; offer to block. [FS]
   - next site states: home@in.live.live (Close), **reported+block@in.live** (Block Maya too)
   - enterable flows: none
4. **reported+block@in.live** · user: Wants them gone · action: taps Block too · edge: sheet: Block Maya too
   - Block: neither sees the other; they aren't told. [FS] [F059]
   - next site states: reported@in.live (close), home@in.live.live (Block), **settings@in.live** (Blocked people (Settings))
   - enterable flows: none
5. **settings@in.live** · user: Might undo later · action: opens Settings · edge: tap: Blocked people (Settings)
   - Blocked people list to undo. [FS] [F065]
   - next site states: back (Back), home@out.live.live (Sign out), settings+delacct@in.live (Delete account)
   - enterable flows: delete-account step 2 (if Looking for the delete option), settings-notify step 1 (if Tuning alerts)

### Connected flows [M1025]
- `delete-account`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `settings-notify`: branch out at step 5→1; merge in at —

### Screens
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#reported)
4. `#reported` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block#reported)
5. `#settings` · auth=in live=live — Blocked people list to undo. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=live#settings)

### Branches and edge cases
- From a chat message: Message options → Report message. [F096]

### Success criteria
- No safety-tip screens. [F059] [FS]

### Needs Martin's decision
- No ban system yet: who reviews reports? [TK§4]

---

## Flow: Leave a postup you joined (`leave`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/leave.html

### Persona
- Signed-in joiner whose plans changed.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Back out politely. [M1024]

### Steps
1. **joined@in.live** · user: Plans changed · action: opens their joined postup · edge: entry
   - Leave link. [drawn]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), joined+dirs@in.live (Directions), project@in.live (Project), **joined+leave@in.live** (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: cautious-joiner step 9 (if Committed; needs to get there), quick-joiner step 3 (if Committed), invite-live step 3 (if Signed in; going)
2. **joined+leave@in.live** · user: Backing out politely · action: taps Leave · edge: sheet: Leave
   - Confirm; poster alerted. [FS] [drawn]
   - next site states: joined@in.live (close), **postup@in.live** (Leave)
   - enterable flows: none
3. **postup@in.live** · user: Out; back on the postup page · action: confirms Leave · edge: tap: Leave
   - Back home. [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)

### Connected flows [M1025]
- `cautious-joiner`: branch out at step 1→9, step 3→2; merge in at step 1 (from its step 9), step 3 (from its step 2)
- `quick-joiner`: branch out at step 1→3, step 3→2; merge in at step 1 (from its step 3), step 3 (from its step 2)
- `invite-live`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `desktop-browse`: branch out at step 3→2; merge in at step 3 (from its step 2)

### Screens
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave#joined)
3. `#postup` · auth=in live=live — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

### Branches and edge cases
- The poster ended or cancelled first: #postup-cancelled. [F060]

### Success criteria
- Poster knows. [FS]

---

## Flow: Postup ends, fills or is cancelled while you look (`postup-states`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/postup-states.html

### Persona
- Anyone viewing a postup.

### Starting state
- auth=in · live=live · device=phone · entry URL `/p/…`

### Goal
- Clear state and a next step. [F060] [M1024]

### Steps
1. **postup-full@in.live** · user: Wanted to join; it's full · action: opens a full postup · edge: entry
   - Full. [F060] [R47]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none
2. **postup-cancelled@in.live** · user: Host cancelled · action: later: postup cancelled · edge: event: postup fills / is cancelled / ends
   - Cancelled. [F060] [R47]
   - next site states: back (Back), postup-cancelled+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none
3. **postup-ended@in.none** · user: Too late; it ended · action: later: postup ended · edge: 2 taps: Inbox, then T Tess's postup Ended · Tue Tue
   - Ended: see what's nearby, follow. [drawn]
   - next site states: back (Back), postup-ended+more@in.none (More), profile@in.none (M Maya Bean Theory), quiet-feed@in.none (See what's nearby), home@in.none.building (Go to Home), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox)
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#postup-full` · auth=in live=live — Full. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-full)
2. `#postup-cancelled` · auth=in live=live — Cancelled. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-cancelled)
3. `#postup-ended` · auth=in live=none — Ended: see what's nearby, follow. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none#postup-ended)

### Success criteria
- Never a blank page. [F060]

---

## Flow: Empty area: be the first (`empty-area`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area.html

### Persona
- Signed-in user in a city with no postups yet.

### Starting state
- auth=in · live=none · device=phone · entry URL `/`

### Goal
- Seed the area. [M1024]

### Steps
1. **home@in.none.building** · user: Nobody around here yet · action: arrives at / · edge: entry
   - Closest projects even if far. [M1018c]
   - next site states: home@in.none.live (Live), me@in.none (S), projects@in.none (See all projects), project@in.none (Star Fox 64 mod M Maya · Yesterday), post@in.none (Post up), cafe@in.none (Lantern Tea A D M 3 postups), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), cafe-gfail@in.none (Lantern Tea A D M 3 postups (Google card fails)), **empty-area@in.none** (area has no postups)
   - enterable flows: none
2. **empty-area@in.none** · user: Sees the area is empty · action: opens the empty area · edge: cond: area has no postups
   - "Be the first here". [FS]
   - next site states: cafe@in.none (tap), me@in.none (S), **post@in.none** (Stories Cafe 0.3 mi), home@in.none.building (Home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), cafe-gfail@in.none ( (Google card fails))
   - enterable flows: none
3. **post@in.none** · user: Will be the first · action: taps Post up · edge: tap: Stories Cafe 0.3 mi
   - Post up. [FS]
   - next site states: back (Back), where@in.none (Bean Theory Nearest · 0.4 mi Chang), project-new@in.none (Project), posted@in.none (Post up)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today), desktop-browse step 3 (if Wants to post too)

### Connected flows [M1025]
- `desktop-browse`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `returning-post`: branch out at step 3→1; merge in at —

### Screens
1. `#home` · auth=in live=none mode=building — Closest projects even if far. [M1018c] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)
2. `#empty-area` · auth=in live=none — "Be the first here". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#empty-area)
3. `#post` · auth=in live=none — Post up. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#post)

### Success criteria
- Positive copy, never "quiet". [F035] [R4]

### Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

---

## Flow: Slow network and offline (`loading-offline`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/loading-offline.html

### Persona
- Anyone on bad wifi.

### Starting state
- auth=in · live=live · device=phone · entry URL `/nearby`

### Goal
- Keep showing something useful. [M1024]

### Steps
1. **loading@in.live** · user: Opened the feed on bad wifi · action: opens Nearby · edge: entry
   - Skeleton. [FS] [F060]
   - next site states: home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none
2. **offline@in.live** · user: Connection dropped · action: later: network drops · edge: event: network drops
   - Cached feed + offline banner + Retry. [FS]
   - next site states: me@in.live (S), quiet@in.live (tap), **quiet-feed@in.live** (Retry), post@in.live (Post up), cafe@in.live (Maya's photo), project@in.live (Star Fox 64 mod), home@in.live.live (Home), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: none
3. **quiet-feed@in.live** · user: Back online · action: taps Retry · edge: tap: Retry
   - Retry succeeds. [FS]
   - next site states: me@in.live (S), quiet@in.live (tap), post@in.live (Post up), cafe@in.live (Maya's photo), project@in.live (Star Fox 64 mod), home@in.live.live (Home), projects@in.live (Projects), inbox@in.live (Inbox), **cafe-gfail@in.live** (Maya's photo (Google card fails))
   - enterable flows: none
4. **cafe-gfail@in.live** · user: Checking a cafe; Google is down · action: taps a cafe · edge: cond: Maya's photo (Google card fails)
   - Google card failed: rest of cafe still works. [F060]
   - next site states: back (Back), cafe-gfail+share@in.live (Share), cafe@in.live (Bean Theory), project@in.live (Star Fox 64 mod), postup@in.live (Join), cafe-gfail+dirs@in.live (Open in Maps), post@in.live (Post up here), home@in.live.live (Home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox)
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#loading` · auth=in live=live — Skeleton. [FS] [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#loading)
2. `#offline` · auth=in live=live — Cached feed + offline banner + Retry. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#offline)
3. `#quiet-feed` · auth=in live=live — Retry succeeds. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#quiet-feed)
4. `#cafe-gfail` · auth=in live=live — Google card failed: rest of cafe still works. [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe-gfail)

### Branches and edge cases
- First visit while offline: nothing cached (fails in the build today). [unsourced]

### Success criteria
- No blank screens. [FS]

### Needs Martin's decision
- Full offline screen vs banner only. [R46⚠] [FS]

---

## Flow: Delete account (`delete-account`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/delete-account.html

### Persona
- Signed-in user leaving.

### Starting state
- auth=in · live=none · device=phone · entry URL `/me`

### Goal
- Remove profile, postups and projects. [M1024]

### Steps
1. **me@in.none** · user: Leaving PostUp · action: opens My profile · edge: entry
   - My profile → Settings. [FS]
   - next site states: back (Back), **settings@in.none** (Settings), live@in.none (1:42 You're live at Bean Theory Ti), cafe@in.none (Lantern Tea), project-new@in.none (Tide Clock Updated Sun), cafe-gfail@in.none (Lantern Tea (Google card fails))
   - enterable flows: none
2. **settings@in.none** · user: Looking for the delete option · action: taps Settings · edge: tap: Settings
   - Account section. [FS] [F065]
   - next site states: back (Back), home@out.none.building (Sign out), **settings+delacct@in.none** (Delete account)
   - enterable flows: settings-notify step 1 (if Tuning alerts)
3. **settings+delacct@in.none** · user: Sure about it · action: taps Delete account · edge: sheet: Delete account
   - Confirm; can't be undone. [FS] [drawn]
   - next site states: settings@in.none (close), **home@out.none.building** (Delete account)
   - enterable flows: none
4. **home@out.none.building** · user: Gone · action: confirms · edge: tap: Delete account
   - Signed out at Home. [M1024]
   - next site states: home@out.none.live (Live), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), cafe@out.none (Lantern Tea A D M 3 postups), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@out.none (area has no postups)
   - enterable flows: first-post step 1 (if Came to post up right now)

### Connected flows [M1025]
- `settings-notify`: branch out at step 2→1; merge in at —
- `first-post`: branch out at step 4→1; merge in at —

### Screens
1. `#me` · auth=in live=none — My profile → Settings. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#me)
2. `#settings` · auth=in live=none — Account section. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
3. `#settings` + sheet `delacct` · auth=in live=none — Confirm; can't be undone. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=delacct#settings)
4. `#home` · auth=out live=none mode=building — Signed out at Home. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

### Branches and edge cases
- Deleting while live: postup ends and joiners are alerted? [unsourced]

### Success criteria
- All their content gone. [FS]

### Needs Martin's decision
- What happens to a live postup and chats on delete. [unsourced]

---

## Flow: Desktop browse and post (`desktop-browse`)
Priority: **nice** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/desktop-browse.html

### Persona
- Signed-in user at a laptop.

### Starting state
- auth=in · live=live · device=desktop · entry URL `/`

### Goal
- Same flows with map + right panel. [FS] [M1024]

### Steps
1. **home@in.live.live** · user: At a laptop; browsing · action: arrives at / · edge: entry
   - Map with 440px panel. [FS]
   - next site states: **postup@in.live** (M 2), postup-ask@in.live (T), cafe@in.live (tap), home@in.live.building (Building), quiet@in.live (Locate), project@in.live (Star Fox 64 mod), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live ( (Google card fails))
   - enterable flows: cautious-joiner step 1 (if Wants company today, but careful about who), quick-joiner step 1 (if Knows a friend is live; wants to go now)
2. **postup@in.live** · user: Checking one postup · action: taps a live pin · edge: tap: M 2
   - Postup in the panel. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), quick-joiner step 2 (if Found them; joining)
3. **post@in.live** · user: Wants to post too · action: taps Post up · edge: back, then tap: Post up
   - Post up as a centered dialog. [FS]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), project-new@in.live (Project), **posted@in.live** (Post up)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today)
4. **posted@in.live** · user: Live · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), project@in.live (Star Fox 64 mod), posted+share@in.live (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), inbox@in.live (Inbox), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Live)

### Connected flows [M1025]
- `first-post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `cautious-joiner`: branch out at step 2→2; merge in at —
- `quick-joiner`: branch out at step 2→2; merge in at —
- `returning-post`: branch out at step 4→2; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#postup)
3. `#post` · auth=in live=live — Post up as a centered dialog. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#post)
4. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live#posted)

### Success criteria
- Rail and tab bar have the same items. [F064] [R12]

---

## Flow: Notification settings and sign out (`settings-notify`)
Priority: **nice** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/settings-notify.html

### Persona
- Signed-in user.

### Starting state
- auth=in · live=none · device=phone · entry URL `/settings`

### Goal
- Tune alerts, sign out. [M1024]

### Steps
1. **settings@in.none** · user: Tuning alerts · action: opens Settings · edge: entry
   - Toggles; Sign out. [FS] [F065]
   - next site states: back (Back), **home@out.none.building** (Sign out), settings+delacct@in.none (Delete account)
   - enterable flows: delete-account step 2 (if Looking for the delete option)
2. **home@out.none.building** · user: Done for now · action: taps Sign out · edge: tap: Sign out
   - Signed out. [M1024]
   - next site states: home@out.none.live (Live), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), post@out.none (Post up), cafe@out.none (Lantern Tea A D M 3 postups), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails)), empty-area@out.none (area has no postups)
   - enterable flows: first-post step 1 (if Came to post up right now)

### Connected flows [M1025]
- `delete-account`: branch out at step 1→2; merge in at step 1 (from its step 2)
- `first-post`: branch out at step 2→1; merge in at —

### Screens
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

### Success criteria
- Toggles actually change alerts. [M1024]

### Needs Martin's decision
- Email alerts at launch? [TK§4]
