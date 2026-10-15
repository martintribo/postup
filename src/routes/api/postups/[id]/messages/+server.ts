import { json } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { listMessages, sendMessage, ChatError } from '$lib/server/chat';
import type { RequestHandler } from './$types';

async function guard(locals: App.Locals, fn: (uid: string) => Promise<Response>) {
	if (!flag('chat')) return json({ error: 'Not found' }, { status: 404 });
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	try {
		return await fn(locals.user.id);
	} catch (e) {
		if (e instanceof ChatError) return json({ error: e.message }, { status: e.status });
		throw e;
	}
}

/** Polling endpoint (?after=<id>); SSE/realtime can replace it without changing the client contract. */
export const GET: RequestHandler = ({ params, locals, url }) =>
	guard(locals, async (uid) => json(await listMessages(Number(params.id), uid, Number(url.searchParams.get('after') || 0))));

export const POST: RequestHandler = ({ params, locals, request }) =>
	guard(locals, async (uid) => {
		const body = await request.json().catch(() => ({}));
		return json({ message: await sendMessage(Number(params.id), uid, body?.body) }, { status: 201 });
	});
