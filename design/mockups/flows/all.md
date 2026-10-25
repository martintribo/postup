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
1. `#home` · auth=in live=live mode=live — Opens / in Live mode: map + Live now list. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)
2. `#postup` · auth=in live=live — Taps Maya's row: who, project, cafe, who else is joining. Does not join yet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
3. `#project` · auth=in live=live — Opens Maya's project to see what she's working on, then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#project)
4. `#profile` · auth=in live=live — Opens Maya's profile: postup count, regular cafes, past postups. [FS] [F065] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#profile)
5. `#cafe` · auth=in live=live — Checks the cafe: hero photo, who's here now, Google card. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#cafe)
6. `#postup-ask` · auth=in live=live — Compares a second postup (Tess approves who joins), then Back. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup-ask)
7. `#postup` · auth=in live=live — Returns to Maya's postup and taps Join (no sign-in sheet; already signed in). [TK§1] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#postup)
8. `#joined` · auth=in live=live — You're joining Maya; Maya is told. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
9. `#joined` + sheet `dirs` · auth=in live=live — Directions sheet: Apple / Google Maps. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=dirs#joined)

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
1. `#invite-ended` · auth=out live=none — "This postup ended" + what's around. [FS] [R39] (/mockups/?style=fresh&device=phone&auth=out&live=none#invite-ended)
2. `#profile` + sheet `signin` · auth=out live=none — Follow the poster → sign-in sheet. [FS] [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&ov=signin#profile)
3. `#home` · auth=in live=none mode=building — Continues to Home. [M1018b] [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

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
1. `#live` · auth=in live=live — +30 min extends. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
2. `#post-edit` · auth=in live=live — Edit cafe/what/until; Save → #live. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#post-edit)
3. `#live` · auth=in live=live — Back on live. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#live)
4. `#live` + sheet `endlive` · auth=in live=live — End postup → confirm; joiners and waiters alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=endlive#live)
5. `#home` · auth=in live=none mode=building — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=none&mode=building#home)

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
1. `#postup` + sheet `more` · auth=in live=live — More: profile, share, report, block. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=more#postup)
2. `#report` · auth=in live=live — Reason + details. [F059] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#report)
3. `#reported` · auth=in live=live — Thanks; offer to block. [FS] (/mockups/?style=fresh&device=phone&auth=in&live=live#reported)
4. `#postup` + sheet `block` · auth=in live=live — Block: neither sees the other; they aren't told. [FS] [F059] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=block#postup)
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
1. `#joined` · auth=in live=live — Leave link. [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live#joined)
2. `#joined` + sheet `leave` · auth=in live=live — Confirm; poster alerted. [FS] [drawn] (/mockups/?style=fresh&device=phone&auth=in&live=live&ov=leave#joined)
3. `#home` · auth=in live=live mode=live — Back home. [M1024] (/mockups/?style=fresh&device=phone&auth=in&live=live&mode=live#home)

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
1. `#settings` · auth=in live=none — Toggles; Sign out. [FS] [F065] (/mockups/?style=fresh&device=phone&auth=in&live=none#settings)
2. `#home` · auth=out live=none mode=building — Signed out. [M1024] (/mockups/?style=fresh&device=phone&auth=out&live=none&mode=building#home)

### Success criteria
- Toggles actually change alerts. [M1024]

### Needs Martin's decision
- Email alerts at launch? [TK§4]
