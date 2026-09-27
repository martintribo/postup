import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { project, projectChange } from '$lib/server/db/schema';
import { and, eq } from 'drizzle-orm';

export const POST: RequestHandler = async ({ locals, params, request }) => {
	if (!locals.agent) {
		return json({ error: 'Invalid or missing agent token' }, { status: 401 });
	}
	if (locals.agent.scope !== 'status') {
		return json({ error: 'Token does not have status scope' }, { status: 403 });
	}

	const id = Number(params.id);
	if (!Number.isInteger(id) || id <= 0) {
		return json({ error: 'Invalid project id' }, { status: 400 });
	}

	const [target] = await db
		.select({ id: project.id })
		.from(project)
		.where(and(eq(project.id, id), eq(project.userId, locals.agent.userId)));
	if (!target) {
		return json({ error: 'Project not found or not owned by user' }, { status: 404 });
	}

	const body = await request.json().catch(() => null);
	if (!body || typeof body !== 'object') {
		return json({ error: 'Body must be JSON' }, { status: 400 });
	}

	const text = typeof body.body === 'string' ? body.body.trim() : '';
	if (!text) {
		return json({ error: 'body (text) is required' }, { status: 400 });
	}
	const title = typeof body.title === 'string' ? body.title.trim() : '';

	const occurredAtRaw = typeof body.occurredAt === 'string' ? body.occurredAt : '';
	const occurredAt = occurredAtRaw ? new Date(occurredAtRaw) : new Date();
	if (Number.isNaN(occurredAt.getTime())) {
		return json({ error: 'occurredAt must be an ISO 8601 timestamp' }, { status: 400 });
	}

	const [change] = await db
		.insert(projectChange)
		.values({
			userId: locals.agent.userId,
			agentSessionId: locals.agent.agentSessionId,
			action: 'status_update',
			targetProjectId: id,
			payload: {
				title: title || null,
				body: text,
				occurredAt: occurredAt.toISOString()
			}
		})
		.returning();

	return json({ change, status: 'pending' }, { status: 202 });
};
