import { flag } from '$lib/flags';
import { availableProviders } from '$lib/server/oauth';
import { db } from '$lib/server/db';
import { notification } from '$lib/server/db/schema';
import { and, eq, isNull, sql } from 'drizzle-orm';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async (event) => {
	const user = event.locals.user;
	let unread = 0;
	if (user) {
		try {
			const [r] = await db.select({ n: sql<number>`count(*)::int` }).from(notification).where(and(eq(notification.userId, user.id), isNull(notification.readAt)));
			unread = r?.n ?? 0;
		} catch {
			unread = 0;
		}
	}
	return {
		user,
		unreadInbox: unread,
		providers: flag('oauth') ? availableProviders(event.url.origin) : []
	};
};
