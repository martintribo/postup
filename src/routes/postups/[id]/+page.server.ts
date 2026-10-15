import { error } from '@sveltejs/kit';
import { getPostup } from '$lib/server/postup-manage';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
	const p = await getPostup(Number(params.id));
	if (!p) error(404, 'This postup does not exist');
	return {
		title: `${p.displayName || p.name} at ${p.placeName || p.location}`,
		postup: { ...p, startTime: p.startTime.toISOString(), endsAt: p.endsAt.toISOString() },
		isOwner: !!locals.user && locals.user.id === p.userId
	};
};
