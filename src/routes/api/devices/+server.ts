import { json } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { deviceToken } from '$lib/server/db/schema';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ locals, request }) => {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const { token, platform } = await request.json().catch(() => ({}));
	if (typeof token !== 'string' || !token || !['ios', 'android'].includes(platform)) return json({ error: 'token and platform required' }, { status: 400 });
	await db
		.insert(deviceToken)
		.values({ token, platform, userId: locals.user.id })
		.onConflictDoUpdate({ target: deviceToken.token, set: { userId: locals.user.id, lastSeenAt: new Date() } });
	return json({ ok: true });
};
