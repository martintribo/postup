import { sql, eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { post, place } from '$lib/server/db/schema';

/** A postup is live when status='live' and its end (ends_at, or legacy start+hours) is in the future. */
export const liveCondition = sql`${post.status} = 'live' AND coalesce(${post.endsAt}, ${post.startTime} + (${post.hours} || ' hours')::interval) > now()`;

export function computeEndsAt(start: Date, hours: number): Date {
	return new Date(start.getTime() + hours * 3600_000);
}

/** Find or create our place row for a Google place id (stores only id + coords + our label). */
export async function upsertGooglePlace(p: { googlePlaceId: string; name: string; latitude: number; longitude: number; address?: string }, userId?: string | null) {
	const [hit] = await db.select({ id: place.id }).from(place).where(eq(place.googlePlaceId, p.googlePlaceId));
	if (hit) return hit.id;
	const [row] = await db
		.insert(place)
		.values({ name: p.name, address: p.address ?? '', latitude: p.latitude, longitude: p.longitude, googlePlaceId: p.googlePlaceId, createdBy: userId ?? null, category: 'cafe' })
		.onConflictDoNothing()
		.returning();
	if (row) return row.id;
	const [again] = await db.select({ id: place.id }).from(place).where(eq(place.googlePlaceId, p.googlePlaceId));
	return again.id;
}
