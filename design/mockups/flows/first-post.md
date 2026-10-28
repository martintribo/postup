# Flow: Came to post up: first post with sign-in (`first-post`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/first-post.html

## Persona
- First-time visitor already at a cafe who came to go live right now (signed out).

## Starting state
- auth=out · live=none · device=phone · entry URL `/`

## Goal
- Go live in about ten seconds. [M1024]

## Steps
1. **home@out.none.building** · user: Came to post up right now · action: arrives at / · edge: entry
   - Taps Post up. [M1018b]
   - next site states: home@out.none.live (Live), cafe@out.none (Lantern Tea A D M 3 postups), me@out.none (S), projects@out.none (See all projects), project@out.none (Star Fox 64 mod M Maya · Yesterday), **post@out.none** (Post up), quiet-feed@out.none (Nearby), inbox@out.none (Inbox), empty-area@out.none (area has no postups), cafe-gfail@out.none (Lantern Tea A D M 3 postups (Google card fails))
   - enterable flows: none
2. **post@out.none** · user: Filling in the post · action: taps Post up · edge: tap: Post up
   - Nearest cafe prefilled. [FS] [F062]
   - next site states: back (Back), **where@out.none** (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), post+signin@out.none (Post up), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), me@out.none (S)
   - enterable flows: none
3. **where@out.none** · user: Not at the nearest cafe · action: taps Change · edge: tap: Bean Theory Nearest · 0.4 mi Chang
   - Change → cafe picker by distance. [F062] [R17]
   - next site states: back (Back), project-new@out.none (Project), where+signin@out.none (Post up), **where-search@out.none** (Search cafes), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), post@out.none (Post up), me@out.none (S)
   - enterable flows: none
4. **where-search@out.none** · user: Looking for the right cafe · action: searches · edge: tap: Search cafes
   - Searches a cafe. [FS]
   - next site states: back (Back), where@out.none (Bean Theory Nearest · 0.4 mi Chang), project-new@out.none (Project), **where-search+signin@out.none** (Post up), home@out.none.building (home), quiet-feed@out.none (Nearby), projects@out.none (Projects), inbox@out.none (Inbox), post@out.none (Post up), me@out.none (S)
   - enterable flows: none
5. **where-search+signin@out.none** · user: Ready; asked to sign in · action: taps Post up 🔒 · edge: tap: Post up
   - Post up 🔒 → sign-in. [FS] [TK§1]
   - next site states: where-search@out.none (close), where-search@in.none (Continue with Apple), **posted@in.none** (signs in → continues)
   - enterable flows: none
6. **posted@in.none** · user: Live; wants company · action: signs in · edge: tap: Continue with Apple
   - Posted; link to copy. [FS]
   - next site states: home@in.none.building (Close), project@in.none (Star Fox 64 mod), **posted+share@in.none** (Invite friends), live@in.none (Manage postup), cafe@in.none (Cafe), quiet-feed@in.none (Nearby), post@in.none (Post up), projects@in.none (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Cafe (Google card fails))
   - enterable flows: returning-post step 2 (if Posted; now live for others)
7. **posted+share@in.none** · user: Wants friends to come too · action: taps Invite friends · edge: tap: Invite friends
   - Invite friends: share sheet. [drawn] [M1024]
   - next site states: posted@in.none (close)
   - enterable flows: none

## Connected flows [M1025]
- `returning-post`: branch out at step 6→2; merge in at step 6 (from its step 2)

## Screens
1. `#home` · auth=out live=none mode=building — Taps Post up. [M1018b] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)
2. `#post` · auth=out live=none — Nearest cafe prefilled. [FS] [F062] (/mockups/?style=fresh&device=phone&auth=out&live=none#post)
3. `#where` · auth=out live=none — Change → cafe picker by distance. [F062] [R17] (/mockups/?style=fresh&device=phone&auth=out&live=none#where)
4. `#where-search` · auth=out live=none — Searches a cafe. [FS] (/mockups/?style=fresh&device=phone&auth=out&live=none#where-search)
5. `#where-search` + sheet `signin` · auth=out live=none — Post up 🔒 → sign-in. [FS] [TK§1] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#where-search)
6. `#posted` · auth=in live=none — Posted; link to copy. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#posted)
7. `#posted` + sheet `share` · auth=in live=none — Invite friends: share sheet. [drawn] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&ov=share#posted)

## Branches and edge cases
- Location denied: picker falls back to search. [R21] [unsourced]
- Cafe search fails without a Maps key → error state. [unsourced]

## Success criteria
- The form is not lost through sign-in. [M1018] [M1024]

## Needs Martin's decision
- Location-permission explainer: in or out? (ledger open, final list says not adopted) [R21] [FS]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
