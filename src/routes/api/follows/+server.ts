import { json } from '@sveltejs/kit';
import { setFollow } from '$lib/server/profile';
import type { RequestHandler } from './$types';

async function handle(locals: App.Locals, request: Request, on: boolean) {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const { targetType, targetId } = await request.json().catch(() => ({}));
	if (targetType !== 'user' && targetType !== 'project') return json({ error: 'targetType must be user or project' }, { status: 400 });
	try {
		await setFollow(locals.user.id, targetType, String(targetId), on);
	} catch (e) {
		return json({ error: (e as Error).message }, { status: 400 });
	}
	return json({ ok: true, following: on });
}
export const POST: RequestHandler = ({ locals, request }) => handle(locals, request, true);
export const DELETE: RequestHandler = ({ locals, request }) => handle(locals, request, false);
