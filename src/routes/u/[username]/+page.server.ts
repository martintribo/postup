import { error } from '@sveltejs/kit';
import { getProfile, isFollowing } from '$lib/server/profile';
import { isBlockedBetween } from '$lib/server/safety';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
	const p = await getProfile(params.username);
	if (!p) error(404, 'Profile not found');
	if (locals.user && locals.user.id !== p.id && (await isBlockedBetween(locals.user.id, p.id))) error(404, 'Profile not found');
	const isMe = locals.user?.id === p.id;
	return {
		title: p.name,
		description: p.bio || `${p.name} on PostUp`,
		profile: p,
		isMe,
		signedIn: !!locals.user,
		following: locals.user && !isMe ? await isFollowing(locals.user.id, 'user', p.id) : false
	};
};
