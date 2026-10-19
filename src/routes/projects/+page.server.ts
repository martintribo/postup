import { listProjectCards, dayLabel } from '$lib/server/projects-view';
import { db } from '$lib/server/db';
import { projectChange } from '$lib/server/db/schema';
import { and, eq, sql } from 'drizzle-orm';
import { getUserLocation } from '$lib/server/location';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
	const { url, locals } = event;
	const { location } = await getUserLocation(event);
	// Closest first, even when none are local (mockup #projects, M1018c).
	const f = url.searchParams.get('f');
	const filter = f === 'following' || f === 'mine' ? f : 'all';
	const cards = (await listProjectCards(filter, locals.user?.id, { lat: location.latitude, lng: location.longitude })).map((c) => ({ ...c, when: dayLabel(c.lastAt) }));
	const [pending] = locals.user
		? await db.select({ n: sql<number>`count(*)::int` }).from(projectChange).where(and(eq(projectChange.userId, locals.user.id), eq(projectChange.status, 'pending')))
		: [];
	return { title: 'Projects', filter, cards, pending: pending?.n ?? 0, signedIn: !!locals.user };
};
