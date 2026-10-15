import { json } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { decide, JoinError } from '$lib/server/join';
import type { RequestHandler } from './$types';

export const PATCH: RequestHandler = async ({ params, locals, request }) => {
	if (!flag('join')) return json({ error: 'Not found' }, { status: 404 });
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const body = await request.json().catch(() => ({}));
	if (!['approve', 'decline', 'remove'].includes(body?.action)) return json({ error: 'action must be approve, decline or remove' }, { status: 400 });
	try {
		return json({ request: await decide(Number(params.id), Number(params.rid), locals.user.id, body.action) });
	} catch (e) {
		if (e instanceof JoinError) return json({ error: e.message }, { status: e.status });
		throw e;
	}
};
