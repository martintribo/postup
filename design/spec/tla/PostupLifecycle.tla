---- MODULE PostupLifecycle ----
\* Formal model of the PostUp lifecycle, grounded in design/mockups/model
\* and documented in design/spec/areas/postup-lifecycle.md.
\* Each action is enabled only when its sub-feature is in Delivered.
\* Bug is "none" for the real model; broken variants set it so an invariant
\* can be shown to fail (create-formal-verification-skill: able to fail).

EXTENDS TLC, Integers, FiniteSets

CONSTANTS Delivered, Bug

FeatureIds == {
  "lifecycle-view-live",
  "lifecycle-join",
  "lifecycle-host",
  "lifecycle-end-now",
  "lifecycle-time-runs-out",
  "lifecycle-cancelled-view",
  "lifecycle-leave",
  "lifecycle-extend",
  "lifecycle-fills",
  "lifecycle-share-link-live",
  "lifecycle-share-link-ended",
  "lifecycle-ask-to-join"
}

Has(f) == f \in Delivered

Status == {"live", "full", "ended", "cancelled"}
Who    == {"browsing", "joined", "hosting", "requested"}
Entry  == {"app", "live-link", "ended-link"}
Bugs   == {"none", "join-when-full", "ended-link-live", "no-way-to-end",
           "requested-without-ask", "full-without-fills", "bad-type"}

VARIABLES status, who, entry, illegalJoin, extended

vars == <<status, who, entry, illegalJoin, extended>>

TypeOK ==
    /\ status \in Status
    /\ who \in Who
    /\ entry \in Entry
    /\ illegalJoin \in BOOLEAN
    /\ extended \in BOOLEAN
    /\ Bug \in Bugs
    /\ Delivered \subseteq FeatureIds

Open   == status \in {"live", "full"}
Closed == status \in {"ended", "cancelled"}

\* Starting situations that exist in the mocks when their sub-feature is delivered:
\* view a live postup in the app, host a live postup, open a live shared link,
\* or open an already-ended shared link (never live — unless the broken variant).
Init ==
    /\ illegalJoin = FALSE
    /\ extended = FALSE
    /\ \/ /\ Has("lifecycle-view-live")
          /\ status = "live"
          /\ who = "browsing"
          /\ entry = "app"
       \/ /\ Has("lifecycle-host")
          /\ status = "live"
          /\ who = "hosting"
          /\ entry = "app"
       \/ /\ Has("lifecycle-share-link-live")
          /\ status = "live"
          /\ who = "browsing"
          /\ entry = "live-link"
       \/ /\ Has("lifecycle-share-link-ended")
          /\ status = "ended"
          /\ who = "browsing"
          /\ entry = "ended-link"
       \/ /\ Bug = "ended-link-live"
          /\ Has("lifecycle-share-link-ended")
          /\ status = "live"
          /\ who = "browsing"
          /\ entry = "ended-link"
       \/ /\ Bug = "requested-without-ask"
          /\ status = "live"
          /\ who = "requested"
          /\ entry = "app"
       \/ /\ Bug = "full-without-fills"
          /\ status = "full"
          /\ who = "browsing"
          /\ entry = "app"
       \/ /\ Bug = "bad-type"
          /\ status = "bogus"
          /\ who = "browsing"
          /\ entry = "app"

\* --- actions (each tagged with its sub-feature id) ---

\* lifecycle-join. Grounded in postup.toml: join is for a live, open postup.
\* The broken variant also lets you "join" a full one and raises illegalJoin.
Join ==
    /\ Has("lifecycle-join")
    /\ who = "browsing"
    /\ entry \in {"app", "live-link"}
    /\ IF Bug = "join-when-full"
       THEN /\ status \in {"live", "full"}
            /\ who' = "joined"
            /\ illegalJoin' = (status = "full")
            /\ UNCHANGED <<status, entry, extended>>
       ELSE /\ status = "live"
            /\ who' = "joined"
            /\ UNCHANGED <<status, entry, illegalJoin, extended>>

\* lifecycle-ask-to-join. Grounded in postup-ask.toml / requested.toml / live.toml.
AskToJoin ==
    /\ Has("lifecycle-ask-to-join")
    /\ who = "browsing"
    /\ status = "live"
    /\ entry \in {"app", "live-link"}
    /\ who' = "requested"
    /\ UNCHANGED <<status, entry, illegalJoin, extended>>

\* Host approves a pending request while the postup is still live (not full).
Approve ==
    /\ Has("lifecycle-ask-to-join")
    /\ who = "requested"
    /\ status = "live"
    /\ who' = "joined"
    /\ UNCHANGED <<status, entry, illegalJoin, extended>>

\* lifecycle-leave. Grounded in joined.toml / leave.toml, since=share-and-chat.
Leave ==
    /\ Has("lifecycle-leave")
    /\ who = "joined"
    /\ Open
    /\ who' = "browsing"
    /\ UNCHANGED <<status, entry, illegalJoin, extended>>

\* lifecycle-extend. Visual only in the mocks (phasev.py, [M1037]); stays live.
\* Allowed only while status is live, not full — see [M1049-draft].
Extend ==
    /\ Has("lifecycle-extend")
    /\ who = "hosting"
    /\ status = "live"
    /\ extended' = TRUE
    /\ UNCHANGED <<status, who, entry, illegalJoin>>

\* lifecycle-end-now. Grounded in live.toml / endlive.toml (host only).
EndNow ==
    /\ Bug # "no-way-to-end"
    /\ Has("lifecycle-end-now")
    /\ who = "hosting"
    /\ Open
    /\ status' = "ended"
    /\ UNCHANGED <<who, entry, illegalJoin, extended>>

\* lifecycle-time-runs-out. Grounded in events.toml postup-ends.
TimeRunsOut ==
    /\ Bug # "no-way-to-end"
    /\ Has("lifecycle-time-runs-out")
    /\ Open
    /\ status' = "ended"
    /\ UNCHANGED <<who, entry, illegalJoin, extended>>

\* lifecycle-fills. Grounded in events.toml postup-fills, since=share-and-chat.
Fills ==
    /\ Has("lifecycle-fills")
    /\ status = "live"
    /\ status' = "full"
    /\ UNCHANGED <<who, entry, illegalJoin, extended>>

\* lifecycle-cancelled-view. Grounded in events.toml postup-cancelled.
Cancelled ==
    /\ Bug # "no-way-to-end"
    /\ Has("lifecycle-cancelled-view")
    /\ Open
    /\ status' = "cancelled"
    /\ UNCHANGED <<who, entry, illegalJoin, extended>>

\* Stutter once the postup is closed so TLC's deadlock check can pass
\* (statechart: end states need a Done stutter, or CHECK_DEADLOCK).
Done ==
    /\ Closed
    /\ UNCHANGED vars

Next ==
    \/ Join
    \/ AskToJoin
    \/ Approve
    \/ Leave
    \/ Extend
    \/ EndNow
    \/ TimeRunsOut
    \/ Fills
    \/ Cancelled
    \/ Done

Spec == Init /\ [][Next]_vars

\* --- invariants (rules about reachable situations) ---

\* You never join a postup that is already full (or otherwise not live).
NoJoinWhenClosed ==
    illegalJoin = FALSE

\* A shared ended-or-cancelled link never shows the postup as live.
EndedLinkNeverLive ==
    entry = "ended-link" => status \in {"ended", "cancelled"}

\* The "requested" situation only exists when ask-to-join is delivered.
AskOnlyWhenDelivered ==
    who = "requested" => Has("lifecycle-ask-to-join")

\* A full postup only exists when the size-limit feature is delivered.
FullOnlyWhenFillsDelivered ==
    status = "full" => Has("lifecycle-fills")

\* Every reachable open situation still has a way out to ended or cancelled,
\* unless no closing feature is in the delivered set (then ending is out of scope).
WayOutToEnded ==
    \/ Closed
    \/ ENABLED TimeRunsOut
    \/ ENABLED EndNow
    \/ ENABLED Cancelled
    \/ /\ ~Has("lifecycle-time-runs-out")
       /\ ~Has("lifecycle-end-now")
       /\ ~Has("lifecycle-cancelled-view")

\* Demo-only: used by the deliberately failing plan item. A joiner can leave
\* now. The first release does not deliver leave [M1037], so this fails there
\* on purpose when the plan asks for it too early. Not a product claim.
JoinerCanLeaveNow ==
    \/ who # "joined"
    \/ ~Open
    \/ ENABLED Leave

====
