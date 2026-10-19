import { fail, redirect } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { project } from '$lib/server/db/schema';
import { saveImage } from '$lib/server/uploads';
import type { Actions, PageServerLoad } from './$types';

const KINDS = ['software', 'game', 'art', 'other'];

export const load: PageServerLoad = async ({ locals, url }) => {
	// Signed out keeps the form up; Create opens the sign-in sheet (mockup #project-new).
	return { title: 'New project', back: url.searchParams.get('back'), signedIn: !!locals.user };
};

export const actions: Actions = {
	default: async ({ request, locals, url }) => {
		if (!locals.user) return fail(401, { message: 'Sign in to create a project', name: '', short: '', type: 'other' });
		const f = await request.formData();
		const name = String(f.get('name') ?? '').trim();
		const type = KINDS.includes(String(f.get('type'))) ? String(f.get('type')) : 'other';
		const short = String(f.get('short') ?? '').trim();
		if (!name) return fail(400, { message: 'Give your project a name', name, short, type });
		if (name.length > 80) return fail(400, { message: 'Keep the name under 80 characters', name, short, type });
		let cover: string | null = null;
		try {
			cover = await saveImage(f.get('cover'), 'projects');
		} catch (e) {
			return fail(400, { message: (e as Error).message, name, short, type });
		}
		const [created] = await db
			.insert(project)
			.values({ name, type, shortDescription: short, description: cover ? `![cover](${cover})\n\n${short}` : short, userId: locals.user.id })
			.returning();
		const back = url.searchParams.get('back');
		if (back === 'post') redirect(303, `/post?project=${created.id}`);
		redirect(303, `/projects/${created.id}`);
	}
};
