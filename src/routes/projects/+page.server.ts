import type { PageServerLoad } from './$types';
import { db } from '$lib/server/db';
import { project } from '$lib/server/db/schema';
import { desc, eq } from 'drizzle-orm';

export const load: PageServerLoad = async () => {
	const projects = await db
		.select()
		.from(project)
		.where(eq(project.hidden, false))
		.orderBy(desc(project.createdAt));

	return {
		title: 'Projects',
		projects
	};
};
