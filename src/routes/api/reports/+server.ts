import { json } from '@sveltejs/kit';
import { fileReport } from '$lib/server/safety';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ locals, request }) => {
	if (!locals.user) return json({ error: 'Sign in first' }, { status: 401 });
	const b = await request.json().catch(() => ({}));
	try {
		const r = await fileReport({ reporterId: locals.user.id, targetType: b.targetType, targetId: String(b.targetId ?? ''), reason: b.reason, details: b.details });
		return json({ report: { id: r.id } }, { status: 201 });
	} catch (e) {
		return json({ error: (e as Error).message }, { status: 400 });
	}
};
