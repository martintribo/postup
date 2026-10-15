import { getNearbyFeed } from '$lib/server/feed';
import { getUserLocation } from '$lib/server/location';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
	const { location } = await getUserLocation(event);
	const feed = await getNearbyFeed(location.latitude, location.longitude, 30, event.locals.user?.id);
	return { title: 'Nearby', feed };
};
