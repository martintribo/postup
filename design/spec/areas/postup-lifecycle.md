# Postup lifecycle

A postup is a live, time-limited presence at a place. This area is the full intended life of that postup: people join or ask to join, the host extends or ends it, a joiner leaves, it fills up, time runs out, someone opens a shared link that is still live or already ended, and everyone sees a closed state rather than a live one. The map is grounded in the existing mock model. Sub-features the mocks do not yet specify are marked as questions for Martin and are not given invented product rules. [M1049-draft]

Model sources: `design/mockups/model/screens/postup.toml`, `joined.toml`, `posted.toml`, `live.toml`, `endlive.toml`, `leave.toml`, `share.toml`, `postup-ended.toml`, `postup-cancelled.toml`, `postup-full.toml`, `invite.toml`, `invite-ended.toml`, `postup-ask.toml`, `requested.toml`, `ask.toml`, and `design/mockups/model/events.toml`. Phase bounds come from `since` / `until` on those items and from notes tagged [M1037], [M1036], [M1040], [M1046], [M1047-draft]. The +30 min extend control is drawn and phase-gated in `design/mockups/gen/phasev.py` but has no model link.

## Sub-features

- `lifecycle-view-live` sees someone else's live, open postup (the `#postup` screen; untagged, every phase). [FS]
- `lifecycle-join` joins an "anyone can join" postup: signed out opens the sign-in sheet, signed in goes to `#joined`. Links `postup:join`. [FS]
- `lifecycle-host` is the host's view after posting: `#posted` then `#live` ("You're live"). Screens `posted.toml`, `live.toml` are untagged. [FS] [F057]
- `lifecycle-end-now` lets the host end the postup now: `#live` → sheet `#endlive` → "End now" goes to `#me`. Link `live:end-postup` and `endlive:end-now`, untagged. Joiners and anyone waiting are told it ended. [FS] [drawn]
- `lifecycle-time-runs-out` is the site event `postup-ends`: on `#postup`, `#joined`, `#requested`, `#invite`, `#postup-ask`, or `#postup-full` the person is taken to `#postup-ended`. Untagged. Nearby `live` is unchanged. [F060] [M1031-draft]
- `lifecycle-cancelled-view` is the site event `postup-cancelled`, landing on `#postup-cancelled`. Untagged. The mocks describe this as "the poster cancelled" [F060] [R47], but there is no separate host "Cancel" control — only "End postup". See the question below. [M1049-draft]
- `lifecycle-leave` lets a joiner leave early: `#joined` → sheet `#leave` → "Leave" goes to `#postup`. `since = "share-and-chat"`. Not in phase 0: joining means you are coming, and the postup ends at its set time. [FS] [M1037]
- `lifecycle-extend` is the host's +30 min control on `#live`. Notes and HTML hide it in phase 0 ("the host posts again when time runs out"). [M1037] There is no model link for extend, only a visual mark in `phasev.py`. The spec treats it as staying live when the feature is delivered.
- `lifecycle-fills` is the size limit: event `postup-fills` and screen `#postup-full`, both `since = "share-and-chat"`. You cannot join a full postup; the screen offers nearby and follow. [F060] [R47] [M1040] [M1047-draft]
- `lifecycle-share-link-live` is a shared link to a still-live postup: way `link-live` starts at `#invite` (`invite.toml`, `since = "share-and-chat"`). Share itself is the `#share` sheet on `#live` / `#postup` / `#posted`. [FS] [R39] [M1046]
- `lifecycle-share-link-ended` is a shared link opened after the postup has ended: way `link-ended` starts at `#invite-ended`. It must not show the postup as live. [FS] [R39] [M1032] [M1046]
- `lifecycle-ask-to-join` is a postup where the host approves joiners: `#postup-ask`, `#ask`, `#requested`, and the Requests section on `#live`, all `since = "projects"`. [FS] [F055] [M1036]
- `lifecycle-cancel-before-join` (future, not in the mocks) would be the host cancelling a postup before anyone has joined, if that is different from "End now". Not modeled as a rule. [M1049-draft]

## How to get to it (user POV)

- Post up from the tab bar or a place, finish the post flow, and land on `#posted` / `#live` (host). Start screens and links are in `post.toml` and `posted.toml`.
- Open a live postup from Home, Nearby, a cafe, or a profile, and land on `#postup` or `#postup-ask`.
- Come back already hosting (`ways.toml` `hosting` starts at `#live`) or already joined (`joined` starts at `#joined`).
- Open a friend's shared link while it is live (`link-live` → `#invite`) or after it has ended (`link-ended` → `#invite-ended`). These ways are `since = "share-and-chat"`. [M1046]
- Be on a live postup when the site event `postup-ends`, `postup-fills`, or `postup-cancelled` fires (see `events.toml` for the screens each event applies to).

## Driving it with the mock model

Preconditions:

- The mockups are built from `design/mockups/model/` (`python3 gen/build.py` in `design/mockups`).
- Phase is one of `post-and-join`, `share-and-chat`, or `projects` (aliases `0` / `smallest`, `1` / `pre-mvp`, `2` / `mvp` still work).
- Checks read the model files, not invented screens.

- **Join a live postup.** From `#postup` with `auth=in`, follow `join` to `#joined`. With `auth=out`, `join` opens the sign-in sheet. Available in every phase.
- **Leave early.** From `#joined` in `share-and-chat` or `projects`, follow `leave` to the leave sheet and confirm; you land on `#postup`. In `post-and-join` the `leave` link is not available. [M1037]
- **Host ends now.** From `#live`, open `#endlive` and choose "End now" (`endlive:end-now` → `#me`). Available in every phase.
- **Time runs out.** Event `postup-ends` on a viewing or joined screen goes to `#postup-ended`. Available in every phase.
- **It fills up.** Event `postup-fills` goes to `#postup-full`, only from `share-and-chat` onward. [M1040]
- **Open an ended link.** Way `link-ended` starts at `#invite-ended`, only from `share-and-chat` onward. The screen is an ended state, not a live join. [M1046]
- **Ask to join.** From `#postup-ask` in the `projects` phase, ask and land on `#requested`. Approve/decline is on `#live`. [M1036]

## Gotchas

- Leave and extend are intentionally absent in `post-and-join`. That is not a missing screen; it is [M1037]. A joiner in that phase waits for the set end time or for the host to end now.
- Share links, the share sheet, chat, and the size limit also start at `share-and-chat`. [M1046] [M1040]
- Ask-to-join and the host's Requests section start at `projects`. [M1036]
- "End now" is a host action (sheet `#endlive`). "Leave" is a joiner action (sheet `#leave`). They are different screens.
- The +30 min extend control is visible in the mock from `share-and-chat` onward, but it is not a link in `live.toml`. Do not treat a missing link as "extend does nothing" without asking; the spec only models "stays live" when the feature is delivered.
- Event `postup-cancelled` exists in every phase, and `#postup-cancelled` is untagged, but the host's only close control is "End postup". Whether cancel-before-anyone-joins is a distinct product path is an open question. [M1049-draft]
- After leaving, the mock lands you on `#postup` (the same postup, now as a visitor). Whether you can join again is not spelled out. [M1049-draft]
- Whether a host can extend a postup that is already full is not spelled out. The spec allows extend only while the status is live (not full). [M1049-draft]
- `postups-end` (all nearby postups end, `live=none`) is a different event from `postup-ends` (this postup's status). This area models the one postup's status. [M1031-draft]
