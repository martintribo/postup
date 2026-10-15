import { redirect } from '@sveltejs/kit';
import { desc, eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { notification } from '$lib/server/db/schema';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user) redirect(302, `/login?next=${encodeURIComponent(url.pathname)}`);
	const items = await db.select().from(notification).where(eq(notification.userId, locals.user.id)).orderBy(desc(notification.createdAt)).limit(50);
	return { title: 'Activity', items: items.map((n) => ({ ...n, createdAt: n.createdAt.toISOString(), readAt: n.readAt?.toISOString() ?? null })) };
};
