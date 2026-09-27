import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { AGENT_SCOPES, createAgentToken, revokeAgentToken, type AgentScope } from '$lib/server/auth';
import { db } from '$lib/server/db';
import { agentToken } from '$lib/server/db/schema';
import { and, eq, isNull } from 'drizzle-orm';

export const POST: RequestHandler = async ({ locals, url, request }) => {
	if (!locals.user) {
		return json({ error: 'Must be logged in' }, { status: 401 });
	}

	let scope: AgentScope = 'projects';
	const body = await request.json().catch(() => null);
	if (body && typeof body === 'object' && typeof body.scope === 'string') {
		if (!AGENT_SCOPES.includes(body.scope as AgentScope)) {
			return json(
				{ error: `scope must be one of ${AGENT_SCOPES.join(', ')}` },
				{ status: 400 }
			);
		}
		scope = body.scope as AgentScope;
	}

	const { token, record } = await createAgentToken(locals.user.id, scope);
	const handoffUrl = `${url.origin}/agent/handoff/${token}`;

	return json({
		token,
		handoffUrl,
		scope,
		expiresAt: record.expiresAt.toISOString(),
		agentSessionId: record.agentSessionId
	});
};

export const DELETE: RequestHandler = async ({ locals }) => {
	if (!locals.user) {
		return json({ error: 'Must be logged in' }, { status: 401 });
	}

	const active = await db
		.select({ id: agentToken.id })
		.from(agentToken)
		.where(and(eq(agentToken.userId, locals.user.id), isNull(agentToken.revokedAt)));

	for (const { id } of active) {
		await revokeAgentToken(id);
	}

	return json({ revoked: active.length });
};
