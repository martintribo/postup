# Flow: Follow a person or project (`following`)
Priority: **Unphased** · Status: Draft, inferred from the notes; confirm with Martin [M1024]
Player: /mockups/flows/following.html

## Persona
- Signed-in user who liked someone's work.

## Starting state
- auth=in · live=none · device=phone · entry URL `/u/maya`

## Goal
- Hear when they post up next. [M1024]

## Steps
1. **profile@in.none** · user: Likes someone's work · action: opens a profile · edge: entry
   - Follow → Following. [FS]
   - next site states: back (Back), profile+more@in.none (More), cafe@in.none (Bean Theory), **project@in.none** (Star Fox 64 mod Updated yesterday), home@in.none.building (home), quiet-feed@in.none (Nearby), projects@in.none (Projects), inbox@in.none (Inbox), post@in.none (Post up), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: none
2. **project@in.none** · user: Wants to see what else is being built · action: taps Maya's project · edge: tap: Star Fox 64 mod Updated yesterday
   - Profile has no tab bar (as in the app), so: project first, then the Projects tab. [M1031-draft]
   - next site states: back (Back), project-new@in.none (New), profile@in.none (Maya), project-update@in.none (Update), project-attach@in.none (Post up), cafe@in.none (Bean Theory), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), **projects@in.none** (Projects), inbox@in.none (Inbox), me@in.none (S), cafe-gfail@in.none (Bean Theory (Google card fails))
   - enterable flows: project-builder step 3 (if Project exists)
3. **projects@in.none** · user: Wants to see who they follow · action: taps Projects · edge: tap: Projects
   - Projects → Following filter. [FS] [R32]
   - next site states: project-new@in.none (New project), project@in.none (Star Fox 64 mod M Maya · Yesterday), home@in.none.building (Home), quiet-feed@in.none (Nearby), post@in.none (Post up), inbox@in.none (Inbox), me@in.none (S)
   - enterable flows: project-builder step 1 (if Wants a home for their project)
4. **activity@in.live** · user: Hears that someone posted up · action: later: someone they follow posts up · edge: event: someone you follow posts up
   - Later: "Maya posted up" alert. [FS] [M1024] Event "someone you follow posts up": the alert lands in Activity and Nearby now has someone live. [M1031-draft]
   - next site states: inbox@in.live (Chats), **postup@in.live** (Maya posted up at Bean Theory), live@in.live (D Dev asked to join your postup 2), chat@in.live (M Maya: Hey! Here till 4 — come sa), postup-ask@in.live (T Tess said yes to your request Ye), profile@in.live (A Ari followed you Mon), home@in.live.live (Home), quiet-feed@in.live (Nearby), post@in.live (Post up), projects@in.live (Projects), me@in.live (S)
   - enterable flows: ask-join step 4 (if Gets the yes), host-approve step 1 (if Hosting; someone wants in), catch-up step 3 (if What else happened?)
5. **postup@in.live** · user: Wants to go · action: taps the alert · edge: tap: Maya posted up at Bean Theory
   - Opens and joins. [FS]
   - next site states: back (Back), postup+share@in.live (Share), postup+more@in.live (More), profile@in.live (M Maya Live · till 4pm), project@in.live (Star Fox 64 mod Adding a new Corne), cafe@in.live (Bean Theory 0.4 mi · 8 min walk), joined@in.live (Join), home@in.live.live (home), quiet-feed@in.live (Nearby), projects@in.live (Projects), inbox@in.live (Inbox), post@in.live (Post up), me@in.live (S), cafe-gfail@in.live (Bean Theory 0.4 mi · 8 min walk (Google card fails))
   - enterable flows: cautious-joiner step 2 (if Interested in Maya, not sure yet), quick-joiner step 2 (if Found them; joining), desktop-browse step 2 (if Checking one postup)

## Connected flows [M1025]
- `project-builder`: branch out at step 2→3, step 3→1; merge in at step 2 (from its step 3)
- `ask-join`: branch out at step 4→4; merge in at step 4 (from its step 4)
- `catch-up`: branch out at step 4→3; merge in at step 4 (from its step 3)
- `cautious-joiner`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `quick-joiner`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `desktop-browse`: branch out at step 5→2; merge in at step 5 (from its step 2)
- `host-approve`: branch out at step 4→1; merge in at —

## Screens
1. `#profile` · auth=in live=none — Follow → Following. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=none#profile)
2. `#project` · auth=in live=none — Profile has no tab bar (as in the app), so: project first, then the Projects tab. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=none#project)
3. `#projects` · auth=in live=none — Projects → Following filter. [FS] [R32] (/mockups/?style=fresh&device=phone&auth=in&live=none#projects)
4. `#activity` · auth=in live=live — Later: "Maya posted up" alert. [FS] [M1024] Event "someone you follow posts up": the alert lands in Activity and Nearby now has someone live. [M1031-draft] (/mockups/?style=fresh&device=phone&auth=in&live=live#activity)
5. `#postup` · auth=in live=live — Opens and joins. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)

## Branches and edge cases
- Signed out: Follow → sign-in sheet. [FS]

## Success criteria
- Follow alerts arrive. [M1024]

## Needs Martin's decision
- Alert for "people you follow post up" is saved but not sent yet in the build. [unsourced]

Tags: F### = fact (Martin's words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing. M1024 = Martin, Oct 24 2026: track critical flows.
