import { getNearbyFeed } from '$lib/server/feed';
import { listProjectCards, dayLabel } from '$lib/server/projects-view';
import { getUserLocation } from '$lib/server/location';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
	const { location } = await getUserLocation(event);
	const feed = await getNearbyFeed(location.latitude, location.longitude, 30, event.locals.user?.id);
	// Nothing this week: fall back to recent projects of any age, never an empty screen.
	const projects = feed.items.length ? [] : (await listProjectCards('all', event.locals.user?.id)).slice(0, 12).map((c) => ({ ...c, when: dayLabel(c.lastAt) }));
	return { title: 'Nearby', feed, projects };
};
