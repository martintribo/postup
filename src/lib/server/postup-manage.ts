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
			username: user.username,
			avatarUrl: user.avatarUrl,
			activity: post.activity,
			goals: post.goals,
			note: post.note,
			photoUrl: post.photoUrl,
			location: post.location,
			neighborhood: post.neighborhood,
			locality: post.locality,
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
	| { action: 'extend'; hours?: number; minutes?: number }
	| { action: 'end' }
	| { action: 'cancel' }
	| { action: 'edit'; activity?: string; note?: string | null; joinMode?: 'open' | 'ask'; capacity?: number | null; projectId?: number | null; placeId?: number; untilHours?: number };

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
		// Mockup #live: "+30 min". Hours (1–4) still work for the API.
		const mins = a.minutes != null ? Math.trunc(a.minutes) : Math.trunc(a.hours ?? 0) * 60;
		if (!(mins >= 15 && mins <= 240)) throw new ManageError(400, 'Extend by 15 minutes to 4 hours');
		const endsAt = new Date(p.endsAt.getTime() + mins * 60_000);
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
		if (a.projectId !== undefined) set.projectId = a.projectId;
		if (a.placeId !== undefined) {
			const [pl] = await db.select().from(place).where(eq(place.id, Number(a.placeId)));
			if (!pl) throw new ManageError(400, 'Unknown cafe');
			Object.assign(set, { placeId: pl.id, location: pl.name, latitude: pl.latitude, longitude: pl.longitude });
		}
		if (a.untilHours !== undefined) {
			const h = Math.trunc(a.untilHours);
			if (!(h >= 1 && h <= 4)) throw new ManageError(400, 'Until is 1 to 4 hours from now');
			set.endsAt = new Date(Date.now() + h * 3600_000);
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
