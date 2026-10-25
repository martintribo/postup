# PostUp site graph
Site graph (Martin, Oct 25 2026 [M1025]): 44 pages + 9 sheets, 296 site states (page [+ sheet] × auth out|in × live|none, Home × mode), 2806 edges derived from the mockup links plus site events. A flow is a path of steps, each = (site state, user state, action). Site-state id: page[+sheet]@auth.live[.mode].

Site events on every page: someone goes live / postups end (live ↔ none), alert arrives → Activity (signed in), comes back later → Home, network drops → Offline (Home, Nearby, Loading), postup fills / is cancelled / ends (postup pages).

Dimensions: auth = out | in; live = live (someone live nearby) | none; mode = live | building (Home only); data conditions are pages: postup-ask (host approves), postup-full, postup-cancelled, postup-ended, live (you are hosting), joined, requested (pending ask), empty-area, offline, cafe-gfail.

## Home & discover

### Home page (/) (`home`)
States: `home@out.live.live`, `home@out.live.building`, `home@out.none.live`, `home@out.none.building`, `home@in.live.live`, `home@in.live.building`, `home@in.none.live`, `home@in.none.building`
- (tap) → `cafe` [tap] — only in·live·live, in·none·live, out·live·live, out·none·live
- Bean Theory → `cafe` [tap] — only in·live·live, out·live·live
- Grindhouse → `cafe` [tap] — only in·live·live, out·live·live
- Lantern Tea A D M 3 postups → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Post up → `post` [tap]
- M 2 → `postup` [tap] — only in·live·live, out·live·live
- T → `postup` [tap] — only in·live·live, out·live·live
- M Maya Live Bean Theory · till 4pm → `postup` [tap] — only in·live·live, out·live·live
- J Jon Live Bean Theory · till 5pm → `postup` [tap] — only in·live·live, out·live·live
- T Tess Live Grindhouse · till 3pm  → `postup` [tap] — only in·live·live, out·live·live
- Star Fox 64 mod → `project` [tap] — only in·live·live, out·live·live
- Pixel Garden → `project` [tap] — only in·live·live, out·live·live
- Star Fox 64 mod M Maya · Yesterday → `project` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Pixel Garden T Tess · Tue New crop → `project` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Bus Stop Zine J Jon · Mon Page 12  → `project` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Projects → `projects` [tap]
- See all projects → `projects` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Locate → `quiet` [tap] — only in·live·live, in·none·live, out·live·live, out·none·live
- Nearby → `quiet-feed` [tap]
-  (Google card fails) → `cafe-gfail` [cond] — only in·live·live, in·none·live, out·live·live, out·none·live
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live·live, out·live·live
- Grindhouse (Google card fails) → `cafe-gfail` [cond] — only in·live·live, out·live·live
- Lantern Tea A D M 3 postups (Google card fails) → `cafe-gfail` [cond]
- area has no postups → `empty-area` [cond] — only in·none·building, in·none·live, out·none·building, out·none·live
- Live → `home` [mode]
- Building → `home` [mode]
- See map → `home` [mode] — only in·live·building, out·live·building

### Nearby (/nearby) · photos (A) (`quiet-feed`)
States: `quiet-feed@out.live`, `quiet-feed@out.none`, `quiet-feed@in.live`, `quiet-feed@in.none`
- Maya's photo → `cafe` [tap] — only in·live, out·live
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Tess's photo → `cafe` [tap] — only in·live, out·live
- Grindhouse → `cafe` [tap] — only in·live, out·live
- Jon's photo → `cafe` [tap] — only in·live, out·live
- Bean Theory M J A 3 this week → `cafe` [tap]
- Grindhouse T 1 this week → `cafe` [tap]
- Lantern Tea A D 2 this week → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up here → `post` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap] — only in·live, out·live
- Pixel Garden → `project` [tap] — only in·live, out·live
- Maya's photo → `project` [tap] — only in·live, out·live
- Star Fox 64 mod M Maya · Yesterday → `project` [tap] — only in·none, out·none
- Pixel Garden T Tess · Tue New crop → `project` [tap] — only in·none, out·none
- Bus Stop Zine J Jon · Mon Page 12  → `project` [tap] — only in·none, out·none
- Lantern Lights A Ari · Sun Wiring  → `project` [tap] — only in·none, out·none
- Projects → `projects` [tap]
- (tap) → `quiet` [tap]
- Venice Blvd Oakwood Park Marina Op → `quiet` [tap]
- Map → `quiet` [tap]
- Nearby → `quiet-feed` [tap]
- Maya's photo (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Tess's photo (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Grindhouse (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Jon's photo (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Bean Theory M J A 3 this week (Google card fails) → `cafe-gfail` [cond]
- Grindhouse T 1 this week (Google card fails) → `cafe-gfail` [cond]
- Lantern Tea A D 2 this week (Google card fails) → `cafe-gfail` [cond]

### Nearby (/nearby) · no photos (B) (`quiet-feed-b`)
States: `quiet-feed-b@out.live`, `quiet-feed-b@out.none`, `quiet-feed-b@in.live`, `quiet-feed-b@in.none`
- (tap) → `cafe` [tap] — only in·live, out·live
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Grindhouse → `cafe` [tap] — only in·live, out·live
- Bean Theory M J A 3 this week → `cafe` [tap]
- Grindhouse T 1 this week → `cafe` [tap]
- Lantern Tea A D 2 this week → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up here → `post` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap] — only in·live, out·live
- Pixel Garden → `project` [tap] — only in·live, out·live
- Star Fox 64 mod M Maya · Yesterday → `project` [tap] — only in·none, out·none
- Pixel Garden T Tess · Tue New crop → `project` [tap] — only in·none, out·none
- Bus Stop Zine J Jon · Mon Page 12  → `project` [tap] — only in·none, out·none
- Lantern Lights A Ari · Sun Wiring  → `project` [tap] — only in·none, out·none
- Projects → `projects` [tap]
- (tap) → `quiet` [tap]
- Venice Blvd Oakwood Park Marina Op → `quiet` [tap]
- Map → `quiet` [tap]
- Nearby → `quiet-feed` [tap]
-  (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Grindhouse (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Bean Theory M J A 3 this week (Google card fails) → `cafe-gfail` [cond]
- Grindhouse T 1 this week (Google card fails) → `cafe-gfail` [cond]
- Lantern Tea A D 2 this week (Google card fails) → `cafe-gfail` [cond]

### Recent map · old no-live home (not /) (`quiet`)
States: `quiet@out.live`, `quiet@out.none`, `quiet@in.live`, `quiet@in.none`
- 3 this week → `cafe` [tap]
- 1 this week → `cafe` [tap]
- (tap) → `cafe` [tap]
- Bean Theory M J A 3 postups · Tue → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod New level yesterda → `project` [tap]
- Projects → `projects` [tap]
- List → `quiet-feed` [tap]
- See all → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- 3 this week (Google card fails) → `cafe-gfail` [cond]
- 1 this week (Google card fails) → `cafe-gfail` [cond]
-  (Google card fails) → `cafe-gfail` [cond]
- Bean Theory M J A 3 postups · Tue (Google card fails) → `cafe-gfail` [cond]

### Empty area (`empty-area`)
States: `empty-area@out.live`, `empty-area@out.none`, `empty-area@in.live`, `empty-area@in.none`
- (tap) → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Stories Cafe 0.3 mi → `post` [tap]
- Lot 1 Coffee 0.6 mi → `post` [tap]
- Post up → `post` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
-  (Google card fails) → `cafe-gfail` [cond]

### Loading (`loading`)
States: `loading@out.live`, `loading@out.none`, `loading@in.live`, `loading@in.none`
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]

### Offline (`offline`)
States: `offline@out.live`, `offline@out.none`, `offline@in.live`, `offline@in.none`
- Maya's photo → `cafe` [tap]
- Bean Theory → `cafe` [tap]
- Tess's photo → `cafe` [tap]
- Grindhouse → `cafe` [tap]
- Jon's photo → `cafe` [tap]
- Bean Theory M J A 3 this week → `cafe` [tap]
- Grindhouse T 1 this week → `cafe` [tap]
- Lantern Tea A D 2 this week → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up here → `post` [tap]
- Star Fox 64 mod → `project` [tap]
- Pixel Garden → `project` [tap]
- Maya's photo → `project` [tap]
- Projects → `projects` [tap]
- (tap) → `quiet` [tap]
- Venice Blvd Oakwood Park Marina Op → `quiet` [tap]
- Map → `quiet` [tap]
- Retry → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Maya's photo (Google card fails) → `cafe-gfail` [cond]
- Bean Theory (Google card fails) → `cafe-gfail` [cond]
- Tess's photo (Google card fails) → `cafe-gfail` [cond]
- Grindhouse (Google card fails) → `cafe-gfail` [cond]
- Jon's photo (Google card fails) → `cafe-gfail` [cond]
- Bean Theory M J A 3 this week (Google card fails) → `cafe-gfail` [cond]
- Grindhouse T 1 this week (Google card fails) → `cafe-gfail` [cond]
- Lantern Tea A D 2 this week (Google card fails) → `cafe-gfail` [cond]

### Home overlay · alternative, not chosen (`home-overlay-alt`)
States: `home-overlay-alt@out.live`, `home-overlay-alt@out.none`, `home-overlay-alt@in.live`, `home-overlay-alt@in.none`
- 3 this week → `cafe` [tap]
- (tap) → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod Maya · Corneria II → `project` [tap]
- Pixel Garden Tess · New crop sprit → `project` [tap]
- Bus Stop Zine Jon · Page 12 inked → `project` [tap]
- See all projects → `projects` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- 3 this week (Google card fails) → `cafe-gfail` [cond]
-  (Google card fails) → `cafe-gfail` [cond]

## Cafes & picking a place

### Cafe (`cafe`)
States: `cafe@out.live`, `cafe@out.none`, `cafe@in.live`, `cafe@in.none`
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up here → `post` [tap]
- Post up → `post` [tap]
- Join → `postup` [tap] — only in·live, out·live
- M Maya Live Bean Theory · till 4pm → `postup` [tap] — only in·live, out·live
- J Jon Live Bean Theory · till 5pm  → `postup` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Share → `cafe+share` [sheet]
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- postups end (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- someone goes live (Google card fails) → `cafe-gfail` [cond] — only in·none, out·none
- sheet `share` over this page: close → `cafe`; Messages → `cafe`; WhatsApp → `cafe`; Email → `cafe`; More → `cafe`; Cancel → `cafe`; close (Google card fails) → `cafe-gfail`; Messages (Google card fails) → `cafe-gfail`; WhatsApp (Google card fails) → `cafe-gfail`; Email (Google card fails) → `cafe-gfail`; More (Google card fails) → `cafe-gfail`; Cancel (Google card fails) → `cafe-gfail`

### Cafe · Google card failed (`cafe-gfail`)
States: `cafe-gfail@out.live`, `cafe-gfail@out.none`, `cafe-gfail@in.live`, `cafe-gfail@in.none`
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Retry → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up here → `post` [tap]
- Post up → `post` [tap]
- Join → `postup` [tap] — only in·live, out·live
- M Maya Live Bean Theory · till 4pm → `postup` [tap] — only in·live, out·live
- J Jon Live Bean Theory · till 5pm  → `postup` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Retry (Google card fails) → `cafe-gfail` [cond]
- Open in Maps → `cafe-gfail+dirs` [sheet]
- Share → `cafe-gfail+share` [sheet]
- sheet `dirs` over this page: close → `cafe-gfail`; Open in Apple Maps → `cafe-gfail`; Open in Google Maps → `cafe-gfail`; Cancel → `cafe-gfail`
- sheet `share` over this page: close → `cafe-gfail`; Messages → `cafe-gfail`; WhatsApp → `cafe-gfail`; Email → `cafe-gfail`; More → `cafe-gfail`; Cancel → `cafe-gfail`

### Where are you? (`where`)
States: `where@out.live`, `where@out.none`, `where@in.live`, `where@in.none`
- Post up → `post-signin` [tap] — only out·live, out·none
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]

### Cafe search (`where-search`)
States: `where-search@out.live`, `where-search@out.none`, `where-search@in.live`, `where-search@in.none`
- Post up → `post-signin` [tap] — only out·live, out·none
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]

## Postups & joining

### Postup · anyone can join (`postup`)
States: `postup@out.live`, `postup@out.none`, `postup@in.live`, `postup@in.none`
- Bean Theory 0.4 mi · 8 min walk → `cafe` [tap]
- Join → `join-signin` [tap] — only out·live, out·none
- Join → `joined` [tap] — only in·live, in·none
- M Maya Live · till 4pm → `profile` [tap]
- Star Fox 64 mod Adding a new Corne → `project` [tap]
- Back → `Back` [back]
- Bean Theory 0.4 mi · 8 min walk (Google card fails) → `cafe-gfail` [cond]
- More → `postup+more` [sheet]
- Share → `postup+share` [sheet]
- sheet `block` over this page: Block → `home`; close → `postup`; Cancel → `postup`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup`; Cancel → `postup`; Block Maya → `postup+block`; Share → `postup+share`
- sheet `share` over this page: close → `postup`; Messages → `postup`; WhatsApp → `postup`; Email → `postup`; More → `postup`; Cancel → `postup`

### Postup · ask to join (`postup-ask`)
States: `postup-ask@out.live`, `postup-ask@out.none`, `postup-ask@in.live`, `postup-ask@in.none`
- Ask to join → `ask` [tap] — only in·live, in·none
- Ask to join → `ask-signin` [tap] — only out·live, out·none
- Grindhouse 1.1 mi · 22 min walk → `cafe` [tap]
- T Tess Live · till 3pm → `profile` [tap]
- Pixel Garden Drawing crop sprites. → `project` [tap]
- Back → `Back` [back]
- Grindhouse 1.1 mi · 22 min walk (Google card fails) → `cafe-gfail` [cond]
- More → `postup-ask+more` [sheet]
- Share → `postup-ask+share` [sheet]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-ask`; Cancel → `postup-ask`; Share → `postup-ask+share`
- sheet `share` over this page: close → `postup-ask`; Messages → `postup-ask`; WhatsApp → `postup-ask`; Email → `postup-ask`; More → `postup-ask`; Cancel → `postup-ask`

### Sign-in sheet · join (`join-signin`)
States: `join-signin@out.live`, `join-signin@out.none`, `join-signin@in.live`, `join-signin@in.none`
- Bean Theory 0.4 mi · 8 min walk → `cafe` [tap]
- Join → `join-signin` [tap] — only out·live, out·none
- Join → `joined` [tap] — only in·live, in·none
- M Maya Live · till 4pm → `profile` [tap]
- Star Fox 64 mod Adding a new Corne → `project` [tap]
- Back → `Back` [back]
- Bean Theory 0.4 mi · 8 min walk (Google card fails) → `cafe-gfail` [cond]
- More → `join-signin+more` [sheet]
- Share → `join-signin+share` [sheet]
- signs in → `joined (signs in)` [sign-in] — only out·live, out·none
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `join-signin`; Cancel → `join-signin`; Share → `join-signin+share`
- sheet `share` over this page: close → `join-signin`; Messages → `join-signin`; WhatsApp → `join-signin`; Email → `join-signin`; More → `join-signin`; Cancel → `join-signin`

### Sign-in sheet · ask (`ask-signin`)
States: `ask-signin@out.live`, `ask-signin@out.none`, `ask-signin@in.live`, `ask-signin@in.none`
- Ask to join → `ask` [tap] — only in·live, in·none
- Ask to join → `ask-signin` [tap] — only out·live, out·none
- Grindhouse 1.1 mi · 22 min walk → `cafe` [tap]
- T Tess Live · till 3pm → `profile` [tap]
- Pixel Garden Drawing crop sprites. → `project` [tap]
- Back → `Back` [back]
- signs in → `ask (signs in)` [sign-in] — only out·live, out·none
- More → `ask-signin+more` [sheet]
- Share → `ask-signin+share` [sheet]
- Grindhouse 1.1 mi · 22 min walk (Google card fails) → `cafe-gfail` [cond]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `ask-signin`; Cancel → `ask-signin`; Share → `ask-signin+share`
- sheet `share` over this page: close → `ask-signin`; Messages → `ask-signin`; WhatsApp → `ask-signin`; Email → `ask-signin`; More → `ask-signin`; Cancel → `ask-signin`

### Ask to join (`ask`)
States: `ask@out.live`, `ask@out.none`, `ask@in.live`, `ask@in.none`
- Ask to join → `ask` [tap] — only in·live, in·none
- Ask to join → `ask-signin` [tap] — only out·live, out·none
- Grindhouse 1.1 mi · 22 min walk → `cafe` [tap]
- T Tess Live · till 3pm → `profile` [tap]
- Pixel Garden Drawing crop sprites. → `project` [tap]
- Send request → `requested` [tap]
- Back → `Back` [back]
- More → `ask+more` [sheet]
- Share → `ask+share` [sheet]
- Grindhouse 1.1 mi · 22 min walk (Google card fails) → `cafe-gfail` [cond]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `ask`; Cancel → `ask`; Share → `ask+share`
- sheet `share` over this page: close → `ask`; Messages → `ask`; WhatsApp → `ask`; Email → `ask`; More → `ask`; Cancel → `ask`

### Request sent (`requested`)
States: `requested@out.live`, `requested@out.none`, `requested@in.live`, `requested@in.none`
- Close → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- View postup → `postup-ask` [tap]
- Cancel request → `postup-ask` [tap]
- Projects → `projects` [tap]
- See who else is nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]

### You're joining (`joined`)
States: `joined@out.live`, `joined@out.none`, `joined@in.live`, `joined@in.none`
- Bean Theory → `cafe` [tap]
- Cafe → `cafe` [tap]
- Group chat → `chat` [tap]
- Close → `home` [tap]
- Back to map → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- Project → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Bean Theory (Google card fails) → `cafe-gfail` [cond]
- Cafe (Google card fails) → `cafe-gfail` [cond]
- Directions → `joined+dirs` [sheet]
- Leave → `joined+leave` [sheet]
- sheet `dirs` over this page: close → `joined`; Open in Apple Maps → `joined`; Open in Google Maps → `joined`; Cancel → `joined`
- sheet `leave` over this page: Leave → `postup`; close → `joined`; Stay → `joined`

### Postup full (`postup-full`)
States: `postup-full@out.live`, `postup-full@out.none`, `postup-full@in.live`, `postup-full@in.none`
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- M Maya Bean Theory → `profile` [tap]
- Follow Maya for next time → `profile` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- More → `postup-full+more` [sheet]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-full`; Cancel → `postup-full`

### Postup cancelled (`postup-cancelled`)
States: `postup-cancelled@out.live`, `postup-cancelled@out.none`, `postup-cancelled@in.live`, `postup-cancelled@in.none`
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- M Maya Bean Theory → `profile` [tap]
- Follow Maya for next time → `profile` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- More → `postup-cancelled+more` [sheet]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-cancelled`; Cancel → `postup-cancelled`

### Postup ended (`postup-ended`)
States: `postup-ended@out.live`, `postup-ended@out.none`, `postup-ended@in.live`, `postup-ended@in.none`
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- M Maya Bean Theory → `profile` [tap]
- Follow Maya for next time → `profile` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- More → `postup-ended+more` [sheet]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-ended`; Cancel → `postup-ended`

## Posting & hosting

### Post up (`post`)
States: `post@out.live`, `post@out.none`, `post@in.live`, `post@in.none`
- Post up → `post-signin` [tap] — only out·live, out·none
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]

### Sign-in sheet · post (`post-signin`)
States: `post-signin@out.live`, `post-signin@out.none`, `post-signin@in.live`, `post-signin@in.none`
- Post up → `post-signin` [tap] — only out·live, out·none
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]
- signs in → `posted (signs in)` [sign-in] — only out·live, out·none

### You're posted up (`posted`)
States: `posted@out.live`, `posted@out.none`, `posted@in.live`, `posted@in.none`
- Cafe → `cafe` [tap]
- Close → `home` [tap]
- Map → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Manage postup → `live` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod → `project` [tap]
- Project → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Cafe (Google card fails) → `cafe-gfail` [cond]
- Invite friends → `posted+share` [sheet]
- sheet `share` over this page: close → `posted`; Messages → `posted`; WhatsApp → `posted`; Email → `posted`; More → `posted`; Cancel → `posted`

### You're live (`live`)
States: `live@out.live`, `live@out.none`, `live@in.live`, `live@in.none`
- Group chat → `chat` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- Edit → `post-edit` [tap]
- D Dev · 2 min ago → `profile` [tap]
- J Jon On the way · 10 min → `profile` [tap]
- Star Fox 64 mod → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- signs in → `live (signs in)` [sign-in] — only out·live, out·none
- End postup → `live+endlive` [sheet]
- Share → `live+share` [sheet]
- sheet `endlive` over this page: End now → `me`; close → `live`; Keep going → `live`
- sheet `share` over this page: close → `live`; Messages → `live`; WhatsApp → `live`; Email → `live`; More → `live`; Cancel → `live`

### Edit postup (`post-edit`)
States: `post-edit@out.live`, `post-edit@out.none`, `post-edit@in.live`, `post-edit@in.none`
- Save → `live` [tap]
- Project → `project-new` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]
- signs in → `post-edit (signs in)` [sign-in] — only out·live, out·none

## Projects

### Projects (`projects`)
States: `projects@out.live`, `projects@out.none`, `projects@in.live`, `projects@in.none`
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod M Maya · Yesterday → `project` [tap]
- Pixel Garden T Tess · Tue New crop → `project` [tap]
- Bus Stop Zine J Jon · Mon Page 12  → `project` [tap]
- Lantern Lights A Ari · Sun Wiring  → `project` [tap]
- New project → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]

### Project (`project`)
States: `project@out.live`, `project@out.none`, `project@in.live`, `project@in.none`
- Bean Theory → `cafe` [tap]
- (tap) → `cafe` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- M Maya Bean Theory · till 4pm Live → `postup` [tap] — only in·live, out·live
- Maya → `profile` [tap]
- Post up → `project-attach` [tap]
- Post up for this → `project-attach` [tap]
- New → `project-new` [tap]
- Update → `project-update` [tap]
- Post update → `project-update` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Bean Theory (Google card fails) → `cafe-gfail` [cond]
-  (Google card fails) → `cafe-gfail` [cond]

### New project (`project-new`)
States: `project-new@out.live`, `project-new@out.none`, `project-new@in.live`, `project-new@in.none`
- Create → `project` [tap] — only in·live, in·none
- Create → `project-new+signin` [tap] — only out·live, out·none
- Back → `Back` [back]
- sheet `signin` over this page: close → `project-new`; Not now → `project-new`; signs in → `project-new (signs in)`

### Project update (`project-update`)
States: `project-update@out.live`, `project-update@out.none`, `project-update@in.live`, `project-update@in.none`
- Post update → `project` [tap] — only in·live, in·none
- Post update → `project-update+signin` [tap] — only out·live, out·none
- Back → `Back` [back]
- sheet `signin` over this page: close → `project-update`; Not now → `project-update`; signs in → `project-update (signs in)`

### Post up for a project (`project-attach`)
States: `project-attach@out.live`, `project-attach@out.none`, `project-attach@in.live`, `project-attach@in.none`
- Post up → `attach-signin` [tap] — only out·live, out·none
- Post up → `posted` [tap] — only in·live, in·none
- Back → `Back` [back]

### Sign-in sheet · attach (`attach-signin`)
States: `attach-signin@out.live`, `attach-signin@out.none`, `attach-signin@in.live`, `attach-signin@in.none`
- Post up → `attach-signin` [tap] — only out·live, out·none
- Post up → `posted` [tap] — only in·live, in·none
- Back → `Back` [back]
- signs in → `posted (signs in)` [sign-in] — only out·live, out·none

## Share-link landings

### Share link · live postup (`invite`)
States: `invite@out.live`, `invite@out.none`, `invite@in.live`, `invite@in.none`
- Bean Theory · 0.4 mi → `cafe` [tap]
- Join Maya → `join-signin` [tap] — only out·live, out·none
- Join Maya → `joined` [tap] — only in·live, in·none
- Star Fox 64 mod → `project` [tap]
- Bean Theory · 0.4 mi (Google card fails) → `cafe-gfail` [cond]

### Share link · ended (`invite-ended`)
States: `invite-ended@out.live`, `invite-ended@out.none`, `invite-ended@in.live`, `invite-ended@in.none`
- See what's nearby → `quiet-feed` [tap]

### Share link · project (`invite-project`)
States: `invite-project@out.live`, `invite-project@out.none`, `invite-project@in.live`, `invite-project@in.none`
- Next postup: weekdays at Bean Theo → `profile` [tap]
- See updates → `project` [tap]
- Follow → `invite-project+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: close → `invite-project`; Not now → `invite-project`; signs in → `invite-project (signs in)`

## Inbox & people

### Inbox · Chats (`inbox`)
States: `inbox@out.live`, `inbox@out.none`, `inbox@in.live`, `inbox@in.none`
- Activity 2 → `activity` [tap]
- M Maya's postup Maya: Grabbing ano → `chat` [tap]
- S Your postup Jon: On the way 1:58 → `chat` [tap]
- Home → `home` [tap]
- Chats → `inbox` [tap]
- Inbox → `inbox` [tap]
- Post up → `post` [tap]
- T Tess's postup Ended · Tue Tue → `postup-ended` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back] — only out·live, out·none
- signs in → `inbox (signs in)` [sign-in] — only out·live, out·none

### Inbox · Activity (`activity`)
States: `activity@out.live`, `activity@out.none`, `activity@in.live`, `activity@in.none`
- Activity 2 → `activity` [tap]
- M Maya: Hey! Here till 4 — come sa → `chat` [tap]
- Home → `home` [tap]
- Chats → `inbox` [tap]
- Inbox → `inbox` [tap]
- D Dev asked to join your postup 2  → `live` [tap]
- J Jon joined your postup 14 min ag → `live` [tap]
- Post up → `post` [tap]
- T Tess said yes to your request Ye → `postup-ask` [tap]
- A Ari followed you Mon → `profile` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back] — only out·live, out·none
- signs in → `activity (signs in)` [sign-in] — only out·live, out·none

### Group chat (`chat`)
States: `chat@out.live`, `chat@out.none`, `chat@in.live`, `chat@in.none`
- M J S Bean Theory · till 4pm · 3 p → `postup` [tap]
- Back → `Back` [back]
- signs in → `chat (signs in)` [sign-in] — only out·live, out·none
- More → `chat+more` [sheet]
- Message options → `chat+msg` [sheet]
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `chat`; Cancel → `chat`
- sheet `msg` over this page: Report message → `report`; close → `chat`; Copy → `chat`; Cancel → `chat`

### Profile (`profile`)
States: `profile@out.live`, `profile@out.none`, `profile@in.live`, `profile@in.none`
- Bean Theory → `cafe` [tap]
- Grindhouse → `cafe` [tap]
- Ship models imported Bean Theory · → `cafe` [tap]
- Level editor Lantern Tea · Oct 9 → `cafe` [tap]
- Live at Bean Theory Till 4pm · Sta → `postup` [tap] — only in·live, out·live
- Star Fox 64 mod Updated yesterday → `project` [tap]
- Back → `Back` [back]
- Bean Theory (Google card fails) → `cafe-gfail` [cond]
- Grindhouse (Google card fails) → `cafe-gfail` [cond]
- Ship models imported Bean Theory · (Google card fails) → `cafe-gfail` [cond]
- Level editor Lantern Tea · Oct 9 (Google card fails) → `cafe-gfail` [cond]
- More → `profile+more` [sheet]
- Follow → `profile+signin` [sheet] — only out·live, out·none
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `profile`; Cancel → `profile`
- sheet `signin` over this page: close → `profile`; Not now → `profile`; signs in → `profile (signs in)`

### My profile (`me`)
States: `me@out.live`, `me@out.none`, `me@in.live`, `me@in.none`
- Lantern Tea → `cafe` [tap]
- Grindhouse → `cafe` [tap]
- Ship models imported Bean Theory · → `cafe` [tap]
- Level editor Lantern Tea · Oct 9 → `cafe` [tap]
- 1:42 You're live at Bean Theory Ti → `live` [tap]
- Edit profile → `me` [tap]
- Tide Clock Updated Sun → `project-new` [tap]
- Settings → `settings` [tap]
- Back → `Back` [back]
- Lantern Tea (Google card fails) → `cafe-gfail` [cond]
- Grindhouse (Google card fails) → `cafe-gfail` [cond]
- Ship models imported Bean Theory · (Google card fails) → `cafe-gfail` [cond]
- Level editor Lantern Tea · Oct 9 (Google card fails) → `cafe-gfail` [cond]
- signs in → `me (signs in)` [sign-in] — only out·live, out·none

## Account & safety

### Settings (`settings`)
States: `settings@out.live`, `settings@out.none`, `settings@in.live`, `settings@in.none`
- Sign out → `invite` [tap] — only out·live, out·none
- Sign out → `invite (signed out)` [tap] — only in·live, in·none
- Back → `Back` [back]
- signs in → `settings (signs in)` [sign-in] — only out·live, out·none
- Delete account → `settings+delacct` [sheet]
- sheet `delacct` over this page: Delete account → `invite-ended`; Delete account → `invite-ended (signed out)`; close → `settings`; Cancel → `settings`

### Report (`report`)
States: `report@out.live`, `report@out.none`, `report@in.live`, `report@in.none`
- Send report → `reported` [tap]
- Back → `Back` [back]

### Reported (`reported`)
States: `reported@out.live`, `reported@out.none`, `reported@in.live`, `reported@in.none`
- Close → `home` [tap]
- Done → `home` [tap]
- Block Maya too → `reported+block` [sheet]
- sheet `block` over this page: Block → `home`; close → `reported`; Cancel → `reported`

## Missing edges found by the flows (design gaps)
- `cautious-joiner` step 6: `cafe@in.live` → `postup-ask@in.live` ("comes back later to another postup (ask-to-join)") [M1025]
- `invite-ended` step 2: `invite-ended@out.none` → `profile+signin@out.none` ("taps Follow 🔒") [M1025]
- `invite-ended` step 3: `profile+signin@out.none` → `home@in.none.building` ("signs in, continues to Home") [M1025]
- `first-post` step 4: `where@out.none` → `where-search@out.none` ("searches") [M1025]
- `safety` step 5: `reported+block@in.live` → `settings@in.live` ("opens Settings") [M1025]
- `delete-account` step 4: `settings+delacct@in.none` → `home@out.none.building` ("confirms") [M1025]
- `settings-notify` step 2: `settings@in.none` → `home@out.none.building` ("taps Sign out") [M1025]
