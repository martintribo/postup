import { and, desc, eq, or, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { block, chatRead, deviceToken, follow, joinRequest, message, notification, oauthAccount, place, post, project, session, user } from '$lib/server/db/schema';

export async function getProfile(username: string) {
	const [u] = await db.select().from(user).where(eq(user.username, username));
	if (!u || u.deletedAt) return null;
	const projects = await db.select({ id: project.id, name: project.name, short: project.shortDescription, updatedAt: project.updatedAt }).from(project).where(and(eq(project.userId, u.id), eq(project.hidden, false))).orderBy(desc(project.updatedAt));
	// Past/live postups: ask-mode ones show the area only (D2 consistency).
	const posts = await db
		.select({ id: post.id, activity: post.activity, location: post.location, neighborhood: post.neighborhood, joinMode: post.joinMode, startTime: post.startTime, endsAt: post.endsAt, hours: post.hours, status: post.status, placeId: post.placeId, placeName: place.name, projectName: project.name })
		.from(post)
		.leftJoin(place, eq(post.placeId, place.id))
		.leftJoin(project, eq(post.projectId, project.id))
		.where(and(eq(post.userId, u.id), sql`${post.status} <> 'cancelled'`))
		.orderBy(desc(post.startTime))
		.limit(40);
	const [f] = await db.select({ n: sql<number>`count(*)::int` }).from(follow).where(and(eq(follow.targetType, 'user'), eq(follow.targetId, u.id)));
	const [c] = await db.select({ n: sql<number>`count(*)::int` }).from(post).where(and(eq(post.userId, u.id), sql`${post.status} <> 'cancelled'`));
	const now = Date.now();
	const end = (p: (typeof posts)[number]) => p.endsAt ?? new Date(p.startTime.getTime() + p.hours * 3600e3);
	const hide = (p: (typeof posts)[number]) => p.joinMode === 'ask';
	const liveRow = posts.find((p) => p.status === 'live' && end(p).getTime() > now);
	// Regular cafes: the open-mode cafes they post up at most (ask-mode cafes stay private).
	const counts = new Map<number, { id: number; name: string; n: number }>();
	for (const p of posts) if (p.placeId && p.placeName && !hide(p)) counts.set(p.placeId, { id: p.placeId, name: p.placeName, n: (counts.get(p.placeId)?.n ?? 0) + 1 });
	return {
		id: u.id,
		username: u.username,
		name: u.displayName || u.username,
		bio: u.bio,
		avatarUrl: u.avatarUrl,
		since: u.createdAt?.toISOString() ?? null,
		followers: f?.n ?? 0,
		postCount: c?.n ?? 0,
		live: liveRow ? { id: liveRow.id, cafe: hide(liveRow) ? `a cafe in ${liveRow.neighborhood || 'the area'}` : liveRow.placeName || liveRow.location, endsAt: end(liveRow).toISOString(), startTime: liveRow.startTime.toISOString(), project: liveRow.projectName } : null,
		cafes: [...counts.values()].sort((a, b) => b.n - a.n).slice(0, 4),
		projects: projects.map((p) => ({ id: p.id, name: p.name, short: p.short, updatedAt: p.updatedAt.toISOString() })),
		posts: posts
			.filter((p) => p !== liveRow)
			.slice(0, 20)
			.map((p) => ({ id: p.id, activity: p.activity, where: hide(p) ? `a cafe in ${p.neighborhood || 'the area'}` : p.placeName || p.location, placeId: hide(p) ? null : p.placeId, at: p.startTime.toISOString() }))
	};
}

export async function isFollowing(followerId: string, targetType: 'user' | 'project', targetId: string) {
	const [r] = await db.select().from(follow).where(and(eq(follow.followerId, followerId), eq(follow.targetType, targetType), eq(follow.targetId, targetId)));
	return !!r;
}

export async function setFollow(followerId: string, targetType: 'user' | 'project', targetId: string, on: boolean) {
	if (targetType === 'user' && targetId === followerId) throw new Error("You can't follow yourself");
	if (on) {
		const added = await db.insert(follow).values({ followerId, targetType, targetId }).onConflictDoNothing().returning();
		// Mockup #activity: "Ari followed you".
		if (added.length && targetType === 'user') {
			const [me] = await db.select({ n: sql<string>`coalesce(${user.displayName}, ${user.username})` }).from(user).where(eq(user.id, followerId));
			const { notify } = await import('$lib/server/notify');
			await notify({ userId: targetId, type: 'followed', actorId: followerId, body: `${me?.n ?? 'Someone'} followed you` });
		}
	}
	else await db.delete(follow).where(and(eq(follow.followerId, followerId), eq(follow.targetType, targetType), eq(follow.targetId, targetId)));
}

export async function updateSettings(userId: string, s: { displayName?: string; bio?: string }) {
	const set: Partial<typeof user.$inferInsert> = {};
	if (s.displayName !== undefined) {
		const n = s.displayName.trim();
		if (!n || n.length > 50) throw new Error('Name is 1–50 characters');
		set.displayName = n;
	}
	if (s.bio !== undefined) set.bio = s.bio.trim().slice(0, 300) || null;
	if (Object.keys(set).length) await db.update(user).set(set).where(eq(user.id, userId));
}

/**
 * Delete account (App Store 5.1.1(v)): ends live postups, removes sign-ins, sessions, devices,
 * follows, blocks, notifications, join requests and chat messages, and wipes profile fields.
 * The user row stays as a tombstone so foreign keys on old postups/projects keep working.
 */
export async function deleteAccount(userId: string) {
	await db.update(post).set({ status: 'cancelled' }).where(and(eq(post.userId, userId), eq(post.status, 'live')));
	await db.update(project).set({ hidden: true }).where(eq(project.userId, userId));
	await db.update(message).set({ deletedAt: new Date(), body: '' }).where(eq(message.userId, userId));
	await db.delete(chatRead).where(eq(chatRead.userId, userId));
	await db.delete(joinRequest).where(eq(joinRequest.userId, userId));
	await db.delete(notification).where(or(eq(notification.userId, userId), eq(notification.actorId, userId)));
	await db.delete(follow).where(or(eq(follow.followerId, userId), and(eq(follow.targetType, 'user'), eq(follow.targetId, userId))));
	await db.delete(block).where(or(eq(block.blockerId, userId), eq(block.blockedId, userId)));
	await db.delete(deviceToken).where(eq(deviceToken.userId, userId));
	await db.delete(oauthAccount).where(eq(oauthAccount.userId, userId));
	await db.delete(session).where(eq(session.userId, userId));
	await db
		.update(user)
		.set({ username: `deleted-${userId.slice(0, 10)}`, passwordHash: null, displayName: 'Deleted user', avatarUrl: null, email: null, bio: null, deletedAt: new Date() })
		.where(eq(user.id, userId));
	await db.update(post).set({ name: 'Deleted user' }).where(eq(post.userId, userId));
}
