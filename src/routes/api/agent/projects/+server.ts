import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { project, projectChange, projectStatus } from '$lib/server/db/schema';
import { and, desc, eq, inArray, max } from 'drizzle-orm';

const ALLOWED_TYPES = new Set(['software', 'art', 'writing', 'business', 'activities']);

export const GET: RequestHandler = async ({ locals }) => {
	if (!locals.agent) {
		return json({ error: 'Invalid or missing agent token' }, { status: 401 });
	}
	// Both scopes need to read the project list (status agents use lastStatusAt to choose dates).

	const [projects, pendingChanges] = await Promise.all([
		db
			.select()
			.from(project)
			.where(eq(project.userId, locals.agent.userId))
			.orderBy(desc(project.createdAt)),
		db
			.select()
			.from(projectChange)
			.where(
				and(
					eq(projectChange.agentSessionId, locals.agent.agentSessionId),
					eq(projectChange.status, 'pending')
				)
			)
			.orderBy(desc(projectChange.createdAt))
	]);

	const projectIds = projects.map((p) => p.id);
	const lastStatusByProject = new Map<number, string>();
	if (projectIds.length > 0) {
		const rows = await db
			.select({
				projectId: projectStatus.projectId,
				lastStatusAt: max(projectStatus.occurredAt)
			})
			.from(projectStatus)
			.where(inArray(projectStatus.projectId, projectIds))
			.groupBy(projectStatus.projectId);
		for (const row of rows) {
			if (row.lastStatusAt) {
				lastStatusByProject.set(
					row.projectId,
					new Date(row.lastStatusAt as unknown as string).toISOString()
				);
			}
		}
	}

	const projectsWithStatus = projects.map((p) => ({
		...p,
		lastStatusAt: lastStatusByProject.get(p.id) ?? null
	}));

	return json({ projects: projectsWithStatus, pendingChanges });
};

export const POST: RequestHandler = async ({ locals, request }) => {
	if (!locals.agent) {
		return json({ error: 'Invalid or missing agent token' }, { status: 401 });
	}
	if (locals.agent.scope !== 'projects') {
		return json({ error: 'Token does not have projects scope' }, { status: 403 });
	}

	const body = await request.json().catch(() => null);
	if (!body || typeof body !== 'object') {
		return json({ error: 'Body must be JSON' }, { status: 400 });
	}

	const name = typeof body.name === 'string' ? body.name.trim() : '';
	if (!name) {
		return json({ error: 'name is required' }, { status: 400 });
	}

	const type = typeof body.type === 'string' && ALLOWED_TYPES.has(body.type) ? body.type : 'software';
	const shortDescription =
		typeof body.shortDescription === 'string' ? body.shortDescription.trim() : '';
	const description = typeof body.description === 'string' ? body.description.trim() : '';

	const payload = {
		name,
		type,
		shortDescription: shortDescription || name,
		description: description || shortDescription || name
	};

	const [change] = await db
		.insert(projectChange)
		.values({
			userId: locals.agent.userId,
			agentSessionId: locals.agent.agentSessionId,
			action: 'create',
			targetProjectId: null,
			payload
		})
		.returning();

	return json({ change, status: 'pending' }, { status: 202 });
};
