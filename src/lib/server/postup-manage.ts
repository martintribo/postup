import { and, eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { post, place, project, user } from '$lib/server/db/schema';

export type PostupView = Awaited<ReturnType<typeof getPostup>>;

export async function getPostup(id: number) {
	const [row] = await db
		.select({
			id: post.id,
			userId: post.userId,
			name: post.name,
			displayName: user.displayName,
			avatarUrl: user.avatarUrl,
			activity: post.activity,
			goals: post.goals,
			note: post.note,
			location: post.location,
			placeId: post.placeId,
			placeName: place.name,
			latitude: post.latitude,
			longitude: post.longitude,
			startTime: post.startTime,
			endsAt: post.endsAt,
			hours: post.hours,
			status: post.status,
			joinMode: post.joinMode,
			capacity: post.capacity,
			projectId: post.projectId,
			projectName: project.name
		})
		.from(post)
		.leftJoin(user, eq(post.userId, user.id))
		.leftJoin(place, eq(post.placeId, place.id))
		.leftJoin(project, eq(post.projectId, project.id))
		.where(eq(post.id, id));
	if (!row) return null;
	const endsAt = row.endsAt ?? new Date(row.startTime.getTime() + row.hours * 3600_000);
	const effective = row.status === 'live' && endsAt.getTime() <= Date.now() ? 'ended' : row.status;
	return { ...row, endsAt, state: effective as 'live' | 'ended' | 'cancelled' };
}

export type ManageAction =
	| { action: 'extend'; hours: number }
	| { action: 'end' }
	| { action: 'cancel' }
	| { action: 'edit'; activity?: string; note?: string | null; joinMode?: 'open' | 'ask'; capacity?: number | null };

export class ManageError extends Error {
	constructor(public status: number, msg: string) {
		super(msg);
	}
}

const MAX_HOURS = 12;

/** Owner-only changes to a postup. Returns the updated view. */
export async function managePostup(id: number, userId: string, a: ManageAction) {
	const p = await getPostup(id);
	if (!p) throw new ManageError(404, 'Postup not found');
	if (p.userId !== userId) throw new ManageError(403, 'Only the person who posted can change this');
	if (p.state !== 'live') throw new ManageError(409, `This postup has ${p.state === 'cancelled' ? 'been cancelled' : 'ended'}`);

	if (a.action === 'extend') {
		const h = Math.trunc(a.hours);
		if (!(h >= 1 && h <= 4)) throw new ManageError(400, 'Extend by 1 to 4 hours');
		const endsAt = new Date(p.endsAt.getTime() + h * 3600_000);
		if (endsAt.getTime() - p.startTime.getTime() > MAX_HOURS * 3600_000) throw new ManageError(400, `Postups can last at most ${MAX_HOURS} hours`);
		await db.update(post).set({ endsAt }).where(eq(post.id, id));
	} else if (a.action === 'end') {
		await db.update(post).set({ status: 'ended', endsAt: new Date() }).where(eq(post.id, id));
	} else if (a.action === 'cancel') {
		await db.update(post).set({ status: 'cancelled' }).where(eq(post.id, id));
	} else if (a.action === 'edit') {
		const set: Partial<typeof post.$inferInsert> = {};
		if (typeof a.activity === 'string') {
			const t = a.activity.trim();
			if (!t || t.length > 140) throw new ManageError(400, 'Say what you are working on (up to 140 characters)');
			set.activity = t;
		}
		if (a.note !== undefined) set.note = a.note?.trim().slice(0, 280) || null;
		if (a.joinMode) {
			if (a.joinMode !== 'open' && a.joinMode !== 'ask') throw new ManageError(400, 'Bad join mode');
			set.joinMode = a.joinMode;
		}
		if (a.capacity !== undefined) {
			if (a.capacity !== null && !(Number.isInteger(a.capacity) && a.capacity >= 1 && a.capacity <= 20)) throw new ManageError(400, 'Capacity is 1–20 or none');
			set.capacity = a.capacity;
		}
		if (Object.keys(set).length) await db.update(post).set(set).where(and(eq(post.id, id)));
	} else {
		throw new ManageError(400, 'Unknown action');
	}
	return getPostup(id);
}

export function minutesLeft(endsAt: Date, now = Date.now()) {
	return Math.max(0, Math.round((endsAt.getTime() - now) / 60000));
}
