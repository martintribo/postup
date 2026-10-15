import { json, error } from '@sveltejs/kit';
import { getNearbyFeed } from '$lib/server/feed';
import type { RequestHandler } from './$types';

/** JSON feed so the same view works in the native shell (M10). */
export const GET: RequestHandler = async ({ url }) => {
	const lat = Number(url.searchParams.get('lat'));
	const lng = Number(url.searchParams.get('lng'));
	if (!Number.isFinite(lat) || !Number.isFinite(lng)) error(400, 'lat and lng required');
	return json(await getNearbyFeed(lat, lng));
};
