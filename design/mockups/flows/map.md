# PostUp flow map
Flow map (Martin, Oct 25 2026 [M1025]): a state machine from a first-time visitor (signed out, never registered) to the starting point of every critical flow. User states are grouped into four boxes, left to right: Arrive, Signed out browsing, Signed in, Doing something. Arrows are events or conditions (dashed = going back). Each flow’s badge sits inside the state where it starts (green = MVP must, grey = nice) and opens the flow player. All 23 flows are reachable from the root.

Page: /mockups/flows/map.html (grouped boxes, hand-placed) · grid: /mockups/flows/grid.html

## Groups
- **1 · Arrive**: First-time visitor · signed out · never registered, Slow network or offline [M1025]
- **2 · Signed out, browsing**: Signed out · on a live postup link, Signed out · someone live nearby, Signed out · nobody live, Signed out · on an ended postup link, Signed out · on a project link [M1025]
- **3 · Signed in**: Signed in · someone live nearby, Returning user · signed in, Signed in · nobody live [M1025]
- **4 · Doing something**: Signed in · ask pending, Signed in · joined a postup, Signed in · hosting (live) [M1025]

```mermaid
flowchart LR
  subgraph arrive["1 · Arrive"]
    direction TB
    V0(("First-time visitor<br>signed out · never registered"))
    OFF("Slow network or offline")
  end
  subgraph out["2 · Signed out, browsing"]
    direction TB
    SLK("Signed out<br>on a live postup link")
    SL("Signed out<br>someone live nearby")
    SN("Signed out<br>nobody live")
    SEN("Signed out<br>on an ended postup link")
    SPJ("Signed out<br>on a project link")
  end
  subgraph in["3 · Signed in"]
    direction TB
    RL("Signed in<br>someone live nearby")
    RET("Returning user<br>signed in")
    RN("Signed in<br>nobody live")
  end
  subgraph doing["4 · Doing something"]
    direction TB
    PEND("Signed in<br>ask pending")
    JN("Signed in<br>joined a postup")
    HOST("Signed in<br>hosting (live)")
  end
  V0 -->|"/ · someone live"| SL
  V0 -->|"/ · nobody live"| SN
  V0 -->|"link · live"| SLK
  V0 -->|"link · ended"| SEN
  V0 -->|"link · project"| SPJ
  V0 -->|"network drops"| OFF
  SL -->|"Join · signs in"| JN
  SL -->|"postups end"| SN
  SN -->|"Post up · signs in"| HOST
  SLK -->|"Join · signs in"| JN
  SEN -->|"Follow · signs in"| RN
  SPJ -->|"Follow · signs in"| RN
  JN -->|"ends · leaves"| RET
  HOST -->|"ends"| RET
  RET -->|"someone live"| RL
  RET -->|"nobody live"| RN
  RL -->|"joins"| JN
  RL -->|"asks"| PEND
  PEND -->|"approved"| JN
  PEND -->|"declined"| RL
  RL -->|"posts up"| HOST
  RN -->|"posts up"| HOST
  OFF -->|"back online"| RET
  SL -.-> F_first_visit_live(["▶ First-time visitor, someone is live"])
  click F_first_visit_live href "first-visit-live.html"
  SN -.-> F_first_visit_none(["▶ First-time visitor, nobody live"])
  click F_first_visit_none href "first-visit-none.html"
  SN -.-> F_first_post(["▶ First post up (with sign-in)"])
  click F_first_post href "first-post.html"
  SLK -.-> F_invite_live(["▶ Share link to a live postup"])
  click F_invite_live href "invite-live.html"
  SEN -.-> F_invite_ended(["▶ Share link to an ended postup"])
  click F_invite_ended href "invite-ended.html"
  SPJ -.-> F_invite_project(["▶ Share link to a project"])
  click F_invite_project href "invite-project.html"
  OFF -.-> F_loading_offline(["▶ Slow network and offline"])
  click F_loading_offline href "loading-offline.html"
  RL -.-> F_cautious_joiner(["▶ Cautious joiner checks a few postups, then joins"])
  click F_cautious_joiner href "cautious-joiner.html"
  RL -.-> F_quick_joiner(["▶ Quick joiner"])
  click F_quick_joiner href "quick-joiner.html"
  RL -.-> F_ask_join(["▶ Ask to join, then get approved (joiner side)"])
  click F_ask_join href "ask-join.html"
  RL -.-> F_returning_post(["▶ Returning poster"])
  click F_returning_post href "returning-post.html"
  RL -.-> F_desktop_browse(["▶ Desktop browse and post"])
  click F_desktop_browse href "desktop-browse.html"
  RL -.-> F_postup_states(["▶ Postup ends, fills or is cancelled while you look"])
  click F_postup_states href "postup-states.html"
  RL -.-> F_safety(["▶ Report and block"])
  click F_safety href "safety.html"
  HOST -.-> F_host_approve(["▶ Host approves a request"])
  click F_host_approve href "host-approve.html"
  HOST -.-> F_hosting(["▶ Hosting live: extend, edit, end"])
  click F_hosting href "hosting.html"
  JN -.-> F_leave(["▶ Leave a postup you joined"])
  click F_leave href "leave.html"
  JN -.-> F_chat(["▶ Postup chat"])
  click F_chat href "chat.html"
  RN -.-> F_project_builder(["▶ Project builder: create, update, post up for it"])
  click F_project_builder href "project-builder.html"
  RN -.-> F_following(["▶ Follow a person or project"])
  click F_following href "following.html"
  RN -.-> F_empty_area(["▶ Empty area: be the first"])
  click F_empty_area href "empty-area.html"
  RET -.-> F_delete_account(["▶ Delete account"])
  click F_delete_account href "delete-account.html"
  RET -.-> F_settings_notify(["▶ Notification settings and sign out"])
  click F_settings_notify href "settings-notify.html"
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
