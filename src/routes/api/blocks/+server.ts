import { json } from '@sveltejs/kit';
import { blockUser, unblockUser } from '$lib/server/safety';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ locals, request }) => {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const { userId } = await request.json().catch(() => ({}));
	try {
		await blockUser(locals.user.id, String(userId));
		return json({ ok: true });
	} catch (e) {
		return json({ error: (e as Error).message }, { status: 400 });
	}
};

export const DELETE: RequestHandler = async ({ locals, request }) => {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const { userId } = await request.json().catch(() => ({}));
	await unblockUser(locals.user.id, String(userId));
	return json({ ok: true });
};
