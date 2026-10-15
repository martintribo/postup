import { error, fail, redirect } from '@sveltejs/kit';
import { eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { project, projectStatus } from '$lib/server/db/schema';
import { saveImage } from '$lib/server/uploads';
import type { Actions, PageServerLoad } from './$types';

async function own(id: number, userId: string | undefined) {
	const [p] = await db.select({ id: project.id, name: project.name, userId: project.userId }).from(project).where(eq(project.id, id));
	if (!p) error(404, 'Project not found');
	if (p.userId !== userId) error(403, 'Only the owner can post updates');
	return p;
}

export const load: PageServerLoad = async ({ params, locals, url }) => {
	if (!locals.user) redirect(302, `/login?next=${encodeURIComponent(url.pathname)}`);
	const p = await own(Number(params.id), locals.user.id);
	return { title: `Update · ${p.name}`, project: p };
};

export const actions: Actions = {
	default: async ({ params, request, locals }) => {
		if (!locals.user) return fail(401, { message: 'Sign in to post an update', title: '', notes: '' });
		const p = await own(Number(params.id), locals.user.id);
		const f = await request.formData();
		const title = String(f.get('title') ?? '').trim();
		const notes = String(f.get('notes') ?? '').trim();
		if (!title && !notes) return fail(400, { message: 'Add a title or a note', title, notes });
		let img: string | null = null;
		try {
			img = await saveImage(f.get('image'), 'updates');
		} catch (e) {
			return fail(400, { message: (e as Error).message, title, notes });
		}
		const body = [notes, img ? `![](${img})` : ''].filter(Boolean).join('\n\n');
		const now = new Date();
		await db.insert(projectStatus).values({ projectId: p.id, title: title || null, body, occurredAt: now });
		await db.update(project).set({ updatedAt: now }).where(eq(project.id, p.id));
		redirect(303, `/projects/${p.id}`);
	}
};
