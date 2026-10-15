import { error, fail } from '@sveltejs/kit';
import { desc, eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { report } from '$lib/server/db/schema';
import { isAdmin, resolveReport } from '$lib/server/safety';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
	if (!(await isAdmin(locals.user?.id))) error(404);
	const rows = await db.select().from(report).where(eq(report.status, 'open')).orderBy(desc(report.createdAt)).limit(100);
	return { title: 'Reports', reports: rows.map((r) => ({ ...r, createdAt: r.createdAt.toISOString(), resolvedAt: null })) };
};

export const actions: Actions = {
	default: async ({ locals, request }) => {
		if (!(await isAdmin(locals.user?.id))) error(404);
		const f = await request.formData();
		const id = Number(f.get('id'));
		const action = f.get('action');
		if (action !== 'hide' && action !== 'dismiss') return fail(400);
		await resolveReport(id, action);
		return { ok: true };
	}
};
