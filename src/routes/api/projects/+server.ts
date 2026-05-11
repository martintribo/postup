import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { project } from '$lib/server/db/schema';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.user) {
		return json({ error: 'Must be logged in' }, { status: 401 });
	}

	const body = await request.json();
	const name = body.name?.trim();
	const type = body.type || 'software';
	const shortDescription = body.shortDescription?.trim() || '';
	const description = body.description?.trim() || '';

	if (!name) {
		return json({ error: 'Name is required' }, { status: 400 });
	}

	const [created] = await db.insert(project).values({
		name,
		type,
		shortDescription: shortDescription || name,
		description: description || shortDescription || name,
		userId: locals.user.id
	}).returning();

	return json({ project: created });
};
