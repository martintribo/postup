# Flow: Returning poster (`returning-post`)
Priority: **Phase 1** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/returning-post.html

## Persona
- Signed-in regular.

## Starting state
- auth=in · live=live · device=phone · entry URL `/`

## Goal
- Post up with defaults, then see you're live. [M1024]

## Steps
1. **post@in.live** · user: Regular; working at a cafe today · action: taps Post up · edge: entry
   - Last project and nearest cafe preselected; no 🔒. [FS] [M1024]
   - next site states: back (Back), where@in.live (Bean Theory Nearest · 0.4 mi Chang), **posted@in.live** (Post up), home@in.live.live (home), quiet-feed@in.live (Nearby), inbox@in.live (Inbox), me@in.live (S), project-new@in.live (Project), projects@in.live (Projects)
   - enterable flows: desktop-browse step 3 (if Wants to post too)
2. **posted@in.live** · user: Posted; now live for others · action: taps Post up · edge: tap: Post up
   - Posted. [FS]
   - next site states: home@in.live.live (Close), posted+share@in.live (Invite friends), **live@in.live** (Manage postup), cafe@in.live (Cafe), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), me@in.live (S), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (Cafe (Google card fails))
   - enterable flows: first-post step 6 (if Live; wants company)
3. **live@in.live** · user: Managing their postup · action: opens their live postup · edge: tap: Manage postup
   - You're live: time left, requests, chat. [FS] [F057]
   - next site states: back (Back), live+share@in.live (Share), post-edit@in.live (Edit), profile@in.live (D Dev · 2 min ago), chat@in.live (Group chat), live+endlive@in.live (End postup), **home@in.live.live** (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), me@in.live (S), project@in.live (Star Fox 64 mod), projects@in.live (Projects)
   - enterable flows: hosting step 1 (if Live; wants more time), host-approve step 2 (if Deciding on the request)
4. **home@in.live.live** · user: Checks they show up on Home · action: goes Home · edge: tap: Home
   - Your live state shows on home. [R22]
   - next site states: postup@in.live (M 2), postup-ask@in.live (T), cafe@in.live (cafe), quiet@in.live (Locate), quiet-feed@in.live (Nearby), post@in.live (Post up), inbox@in.live (Inbox), me@in.live (S), home@in.live.building (Building), project@in.live (Star Fox 64 mod), projects@in.live (Projects), cafe-gfail@in.live (cafe (Google card fails))
   - enterable flows: join step 1 (if Wants company now), desktop-browse step 1 (if At a laptop; browsing), catch-up step 1 (if What did I miss?)

## Connected flows [M1025]
- `first-post`: branch out at step 2→6; merge in at step 2 (from its step 6)
- `host-approve`: branch out at step 3→2; merge in at step 3 (from its step 2)
- `desktop-browse`: branch out at step 4→1; merge in at step 1 (from its step 3)
- `hosting`: branch out at step 3→1; merge in at —
- `join`: branch out at step 4→1; merge in at —
- `catch-up`: branch out at step 4→1; merge in at —

## Screens
1. `#post` · auth=in live=live — Last project and nearest cafe preselected; no 🔒. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#post)
2. `#posted` · auth=in live=live — Posted. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#posted)
3. `#live` · auth=in live=live — You're live: time left, requests, chat. [FS] [F057] (/mockups/?style=fresh&device=phone&auth=in&live=live&ph=1#live)
4. `#home` · auth=in live=live mode=live — Your live state shows on home. [R22] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live&ph=1#home)

## Branches and edge cases
- Already live: Post up opens #live instead of a second postup. [unsourced] [M1024]

## Success criteria
- Home → live in 2 taps. [M1024]

## Needs Martin's decision
- Can someone have two postups at once? [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
