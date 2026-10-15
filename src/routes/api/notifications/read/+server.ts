import { json } from '@sveltejs/kit';
import { and, eq, isNull } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { notification } from '$lib/server/db/schema';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ locals }) => {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	await db.update(notification).set({ readAt: new Date() }).where(and(eq(notification.userId, locals.user.id), isNull(notification.readAt)));
	return json({ ok: true });
};
