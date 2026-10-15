import { error } from '@sveltejs/kit';
import { and, desc, eq, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { project, projectStatus, user, post } from '$lib/server/db/schema';
import { liveCondition } from '$lib/server/postups';
import type { PageServerLoad } from './$types';

/** Project page + shared-project landing (mockups #project, #invite-project). */
export const load: PageServerLoad = async ({ params }) => {
	const id = Number(params.id);
	const [p] = await db
		.select({ id: project.id, name: project.name, short: project.shortDescription, description: project.description, hidden: project.hidden, owner: sql<string | null>`coalesce(${user.displayName}, ${user.username})` })
		.from(project)
		.leftJoin(user, eq(project.userId, user.id))
		.where(eq(project.id, id));
	if (!p || p.hidden) error(404, 'Project not found');
	const updates = await db.select().from(projectStatus).where(eq(projectStatus.projectId, id)).orderBy(desc(projectStatus.occurredAt)).limit(20);
	const [live] = await db.select({ id: post.id }).from(post).where(and(eq(post.projectId, id), liveCondition)).limit(1);
	return {
		title: p.owner ? `${p.owner} is building ${p.name}` : p.name,
		description: p.short || 'A project on PostUp',
		project: p,
		liveId: live?.id ?? null,
		updates: updates.map((u) => ({ id: u.id, title: u.title, body: u.body, at: u.occurredAt.toISOString() }))
	};
};
