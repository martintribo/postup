import { error } from '@sveltejs/kit';
import { getPostup } from '$lib/server/postup-manage';
import { config } from '$lib/config';
import type { PageServerLoad } from './$types';

/** Public invite landing for a shared postup (mockups #invite, #invite-ended). SSR so link previews work. */
export const load: PageServerLoad = async ({ params }) => {
	const p = await getPostup(Number(params.id));
	if (!p || p.state === 'cancelled') error(404, 'This postup is no longer available');
	const who = p.displayName || p.name;
	const hide = config.askHidesCafe && p.joinMode === 'ask';
	const where = hide ? `a cafe in ${p.neighborhood || p.locality || 'the area'}` : p.placeName || p.location;
	const until = p.endsAt.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' });
	const live = p.state === 'live';
	return {
		title: live ? `${who} is working at ${where}` : `${who} posted up at ${where}`,
		description: live ? `${p.activity} · here till ${until}. Join on PostUp.` : `${p.activity}. See who's posted up nearby now.`,
		invite: { id: p.id, who, where, activity: p.activity, until, live, ask: p.joinMode === 'ask', avatarUrl: p.avatarUrl, projectName: p.projectName, projectId: p.projectId }
	};
};
