import type { PageServerLoad } from './$types';
import { db } from '$lib/server/db';
import { project, projectChange, projectStatus } from '$lib/server/db/schema';
import { and, desc, eq, inArray } from 'drizzle-orm';

export const load: PageServerLoad = async ({ locals }) => {
	const projects = await db.select().from(project).orderBy(desc(project.createdAt));

	const statusesByProject = new Map<number, typeof projectStatus.$inferSelect[]>();
	if (projects.length > 0) {
		const rows = await db
			.select()
			.from(projectStatus)
			.where(inArray(projectStatus.projectId, projects.map((p) => p.id)))
			.orderBy(desc(projectStatus.occurredAt));
		for (const row of rows) {
			const list = statusesByProject.get(row.projectId) ?? [];
			list.push(row);
			statusesByProject.set(row.projectId, list);
		}
	}

	const projectsWithStatuses = projects.map((p) => ({
		...p,
		statuses: statusesByProject.get(p.id) ?? []
	}));

	const pendingChanges = locals.user
		? await db
				.select()
				.from(projectChange)
				.where(
					and(eq(projectChange.userId, locals.user.id), eq(projectChange.status, 'pending'))
				)
				.orderBy(desc(projectChange.createdAt))
		: [];

	return {
		projects: projectsWithStatuses,
		pendingChanges
	};
};
