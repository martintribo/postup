import { flag } from '$lib/flags';
import { phase } from '$lib/phase';

/** Phase 0 cuts, gated so phase 1/2 code stays. Flags still apply once the phase allows the feature. */
export function showChat() {
	return phase() >= 1 && flag('chat');
}
export function showInbox() {
	return phase() >= 1 && flag('chat');
}
export function showShare() {
	return phase() >= 1 && flag('share_links');
}
export function showLeave() {
	return phase() >= 1;
}
export function showExtend() {
	return phase() >= 1;
}
export function showProjects() {
	return phase() >= 2 && flag('projects_v2');
}
export function showAskJoin() {
	return phase() >= 2;
}
export function showBuilding() {
	return phase() >= 2;
}
/** Phase 0 accounts are verified identities only (Apple, Google, X, GitHub). */
export function verifiedOnly() {
	return phase() < 1;
}
