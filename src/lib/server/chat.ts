import { and, desc, eq, gt, inArray, isNull, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { chatRead, joinRequest, message, post, user } from '$lib/server/db/schema';
import { getPostup } from '$lib/server/postup-manage';
import { config } from '$lib/config';

export class ChatError extends Error {
	constructor(public status: number, msg: string) {
		super(msg);
	}
}

export function chatWindow(endsAt: Date, state: string, now = Date.now()) {
	const readableUntil = endsAt.getTime() + config.chatReadHours * 3600_000;
	return { canWrite: state === 'live', canRead: state !== 'cancelled' ? now < readableUntil : now < readableUntil, readableUntil: new Date(readableUntil) };
}

export async function isMember(postId: number, userId: string, ownerId: string | null) {
	if (ownerId === userId) return true;
	const [r] = await db
		.select({ id: joinRequest.id })
		.from(joinRequest)
		.where(and(eq(joinRequest.postId, postId), eq(joinRequest.userId, userId), eq(joinRequest.status, 'approved')));
	return !!r;
}

async function access(postId: number, userId: string) {
	const p = await getPostup(postId);
	if (!p) throw new ChatError(404, 'Postup not found');
	if (!(await isMember(postId, userId, p.userId))) throw new ChatError(403, 'Only people in this postup can see the chat');
	const w = chatWindow(p.endsAt, p.state);
	if (!w.canRead) throw new ChatError(410, 'This chat has closed');
	return { p, ...w };
}

export async function listMessages(postId: number, userId: string, afterId = 0) {
	const { p, canWrite, readableUntil } = await access(postId, userId);
	const rows = await db
		.select({ id: message.id, userId: message.userId, name: sql<string>`coalesce(${user.displayName}, ${user.username})`, avatarUrl: user.avatarUrl, body: message.body, createdAt: message.createdAt })
		.from(message)
		.innerJoin(user, eq(message.userId, user.id))
		.where(and(eq(message.postId, postId), gt(message.id, afterId), isNull(message.deletedAt)))
		.orderBy(message.id)
		.limit(200);
	const last = rows.at(-1)?.id;
	if (last) {
		await db
			.insert(chatRead)
			.values({ postId, userId, lastReadId: last })
			.onConflictDoUpdate({ target: [chatRead.postId, chatRead.userId], set: { lastReadId: sql`greatest(${chatRead.lastReadId}, ${last})` } });
	}
	return { messages: rows.map((m) => ({ ...m, createdAt: m.createdAt.toISOString() })), canWrite, readableUntil: readableUntil.toISOString(), postup: { id: p.id, activity: p.activity, state: p.state } };
}

export async function sendMessage(postId: number, userId: string, body: string) {
	const { canWrite } = await access(postId, userId);
	if (!canWrite) throw new ChatError(409, 'This postup has ended; the chat is read-only');
	const text = (body ?? '').trim();
	if (!text || text.length > 1000) throw new ChatError(400, 'Messages are 1–1000 characters');
	const [m] = await db.insert(message).values({ postId, userId, body: text }).returning();
	return m;
}

/** Inbox: chats I'm in that are still readable, newest activity first, with unread counts. */
export async function inbox(userId: string) {
	const joined = await db.select({ postId: joinRequest.postId }).from(joinRequest).where(and(eq(joinRequest.userId, userId), eq(joinRequest.status, 'approved')));
	const owned = await db.select({ postId: post.id }).from(post).where(eq(post.userId, userId));
	const ids = [...new Set([...joined, ...owned].map((r) => r.postId))];
	if (!ids.length) return [];
	const out = [];
	for (const id of ids) {
		const p = await getPostup(id);
		if (!p || !chatWindow(p.endsAt, p.state).canRead) continue;
		const [last] = await db.select({ body: message.body, createdAt: message.createdAt, id: message.id }).from(message).where(and(eq(message.postId, id), isNull(message.deletedAt))).orderBy(desc(message.id)).limit(1);
		const [rd] = await db.select({ lastReadId: chatRead.lastReadId }).from(chatRead).where(and(eq(chatRead.postId, id), eq(chatRead.userId, userId)));
		const [u] = await db
			.select({ n: sql<number>`count(*)::int` })
			.from(message)
			.where(and(eq(message.postId, id), gt(message.id, rd?.lastReadId ?? 0), isNull(message.deletedAt), sql`${message.userId} <> ${userId}`));
		out.push({
			postId: id,
			title: `${p.displayName || p.name} · ${p.activity}`,
			state: p.state,
			last: last ? { body: last.body, at: last.createdAt.toISOString() } : null,
			unread: u?.n ?? 0,
			sort: (last?.createdAt ?? p.startTime).getTime()
		});
	}
	return out.sort((a, b) => b.sort - a.sort);
}

export { inArray };
