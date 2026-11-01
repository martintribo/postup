import { error } from '@sveltejs/kit';
import { getPostup } from '$lib/server/postup-manage';
import { config } from '$lib/config';
import { showAskJoin } from '$lib/features';
import { isPostHiddenByReports } from '$lib/server/safety';
import type { PageServerLoad } from './$types';

/** Public invite landing for a shared postup (mockups #invite, #invite-ended). SSR so link previews work. */
export const load: PageServerLoad = async ({ params, locals }) => {
	const p = await getPostup(Number(params.id));
	if (!p || p.state === 'cancelled') error(404, 'This postup is no longer available');
	const isOwner = !!locals.user && locals.user.id === p.userId;
	if (!isOwner && (await isPostHiddenByReports(p.id))) error(404, 'This postup is no longer available');
	const who = p.displayName || p.username || p.name;
	const hide = showAskJoin() && config.askHidesCafe && p.joinMode === 'ask';
	const where = hide ? `a cafe in ${p.neighborhood || p.locality || 'the area'}` : p.placeName || p.location;
	const until = p.endsAt.toISOString();
	const day = (d: Date) => d.toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
	const ago = Math.round((new Date(day(new Date())).getTime() - new Date(day(p.startTime)).getTime()) / 86400e3);
	const when = ago <= 0 ? 'earlier today' : ago === 1 ? 'yesterday' : `on ${p.startTime.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'America/Los_Angeles' })}`;
	const live = p.state === 'live';
	return {
		title: live ? `${who} is working at ${where}` : `${who} posted up at ${where}`,
		description: live ? `${p.activity} · here till ${until}. Join on PostUp.` : `${p.activity}. See who's posted up nearby now.`,
		signedIn: !!locals.user,
		noTabs: true,
		invite: { id: p.id, who, where, when, activity: p.activity, until, live, ask: p.joinMode === 'ask', avatarUrl: p.avatarUrl, projectName: p.projectName, projectId: p.projectId }
	};
};
