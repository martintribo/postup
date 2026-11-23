// Coarse labels for the lifecycle chart. Aim: under ~20 arrows.
// Entry path and the +30 mark are omitted so a live-link visit is drawn
// the same as visiting from the app, and extend stays on "hosting · live".
// An already-ended shared link starts in "visiting · ended".

export const title = "Postup lifecycle";

const STEPS = {
  Join: "you join",
  AskToJoin: "you ask to join",
  Approve: "the host approves",
  Leave: "you leave",
  Extend: "the host adds 30 minutes",
  EndNow: "the host ends it now",
  TimeRunsOut: "time runs out",
  Fills: "it fills up",
  Cancelled: "it is cancelled",
  Done: "it stays ended",
};

export function state(v) {
  const who = {
    browsing: "visiting",
    joined: "joined",
    hosting: "hosting",
    requested: "asked to join",
  }[v.who] || v.who;
  const st = {
    live: "live",
    full: "full",
    ended: "ended",
    cancelled: "cancelled",
  }[v.status] || v.status;
  return { Situation: `${who} / ${st}` };
}

export function step(action) {
  if (STEPS[action]) return STEPS[action];
  return action
    .replace(/(?<=[a-z])(?=[A-Z0-9])|(?<=[A-Z])(?=[A-Z][a-z])/g, " ")
    .toLowerCase();
}
