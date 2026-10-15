import { error } from '@sveltejs/kit';
import { getPostup } from '$lib/server/postup-manage';
import { myRequest, listRequests, approvedCount } from '$lib/server/join';
import { config } from '$lib/config';
import { flag } from '$lib/flags';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
	const p = await getPostup(Number(params.id));
	if (!p) error(404, 'This postup does not exist');
	const isOwner = !!locals.user && locals.user.id === p.userId;
	const mine = locals.user && !isOwner ? await myRequest(p.id, locals.user.id) : null;
	const approved = mine?.status === 'approved';
	// D2: in ask mode, non-approved viewers see the neighborhood, not the cafe.
	const hideCafe = config.askHidesCafe && p.joinMode === 'ask' && !isOwner && !approved;
	const area = p.neighborhood || p.locality || 'nearby';
	const view = {
		...p,
		placeName: hideCafe ? null : p.placeName,
		placeId: hideCafe ? null : p.placeId,
		location: hideCafe ? `a cafe in ${area}` : p.location,
		latitude: hideCafe ? null : p.latitude,
		longitude: hideCafe ? null : p.longitude,
		startTime: p.startTime.toISOString(),
		endsAt: p.endsAt.toISOString()
	};
	const joined = await approvedCount(p.id);
	return {
		title: `${p.displayName || p.name} at ${view.placeName || view.location}`,
		postup: view,
		hideCafe,
		isOwner,
		joinEnabled: flag('join'),
		signedIn: !!locals.user,
		myRequest: mine ? { id: mine.id, status: mine.status } : null,
		requests: isOwner ? (await listRequests(p.id)).map((r) => ({ ...r, createdAt: r.createdAt.toISOString() })) : [],
		joinedCount: joined,
		full: !!p.capacity && joined >= p.capacity
	};
};
