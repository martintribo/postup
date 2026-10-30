# PostUp critical flows
Critical flows (Martin, Oct 24 2026 [M1024]): a type of user arrives in a certain situation and goes through a scenario step by step. Each step names the screen and the scenario params (auth, live, Home mode, sheet). Flows marked Draft were inferred from the screen notes; confirm with Martin.

- [look-around](look-around.md) · Phase 0 · Newcomer looks around, then joins
- [empty-area-newcomer](empty-area-newcomer.md) · Phase 0 · Nobody live nearby (newcomer)
- [join](join.md) · Phase 0 · Join someone live
- [invite-live](invite-live.md) · Phase 0 · Share link to a live postup
- [empty-area](empty-area.md) · Phase 0 · Nobody live nearby (signed in)
- [first-post](first-post.md) · Phase 0 · Came to post up: first post with sign-in
- [returning-post](returning-post.md) · Phase 1 · Returning poster
- [hosting](hosting.md) · Phase 1 · Hosting live: extend, edit, end
- [chat](chat.md) · Phase 1 · Postup chat
- [safety](safety.md) · Phase 0 · Report and block
- [leave](leave.md) · Phase 1 · Leave a postup you joined
- [invite-project](invite-project.md) · Phase 2 (MVP) · Share link to a project
- [ask-join](ask-join.md) · Phase 2 (MVP) · Ask to join, then get approved (joiner side)
- [host-approve](host-approve.md) · Phase 2 (MVP) · Host approves a request
- [project-builder](project-builder.md) · Phase 2 (MVP) · Project builder: create, update, post up for it
- [following](following.md) · Unphased · Follow a person or project
- [postup-states](postup-states.md) · Unphased · Postup ends, fills or is cancelled while you look
- [loading-offline](loading-offline.md) · Unphased · Slow network and offline
- [delete-account](delete-account.md) · Unphased · Delete account
- [desktop-browse](desktop-browse.md) · Unphased · Desktop browse and post
- [settings-notify](settings-notify.md) · Unphased · Notification settings and sign out
- [catch-up](catch-up.md) · Unphased · Catch up on what happened

## Flow: Newcomer looks around, then joins (`look-around`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/look-around.html

### Persona
- First-time visitor, signed out: curious what PostUp is, or has no idea and arrived from search, a social post or a link.

### Starting state
- auth=out · live=live · device=phone · entry URL `/`

### Goal
- Understand PostUp from the first screen, see live and past content, and join someone; sign in only at Join. [M1024] [M1025] [M1032]

### Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: **postup@out.live** (M 2), cafe@out.live (cafe), quiet@out.live (Locate), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), postup-ask@out.live (T), home@out.live.building (Building), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: none
2. **postup@out.live** · user: What is she doing? · action: taps Maya's live row · edge: tap: M Maya Live Bean Theory · till 4pm
   - Her live postup: who, cafe, till when; Join shows 🔒. Projects are phase 2, so the newcomer learns by example from a live postup. [FS] [M1024] [M1034]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), **profile@out.live** (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), postup+signin@out.live (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: none
3. **profile@out.live** · user: Who is behind it? · action: taps Maya · edge: tap: M Maya Live · till 4pm
   - Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025]
   - next site states: back (Back), profile+more@out.live (More), **postup@out.live** (Live at Bean Theory Till 4pm · Sta), profile+signin@out.live (Follow), cafe@out.live (Bean Theory), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Updated yesterday), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **postup@out.live** · user: She's live right now · action: taps Live at Bean Theory · edge: tap: Live at Bean Theory Till 4pm · Sta
   - Her live postup; Join shows 🔒. [FS] [M1024]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **postup+signin@out.live** (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: none
5. **postup+signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: postup@out.live (close), postup@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
6. **joined@in.live** · user: Signed in; committed · action: signs in · edge: tap: Continue with Apple
   - Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), leave step 1 (if Plans changed)

### Connected flows [M1025]
- `join`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `leave`: branch out at step 6→1; merge in at —

### Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live&ph=0#home)
2. `#postup` · auth=out live=live — Her live postup: who, cafe, till when; Join shows 🔒. Projects are phase 2, so the newcomer learns by example from a live postup. [FS] [M1024] [M1034] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#postup)
3. `#profile` · auth=out live=live — Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#profile)
4. `#postup` · auth=out live=live — Her live postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#postup)
5. `#postup` + sheet `signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#postup)
6. `#joined` · auth=in live=live — Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)

### Branches and edge cases
- Switches to Building mode for the welcome line and projects: phase 2, since projects are phase 2. [M1034]
- Joins straight from Live now: taps a live row, Join 🔒, sign-in sheet, joined in one go (was Curious visitor joins someone live). [FS] [M1018] [M1024]
- Follows the maker instead of joining: Follow 🔒 → sign-in sheet → signed in and following (was Curious browser). [FS] [M1025]
- No idea what PostUp is: taps the first live person, then the cafe, to understand by example (was Stumbled on it). [FS] [M1025]
- Nobody live: Home opens in Building, so the flow starts at the projects (merged from the old first-visit-none flow). [M1018b] [M1025]
- Taps Post up instead: see Came to post up. [M1025]
- Not now on the sheet: stays signed out, nothing lost. [drawn] [M1025]
- Never empty or "quiet" copy when nothing is live. [F035] [R4]
- Nobody live: Home opens in Building, where the welcome line shows first. [M1018b] [drawn] [M1025]
- Dismisses the welcome (×): it should stay dismissed. [drawn] [unsourced]
- Leaves after the first screen: the value has to be clear without scrolling. [M1025]
- Not now on the sheet: stays on the postup, still signed out. [drawn] [M1024]
- Switches to Building to look at projects first. [M1018b] [M1024]

### Success criteria
- No sign-in before an action. [FS]
- After sign-in the original action completes. [M1018] [M1024]
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

### Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

---

## Flow: Nobody live nearby (newcomer) (`empty-area-newcomer`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area-newcomer.html

### Persona
- First-time visitor, signed out, in an area where nobody is live right now.

### Starting state
- auth=out · live=none · device=phone · entry URL `/`

### Goal
- With nobody live nearby, see who posted up here lately, then be the first today. [M1032]

### Steps
1. **home@out.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@out.none (cafe), quiet@out.none (Locate), post@out.none (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), home@out.none.building (Building), projects@out.none (Projects), **empty-area@out.none** (area has no postups), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: first-post step 1 (if Came to post up right now)
2. **empty-area@out.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032]
   - next site states: cafe@out.none (cafe), me@out.none (S), post@out.none (Stories Cafe 0.3 mi), **profile@out.none** (Maya posted up at Bean Theory), home@out.none.live (Home), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.building (Home), projects@out.none (Projects), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: none
3. **profile@out.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@out.none (More), profile+signin@out.none (Follow), cafe@out.none (Bean Theory), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project@out.none (Star Fox 64 mod Updated yesterday), home@out.none.building (home), projects@out.none (Projects), cafe-gfail@out.none (Bean Theory (Google card fails))
   - enterable flows: none
4. **empty-area@out.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@out.none (cafe), me@out.none (S), post@out.none (Stories Cafe 0.3 mi), profile@out.none (Maya posted up at Bean Theory), home@out.none.live (Home), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.building (Home), projects@out.none (Projects), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- `first-post`: branch out at step 1→1; merge in at —

### Screens
1. `#home` · auth=out live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#empty-area` · auth=out live=none — Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#empty-area)
3. `#profile` · auth=out live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#profile)
4. `#empty-area` · auth=out live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#empty-area)

### Branches and edge cases
- No past activity at all in the area: good cafes to be the first. [M1032] [M1034]

### Success criteria
- Never an empty or "quiet" screen: recent postups and projects nearby are shown. [F035] [R4] [M1032]

### Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

---

## Flow: Join someone live (`join`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/join.html

### Persona
- Registered user, signed in, who wants company now.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- Join a live postup and get there; checking the person first is optional. [M1024] [M1032]

### Steps
1. **home@in.live.live** · user: Wants company now · action: arrives at / · edge: entry
   - Live now list. [M1018b] [M1024]
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Found someone · action: taps a live row · edge: tap: M 2
   - Who, project, cafe, who else is joining. [FS] [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), **joined@in.live** (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: desktop-browse step 2 (if Checking one postup)
3. **joined@in.live** · user: Decides to join · action: taps Join · edge: tap: Join
   - You're joining; the poster is told. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), **joined+dirs@in.live** (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: leave step 1 (if Plans changed)
4. **joined+dirs@in.live** · user: Needs the route · action: taps Directions · edge: tap: Directions
   - Directions sheet: Apple / Google Maps. [FS] [M1024]
   - next site states: **joined@in.live** (close)
   - enterable flows: none
5. **joined@in.live** · user: Knows the way · action: closes Directions · edge: tap: Cancel
   - Back on the joined screen. [M1031-draft]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: leave step 1 (if Plans changed)

### Connected flows [M1025]
- `leave`: branch out at step 3→1, step 5→1; merge in at —
- `catch-up`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 2→2; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=0#home)
2. `#postup` · auth=in live=live — Who, project, cafe, who else is joining. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#postup)
3. `#joined` · auth=in live=live — You're joining; the poster is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)
4. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs&ph=0#joined)
5. `#joined` · auth=in live=live — Back on the joined screen. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)

### Branches and edge cases
- Phase 0: no group chat; joining means you're coming in person. The chat step moved to the Chat flow (phase 1). [M1037]
- Optional check first (was Cautious joiner): from the postup, the project tag → project, the owner → profile (postup count, regular cafes, past postups), the cafe → cafe; Back returns each time. [FS] [F065] [M1024]
- Compares with an Ask to join postup (Tess): phase 2, see Ask to join. [M1032]
- Joined by mistake: Leave sheet, poster is alerted (see Leave a postup). [FS] [M1024]
- Every detail page has Back that returns to the list it came from, with the list scroll kept. [F013] [M1024]
- The postup ends while they're reading: Join is replaced by the ended state (#postup-ended). [F060] [M1024]
- Desktop: details open in the right panel and the map stays. [FS] [M1024]

### Success criteria
- Home → joined in 2 taps. [M1024]
- Can reach postup, project, profile and cafe details from one postup and come back without losing place. [M1024]
- Join is one tap once decided. [TK§1] [M1024]

---

## Flow: Share link to a live postup (`invite-live`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: **invite+signin@out.live** (Join Maya), cafe@out.live (Bean Theory · 0.4 mi), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory · 0.4 mi (Google card fails))
   - enterable flows: none
2. **invite+signin@out.live** · user: Wants to join the friend · action: taps Join 🔒 · edge: tap: Join Maya
   - Join → sign-in sheet. [FS] [M1024]
   - next site states: invite@out.live (close), invite@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
3. **joined@in.live** · user: Signed in; going · action: signs in · edge: tap: Continue with Apple
   - Joined. [FS] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), joined+leave@in.live (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), leave step 1 (if Plans changed)

### Connected flows [M1025]
- `join`: branch out at step 3→3; merge in at step 3 (from its step 3)
- `leave`: branch out at step 3→1; merge in at —

### Screens
1. `#invite` · auth=out live=live — Landing for the shared postup. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#invite)
2. `#invite` + sheet `signin` · auth=out live=live — Join → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#invite)
3. `#joined` · auth=in live=live — Joined. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#joined)

### Branches and edge cases
- Phase 0: ends at Joined; no chat step (chat is phase 1, see the Chat flow). [M1037]
- The postup has ended by the time the link is opened: lands on `#invite-ended` (This postup ended; See what's nearby, Follow Maya for next time, Go to Home). Was its own flow. [M1032]
- Link is to an ask-to-join postup → Ask to join flow. [FS] [M1024]
- Already signed in: Join goes straight to joined. [TK§1] [M1024]

### Success criteria
- The link works without an account until Join. [R39] [M1024]

---

## Flow: Nobody live nearby (signed in) (`empty-area`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/empty-area.html

### Persona
- Signed-in user in an area where nobody is live right now.

### Starting state
- auth=in · live=none · device=phone · entry URL `/`

### Goal
- With nobody live nearby, see who posted up here lately, then be the first today. [M1032]

### Steps
1. **home@in.none.live** · user: Nobody around right now · action: arrives at / · edge: entry
   - Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035]
   - next site states: cafe@in.none (cafe), quiet@in.none (Locate), post@in.none (Post up), quiet-feed@in.none (Nearby), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Building), projects@in.none (Projects), **empty-area@in.none** (area has no postups), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none
2. **empty-area@in.none** · user: What happens around here? · action: area has no postups · edge: cond: area has no postups
   - Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), **profile@in.none** (Maya posted up at Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none
3. **profile@in.none** · user: Who comes here? · action: taps Maya posted up at Bean Theory · edge: tap: Maya posted up at Bean Theory
   - Maya's profile: regular cafes, past postups. [FS] [M1032]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), project@in.none (Star Fox 64 mod Updated yesterday), home@in.none.building (home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 1 (if Likes someone's work)
4. **empty-area@in.none** · user: Back to the area · action: taps Back · edge: back
   - The empty-area screen again. [M1032]
   - next site states: cafe@in.none (cafe), me@in.none (S), post@in.none (Stories Cafe 0.3 mi), profile@in.none (Maya posted up at Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (cafe (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- `following`: branch out at step 3→1; merge in at —

### Screens
1. `#home` · auth=in live=none mode=live — Home with nobody live: map of cafes and a Post up invite (no Building mode in phase 1). [M1018c] [M1035] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=live&ph=0#home)
2. `#empty-area` · auth=in live=none — Nobody's live nearby: Recently nearby (past postups), then cafes to be the first. Projects nearby are phase 2. [M1034] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#empty-area)
3. `#profile` · auth=in live=none — Maya's profile: regular cafes, past postups. [FS] [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#profile)
4. `#empty-area` · auth=in live=none — The empty-area screen again. [M1032] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#empty-area)

### Branches and edge cases
- No past activity at all in the area: good cafes to be the first. [M1032] [M1034]

### Success criteria
- Never an empty or "quiet" screen: recent postups and projects nearby are shown. [F035] [R4] [M1032]

### Needs Martin's decision
- A fallback list of good cafes for empty areas? [TK§4]
- Launch area. [FS] [TK§4]

---

## Flow: Came to post up: first post with sign-in (`first-post`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post.html

### Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

### Starting state
- auth=out · live=none · device=phone · entry URL `/`

### Goal
- Go live in about ten seconds. [M1024]

### Steps
1. **home@out.none.live** · user: Came to post up right now · action: arrives at / · edge: entry
   - Taps Post up. [M1018b]
   - next site states: cafe@out.none (cafe), quiet@out.none (Locate), **post@out.none** (Post up), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), home@out.none.building (Building), projects@out.none (Projects), empty-area@out.none (area has no postups), cafe-gfail@out.none (cafe (Google card fails))
   - enterable flows: empty-area-newcomer step 1 (if Nobody around right now)
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), post+signin@out.none (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: none
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: none
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), **where-search+signin@out.none** (Post up), home@out.none.live (home), quiet-feed@out.none (Nearby), post@out.none (Post up), me@out.none (S), inbox@out.none (Inbox), project-new@out.none (Project), home@out.none.building (home), projects@out.none (Projects)
   - enterable flows: none
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), **posted@in.none** (signs in → continues)
   - enterable flows: none
6. **posted@in.none** · user: Live; wants company · action: signs in · edge: tap: Continue with Apple
   - Posted; link to copy. [FS]
   - next site states: home@in.none.live (Close), **posted+share@in.none** (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Close), project@in.none (Star Fox 64 mod), projects@in.none (Projects), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: returning-post step 2 (if Posted; now live for others)
7. **posted+share@in.none** · user: Wants friends to come too · action: taps Invite friends · edge: tap: Invite friends
   - Invite friends: share sheet. [drawn] [M1024]
   - next site states: posted@in.none (close)
   - enterable flows: none

### Connected flows [M1025]
- `returning-post`: branch out at step 6→2; merge in at step 6 (from its step 2)
- `empty-area-newcomer`: branch out at step 1→1; merge in at —

### Screens
1. `#home` · auth=out live=none mode=live — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=live&ph=0#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none&ph=0#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin&ph=0#where-search)
6. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=0#posted)
7. `#posted` + sheet `share` · auth=in live=none — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=share&ph=0#posted)

### Branches and edge cases
- Also covers a returning poster in phase 0: same steps, with the cafe and what you're working on prefilled. The separate Returning poster flow is phase 1. [M1037]
- Location denied: picker falls back to search. [R21] [unsourced]
- Cafe search fails without a Maps key → error state. [unsourced]

### Success criteria
- The form is not lost through sign-in. [M1018] [M1024]

### Needs Martin's decision
- Location-permission explainer: in or out? (ledger open, final list says not adopted) [R21] [FS]

---

## Flow: Returning poster (`returning-post`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects)
   - enterable flows: desktop-browse step 3 (if Wants to post too)
2. **posted@in.live** · user: Posted; now live for others · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), posted+share@in.live (Invite friends), **live@in.live** (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company)
3. **live@in.live** · user: Managing their postup · action: opens their live postup · edge: tap: Manage postup
   - You're live: time left, requests, chat. [FS] [F057]
   - next site states: back (Back), live+share@in.live (Share), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), **home@in.live.live** (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: hosting step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)
4. **home@in.live.live** · user: Checks they show up on Home · action: goes Home · edge: tap: Home
   - Your live state shows on home. [R22]
   - next site states: postup@in.live (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)

### Connected flows [M1025]
- `first-post`: branch out at step 2→6; merge in at step 2 (from its step 6)
- `host-approve`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `desktop-browse`: branch out at step 4→1; merge in at step 1 (from its step 3)
- `hosting`: branch out at step 3→1; merge in at —
- `join`: branch out at step 4→1; merge in at —
- `catch-up`: branch out at step 4→1; merge in at —

### Screens
1. `#post` · auth=in live=live — Last project and nearest cafe preselected; no 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post)
2. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#posted)
3. `#live` · auth=in live=live — You're live: time left, requests, chat. [FS] [F057] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)
4. `#home` · auth=in live=live mode=live — Your live state shows on home. [R22] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=1#home)

### Branches and edge cases
- Already live: Post up opens #live instead of a second postup. [unsourced] [M1024]

### Success criteria
- Home → live in 2 taps. [M1024]

### Needs Martin's decision
- Can someone have two postups at once? [unsourced]

---

## Flow: Hosting live: extend, edit, end (`hosting`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), live+share@in.live (Share), **post-edit@in.live** (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: returning-post step 3 (if Managing their postup), host-approve step 2 (if Deciding on the request)
2. **post-edit@in.live** · user: Plans changed: different time · action: taps Edit · edge: tap: Edit
   - Edit cafe/what/until; Save → #live. [FS] [drawn]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **live@in.live** (Save), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects)
   - enterable flows: none
3. **live@in.live** · user: Saved · action: taps Save · edge: back
   - Back on live. [FS]
   - next site states: back (Back), live+share@in.live (Share), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), **live+endlive@in.live** (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: returning-post step 3 (if Managing their postup), host-approve step 2 (if Deciding on the request)
4. **live+endlive@in.live** · user: Wrapping up · action: taps End postup · edge: tap: End postup
   - End postup → confirm; joiners and waiters alerted. [FS] [drawn]
   - next site states: live@in.live (close), **me@in.live** (End now)
   - enterable flows: none
5. **me@in.live** · user: Done for today · action: confirms End now · edge: tap: End now
   - Back home. [M1024] Ending your own postup doesn't change who else is live nearby (live = nearby, not this postup). [M1031-draft]
   - next site states: back (Back), settings@in.live (Settings), live@in.live (1:42 You're live at Bean Theory Ti), cafe@in.live (Lantern Tea), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), project-new@in.live (Tide Clock Updated Sun), projects@in.live (Projects), cafe-gfail@in.live (Lantern Tea (Google card fails))
   - enterable flows: delete-account step 1 (if Leaving PostUp)

### Connected flows [M1025]
- `returning-post`: branch out at step 1→3, step 3→3; merge in at step 1 (from its step 3), step 3 (from its step 3)
- `host-approve`: branch out at step 1→2, step 3→2; merge in at step 1 (from its step 2), step 3 (from its step 2)
- `delete-account`: branch out at step 5→1; merge in at —

### Screens
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)
2. `#post-edit` · auth=in live=live — Edit cafe/what/until; Save → #live. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post-edit)
3. `#live` · auth=in live=live — Back on live. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup → confirm; joiners and waiters alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive&ph=1#live)
5. `#me` · auth=in live=live — Back home. [M1024] Ending your own postup doesn't change who else is live nearby (live = nearby, not this postup). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#me)

### Branches and edge cases
- Time runs out: ends automatically, chat stays 24h. [R31] [FS]
- Closes "who can join" (full): new visitors see #postup-full. [F060] [R47]

### Success criteria
- Joiners always know the postup ended. [FS] [M1024]

---

## Flow: Postup chat (`chat`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/chat.html

### Persona
- Signed-in poster or joiner.

### Starting state
- auth=in · live=live · device=phone · entry URL `/inbox`

### Goal
- Coordinate in the group chat. [M1024]

### Steps
1. **inbox@in.live** · user: Wants to check messages · action: opens Inbox · edge: entry
   - Inbox: one list of postup chats, newest first, unread dots. [F096] [M1033]
   - next site states: **chat@in.live** (Maya's postup · Bean Theory), postup-ended@in.live (Tess's postup · Grindhouse), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), activity@in.live (Activity 2), projects@in.live (Projects)
   - enterable flows: catch-up step 2 (if Checks messages first)
2. **chat@in.live** · user: Wants to sort out details in chat · action: opens a chat · edge: tap: Maya's postup · Bean Theory
   - One chat per postup. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), **chat+msg@in.live** (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
3. **chat+msg@in.live** · user: Something off about a message · action: long-presses a message · edge: tap: Message options
   - Long-press: copy, report, block sender. [F096] [FS]
   - next site states: chat@in.live (close), report@in.live (Report message), chat+block@in.live (Block sender)
   - enterable flows: none

### Connected flows [M1025]
- `catch-up`: branch out at step 1→2; merge in at step 1 (from its step 2)

### Screens
1. `#inbox` · auth=in live=live — Inbox: one list of postup chats, newest first, unread dots. [F096] [M1033] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#inbox)
2. `#chat` · auth=in live=live — One chat per postup. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#chat)
3. `#chat` + sheet `msg` · auth=in live=live — Long-press: copy, report, block sender. [F096] [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=msg&ph=1#chat)

### Branches and edge cases
- Signed out: sign-in sheet over Inbox. [unsourced]
- Chat closes 24h after the postup. [R31] [FS]

### Success criteria
- Only poster + joined/approved can read. [F061]

### Needs Martin's decision
- Chat retention (24h default). [R31] [FS]

---

## Flow: Report and block (`safety`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: postup@in.live (close), profile@in.live (View profile), postup+share@in.live (Share), **report@in.live** (Report), postup+block@in.live (Block)
   - enterable flows: none
2. **report@in.live** · user: Wants to report · action: taps Report · edge: tap: Report
   - Reason + details. [F059] [drawn]
   - next site states: back (Back), **reported@in.live** (Send report), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
3. **reported@in.live** · user: Reported; still uneasy · action: sends the report · edge: tap: Send report
   - Thanks; offer to block. [FS]
   - next site states: home@in.live.live (Close), **reported+block@in.live** (Block Maya too), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
4. **reported+block@in.live** · user: Wants them gone · action: taps Block too · edge: tap: Block Maya too
   - Block: neither sees the other; they aren't told. [FS] [F059]
   - next site states: reported@in.live (close), home@in.live.live (Block), **settings@in.live** (Blocked people (Settings))
   - enterable flows: none
5. **settings@in.live** · user: Might undo later · action: opens Settings · edge: tap: Blocked people (Settings)
   - Blocked people list to undo. [FS] [F065]
   - next site states: back (Back), home@out.live.live (Sign out), settings+delacct@in.live (Delete account), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: delete-account step 2 (if Looking for the delete option), settings-notify step 1 (if Tuning alerts)

### Connected flows [M1025]
- `delete-account`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `settings-notify`: branch out at step 5→1; merge in at —

### Screens
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more&ph=0#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#reported)
4. `#reported` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block&ph=0#reported)
5. `#settings` · auth=in live=live — Blocked people list to undo. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=0#settings)

### Branches and edge cases
- Phase 0 keeps only Report and Block. [M1037]
- From a chat message: Message options → Report message. [F096]

### Success criteria
- No safety-tip screens. [F059] [FS]

### Needs Martin's decision
- No ban system yet: who reviews reports? [TK§4]

---

## Flow: Leave a postup you joined (`leave`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), joined+dirs@in.live (Directions), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), **joined+leave@in.live** (Leave), inbox@in.live (Inbox), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join)
2. **joined+leave@in.live** · user: Backing out politely · action: taps Leave · edge: tap: Leave
   - Confirm; poster alerted. [FS] [drawn]
   - next site states: joined@in.live (close), **postup@in.live** (Leave)
   - enterable flows: none
3. **postup@in.live** · user: Out; back on the postup page · action: confirms Leave · edge: tap: Leave
   - Back home. [M1024]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)

### Connected flows [M1025]
- `join`: branch out at step 1→3, step 3→2; merge in at step 1 (from its step 3), step 3 (from its step 2)
- `desktop-browse`: branch out at step 3→2; merge in at step 3 (from its step 2)

### Screens
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave&ph=1#joined)
3. `#postup` · auth=in live=live — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#postup)

### Branches and edge cases
- The poster ended or cancelled first: #postup-cancelled. [F060]

### Success criteria
- Poster knows. [FS]

---

## Flow: Share link to a project (`invite-project`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: project@out.live (See updates), **invite-project+signin@out.live** (Follow), profile@out.live (Next postup: weekdays at Bean Theo), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), projects@out.live (Projects)
   - enterable flows: none
2. **invite-project+signin@out.live** · user: Wants updates · action: taps Follow 🔒 · edge: tap: Follow
   - Follow 🔒 → sign-in sheet. [FS] [M1024]
   - next site states: invite-project@out.live (close), **invite-project@in.live** (Continue with Apple)
   - enterable flows: none
3. **invite-project@in.live** · user: Signed in; following · action: signs in · edge: tap: Continue with Apple
   - Sign-in returns to the same page, now following (Follow has no continuation). [M1031-draft]
   - next site states: **project@in.live** (See updates), profile@in.live (Next postup: weekdays at Bean Theo), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
4. **project@in.live** · user: Following · action: taps See updates · edge: tap: See updates
   - Following; live postups for the project shown. [FS] [M1024]
   - next site states: back (Back), project-new@in.live (New), profile@in.live (Maya), project-update@in.live (Update), project-attach@in.live (Post up), cafe@in.live (Bean Theory), postup@in.live (M Maya Bean Theory · till 4pm Live), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#invite-project` · auth=out live=live — "Maya is building Star Fox 64 mod". [FS] [F067] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=2#invite-project)
2. `#invite-project` + sheet `signin` · auth=out live=live — Follow 🔒 → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=2#invite-project)
3. `#invite-project` · auth=in live=live — Sign-in returns to the same page, now following (Follow has no continuation). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#invite-project)
4. `#project` · auth=in live=live — Following; live postups for the project shown. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#project)

### Branches and edge cases
- Project owner is live now: join from the project. [FS] [M1024]

### Success criteria
- Follow survives sign-in. [M1018] [M1024]

---

## Flow: Ask to join, then get approved (joiner side) (`ask-join`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), postup-ask+share@in.live (Share), postup-ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **ask@in.live** (Ask to join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: catch-up step 4 (if My request was approved)
2. **ask@in.live** · user: Explaining why they want to join · action: taps Ask to join · edge: tap: Ask to join
   - Short reason. [F061] [F095]
   - next site states: back (Back), ask+share@in.live (Share), ask+more@in.live (More), profile@in.live (T Tess Live · till 3pm), project@in.live (Pixel Garden Drawing crop sprites.), cafe@in.live (Grindhouse 1.1 mi · 22 min walk), **requested@in.live** (Send request), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects), cafe-gfail@in.live (Grindhouse 1.1 mi · 22 min walk (Google card fails))
   - enterable flows: none
3. **requested@in.live** · user: Waiting for an answer · action: sends the request · edge: tap: Send request
   - Request sent; can cancel. [FS] [drawn]
   - next site states: home@in.live.live (Close), quiet-feed@in.live (See who else is nearby), postup-ask@in.live (View postup), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
4. **activity@in.live** · user: Gets the yes · action: later: alert arrives · edge: event: alert arrives
   - Activity: "Tess said yes". [FS] [M1024]
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), **chat@in.live** (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: host-approve step 1 (if Hosting; someone wants in), following step 4 (if Hears that someone posted up), catch-up step 3 (if What else happened?)
5. **chat@in.live** · user: Now part of the group · action: opens the chat · edge: tap: M Maya: Hey! Here till 4 — come sa
   - Now in the postup chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `catch-up`: branch out at step 1→4, step 4→3; merge in at step 1 (from its step 4), step 4 (from its step 3)
- `following`: branch out at step 4→4; merge in at step 4 (from its step 4)
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

### Screens
1. `#postup-ask` · auth=in live=live — "Tess approves who joins". [FS] [F055] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-ask)
2. `#ask` · auth=in live=live — Short reason. [F061] [F095] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#ask)
3. `#requested` · auth=in live=live — Request sent; can cancel. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#requested)
4. `#activity` · auth=in live=live — Activity: "Tess said yes". [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
5. `#chat` · auth=in live=live — Now in the postup chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#chat)

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
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: inbox@in.live (Chats), postup@in.live (Maya posted up at Bean Theory), **live@in.live** (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: ask-join step 4 (if Gets the yes), following step 4 (if Hears that someone posted up), catch-up step 3 (if What else happened?)
2. **live@in.live** · user: Deciding on the request · action: opens the request · edge: tap: D Dev asked to join your postup 2
   - Requests with reason: Approve / Decline. [FS] [F061]
   - next site states: back (Back), live+share@in.live (Share), post-edit@in.live (Edit), **profile@in.live** (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), chat@in.live (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time)
3. **profile@in.live** · user: Wants to check the asker first · action: taps the asker · edge: tap: D Dev · 2 min ago
   - Optionally checks the asker's profile first. [FS] [M1024]
   - next site states: back (Back), profile+more@in.live (More), postup@in.live (Live at Bean Theory Till 4pm · Sta), cafe@in.live (Bean Theory), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Updated yesterday), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **live@in.live** · user: Asker looks fine; back to my postup · action: taps Back · edge: back
   - Back on your live postup; the profile has no chat link (as in the app). [M1031-draft]
   - next site states: back (Back), live+share@in.live (Share), post-edit@in.live (Edit), profile@in.live (J Jon On the way · 10 min), live+endlive@in.live (End postup), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), **chat@in.live** (Group chat), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: returning-post step 3 (if Managing their postup), hosting step 1 (if Live; wants more time)
5. **chat@in.live** · user: Approved; welcoming them · action: opens the group chat · edge: tap: Group chat
   - Approved people are in the chat. [F061] [F096]
   - next site states: back (Back), chat+more@in.live (More), postup@in.live (M J S Bean Theory · till 4pm · 3 p), chat+msg@in.live (Message options), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: chat step 2 (if Wants to sort out details in chat)

### Connected flows [M1025]
- `returning-post`: branch out at step 2→3, step 4→3; merge in at step 2 (from its step 3), step 4 (from its step 3)
- `ask-join`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `following`: branch out at step 1→4; merge in at step 1 (from its step 4)
- `catch-up`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `hosting`: branch out at step 2→1, step 4→1; merge in at —
- `chat`: branch out at step 5→2; merge in at step 5 (from its step 2)

### Screens
1. `#activity` · auth=in live=live — Alert: "Ari asked to join". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
2. `#live` · auth=in live=live — Requests with reason: Approve / Decline. [FS] [F061] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#live)
3. `#profile` · auth=in live=live — Optionally checks the asker's profile first. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#profile)
4. `#live` · auth=in live=live — Back on your live postup; the profile has no chat link (as in the app). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#live)
5. `#chat` · auth=in live=live — Approved people are in the chat. [F061] [F096] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#chat)

### Branches and edge cases
- Decline: joiner is told politely. [F095] [unsourced]
- Block from the request via More. [F059] [M1024]

### Success criteria
- Approve in one tap from #live. [FS] [M1024]

---

## Flow: Project builder: create, update, post up for it (`project-builder`)
Priority: **Phase 2 (MVP)** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: **project-new@in.none** (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home)
   - enterable flows: following step 3 (if Wants to see who they follow)
2. **project-new@in.none** · user: Starts a new project page · action: taps New project · edge: tap: New project
   - Cover, name, kind, one line. [FS] [drawn]
   - next site states: back (Back), **project@in.none** (Create), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
3. **project@in.none** · user: Project exists · action: taps Create · edge: tap: Create
   - New project page. [FS]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), **project-update@in.none** (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
4. **project-update@in.none** · user: Sharing progress · action: taps Update · edge: tap: Update
   - Post an update with image. [FS] [R35]
   - next site states: back (Back), **project@in.none** (Post update), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
5. **project@in.none** · user: Update can wait; post up first · action: taps Back · edge: back
   - Back on the project (Update has no Post up link, as in the app). [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), **project-attach@in.none** (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: following step 2 (if Wants to see what else is being built)
6. **project-attach@in.none** · user: Working on it at a cafe · action: taps Post up for this · edge: tap: Post up for this
   - Post up for this project, now or earlier today. [FS]
   - next site states: back (Back), **posted@in.none** (Post up), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: none
7. **posted@in.none** · user: Live for the project · action: taps Post up · edge: tap: Post up
   - Posted, tied to the project. [FS]
   - next site states: home@in.none.live (Close), posted+share@in.none (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Close), project@in.none (Star Fox 64 mod), projects@in.none (Projects), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

### Connected flows [M1025]
- `following`: branch out at step 1→3, step 3→2, step 5→2; merge in at step 1 (from its step 3), step 3 (from its step 2), step 5 (from its step 2)
- `first-post`: branch out at step 7→6; merge in at step 7 (from its step 6)
- `returning-post`: branch out at step 7→2; merge in at step 7 (from its step 2)

### Screens
1. `#projects` · auth=in live=none — Projects, "+". [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#projects)
2. `#project-new` · auth=in live=none — Cover, name, kind, one line. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-new)
3. `#project` · auth=in live=none — New project page. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
4. `#project-update` · auth=in live=none — Post an update with image. [FS] [R35] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-update)
5. `#project` · auth=in live=none — Back on the project (Update has no Post up link, as in the app). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
6. `#project-attach` · auth=in live=none — Post up for this project, now or earlier today. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project-attach)
7. `#posted` · auth=in live=none — Posted, tied to the project. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#posted)

### Branches and edge cases
- Signed out: Create / Post update open the sign-in sheet, form kept. [FS] [M1018]
- Signed out attach: #attach-signin. [FS]

### Success criteria
- Updates and postups show on the project timeline. [FS] [M1024]

### Needs Martin's decision
- Image storage for projects (Vercel Blob?). [TK§4]

---

## Flow: Follow a person or project (`following`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), **project@in.none** (Star Fox 64 mod Updated yesterday), home@in.none.building (home), projects@in.none (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: empty-area step 3 (if Who comes here?)
2. **project@in.none** · user: Wants to see what else is being built · action: taps Maya's project · edge: tap: Star Fox 64 mod Updated yesterday
   - Profile has no tab bar (as in the app), so: project first, then the Projects tab. [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home), **projects@in.none** (Projects), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: project-builder step 3 (if Project exists)
3. **projects@in.none** · user: Wants to see who they follow · action: taps Projects · edge: tap: Projects
   - Projects → Following filter. [FS] [R32]
   - next site states: project-new@in.none (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.live (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@in.none.building (Home)
   - enterable flows: project-builder step 1 (if Wants a home for their project)
4. **activity@in.live** · user: Hears that someone posted up · action: later: someone they follow posts up · edge: event: someone you follow posts up
   - Later: "Maya posted up" alert. [FS] [M1024] Event "someone you follow posts up": the alert lands in Activity and Nearby now has someone live. [M1031-draft]
   - next site states: inbox@in.live (Chats), **postup@in.live** (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), projects@in.live (Projects)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), catch-up step 3 (if What else happened?)
5. **postup@in.live** · user: Wants to go · action: taps the alert · edge: tap: Maya posted up at Bean Theory
   - Opens and joins. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone), desktop-browse step 2 (if Checking one postup)

### Connected flows [M1025]
- `project-builder`: branch out at step 2→3, step 3→1; merge in at step 2 (from its step 3)
- `empty-area`: branch out at step 1→3; merge in at step 1 (from its step 3)
- `ask-join`: branch out at step 4→4; merge in at step 4 (from its step 4)
- `catch-up`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `join`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `desktop-browse`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

### Screens
1. `#profile` · auth=in live=none — Follow → Following. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#profile)
2. `#project` · auth=in live=none — Profile has no tab bar (as in the app), so: project first, then the Projects tab. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#project)
3. `#projects` · auth=in live=none — Projects → Following filter. [FS] [R32] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#projects)
4. `#activity` · auth=in live=live — Later: "Maya posted up" alert. [FS] [M1024] Event "someone you follow posts up": the alert lands in Activity and Nearby now has someone live. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
5. `#postup` · auth=in live=live — Opens and joins. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup)

### Branches and edge cases
- Signed out: Follow → sign-in sheet. [FS]

### Success criteria
- Follow alerts arrive. [M1024]

### Needs Martin's decision
- Alert for "people you follow post up" is saved but not sent yet in the build. [unsourced]

---

## Flow: Postup ends, fills or is cancelled while you look (`postup-states`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
2. **postup-cancelled@in.live** · user: Host cancelled · action: later: postup cancelled · edge: event: postup is cancelled
   - Cancelled. [F060] [R47]
   - next site states: back (Back), postup-cancelled+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
3. **postup-full@in.live** · user: Checks the other postup · action: taps Back · edge: back
   - Back to the full postup (split: a cancelled postup doesn't later end). [M1031-draft]
   - next site states: back (Back), postup-full+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
4. **postup-ended@in.live** · user: Too late; it ended · action: later: postup ended · edge: event: postup ends
   - Ended: see what's nearby, follow. [drawn] Ending is this postup's status; others may still be live nearby. [M1031-draft]
   - next site states: back (Back), postup-ended+more@in.live (More), profile@in.live (M Maya Bean Theory), quiet-feed@in.live (See what's nearby), home@in.live.live (Go to Home), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: catch-up step 7 (if That one's over)

### Connected flows [M1025]
- `catch-up`: branch out at step 4→7; merge in at step 4 (from its step 7)

### Screens
1. `#postup-full` · auth=in live=live — Full. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-full)
2. `#postup-cancelled` · auth=in live=live — Cancelled. [F060] [R47] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-cancelled)
3. `#postup-full` · auth=in live=live — Back to the full postup (split: a cancelled postup doesn't later end). [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-full)
4. `#postup-ended` · auth=in live=live — Ended: see what's nearby, follow. [drawn] Ending is this postup's status; others may still be live nearby. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-ended)

### Success criteria
- Never a blank page. [F060]

---

## Flow: Slow network and offline (`loading-offline`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), projects@in.live (Projects)
   - enterable flows: none
2. **offline@in.live** · user: Connection dropped · action: later: network drops · edge: event: network drops
   - Cached feed + offline banner + Retry. [FS]
   - next site states: me@in.live (S), quiet@in.live (quiet), **quiet-feed@in.live** (Retry), post@in.live (Post up), cafe@in.live (Maya's photo), home@in.live.live (Home), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Maya's photo (Google card fails))
   - enterable flows: none
3. **quiet-feed@in.live** · user: Back online · action: taps Retry · edge: tap: Retry
   - Retry succeeds. [FS]
   - next site states: me@in.live (S), quiet@in.live (quiet), post@in.live (Post up), cafe@in.live (Maya's photo), home@in.live.live (Home), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), **cafe-gfail@in.live** (Maya's photo (Google card fails))
   - enterable flows: none
4. **cafe-gfail@in.live** · user: Checking a cafe; Google is down · action: taps a cafe · edge: tap: Maya's photo (Google card fails)
   - Google card failed: rest of cafe still works. [F060]
   - next site states: back (Back), cafe-gfail+share@in.live (Share), cafe@in.live (Bean Theory), postup@in.live (Join), cafe-gfail+dirs@in.live (Open in Maps), post@in.live (Post up here), home@in.live.live (Home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: none

### Connected flows [M1025]
- none

### Screens
1. `#loading` · auth=in live=live — Skeleton. [FS] [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#loading)
2. `#offline` · auth=in live=live — Cached feed + offline banner + Retry. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#offline)
3. `#quiet-feed` · auth=in live=live — Retry succeeds. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#quiet-feed)
4. `#cafe-gfail` · auth=in live=live — Google card failed: rest of cafe still works. [F060] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#cafe-gfail)

### Branches and edge cases
- First visit while offline: nothing cached (fails in the build today). [unsourced]

### Success criteria
- No blank screens. [FS]

### Needs Martin's decision
- Full offline screen vs banner only. [R46⚠] [FS]

---

## Flow: Delete account (`delete-account`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), **settings@in.none** (Settings), live@in.none (1:42 You're live at Bean Theory Ti), cafe@in.none (Lantern Tea), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), project-new@in.none (Tide Clock Updated Sun), home@in.none.building (home), projects@in.none (Projects), cafe-gfail@in.none (Lantern Tea (Google card fails))
   - enterable flows: none
2. **settings@in.none** · user: Looking for the delete option · action: taps Settings · edge: tap: Settings
   - Account section. [FS] [F065]
   - next site states: back (Back), home@out.none.live (Sign out), **settings+delacct@in.none** (Delete account), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), home@out.none.building (Sign out), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: settings-notify step 1 (if Tuning alerts)
3. **settings+delacct@in.none** · user: Sure about it · action: taps Delete account · edge: tap: Delete account
   - Confirm; can't be undone. [FS] [drawn]
   - next site states: settings@in.none (close), home@out.none.live (Delete account), **home@out.none.building** (Delete account)
   - enterable flows: none
4. **home@out.none.building** · user: Gone · action: confirms · edge: tap: Delete account
   - Signed out at Home. [M1024]
   - next site states: cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.live (Live), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- `settings-notify`: branch out at step 2→1; merge in at —

### Screens
1. `#me` · auth=in live=none — My profile → Settings. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#me)
2. `#settings` · auth=in live=none — Account section. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#settings)
3. `#settings` + sheet `delacct` · auth=in live=none — Confirm; can't be undone. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=delacct&ph=2#settings)
4. `#home` · auth=out live=none mode=building — Signed out at Home. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building&ph=2#home)

### Branches and edge cases
- Deleting while live: postup ends and joiners are alerted? [unsourced]

### Success criteria
- All their content gone. [FS]

### Needs Martin's decision
- What happens to a live postup and chats on delete. [unsourced]

---

## Flow: Desktop browse and post (`desktop-browse`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: **postup@in.live** (M 2), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), postup-ask@in.live (T), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), catch-up step 1 (if What did I miss?)
2. **postup@in.live** · user: Checking one postup · action: taps a live pin · edge: tap: M 2
   - Postup in the panel. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), **post@in.live** (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod Adding a new Corne), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: join step 2 (if Found someone)
3. **post@in.live** · user: Wants to post too · action: taps Post up · edge: tap: Post up
   - Post up as a centered dialog. [FS]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), me@in.live (S), inbox@in.live (Inbox), project-new@in.live (Project), projects@in.live (Projects)
   - enterable flows: returning-post step 1 (if Regular; working at a cafe today)
4. **posted@in.live** · user: Posted; now live for others · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), posted+share@in.live (Invite friends), live@in.live (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), me@in.live (S), inbox@in.live (Inbox), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company), returning-post step 2 (if Posted; now live for others)

### Connected flows [M1025]
- `first-post`: branch out at step 4→6; merge in at step 4 (from its step 6)
- `catch-up`: branch out at step 1→1; merge in at —
- `join`: branch out at step 2→2; merge in at —
- `returning-post`: branch out at step 4→2; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Map with 440px panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&mode=live&ph=2#home)
2. `#postup` · auth=in live=live — Postup in the panel. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#postup)
3. `#post` · auth=in live=live — Post up as a centered dialog. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#post)
4. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=desktop&auth=in&live=live&ph=2#posted)

### Success criteria
- Rail and tab bar have the same items. [F064] [R12]

---

## Flow: Notification settings and sign out (`settings-notify`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
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
   - next site states: back (Back), home@out.none.live (Sign out), settings+delacct@in.none (Delete account), home@in.none.live (home), quiet-feed@in.none (Nearby), post@in.none (Post up), me@in.none (S), inbox@in.none (Inbox), **home@out.none.building** (Sign out), home@in.none.building (home), projects@in.none (Projects)
   - enterable flows: delete-account step 2 (if Looking for the delete option)
2. **home@out.none.building** · user: Done for now · action: taps Sign out · edge: tap: Sign out
   - Signed out. [M1024]
   - next site states: cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), post@out.none (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), home@out.none.live (Live), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none

### Connected flows [M1025]
- `delete-account`: branch out at step 1→2; merge in at step 1 (from its step 2)

### Screens
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none&ph=2#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building&ph=2#home)

### Success criteria
- Toggles actually change alerts. [M1024]

### Needs Martin's decision
- Email alerts at launch? [TK§4]

---

## Flow: Catch up on what happened (`catch-up`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/catch-up.html

### Persona
- Registered user coming back after a while away.

### Starting state
- auth=in · live=live · device=phone · entry URL `/`

### Goal
- See what happened since last time: replies, approvals, ended postups. [M1031-draft]

### Steps
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

### Connected flows [M1025]
- `ask-join`: branch out at step 3→4, step 4→1, step 5→4; merge in at step 3 (from its step 4), step 5 (from its step 4)
- `following`: branch out at step 3→4, step 5→4; merge in at step 3 (from its step 4), step 5 (from its step 4)
- `chat`: branch out at step 2→1, step 6→1, step 9→2; merge in at —
- `host-approve`: branch out at step 3→1, step 5→1; merge in at —
- `join`: branch out at step 1→1; merge in at —
- `desktop-browse`: branch out at step 1→1; merge in at —

### Screens
1. `#home` · auth=in live=live mode=live — Home in Live mode; Inbox tab shows an unread dot. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=2#home)
2. `#inbox` · auth=in live=live — Chats: group chats, newest first, including an ended postup. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#inbox)
3. `#activity` · auth=in live=live — Activity: joins, requests, approvals, follows, messages. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
4. `#postup-ask` · auth=in live=live — Tess's postup. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-ask)
5. `#activity` · auth=in live=live — Activity again. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#activity)
6. `#inbox` · auth=in live=live — Chats list. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#inbox)
7. `#postup-ended` · auth=in live=live — Ended postup: see what's nearby, follow. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#postup-ended)
8. `#inbox` · auth=in live=live — Chats list. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#inbox)
9. `#chat` · auth=in live=live — Group chat with the latest replies. [drawn] [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=2#chat)

### Branches and edge cases
- Nothing happened while away: Activity and Chats need a positive empty state, never "quiet". [F035] [M1031-draft]

### Success criteria
- From Home, the user reaches replies, an approval and an ended postup through the Inbox. [M1031-draft]

### Needs Martin's decision
- No "since you were away" summary exists; catching up means opening Inbox, then each item. [M1031-draft]
- No unread or new markers per item beyond the Activity count badge; there is no way to tell what is new since last visit. [M1031-draft]
- An approval ("Tess said yes") opens Tess's postup as Ask to join, not a joined/approved state. [M1031-draft]
- Ended postups appear only in Chats ("Tess's postup · Ended"), not as an Activity alert. [M1031-draft]
- Replies show as one Activity row per message linking to the group chat; there is no reply thread view. [M1031-draft]
