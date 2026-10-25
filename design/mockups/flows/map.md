# PostUp flow map
Flow map (Martin, Oct 25 2026 [M1025]): a state machine from a first-time visitor (signed out, never registered) to the starting point of every critical flow. Nodes are user states; solid arrows are events or conditions; dashed arrows lead to a flow badge (green = MVP must, grey = nice) that opens the flow player. All 23 flows are reachable from the root.

Page: /mockups/flows/map.html · grid: /mockups/flows/grid.html

```mermaid
flowchart LR
  V0(("First-time visitor<br>signed out · never registered"))
  SL("Signed out<br>someone live nearby")
  SN("Signed out<br>nobody live")
  SLK("Signed out<br>on a live postup link")
  SEN("Signed out<br>on an ended postup link")
  SPJ("Signed out<br>on a project link")
  OFF("Slow network or offline")
  JN("Signed in<br>joined a postup")
  PEND("Signed in<br>ask pending")
  HOST("Signed in<br>hosting (live)")
  RET("Returning user<br>signed in")
  RL("Signed in<br>someone live nearby")
  RN("Signed in<br>nobody live")
  V0 -->|"arrives at / · someone live"| SL
  V0 -->|"arrives at / · nobody live"| SN
  V0 -->|"opens share link · live"| SLK
  V0 -->|"opens share link · ended"| SEN
  V0 -->|"opens share link · project"| SPJ
  V0 -->|"network drops"| OFF
  SL -->|"taps Join · signs in / registers"| JN
  SL -->|"postups end"| SN
  SN -->|"posts up · signs in / registers"| HOST
  SLK -->|"taps Join · signs in"| JN
  SEN -->|"follows poster · signs in"| RN
  SPJ -->|"follows project · signs in"| RN
  JN -->|"postup ends or leaves"| RET
  HOST -->|"ends postup"| RET
  RET -->|"comes back · someone live"| RL
  RET -->|"comes back · nobody live"| RN
  RL -->|"joins"| JN
  RL -->|"asks to join"| PEND
  PEND -->|"gets approved"| JN
  PEND -->|"declined or cancels"| RL
  RL -->|"posts up"| HOST
  RN -->|"posts up"| HOST
  OFF -->|"back online"| RET
  SL -.-> F_first_visit_live(["▶ First-time visitor, someone is live"])
  click F_first_visit_live href "first-visit-live.html" "Open the First-time visitor, someone is live player"
  class F_first_visit_live must
  SN -.-> F_first_visit_none(["▶ First-time visitor, nobody live"])
  click F_first_visit_none href "first-visit-none.html" "Open the First-time visitor, nobody live player"
  class F_first_visit_none must
  SN -.-> F_first_post(["▶ First post up (with sign-in)"])
  click F_first_post href "first-post.html" "Open the First post up (with sign-in) player"
  class F_first_post must
  SLK -.-> F_invite_live(["▶ Share link to a live postup"])
  click F_invite_live href "invite-live.html" "Open the Share link to a live postup player"
  class F_invite_live must
  SEN -.-> F_invite_ended(["▶ Share link to an ended postup"])
  click F_invite_ended href "invite-ended.html" "Open the Share link to an ended postup player"
  class F_invite_ended must
  SPJ -.-> F_invite_project(["▶ Share link to a project"])
  click F_invite_project href "invite-project.html" "Open the Share link to a project player"
  class F_invite_project must
  OFF -.-> F_loading_offline(["▶ Slow network and offline"])
  click F_loading_offline href "loading-offline.html" "Open the Slow network and offline player"
  class F_loading_offline must
  RL -.-> F_cautious_joiner(["▶ Cautious joiner checks a few postups, then joins"])
  click F_cautious_joiner href "cautious-joiner.html" "Open the Cautious joiner checks a few postups, then joins player"
  class F_cautious_joiner must
  RL -.-> F_quick_joiner(["▶ Quick joiner"])
  click F_quick_joiner href "quick-joiner.html" "Open the Quick joiner player"
  class F_quick_joiner must
  RL -.-> F_ask_join(["▶ Ask to join, then get approved (joiner side)"])
  click F_ask_join href "ask-join.html" "Open the Ask to join, then get approved (joiner side) player"
  class F_ask_join must
  RL -.-> F_returning_post(["▶ Returning poster"])
  click F_returning_post href "returning-post.html" "Open the Returning poster player"
  class F_returning_post must
  RL -.->|"on a laptop"| F_desktop_browse(["▶ Desktop browse and post"])
  click F_desktop_browse href "desktop-browse.html" "Open the Desktop browse and post player"
  class F_desktop_browse nice
  RL -.->|"postup fills or ends"| F_postup_states(["▶ Postup ends, fills or is cancelled while you look"])
  click F_postup_states href "postup-states.html" "Open the Postup ends, fills or is cancelled while you look player"
  class F_postup_states must
  RL -.->|"someone feels off"| F_safety(["▶ Report and block"])
  click F_safety href "safety.html" "Open the Report and block player"
  class F_safety must
  HOST -.->|"gets a request"| F_host_approve(["▶ Host approves a request"])
  click F_host_approve href "host-approve.html" "Open the Host approves a request player"
  class F_host_approve must
  HOST -.-> F_hosting(["▶ Hosting live: extend, edit, end"])
  click F_hosting href "hosting.html" "Open the Hosting live: extend, edit, end player"
  class F_hosting must
  JN -.->|"plans change"| F_leave(["▶ Leave a postup you joined"])
  click F_leave href "leave.html" "Open the Leave a postup you joined player"
  class F_leave must
  JN -.-> F_chat(["▶ Postup chat"])
  click F_chat href "chat.html" "Open the Postup chat player"
  class F_chat must
  RN -.-> F_project_builder(["▶ Project builder: create, update, post up for it"])
  click F_project_builder href "project-builder.html" "Open the Project builder: create, update, post up for it player"
  class F_project_builder must
  RN -.-> F_following(["▶ Follow a person or project"])
  click F_following href "following.html" "Open the Follow a person or project player"
  class F_following must
  RN -.->|"area has no postups"| F_empty_area(["▶ Empty area: be the first"])
  click F_empty_area href "empty-area.html" "Open the Empty area: be the first player"
  class F_empty_area must
  RET -.-> F_delete_account(["▶ Delete account"])
  click F_delete_account href "delete-account.html" "Open the Delete account player"
  class F_delete_account must
  RET -.-> F_settings_notify(["▶ Notification settings and sign out"])
  click F_settings_notify href "settings-notify.html" "Open the Notification settings and sign out player"
  class F_settings_notify nice
  class V0 root
  class SL out
  class SN out
  class SLK out
  class SEN out
  class SPJ out
  class OFF any
  class JN in
  class PEND in
  class HOST in
  class RET in
  class RL in
  class RN in
  classDef root fill:#0f7a4f,color:#fff,stroke:#0b5c3b,stroke-width:3px
  classDef out fill:#fff,color:#232322,stroke:#8a8984,stroke-width:2px
  classDef in fill:#e6f4ec,color:#0b4a30,stroke:#10a364,stroke-width:2px
  classDef any fill:#fff3d6,color:#5c3d00,stroke:#c48a00,stroke-width:2px
  classDef must fill:#10a364,color:#fff,stroke:#0b5c3b
  classDef nice fill:#eceae4,color:#33332f,stroke:#8a8984
```

## Where each flow starts
- `first-visit-live` (MVP must): from state "Signed out · someone live nearby" [M1025]
- `first-visit-none` (MVP must): from state "Signed out · nobody live" [M1025]
- `first-post` (MVP must): from state "Signed out · nobody live" [M1025]
- `invite-live` (MVP must): from state "Signed out · on a live postup link" [M1025]
- `invite-ended` (MVP must): from state "Signed out · on an ended postup link" [M1025]
- `invite-project` (MVP must): from state "Signed out · on a project link" [M1025]
- `loading-offline` (MVP must): from state "Slow network or offline" [M1025]
- `cautious-joiner` (MVP must): from state "Signed in · someone live nearby" [M1025]
- `quick-joiner` (MVP must): from state "Signed in · someone live nearby" [M1025]
- `ask-join` (MVP must): from state "Signed in · someone live nearby" [M1025]
- `returning-post` (MVP must): from state "Signed in · someone live nearby" [M1025]
- `desktop-browse` (nice): from state "Signed in · someone live nearby" when on a laptop [M1025]
- `postup-states` (MVP must): from state "Signed in · someone live nearby" when postup fills or ends [M1025]
- `safety` (MVP must): from state "Signed in · someone live nearby" when someone feels off [M1025]
- `host-approve` (MVP must): from state "Signed in · hosting (live)" when gets a request [M1025]
- `hosting` (MVP must): from state "Signed in · hosting (live)" [M1025]
- `leave` (MVP must): from state "Signed in · joined a postup" when plans change [M1025]
- `chat` (MVP must): from state "Signed in · joined a postup" [M1025]
- `project-builder` (MVP must): from state "Signed in · nobody live" [M1025]
- `following` (MVP must): from state "Signed in · nobody live" [M1025]
- `empty-area` (MVP must): from state "Signed in · nobody live" when area has no postups [M1025]
- `delete-account` (MVP must): from state "Returning user · signed in" [M1025]
- `settings-notify` (nice): from state "Returning user · signed in" [M1025]
