import { desc, eq } from 'drizzle-orm';
import { alias } from 'drizzle-orm/pg-core';
import { db } from '$lib/server/db';
import { notification, user } from '$lib/server/db/schema';
import type { PageServerLoad } from './$types';

/** Mockup #activity: requests, joins, "said yes", messages, follows. Signed out keeps the screen (sheet over it). */
export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user) return { title: 'Activity', signedIn: false, items: [] };
	const actor = alias(user, 'actor');
	const items = await db
		.select({ id: notification.id, type: notification.type, postId: notification.postId, body: notification.body, createdAt: notification.createdAt, readAt: notification.readAt, actorName: actor.displayName, actorUsername: actor.username, actorAvatar: actor.avatarUrl })
		.from(notification)
		.leftJoin(actor, eq(notification.actorId, actor.id))
		.where(eq(notification.userId, locals.user.id))
		.orderBy(desc(notification.createdAt))
		.limit(50);
	return { title: 'Activity', signedIn: true, items: items.map((n) => ({ ...n, actor: n.actorName || n.actorUsername, createdAt: n.createdAt.toISOString(), readAt: n.readAt?.toISOString() ?? null })) };
};
