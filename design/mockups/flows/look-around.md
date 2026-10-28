# Flow: Newcomer looks around, then joins (`look-around`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/look-around.html

## Persona
- First-time visitor, signed out: curious what PostUp is, or has no idea and arrived from search, a social post or a link.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, see live and past content, and join someone; sign in only at Join. [M1024] [M1025] [M1032]

## Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: **postup@out.live** (M 2), cafe@out.live (cafe), quiet@out.live (Locate), quiet-feed@out.live (Nearby), post@out.live (Post up), inbox@out.live (Inbox), me@out.live (S), postup-ask@out.live (T), home@out.live.building (Building), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: none
2. **postup@out.live** · user: What is she doing? · action: taps Maya's live row · edge: tap: M Maya Live Bean Theory · till 4pm
   - Her live postup: who, cafe, till when; Join shows 🔒. Projects are phase 2, so the newcomer learns by example from a live postup. [FS] [M1024] [M1034]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), **profile@out.live** (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), postup+signin@out.live (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: none
3. **profile@out.live** · user: Who is behind it? · action: taps Maya · edge: tap: M Maya Live · till 4pm
   - Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025]
   - next site states: back (Back), profile+more@out.live (More), **postup@out.live** (Live at Bean Theory Till 4pm · Sta), profile+signin@out.live (Follow), cafe@out.live (Bean Theory), home@out.live.live (home), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), project@out.live (Star Fox 64 mod Updated yesterday), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: none
4. **postup@out.live** · user: She's live right now · action: taps Live at Bean Theory · edge: tap: Live at Bean Theory Till 4pm · Sta
   - Her live postup; Join shows 🔒. [FS] [M1024]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **postup+signin@out.live** (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), inbox@out.live (Inbox), post@out.live (Post up), me@out.live (S), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: none
5. **postup+signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: postup@out.live (close), postup@in.live (Continue with Apple), **joined@in.live** (signs in → continues)
   - enterable flows: none
6. **joined@in.live** · user: Signed in; committed · action: signs in · edge: tap: Continue with Apple
   - Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024]
   - next site states: home@in.live.live (Close), cafe@in.live (Bean Theory), chat@in.live (Group chat), joined+dirs@in.live (Directions), joined+leave@in.live (Leave), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), me@in.live (S), project@in.live (Project), projects@in.live (Projects), cafe-gfail@in.live (Bean Theory (Google card fails))
   - enterable flows: join step 3 (if Decides to join), invite-live step 3 (if Signed in; going), leave step 1 (if Plans changed)

## Connected flows [M1025]
- `join`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `invite-live`: branch out at step 6→3; merge in at step 6 (from its step 3)
- `leave`: branch out at step 6→1; merge in at —

## Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live&ph=1#home)
2. `#postup` · auth=out live=live — Her live postup: who, cafe, till when; Join shows 🔒. Projects are phase 2, so the newcomer learns by example from a live postup. [FS] [M1024] [M1034] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#postup)
3. `#profile` · auth=out live=live — Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#profile)
4. `#postup` · auth=out live=live — Her live postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=1#postup)
5. `#postup` + sheet `signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=1#postup)
6. `#joined` · auth=in live=live — Signed in and joined in one go; the join is not lost. [FS] [M1018] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#joined)

## Branches and edge cases
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

## Success criteria
- No sign-in before an action. [FS]
- After sign-in the original action completes. [M1018] [M1024]
- Sees live and past content without signing in. [FS] [M1025]
- Sign-in asked only at an action (Follow). [FS] [TK§1]
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

## Needs Martin's decision
- Should signed-out browsers ever get a soft sign-in nudge before an action? Today it is only at actions. [M1025]
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
