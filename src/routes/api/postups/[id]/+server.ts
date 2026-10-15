import { json } from '@sveltejs/kit';
import { getPostup, managePostup, ManageError, type ManageAction } from '$lib/server/postup-manage';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const p = await getPostup(Number(params.id));
	if (!p) return json({ error: 'Not found' }, { status: 404 });
	return json({ postup: p });
};

export const PATCH: RequestHandler = async ({ params, locals, request }) => {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const body = (await request.json().catch(() => null)) as ManageAction | null;
	if (!body || typeof body !== 'object') return json({ error: 'Body must be JSON' }, { status: 400 });
	try {
		return json({ postup: await managePostup(Number(params.id), locals.user.id, body) });
	} catch (e) {
		if (e instanceof ManageError) return json({ error: e.message }, { status: e.status });
		throw e;
	}
};
