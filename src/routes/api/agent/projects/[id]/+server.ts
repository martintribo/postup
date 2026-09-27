import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { project, projectChange } from '$lib/server/db/schema';
import { and, eq } from 'drizzle-orm';

const ALLOWED_TYPES = new Set(['software', 'art', 'writing', 'business', 'activities']);

export const PATCH: RequestHandler = async ({ locals, params, request }) => {
	if (!locals.agent) {
		return json({ error: 'Invalid or missing agent token' }, { status: 401 });
	}
	if (locals.agent.scope !== 'projects') {
		return json({ error: 'Token does not have projects scope' }, { status: 403 });
	}

	const id = Number(params.id);
	if (!Number.isInteger(id) || id <= 0) {
		return json({ error: 'Invalid project id' }, { status: 400 });
	}

	const [target] = await db
		.select()
		.from(project)
		.where(and(eq(project.id, id), eq(project.userId, locals.agent.userId)));

	if (!target) {
		return json({ error: 'Project not found or not owned by user' }, { status: 404 });
	}

	const body = await request.json().catch(() => null);
	if (!body || typeof body !== 'object') {
		return json({ error: 'Body must be JSON' }, { status: 400 });
	}

	const payload: Record<string, unknown> = {};
	if (typeof body.name === 'string') payload.name = body.name.trim();
	if (typeof body.type === 'string') {
		if (!ALLOWED_TYPES.has(body.type)) {
			return json({ error: `type must be one of ${[...ALLOWED_TYPES].join(', ')}` }, { status: 400 });
		}
		payload.type = body.type;
	}
	if (typeof body.shortDescription === 'string') payload.shortDescription = body.shortDescription.trim();
	if (typeof body.description === 'string') payload.description = body.description.trim();
	if (typeof body.active === 'boolean') payload.active = body.active;

	if (Object.keys(payload).length === 0) {
		return json({ error: 'No supported fields provided' }, { status: 400 });
	}

	const [change] = await db
		.insert(projectChange)
		.values({
			userId: locals.agent.userId,
			agentSessionId: locals.agent.agentSessionId,
			action: 'update',
			targetProjectId: id,
			payload
		})
		.returning();

	return json({ change, status: 'pending' }, { status: 202 });
};
