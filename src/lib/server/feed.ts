import { sql, and, eq, desc, gt, inArray } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { post, place, project, projectStatus, user } from '$lib/server/db/schema';

export type FeedItem =
	| { kind: 'postup'; id: number; at: string; who: string; avatarUrl: string | null; activity: string; cafe: string; placeId: number | null; projectName: string | null; projectId: number | null; live: boolean }
	| { kind: 'update'; id: number; at: string; projectId: number; projectName: string; title: string | null; body: string };

const DAYS = 7;
const RADIUS_MI = 25;

/** Recent nearby activity for the Nearby feed (shown when nobody nearby is live). */
export async function getNearbyFeed(lat: number, lng: number, limit = 30): Promise<{ items: FeedItem[]; weekCount: number }> {
	const since = sql`now() - interval '${sql.raw(String(DAYS))} days'`;
	const dist = sql`(3959 * acos(least(1, cos(radians(${lat})) * cos(radians(${post.latitude})) * cos(radians(${post.longitude}) - radians(${lng})) + sin(radians(${lat})) * sin(radians(${post.latitude})))))`;
	const posts = await db
		.select({
			id: post.id,
			at: post.startTime,
			name: post.name,
			displayName: user.displayName,
			avatarUrl: user.avatarUrl,
			activity: post.activity,
			location: post.location,
			placeName: place.name,
			placeId: post.placeId,
			projectId: post.projectId,
			projectName: project.name,
			projectHidden: project.hidden,
			live: sql<boolean>`${post.status} = 'live' AND coalesce(${post.endsAt}, ${post.startTime} + (${post.hours} || ' hours')::interval) > now()`
		})
		.from(post)
		.leftJoin(user, eq(post.userId, user.id))
		.leftJoin(place, eq(post.placeId, place.id))
		.leftJoin(project, eq(post.projectId, project.id))
		.where(and(sql`${post.startTime} > ${since}`, sql`${post.status} <> 'cancelled'`, sql`${dist} <= ${RADIUS_MI}`))
		.orderBy(desc(post.startTime))
		.limit(limit);

	const projectIds = [...new Set(posts.map((p) => p.projectId).filter((x): x is number => !!x))];
	const updates = await db
		.select({ id: projectStatus.id, at: projectStatus.occurredAt, projectId: project.id, projectName: project.name, title: projectStatus.title, body: projectStatus.body })
		.from(projectStatus)
		.innerJoin(project, eq(projectStatus.projectId, project.id))
		.where(
			and(
				eq(project.hidden, false),
				gt(projectStatus.occurredAt, sql`${since}`),
				// Nearby = projects someone posted up for nearby; with no local projects yet, show recent public updates.
				projectIds.length ? inArray(project.id, projectIds) : sql`true`
			)
		)
		.orderBy(desc(projectStatus.occurredAt))
		.limit(limit);

	const items: FeedItem[] = [
		...posts.map((p) => ({
			kind: 'postup' as const,
			id: p.id,
			at: p.at.toISOString(),
			who: p.displayName || p.name,
			avatarUrl: p.avatarUrl,
			activity: p.activity,
			cafe: p.placeName || p.location,
			placeId: p.placeId,
			projectName: p.projectHidden ? null : p.projectName,
			projectId: p.projectHidden ? null : p.projectId,
			live: !!p.live
		})),
		...updates.map((u) => ({ kind: 'update' as const, id: u.id, at: u.at.toISOString(), projectId: u.projectId, projectName: u.projectName, title: u.title, body: u.body }))
	].sort((a, b) => b.at.localeCompare(a.at));

	return { items: items.slice(0, limit), weekCount: posts.length };
}

export function relTime(iso: string, now = Date.now()): string {
	const m = Math.round((now - new Date(iso).getTime()) / 60000);
	if (m < 60) return `${Math.max(m, 1)}m ago`;
	const h = Math.round(m / 60);
	if (h < 24) return h < 6 ? `${h}h ago` : 'earlier today';
	const d = Math.round(h / 24);
	return d === 1 ? 'yesterday' : `${d} days ago`;
}
