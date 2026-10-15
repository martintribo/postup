import { and, eq, inArray, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { joinRequest, user } from '$lib/server/db/schema';
import { getPostup } from '$lib/server/postup-manage';
import { notify } from '$lib/server/notify';
import { isBlockedBetween } from '$lib/server/safety';

export class JoinError extends Error {
	constructor(public status: number, msg: string) {
		super(msg);
	}
}

const ACTIVE = ['pending', 'approved'] as const;

export async function myRequest(postId: number, userId: string) {
	const [r] = await db
		.select()
		.from(joinRequest)
		.where(and(eq(joinRequest.postId, postId), eq(joinRequest.userId, userId)))
		.orderBy(sql`${joinRequest.createdAt} desc`)
		.limit(1);
	return r ?? null;
}

export async function approvedCount(postId: number) {
	const [r] = await db.select({ n: sql<number>`count(*)::int` }).from(joinRequest).where(and(eq(joinRequest.postId, postId), eq(joinRequest.status, 'approved')));
	return r?.n ?? 0;
}

export async function listRequests(postId: number) {
	return db
		.select({ id: joinRequest.id, userId: joinRequest.userId, name: sql<string>`coalesce(${user.displayName}, ${user.username})`, avatarUrl: user.avatarUrl, reason: joinRequest.reason, status: joinRequest.status, createdAt: joinRequest.createdAt })
		.from(joinRequest)
		.innerJoin(user, eq(joinRequest.userId, user.id))
		.where(and(eq(joinRequest.postId, postId), inArray(joinRequest.status, [...ACTIVE])))
		.orderBy(joinRequest.createdAt);
}

async function nameOf(userId: string) {
	const [u] = await db.select({ n: sql<string>`coalesce(${user.displayName}, ${user.username})` }).from(user).where(eq(user.id, userId));
	return u?.n ?? 'Someone';
}

/** Join (open) or ask to join (ask mode, reason required). The poster is always alerted. */
export async function requestJoin(postId: number, userId: string, reason?: string | null) {
	const p = await getPostup(postId);
	if (!p) throw new JoinError(404, 'Postup not found');
	if (p.state !== 'live') throw new JoinError(409, 'This postup has ended');
	if (p.userId === userId) throw new JoinError(400, "That's your postup");
	if (!p.userId) throw new JoinError(409, 'This postup was posted anonymously and cannot be joined');
	if (await isBlockedBetween(p.userId, userId)) throw new JoinError(403, "You can't join this postup");
	const existing = await myRequest(postId, userId);
	if (existing && (ACTIVE as readonly string[]).includes(existing.status)) return existing;
	if (existing?.status === 'removed') throw new JoinError(403, 'You were removed from this postup');
	if (p.capacity && (await approvedCount(postId)) >= p.capacity) throw new JoinError(409, 'This postup is full');

	const who = await nameOf(userId);
	if (p.joinMode === 'ask') {
		const why = (reason ?? '').trim();
		if (!why) throw new JoinError(400, 'Add a short note about why you want to join');
		const [r] = await db.insert(joinRequest).values({ postId, userId, reason: why.slice(0, 280), status: 'pending' }).returning();
		await notify({ userId: p.userId, type: 'join_request', postId, actorId: userId, body: `${who} asked to join: “${why.slice(0, 120)}”` });
		return r;
	}
	const [r] = await db.insert(joinRequest).values({ postId, userId, reason: reason?.trim() || null, status: 'approved', decidedAt: new Date() }).returning();
	await notify({ userId: p.userId, type: 'joined', postId, actorId: userId, body: `${who} is joining you at ${p.placeName || p.location}` });
	return r;
}

/** Owner decides on a request, or removes someone who joined. */
export async function decide(postId: number, requestId: number, ownerId: string, action: 'approve' | 'decline' | 'remove') {
	const p = await getPostup(postId);
	if (!p) throw new JoinError(404, 'Postup not found');
	if (p.userId !== ownerId) throw new JoinError(403, 'Only the poster can do that');
	const [r] = await db.select().from(joinRequest).where(and(eq(joinRequest.id, requestId), eq(joinRequest.postId, postId)));
	if (!r) throw new JoinError(404, 'Request not found');
	if (action === 'approve') {
		if (r.status !== 'pending') throw new JoinError(409, 'Already decided');
		if (p.capacity && (await approvedCount(postId)) >= p.capacity) throw new JoinError(409, 'This postup is full');
	}
	if (action === 'decline' && r.status !== 'pending') throw new JoinError(409, 'Already decided');
	if (action === 'remove' && r.status !== 'approved') throw new JoinError(409, 'Not joined');
	const status = action === 'approve' ? 'approved' : action === 'decline' ? 'declined' : 'removed';
	await db.update(joinRequest).set({ status, decidedAt: new Date() }).where(eq(joinRequest.id, requestId));
	const cafe = p.placeName || p.location;
	const body = action === 'approve' ? `You're in! Meet ${p.displayName || p.name} at ${cafe}` : action === 'decline' ? `Your request to join ${p.displayName || p.name} wasn't accepted this time` : `You were removed from ${p.displayName || p.name}'s postup`;
	await notify({ userId: r.userId, type: status, postId, actorId: ownerId, body });
	return { ...r, status };
}

export async function leave(postId: number, userId: string) {
	const r = await myRequest(postId, userId);
	if (!r || !(ACTIVE as readonly string[]).includes(r.status)) throw new JoinError(409, 'You are not in this postup');
	await db.update(joinRequest).set({ status: 'left', decidedAt: new Date() }).where(eq(joinRequest.id, r.id));
	const p = await getPostup(postId);
	if (p?.userId) await notify({ userId: p.userId, type: 'left', postId, actorId: userId, body: `${await nameOf(userId)} can't make it anymore` });
}
