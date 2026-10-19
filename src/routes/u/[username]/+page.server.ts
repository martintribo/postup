import { error } from '@sveltejs/kit';
import { getProfile, isFollowing } from '$lib/server/profile';
import { isBlockedBetween } from '$lib/server/safety';
import type { PageServerLoad } from './$types';

/** Mockups #profile (someone else) and #me (you). */
export const load: PageServerLoad = async ({ params, locals }) => {
	const p = await getProfile(params.username);
	if (!p) error(404, 'Profile not found');
	if (locals.user && locals.user.id !== p.id && (await isBlockedBetween(locals.user.id, p.id))) error(404, 'Profile not found');
	const isMe = locals.user?.id === p.id;
	let requests = 0;
	if (isMe && p.live) {
		const { listRequests } = await import('$lib/server/join');
		requests = (await listRequests(p.live.id)).filter((r) => r.status === 'pending').length;
	}
	return {
		title: p.name,
		description: p.bio || `${p.name} on PostUp`,
		profile: p,
		isMe,
		requests,
		signedIn: !!locals.user,
		following: locals.user && !isMe ? await isFollowing(locals.user.id, 'user', p.id) : false
	};
};
