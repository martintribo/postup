# Flow: First visit → Leaves without signing in (`first-visit--not-now`)
Priority: **Phase 0** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-visit--not-now.html

## Persona
- First-time visitor, signed out. Arrives at / (someone live nearby or not) or from a link a friend sent.

## Starting state
- auth=out · live=live · device=phone · entry URL `/`

## Goal
- Understand PostUp from the first screen, whatever the area looks like, then join someone, post up, or leave. [M1024] [M1032] [M1041]

## Steps
1. **home@out.live.live** · user: Curious what this is; sees people live · action: arrives at / · edge: entry
   - Home in Live mode: map + Live now. [M1018b] [M1025]
   - next site states: **postup@out.live** (M 2), cafe@out.live (cafe), quiet@out.live (Locate), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), postup-ask@out.live (T), home@out.live.building (Building), project@out.live (Star Fox 64 mod), projects@out.live (Projects), cafe-gfail@out.live (cafe (Google card fails))
   - enterable flows: first-visit step 1 (if Curious what this is; sees people live), first-visit--browse step 1 (if Curious what this is; sees people live)
2. **postup@out.live** · user: What is she doing? · action: taps Maya's live row · edge: tap: M Maya Live Bean Theory · till 4pm
   - Her live postup: who, cafe, till when; Join shows 🔒. Projects are phase 2, so the newcomer learns by example from a live postup. [FS] [M1024] [M1034]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), **profile@out.live** (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), postup+signin@out.live (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit step 2 (if What is she doing?)
3. **profile@out.live** · user: Who is behind it? · action: taps Maya · edge: tap: M Maya Live · till 4pm
   - Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025]
   - next site states: back (Back), profile+more@out.live (More), **postup@out.live** (Live at Bean Theory Till 4pm · Sta), profile+signin@out.live (Follow), cafe@out.live (Bean Theory), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Updated yesterday), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory (Google card fails))
   - enterable flows: first-visit step 3 (if Who is behind it?)
4. **postup@out.live** · user: She's live right now · action: taps Live at Bean Theory · edge: tap: Live at Bean Theory Till 4pm · Sta
   - Her live postup; Join shows 🔒. [FS] [M1024]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), **postup+signin@out.live** (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit step 2 (if What is she doing?)
5. **postup+signin@out.live** · user: Wants to join; asked to sign in · action: taps Join 🔒 · edge: tap: Join
   - Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024]
   - next site states: **postup@out.live** (close), postup@in.live (Continue with Apple), joined@in.live (signs in → continues)
   - enterable flows: first-visit step 5 (if Wants to join; asked to sign in)
6. **postup@out.live** · user: Not ready to make an account · action: taps Not now · edge: tap: Not now
   - Back on the postup, still signed out; they can leave. [drawn] [M1025] [M1041]
   - next site states: back (Back), postup+share@out.live (Share), postup+more@out.live (More), profile@out.live (M Maya Live · till 4pm), cafe@out.live (Bean Theory 0.4 mi · 8 min walk), postup+signin@out.live (Join), home@out.live.live (home), quiet-feed@out.live (Nearby), post@out.live (Post up), me@out.live (S), inbox@out.live (Inbox), project@out.live (Star Fox 64 mod Adding a new Corne), projects@out.live (Projects), cafe-gfail@out.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: first-visit step 2 (if What is she doing?)

## Connected flows [M1025]
- `first-visit`: branch out at step 4→2, step 5→5, step 6→2; merge in at step 4 (from its step 2), step 6 (from its step 2)
- `first-visit--browse`: branch out at step 1→1; merge in at —

## Screens
1. `#home` · auth=out live=live mode=live — Home in Live mode: map + Live now. [M1018b] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&mode=live&ph=0#home)
2. `#postup` · auth=out live=live — Her live postup: who, cafe, till when; Join shows 🔒. Projects are phase 2, so the newcomer learns by example from a live postup. [FS] [M1024] [M1034] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#postup)
3. `#profile` · auth=out live=live — Maker's profile: past postups, regular cafes, live now. [FS] [F065] [M1025] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#profile)
4. `#postup` · auth=out live=live — Her live postup; Join shows 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#postup)
5. `#postup` + sheet `signin` · auth=out live=live — Join → sign-in sheet (Apple / Google). [FS] [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=live&ov=signin&ph=0#postup)
6. `#postup` · auth=out live=live — Back on the postup, still signed out; they can leave. [drawn] [M1025] [M1041] (/mockups/?style=fresh&device=phone&auth=out&live=live&ph=0#postup)

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
