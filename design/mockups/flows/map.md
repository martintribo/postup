# PostUp flow map
Flow map (Martin, Oct 25 2026 [M1025]): a state machine from a first-time visitor (signed out, never registered) to the starting point of every critical flow. User states are grouped into four boxes, left to right: Arrive (first-time visitors split by intent: stumbled on it, curious about content, came to post up, opened a share link), Signed out browsing, Signed in, Doing something. Arrows are events or conditions (dashed = going back). Each flow’s badge sits inside the state where it starts (green = MVP must, grey = nice) and opens the flow player. All 22 flows are reachable from the root.

Page: /mockups/flows/map.html (grouped boxes, hand-placed) · grid: /mockups/flows/grid.html

## Groups
- **1 · Arrive (by intent)**: First-time visitor · signed out · never registered, Stumbled on it · no idea what PostUp is, Curious about content · live now or past, Came to post up · wants to go live now, Opened a share link · arrives with context, Slow network or offline [M1025]
- **2 · Signed out, browsing**: Signed out · someone live nearby, Signed out · nobody live, Signed out · on the Post up form, Signed out · on a live postup link, Signed out · on an ended postup link, Signed out · on a project link [M1025]
- **3 · Signed in**: Signed in · someone live nearby, Signed in · nobody live, Returning user · signed in [M1025]
- **4 · Doing something**: Signed in · ask pending, Signed in · joined a postup, Signed in · hosting (live) [M1025]

```mermaid
flowchart LR
  subgraph arrive["1 · Arrive (by intent)"]
    direction TB
    V0(("First-time visitor<br>signed out · never registered"))
    IST("Stumbled on it<br>no idea what PostUp is")
    ICU("Curious about content<br>live now or past")
    IPO("Came to post up<br>wants to go live now")
    ILK("Opened a share link<br>arrives with context")
    OFF("Slow network or offline")
  end
  subgraph out["2 · Signed out, browsing"]
    direction TB
    SL("Signed out<br>someone live nearby")
    SN("Signed out<br>nobody live")
    SPO("Signed out<br>on the Post up form")
    SLK("Signed out<br>on a live postup link")
    SEN("Signed out<br>on an ended postup link")
    SPJ("Signed out<br>on a project link")
  end
  subgraph in["3 · Signed in"]
    direction TB
    RL("Signed in<br>someone live nearby")
    RN("Signed in<br>nobody live")
    RET("Returning user<br>signed in")
  end
  subgraph doing["4 · Doing something"]
    direction TB
    PEND("Signed in<br>ask pending")
    JN("Signed in<br>joined a postup")
    HOST("Signed in<br>hosting (live)")
  end
  V0 -->|""| IST
  V0 -->|""| ICU
  V0 -->|""| IPO
  V0 -->|""| ILK
  V0 -->|""| OFF
  IST -->|"someone live"| SL
  IST -->|"nobody live"| SN
  ICU -->|"someone live"| SL
  ICU -->|"nobody live"| SN
  IPO -->|"taps Post up"| SPO
  ILK -->|"live"| SLK
  ILK -->|"ended"| SEN
  ILK -->|"project"| SPJ
  SN -->|"Post up"| SPO
  SPO -->|"Post up · signs in"| HOST
  SL -->|"Join · signs in"| JN
  SL -->|"postups end"| SN
  SLK -->|"Join · signs in"| JN
  SEN -->|"Follow · signs in"| RN
  SPJ -->|"Follow · signs in"| RN
  JN -->|"ends · leaves"| RET
  HOST -->|"ends"| RET
  RET -->|""| RL
  RET -->|"nobody live"| RN
  RL -->|"joins"| JN
  RL -->|"asks"| PEND
  PEND -->|"approved"| JN
  PEND -->|"declined"| RL
  RL -->|"posts up"| HOST
  RN -->|"posts up"| HOST
  OFF -->|"back online"| RET
  ICU -.-> F_look_around(["▶ Newcomer looks around, then joins"])
  click F_look_around href "look-around.html"
  SN -.-> F_empty_area_newcomer(["▶ Nobody live nearby (newcomer)"])
  click F_empty_area_newcomer href "empty-area-newcomer.html"
  IPO -.-> F_first_post(["▶ Came to post up: first post with sign-in"])
  click F_first_post href "first-post.html"
  SLK -.-> F_invite_live(["▶ Share link to a live postup"])
  click F_invite_live href "invite-live.html"
  SPJ -.-> F_invite_project(["▶ Share link to a project"])
  click F_invite_project href "invite-project.html"
  OFF -.-> F_loading_offline(["▶ Slow network and offline"])
  click F_loading_offline href "loading-offline.html"
  RL -.-> F_join(["▶ Join someone live"])
  click F_join href "join.html"
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
  RN -.-> F_empty_area(["▶ Nobody live nearby (signed in)"])
  click F_empty_area href "empty-area.html"
  RET -.-> F_delete_account(["▶ Delete account"])
  click F_delete_account href "delete-account.html"
  RET -.-> F_settings_notify(["▶ Notification settings and sign out"])
  click F_settings_notify href "settings-notify.html"
  RET -.-> F_catch_up(["▶ Catch up on what happened"])
  click F_catch_up href "catch-up.html"
```

## Where each flow starts
- `look-around` (Phase 0): from state "Curious about content · live now or past" when curious or no idea, joins [M1025]
- `empty-area-newcomer` (Phase 0): from state "Signed out · nobody live" when nobody live [M1025]
- `first-post` (Phase 0): from state "Came to post up · wants to go live now" [M1025]
- `invite-live` (Phase 0): from state "Signed out · on a live postup link" [M1025]
- `invite-project` (Phase 2 (MVP)): from state "Signed out · on a project link" [M1025]
- `loading-offline` (Unphased): from state "Slow network or offline" [M1025]
- `join` (Phase 0): from state "Signed in · someone live nearby" [M1025]
- `ask-join` (Phase 2 (MVP)): from state "Signed in · someone live nearby" [M1025]
- `returning-post` (Phase 1): from state "Signed in · someone live nearby" [M1025]
- `desktop-browse` (Unphased): from state "Signed in · someone live nearby" when on a laptop [M1025]
- `postup-states` (Unphased): from state "Signed in · someone live nearby" when postup fills or ends [M1025]
- `safety` (Phase 0): from state "Signed in · someone live nearby" when someone feels off [M1025]
- `host-approve` (Phase 2 (MVP)): from state "Signed in · hosting (live)" when gets a request [M1025]
- `hosting` (Phase 1): from state "Signed in · hosting (live)" [M1025]
- `leave` (Phase 1): from state "Signed in · joined a postup" when plans change [M1025]
- `chat` (Phase 1): from state "Signed in · joined a postup" [M1025]
- `project-builder` (Phase 2 (MVP)): from state "Signed in · nobody live" [M1025]
- `following` (Unphased): from state "Signed in · nobody live" [M1025]
- `empty-area` (Phase 0): from state "Signed in · nobody live" when area has no postups [M1025]
- `delete-account` (Unphased): from state "Returning user · signed in" [M1025]
- `settings-notify` (Unphased): from state "Returning user · signed in" [M1025]
- `catch-up` (Unphased): from state "Returning user · signed in" when comes back later [M1025]
