import { json } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { requestJoin, leave, JoinError } from '$lib/server/join';
import type { RequestHandler } from './$types';

function wrap(fn: () => Promise<Response>) {
	return fn().catch((e) => {
		if (e instanceof JoinError) return json({ error: e.message }, { status: e.status });
		throw e;
	});
}

export const POST: RequestHandler = ({ params, locals, request }) =>
	wrap(async () => {
		if (!flag('join')) return json({ error: 'Not found' }, { status: 404 });
		if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
		const body = await request.json().catch(() => ({}));
		const r = await requestJoin(Number(params.id), locals.user.id, body?.reason);
		return json({ request: r });
	});

export const DELETE: RequestHandler = ({ params, locals }) =>
	wrap(async () => {
		if (!flag('join')) return json({ error: 'Not found' }, { status: 404 });
		if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
		await leave(Number(params.id), locals.user.id);
		return json({ ok: true });
	});
