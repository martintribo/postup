# Flow: Stumbled on it: what is this? (`stumbled`)
Priority: **MVP must** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/stumbled.html

## Persona
- First-time visitor with no idea what PostUp is; arrived from search, a social post or a word-of-mouth link.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp within the first screen and reach something real before any sign-in. [M1025]

## Steps
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

## Connected flows [M1025]
- `curious-browser`: branch out at step 2→2, step 4→3, step 5→5; merge in at step 4 (from its step 3), step 5 (from its step 5)
- `first-visit-live`: branch out at step 2→2; merge in at —

## Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. No explainer line is drawn in Live mode, only the brand. [drawn] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live#home)
2. `#postup` · auth=out live=live — Taps the first live person to see what a postup is. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#postup)
3. `#cafe` · auth=out live=live — Taps the cafe: who is here now, Post up here. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#cafe)
4. `#home` · auth=out live=live mode=building — Back on Home, flips to Building: the welcome line "Post up at a cafe. See who's working nearby." and "What people are building". [drawn] [M1018c] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=building#home)
5. `#project` · auth=out live=live — Opens a project and gets the idea; Follow and Post up (🔒) are the next steps. [FS] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live#project)

## Branches and edge cases
- Nobody live: Home opens in Building, where the welcome line shows first. [M1018b] [drawn] [M1025]
- Dismisses the welcome (×): it should stay dismissed. [drawn] [unsourced]
- Leaves after the first screen: the value has to be clear without scrolling. [M1025]

## Success criteria
- Knows what PostUp is from the first screen in either mode. [M1025]
- Reaches a live postup or a project in one tap, no sign-in. [FS] [M1025]

## Needs Martin's decision
- Home in Live mode has no one-line explainer (only Building has the welcome). Add it to Live mode too, or a fuller "How it works"? [M1025]
- Welcome copy and when it stops showing (dismissed, signed in, after N visits). [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
