import type { RequestEvent } from '@sveltejs/kit';
import { and, eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { post } from '$lib/server/db/schema';
import { getUserLocation } from '$lib/server/location';
import { distanceVerdict, type DistanceVerdict, type LatLng } from '$lib/post-distance';
import { liveCondition } from '$lib/server/postups';

export interface LivePostup {
	id: number;
	place: string;
	until: string;
}

/** The account's one live postup, if it has one. [M1039] */
export async function livePostupFor(userId: string): Promise<LivePostup | null> {
	const [row] = await db
		.select({ id: post.id, location: post.location, endsAt: post.endsAt, startTime: post.startTime, hours: post.hours })
		.from(post)
		.where(and(eq(post.userId, userId), liveCondition))
		.limit(1);
	if (!row) return null;
	const until = row.endsAt ?? new Date(row.startTime.getTime() + row.hours * 3600_000);
	return { id: row.id, place: row.location, until: until.toISOString() };
}

/**
 * Browser coords win. An explicit denial blocks the post.
 * A request that never asked (tests, no-JS) falls back to the server guess. [M1039]
 */
export async function checkPostSpot(event: RequestEvent, place: LatLng, form: FormData): Promise<DistanceVerdict> {
	const denied = form.get('hereDenied') === '1';
	const lat = Number(form.get('hereLat'));
	const lng = Number(form.get('hereLng'));
	let here: LatLng | null = Number.isFinite(lat) && Number.isFinite(lng) ? { latitude: lat, longitude: lng } : null;
	if (!here && !denied) {
		const got = await getUserLocation(event);
		here = { latitude: got.location.latitude, longitude: got.location.longitude };
	}
	return distanceVerdict(denied ? null : here, place, { denied });
}
