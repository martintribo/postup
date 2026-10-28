# PostUp site graph
Site graph (Martin, Oct 25 2026 [M1025]): 40 pages + 9 sheets, 336 site states (page [+ child in a slot] × auth out|in × live (nearby) live|none, Home × tab), 3666 edges from the model (model/: screen links, tab bar and rail chrome slots, events, conditions). A flow is a path of steps, each a link (screen:id) or event that reaches the expected site state. Site-state id: page[+child]@auth.live[.tab]. See model/CONCEPTS.md. [M1031-draft]

Site events: postups end; someone goes live; alert arrives; comes back later; postup fills (on postup, postup-ask, joined, requested, invite, postup-full); postup is cancelled (on postup, postup-ask, joined, requested, invite, postup-full); postup ends (on postup, postup-ask, joined, requested, invite, postup-full); someone you follow posts up; network drops (on quiet-feed, loading, home). live = someone live nearby; a postup ending changes only its own page.

Dimensions: auth = out | in; live = live (someone live nearby) | none; mode = live | building (Home only); data conditions are pages: postup-ask (host approves), postup-full, postup-cancelled, postup-ended, live (you are hosting), joined, requested (pending ask), empty-area, offline, cafe-gfail.

## Home & discover

### Home page (/) (`home`)
States: `home@out.live.live`, `home@out.live.building`, `home@out.none.live`, `home@out.none.building`, `home@in.live.live`, `home@in.live.building`, `home@in.none.live`, `home@in.none.building`
- cafe → `cafe` [tap] — only in·live·live, in·none·live, out·live·live, out·none·live
- Bean Theory → `cafe` [tap] — only in·live·live, out·live·live
- Grindhouse → `cafe` [tap] — only in·live·live, out·live·live
- Lantern Tea A D M 3 postups → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- M 2 → `postup` [tap] — only in·live·live, out·live·live
- M Maya Live Bean Theory · till 4pm → `postup` [tap] — only in·live·live, out·live·live
- J Jon Live Bean Theory · till 5pm → `postup` [tap] — only in·live·live, out·live·live
- T → `postup-ask` [tap] — only in·live·live, out·live·live
- T Tess Live · Ask to join Grindhou → `postup-ask` [tap] — only in·live·live, out·live·live
- Star Fox 64 mod → `project` [tap] — only in·live·live, out·live·live
- Pixel Garden → `project` [tap] — only in·live·live, out·live·live
- Star Fox 64 mod M Maya · Yesterday → `project` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Pixel Garden T Tess · Tue New crop → `project` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Bus Stop Zine J Jon · Mon Page 12 → `project` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Projects → `projects` [tap]
- See all projects → `projects` [tap] — only in·live·building, in·none·building, out·live·building, out·none·building
- Locate → `quiet` [tap] — only in·live·live, in·none·live, out·live·live, out·none·live
- Nearby → `quiet-feed` [tap]
- cafe (Google card fails) → `cafe-gfail` [cond] — only in·live·live, in·none·live, out·live·live, out·none·live
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live·live, out·live·live
- Grindhouse (Google card fails) → `cafe-gfail` [cond] — only in·live·live, out·live·live
- Lantern Tea A D M 3 postups (Google card fails) → `cafe-gfail` [cond]
- area has no postups → `empty-area` [cond] — only in·none·building, in·none·live, out·none·building, out·none·live
- Live → `home` [mode]
- Building → `home` [mode]
- See map → `home` [mode] — only in·live·building, out·live·building

### Recent map · old no-live home (not /) (`quiet`)
States: `quiet@out.live`, `quiet@out.none`, `quiet@in.live`, `quiet@in.none`
- 3 this week → `cafe` [tap]
- 1 this week → `cafe` [tap]
- cafe → `cafe` [tap]
- Bean Theory M J A 3 postups · Tue → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod New level yesterda → `project` [tap]
- Projects → `projects` [tap]
- List → `quiet-feed` [tap]
- See all → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- 3 this week (Google card fails) → `cafe-gfail` [cond]
- 1 this week (Google card fails) → `cafe-gfail` [cond]
- cafe (Google card fails) → `cafe-gfail` [cond]
- Bean Theory M J A 3 postups · Tue (Google card fails) → `cafe-gfail` [cond]

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
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up here → `post` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap] — only in·live, out·live
- Pixel Garden → `project` [tap] — only in·live, out·live
- Maya's photo → `project` [tap] — only in·live, out·live
- Star Fox 64 mod M Maya · Yesterday → `project` [tap] — only in·none, out·none
- Pixel Garden T Tess · Tue New crop → `project` [tap] — only in·none, out·none
- Bus Stop Zine J Jon · Mon Page 12 → `project` [tap] — only in·none, out·none
- Lantern Lights A Ari · Sun Wiring → `project` [tap] — only in·none, out·none
- Projects → `projects` [tap]
- quiet → `quiet` [tap]
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
- cafe → `cafe` [tap] — only in·live, out·live
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Grindhouse → `cafe` [tap] — only in·live, out·live
- Bean Theory M J A 3 this week → `cafe` [tap]
- Grindhouse T 1 this week → `cafe` [tap]
- Lantern Tea A D 2 this week → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up here → `post` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap] — only in·live, out·live
- Pixel Garden → `project` [tap] — only in·live, out·live
- Star Fox 64 mod M Maya · Yesterday → `project` [tap] — only in·none, out·none
- Pixel Garden T Tess · Tue New crop → `project` [tap] — only in·none, out·none
- Bus Stop Zine J Jon · Mon Page 12 → `project` [tap] — only in·none, out·none
- Lantern Lights A Ari · Sun Wiring → `project` [tap] — only in·none, out·none
- Projects → `projects` [tap]
- quiet → `quiet` [tap]
- Venice Blvd Oakwood Park Marina Op → `quiet` [tap]
- Map → `quiet` [tap]
- Nearby → `quiet-feed` [tap]
- cafe (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Grindhouse (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- Bean Theory M J A 3 this week (Google card fails) → `cafe-gfail` [cond]
- Grindhouse T 1 this week (Google card fails) → `cafe-gfail` [cond]
- Lantern Tea A D 2 this week (Google card fails) → `cafe-gfail` [cond]

### Empty area (`empty-area`)
States: `empty-area@out.live`, `empty-area@out.none`, `empty-area@in.live`, `empty-area@in.none`
- cafe → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Stories Cafe 0.3 mi → `post` [tap]
- Lot 1 Coffee 0.6 mi → `post` [tap]
- Post up → `post` [tap]
- Maya posted up at Bean Theory → `profile` [tap]
- Jon posted up at Lot 1 Coffee → `profile` [tap]
- Star Fox 64 mod → `project` [tap]
- Bus Stop Zine → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- cafe (Google card fails) → `cafe-gfail` [cond]

### Loading (`loading`)
States: `loading@out.live`, `loading@out.none`, `loading@in.live`, `loading@in.none`
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
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
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up here → `post` [tap]
- Star Fox 64 mod → `project` [tap]
- Pixel Garden → `project` [tap]
- Maya's photo → `project` [tap]
- Projects → `projects` [tap]
- quiet → `quiet` [tap]
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
- cafe → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod Maya · Corneria II → `project` [tap]
- Pixel Garden Tess · New crop sprit → `project` [tap]
- Bus Stop Zine Jon · Page 12 inked → `project` [tap]
- See all projects → `projects` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- 3 this week (Google card fails) → `cafe-gfail` [cond]
- cafe (Google card fails) → `cafe-gfail` [cond]

## Cafes & picking a place

### Cafe (`cafe`)
States: `cafe@out.live`, `cafe@out.none`, `cafe@in.live`, `cafe@in.none`
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up here → `post` [tap]
- Post up → `post` [tap]
- Join → `postup` [tap] — only in·live, out·live
- M Maya Live Bean Theory · till 4pm → `postup` [tap] — only in·live, out·live
- J Jon Live Bean Theory · till 5pm → `postup` [tap] — only in·live, out·live
- Star Fox 64 mod → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Share → `cafe+share` [sheet]
- Bean Theory (Google card fails) → `cafe-gfail` [cond] — only in·live, out·live
- sheet `share` over this page: close → `cafe`; Messages → `cafe`; WhatsApp → `cafe`; Email → `cafe`; More → `cafe`; Cancel → `cafe`; close (Google card fails) → `cafe-gfail`; Messages (Google card fails) → `cafe-gfail`; WhatsApp (Google card fails) → `cafe-gfail`; Email (Google card fails) → `cafe-gfail`; More (Google card fails) → `cafe-gfail`; Cancel (Google card fails) → `cafe-gfail`

### Where are you? (`where`)
States: `where@out.live`, `where@out.none`, `where@in.live`, `where@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Search cafes → `where-search` [tap]
- Back → `Back` [back]
- Post up → `where+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: signs in → continues → `posted (signs in)`; close → `where`; Not now → `where`; Continue with Apple → `where (signs in)`; Continue with Google → `where (signs in)`

### Cafe search (`where-search`)
States: `where-search@out.live`, `where-search@out.none`, `where-search@in.live`, `where-search@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Search cafes → `where-search` [tap]
- Back → `Back` [back]
- Post up → `where-search+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: signs in → continues → `posted (signs in)`; close → `where-search`; Not now → `where-search`; Continue with Apple → `where-search (signs in)`; Continue with Google → `where-search (signs in)`

### Cafe · Google card failed (`cafe-gfail`)
States: `cafe-gfail@out.live`, `cafe-gfail@out.none`, `cafe-gfail@in.live`, `cafe-gfail@in.none`
- Bean Theory → `cafe` [tap] — only in·live, out·live
- Retry → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up here → `post` [tap]
- Post up → `post` [tap]
- Join → `postup` [tap] — only in·live, out·live
- M Maya Live Bean Theory · till 4pm → `postup` [tap] — only in·live, out·live
- J Jon Live Bean Theory · till 5pm → `postup` [tap] — only in·live, out·live
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

## Posting & hosting

### Post up (`post`)
States: `post@out.live`, `post@out.none`, `post@in.live`, `post@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up → `posted` [tap] — only in·live, in·none
- Project → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]
- Post up → `post+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: close → `post`; Not now → `post`; Continue with Apple → `post (signs in)`; Continue with Google → `post (signs in)`; signs in → continues → `posted (signs in)`

### You're posted up (`posted`)
States: `posted@out.live`, `posted@out.none`, `posted@in.live`, `posted@in.none`
- Cafe → `cafe` [tap]
- Close → `home` [tap]
- Map → `home` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- Manage postup → `live` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod → `project` [tap]
- Project → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Cafe (Google card fails) → `cafe-gfail` [cond]
- Invite friends → `posted+share` [sheet]
- sheet `share` over this page: close → `posted`; Messages → `posted`; WhatsApp → `posted`; Email → `posted`; More → `posted`; Cancel → `posted`

### Edit postup (`post-edit`)
States: `post-edit@out.live`, `post-edit@out.none`, `post-edit@in.live`, `post-edit@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Save → `live` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Project → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Bean Theory Nearest · 0.4 mi Chang → `where` [tap]
- Back → `Back` [back]
- Continue with Apple → `post-edit (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `post-edit (signs in)` [sign-in] — only out·live, out·none

### You're live (`live`)
States: `live@out.live`, `live@out.none`, `live@in.live`, `live@in.none`
- Group chat → `chat` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Edit → `post-edit` [tap]
- D Dev · 2 min ago → `profile` [tap]
- J Jon On the way · 10 min → `profile` [tap]
- Star Fox 64 mod → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Continue with Apple → `live (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `live (signs in)` [sign-in] — only out·live, out·none
- End postup → `live+endlive` [sheet]
- Share → `live+share` [sheet]
- sheet `endlive` over this page: End now → `me`; close → `live`; Keep going → `live`
- sheet `share` over this page: close → `live`; Messages → `live`; WhatsApp → `live`; Email → `live`; More → `live`; Cancel → `live`

## Postups & joining

### Postup · anyone can join (`postup`)
States: `postup@out.live`, `postup@out.none`, `postup@in.live`, `postup@in.none`
- Bean Theory 0.4 mi · 8 min walk → `cafe` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Join → `joined` [tap] — only in·live, in·none
- S → `me` [tap]
- Post up → `post` [tap]
- M Maya Live · till 4pm → `profile` [tap]
- Star Fox 64 mod Adding a new Corne → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Bean Theory 0.4 mi · 8 min walk (Google card fails) → `cafe-gfail` [cond]
- More → `postup+more` [sheet]
- Share → `postup+share` [sheet]
- Join → `postup+signin` [sheet] — only out·live, out·none
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `postup`; Cancel → `postup`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup`; Cancel → `postup`; Block → `postup+block`; Share → `postup+share`
- sheet `share` over this page: close → `postup`; Messages → `postup`; WhatsApp → `postup`; Email → `postup`; More → `postup`; Cancel → `postup`
- sheet `signin` over this page: signs in → continues → `joined (signs in)`; close → `postup`; Not now → `postup`; Continue with Apple → `postup (signs in)`; Continue with Google → `postup (signs in)`

### You're joining (`joined`)
States: `joined@out.live`, `joined@out.none`, `joined@in.live`, `joined@in.none`
- Bean Theory → `cafe` [tap]
- Cafe → `cafe` [tap]
- Group chat → `chat` [tap]
- Close → `home` [tap]
- Back to map → `home` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
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

### Postup · ask to join (`postup-ask`)
States: `postup-ask@out.live`, `postup-ask@out.none`, `postup-ask@in.live`, `postup-ask@in.none`
- Ask to join → `ask` [tap] — only in·live, in·none
- Grindhouse 1.1 mi · 22 min walk → `cafe` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- T Tess Live · till 3pm → `profile` [tap]
- Pixel Garden Drawing crop sprites. → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Grindhouse 1.1 mi · 22 min walk (Google card fails) → `cafe-gfail` [cond]
- More → `postup-ask+more` [sheet]
- Share → `postup-ask+share` [sheet]
- Ask to join → `postup-ask+signin` [sheet] — only out·live, out·none
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `postup-ask`; Cancel → `postup-ask`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-ask`; Cancel → `postup-ask`; Block → `postup-ask+block`; Share → `postup-ask+share`
- sheet `share` over this page: close → `postup-ask`; Messages → `postup-ask`; WhatsApp → `postup-ask`; Email → `postup-ask`; More → `postup-ask`; Cancel → `postup-ask`
- sheet `signin` over this page: signs in → continues → `ask (signs in)`; close → `postup-ask`; Not now → `postup-ask`; Continue with Apple → `postup-ask (signs in)`; Continue with Google → `postup-ask (signs in)`

### Ask to join (`ask`)
States: `ask@out.live`, `ask@out.none`, `ask@in.live`, `ask@in.none`
- Ask to join → `ask` [tap] — only in·live, in·none
- Grindhouse 1.1 mi · 22 min walk → `cafe` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- T Tess Live · till 3pm → `profile` [tap]
- Pixel Garden Drawing crop sprites. → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Send request → `requested` [tap]
- Back → `Back` [back]
- More → `ask+more` [sheet]
- Share → `ask+share` [sheet]
- Ask to join → `ask+signin` [sheet] — only out·live, out·none
- Grindhouse 1.1 mi · 22 min walk (Google card fails) → `cafe-gfail` [cond]
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `ask`; Cancel → `ask`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `ask`; Cancel → `ask`; Block → `ask+block`; Share → `ask+share`
- sheet `share` over this page: close → `ask`; Messages → `ask`; WhatsApp → `ask`; Email → `ask`; More → `ask`; Cancel → `ask`
- sheet `signin` over this page: close → `ask`; Not now → `ask`; Continue with Apple → `ask (signs in)`; signs in → continues → `ask (signs in)`; Continue with Google → `ask (signs in)`

### Request sent (`requested`)
States: `requested@out.live`, `requested@out.none`, `requested@in.live`, `requested@in.none`
- Close → `home` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- View postup → `postup-ask` [tap]
- Cancel request → `postup-ask` [tap]
- Projects → `projects` [tap]
- See who else is nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]

### Postup ended (`postup-ended`)
States: `postup-ended@out.live`, `postup-ended@out.none`, `postup-ended@in.live`, `postup-ended@in.none`
- Go to Home → `home` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Follow Maya for next time → `postup-ended` [tap] — only in·live, in·none
- M Maya Bean Theory → `profile` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- More → `postup-ended+more` [sheet]
- Follow Maya for next time → `postup-ended+signin` [sheet] — only out·live, out·none
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `postup-ended`; Cancel → `postup-ended`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-ended`; Cancel → `postup-ended`; Block → `postup-ended+block`; Share → `postup-ended+share`
- sheet `share` over this page: close → `postup-ended`; Messages → `postup-ended`; WhatsApp → `postup-ended`; Email → `postup-ended`; More → `postup-ended`; Cancel → `postup-ended`
- sheet `signin` over this page: close → `postup-ended`; Not now → `postup-ended`; Continue with Apple → `postup-ended (signs in)`; Continue with Google → `postup-ended (signs in)`

### Postup full (`postup-full`)
States: `postup-full@out.live`, `postup-full@out.none`, `postup-full@in.live`, `postup-full@in.none`
- Go to Home → `home` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Follow Maya for next time → `postup-full` [tap] — only in·live, in·none
- M Maya Bean Theory → `profile` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- More → `postup-full+more` [sheet]
- Follow Maya for next time → `postup-full+signin` [sheet] — only out·live, out·none
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `postup-full`; Cancel → `postup-full`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-full`; Cancel → `postup-full`; Block → `postup-full+block`; Share → `postup-full+share`
- sheet `share` over this page: close → `postup-full`; Messages → `postup-full`; WhatsApp → `postup-full`; Email → `postup-full`; More → `postup-full`; Cancel → `postup-full`
- sheet `signin` over this page: close → `postup-full`; Not now → `postup-full`; Continue with Apple → `postup-full (signs in)`; Continue with Google → `postup-full (signs in)`

### Postup cancelled (`postup-cancelled`)
States: `postup-cancelled@out.live`, `postup-cancelled@out.none`, `postup-cancelled@in.live`, `postup-cancelled@in.none`
- Go to Home → `home` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Follow Maya for next time → `postup-cancelled` [tap] — only in·live, in·none
- M Maya Bean Theory → `profile` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- More → `postup-cancelled+more` [sheet]
- Follow Maya for next time → `postup-cancelled+signin` [sheet] — only out·live, out·none
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `postup-cancelled`; Cancel → `postup-cancelled`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `postup-cancelled`; Cancel → `postup-cancelled`; Block → `postup-cancelled+block`; Share → `postup-cancelled+share`
- sheet `share` over this page: close → `postup-cancelled`; Messages → `postup-cancelled`; WhatsApp → `postup-cancelled`; Email → `postup-cancelled`; More → `postup-cancelled`; Cancel → `postup-cancelled`
- sheet `signin` over this page: close → `postup-cancelled`; Not now → `postup-cancelled`; Continue with Apple → `postup-cancelled (signs in)`; Continue with Google → `postup-cancelled (signs in)`

## Projects

### Project (`project`)
States: `project@out.live`, `project@out.none`, `project@in.live`, `project@in.none`
- Bean Theory → `cafe` [tap]
- cafe → `cafe` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
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
- cafe (Google card fails) → `cafe-gfail` [cond]

### Projects (`projects`)
States: `projects@out.live`, `projects@out.none`, `projects@in.live`, `projects@in.none`
- Home → `home` [tap]
- home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod M Maya · Yesterday → `project` [tap]
- Pixel Garden T Tess · Tue New crop → `project` [tap]
- Bus Stop Zine J Jon · Mon Page 12 → `project` [tap]
- Lantern Lights A Ari · Sun Wiring → `project` [tap]
- New project → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]

### New project (`project-new`)
States: `project-new@out.live`, `project-new@out.none`, `project-new@in.live`, `project-new@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Create → `project` [tap] — only in·live, in·none
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Create → `project-new+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: signs in → continues → `project (signs in)`; close → `project-new`; Not now → `project-new`; Continue with Apple → `project-new (signs in)`; Continue with Google → `project-new (signs in)`

### Project update (`project-update`)
States: `project-update@out.live`, `project-update@out.none`, `project-update@in.live`, `project-update@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post update → `project` [tap] — only in·live, in·none
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Post update → `project-update+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: signs in → continues → `project (signs in)`; close → `project-update`; Not now → `project-update`; Continue with Apple → `project-update (signs in)`; Continue with Google → `project-update (signs in)`

### Post up for a project (`project-attach`)
States: `project-attach@out.live`, `project-attach@out.none`, `project-attach@in.live`, `project-attach@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Post up → `posted` [tap] — only in·live, in·none
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Post up → `project-attach+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: signs in → continues → `posted (signs in)`; close → `project-attach`; Not now → `project-attach`; Continue with Apple → `project-attach (signs in)`; Continue with Google → `project-attach (signs in)`

## Share-link landings

### Share link · live postup (`invite`)
States: `invite@out.live`, `invite@out.none`, `invite@in.live`, `invite@in.none`
- Bean Theory · 0.4 mi → `cafe` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Join Maya → `joined` [tap] — only in·live, in·none
- S → `me` [tap]
- Post up → `post` [tap]
- Star Fox 64 mod → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Bean Theory · 0.4 mi (Google card fails) → `cafe-gfail` [cond]
- Join Maya → `invite+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: close → `invite`; Not now → `invite`; Continue with Apple → `invite (signs in)`; Continue with Google → `invite (signs in)`; signs in → continues → `joined (signs in)`

### Share link · ended (`invite-ended`)
States: `invite-ended@out.live`, `invite-ended@out.none`, `invite-ended@in.live`, `invite-ended@in.none`
- Go to Home → `home` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Follow Maya for next time → `invite-ended` [tap] — only in·live, in·none
- S → `me` [tap]
- Post up → `post` [tap]
- Projects → `projects` [tap]
- See what's nearby → `quiet-feed` [tap]
- Nearby → `quiet-feed` [tap]
- Follow Maya for next time → `invite-ended+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: close → `invite-ended`; Not now → `invite-ended`; Continue with Apple → `invite-ended (signs in)`; Continue with Google → `invite-ended (signs in)`

### Share link · project (`invite-project`)
States: `invite-project@out.live`, `invite-project@out.none`, `invite-project@in.live`, `invite-project@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- Follow → `invite-project` [tap] — only in·live, in·none
- S → `me` [tap]
- Post up → `post` [tap]
- Next postup: weekdays at Bean Theo → `profile` [tap]
- See updates → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Follow → `invite-project+signin` [sheet] — only out·live, out·none
- sheet `signin` over this page: close → `invite-project`; Not now → `invite-project`; Continue with Apple → `invite-project (signs in)`; Continue with Google → `invite-project (signs in)`

## Inbox & people

### Group chat (`chat`)
States: `chat@out.live`, `chat@out.none`, `chat@in.live`, `chat@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- M J S Bean Theory · till 4pm · 3 p → `postup` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Continue with Apple → `chat (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `chat (signs in)` [sign-in] — only out·live, out·none
- More → `chat+more` [sheet]
- Message options → `chat+msg` [sheet]
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `chat`; Cancel → `chat`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `chat`; Cancel → `chat`; Block → `chat+block`; Share → `chat+share`
- sheet `msg` over this page: Report message → `report`; close → `chat`; Copy → `chat`; Cancel → `chat`; Block sender → `chat+block`
- sheet `share` over this page: close → `chat`; Messages → `chat`; WhatsApp → `chat`; Email → `chat`; More → `chat`; Cancel → `chat`

### Inbox · Chats (`inbox`)
States: `inbox@out.live`, `inbox@out.none`, `inbox@in.live`, `inbox@in.none`
- Activity 2 → `activity` [tap]
- M Maya's postup Maya: Grabbing ano → `chat` [tap]
- S Your postup Jon: On the way 1:58 → `chat` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Chats → `inbox` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- T Tess's postup Ended · Tue Tue → `postup-ended` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back] — only out·live, out·none
- Continue with Apple → `inbox (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `inbox (signs in)` [sign-in] — only out·live, out·none

### Inbox · Activity (`activity`)
States: `activity@out.live`, `activity@out.none`, `activity@in.live`, `activity@in.none`
- Activity 2 → `activity` [tap]
- M Maya: Hey! Here till 4 — come sa → `chat` [tap]
- Home → `home` [tap]
- home → `home` [tap]
- Chats → `inbox` [tap]
- Inbox → `inbox` [tap]
- D Dev asked to join your postup 2 → `live` [tap]
- J Jon joined your postup 14 min ag → `live` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Maya posted up at Bean Theory → `postup` [tap]
- T Tess said yes to your request Ye → `postup-ask` [tap]
- A Ari followed you Mon → `profile` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back] — only out·live, out·none
- Continue with Apple → `activity (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `activity (signs in)` [sign-in] — only out·live, out·none

### Profile (`profile`)
States: `profile@out.live`, `profile@out.none`, `profile@in.live`, `profile@in.none`
- Bean Theory → `cafe` [tap]
- Grindhouse → `cafe` [tap]
- Ship models imported Bean Theory · → `cafe` [tap]
- Level editor Lantern Tea · Oct 9 → `cafe` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Live at Bean Theory Till 4pm · Sta → `postup` [tap] — only in·live, out·live
- Follow → `profile` [tap] — only in·live, in·none
- Star Fox 64 mod Updated yesterday → `project` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Bean Theory (Google card fails) → `cafe-gfail` [cond]
- Grindhouse (Google card fails) → `cafe-gfail` [cond]
- Ship models imported Bean Theory · (Google card fails) → `cafe-gfail` [cond]
- Level editor Lantern Tea · Oct 9 (Google card fails) → `cafe-gfail` [cond]
- More → `profile+more` [sheet]
- Follow → `profile+signin` [sheet] — only out·live, out·none
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `profile`; Cancel → `profile`
- sheet `more` over this page: View profile → `profile`; Report → `report`; close → `profile`; Cancel → `profile`; Block → `profile+block`; Share → `profile+share`
- sheet `share` over this page: close → `profile`; Messages → `profile`; WhatsApp → `profile`; Email → `profile`; More → `profile`; Cancel → `profile`
- sheet `signin` over this page: close → `profile`; Not now → `profile`; Continue with Apple → `profile (signs in)`; Continue with Google → `profile (signs in)`

### My profile (`me`)
States: `me@out.live`, `me@out.none`, `me@in.live`, `me@in.none`
- Lantern Tea → `cafe` [tap]
- Grindhouse → `cafe` [tap]
- Ship models imported Bean Theory · → `cafe` [tap]
- Level editor Lantern Tea · Oct 9 → `cafe` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- 1:42 You're live at Bean Theory Ti → `live` [tap]
- Edit profile → `me` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Tide Clock Updated Sun → `project-new` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Settings → `settings` [tap]
- Back → `Back` [back]
- Lantern Tea (Google card fails) → `cafe-gfail` [cond]
- Grindhouse (Google card fails) → `cafe-gfail` [cond]
- Ship models imported Bean Theory · (Google card fails) → `cafe-gfail` [cond]
- Level editor Lantern Tea · Oct 9 (Google card fails) → `cafe-gfail` [cond]
- Continue with Apple → `me (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `me (signs in)` [sign-in] — only out·live, out·none

## Account & safety

### Settings (`settings`)
States: `settings@out.live`, `settings@out.none`, `settings@in.live`, `settings@in.none`
- Sign out → `home` [tap] — only out·live, out·none
- home → `home` [tap]
- Home → `home` [tap]
- Sign out → `home (signed out)` [tap] — only in·live, in·none
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Back → `Back` [back]
- Continue with Apple → `settings (signs in)` [sign-in] — only out·live, out·none
- Continue with Google → `settings (signs in)` [sign-in] — only out·live, out·none
- Delete account → `settings+delacct` [sheet]
- sheet `delacct` over this page: Delete account → `home`; Delete account → `home (signed out)`; close → `settings`; Cancel → `settings`

### Report (`report`)
States: `report@out.live`, `report@out.none`, `report@in.live`, `report@in.none`
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Send report → `reported` [tap]
- Back → `Back` [back]

### Reported (`reported`)
States: `reported@out.live`, `reported@out.none`, `reported@in.live`, `reported@in.none`
- Close → `home` [tap]
- Done → `home` [tap]
- home → `home` [tap]
- Home → `home` [tap]
- Inbox → `inbox` [tap]
- S → `me` [tap]
- Post up → `post` [tap]
- Projects → `projects` [tap]
- Nearby → `quiet-feed` [tap]
- Block Maya too → `reported+block` [sheet]
- sheet `block` over this page: Block → `home`; Blocked people (Settings) → `settings`; close → `reported`; Cancel → `reported`

## Missing edges found by the flows (design gaps)
- none
