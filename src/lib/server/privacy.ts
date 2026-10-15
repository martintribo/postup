import { and, eq, inArray } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { joinRequest, type Post } from '$lib/server/db/schema';
import { config } from '$lib/config';

/** Snap to a ~1.5 km grid cell centre so a marker shows the area, not the cafe. */
export function fuzz(lat: number, lng: number, cell = 0.015) {
	const snap = (v: number) => Math.floor(v / cell) * cell + cell / 2;
	return { latitude: Number(snap(lat).toFixed(5)), longitude: Number(snap(lng).toFixed(5)) };
}

/**
 * D2: for ask-to-join postups, viewers who are neither the poster nor approved get the
 * neighborhood and a fuzzed point instead of the cafe name, place id and exact coordinates.
 */
export async function sanitizePosts<T extends Post>(posts: T[], viewerId: string | null | undefined): Promise<(T & { cafeHidden?: boolean })[]> {
	if (!config.askHidesCafe) return posts;
	const askIds = posts.filter((p) => p.joinMode === 'ask' && p.userId !== viewerId).map((p) => p.id);
	if (!askIds.length) return posts;
	const approved = new Set<number>();
	if (viewerId) {
		const rows = await db
			.select({ postId: joinRequest.postId })
			.from(joinRequest)
			.where(and(eq(joinRequest.userId, viewerId), eq(joinRequest.status, 'approved'), inArray(joinRequest.postId, askIds)));
		rows.forEach((r) => approved.add(r.postId));
	}
	return posts.map((p) => {
		if (!askIds.includes(p.id) || approved.has(p.id)) return p;
		return { ...p, ...fuzz(p.latitude, p.longitude), location: `a cafe in ${p.neighborhood || p.locality || 'the area'}`, placeId: null, cafeHidden: true };
	});
}
