import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { project, projectChange, projectStatus } from '$lib/server/db/schema';
import { and, eq } from 'drizzle-orm';

async function loadChange(id: number, userId: string) {
	const [row] = await db
		.select()
		.from(projectChange)
		.where(and(eq(projectChange.id, id), eq(projectChange.userId, userId)));
	return row ?? null;
}

export const POST: RequestHandler = async ({ locals, params, request }) => {
	if (!locals.user) {
		return json({ error: 'Must be logged in' }, { status: 401 });
	}

	const id = Number(params.id);
	if (!Number.isInteger(id) || id <= 0) {
		return json({ error: 'Invalid change id' }, { status: 400 });
	}

	const body = await request.json().catch(() => null);
	const action = body && typeof body === 'object' ? body.action : undefined;
	if (action !== 'accept' && action !== 'reject') {
		return json({ error: "Body must be { action: 'accept' | 'reject' }" }, { status: 400 });
	}

	const change = await loadChange(id, locals.user.id);
	if (!change) {
		return json({ error: 'Change not found' }, { status: 404 });
	}
	if (change.status !== 'pending') {
		return json({ error: `Change is already ${change.status}` }, { status: 409 });
	}

	const reviewedAt = new Date();

	if (action === 'reject') {
		await db
			.update(projectChange)
			.set({ status: 'rejected', reviewedAt })
			.where(eq(projectChange.id, id));
		return json({ status: 'rejected' });
	}

	const payload = change.payload as Record<string, unknown>;

	if (change.action === 'create') {
		const name = String(payload.name ?? '').trim();
		if (!name) {
			return json({ error: 'Staged change is missing a name' }, { status: 422 });
		}
		const [created] = await db
			.insert(project)
			.values({
				name,
				type: typeof payload.type === 'string' ? payload.type : 'software',
				shortDescription:
					typeof payload.shortDescription === 'string' && payload.shortDescription
						? payload.shortDescription
						: name,
				description:
					typeof payload.description === 'string' && payload.description
						? payload.description
						: name,
				userId: locals.user.id
			})
			.returning();
		await db
			.update(projectChange)
			.set({ status: 'applied', reviewedAt, targetProjectId: created.id })
			.where(eq(projectChange.id, id));
		return json({ status: 'applied', project: created });
	}

	if (change.action === 'update') {
		if (!change.targetProjectId) {
			return json({ error: 'Staged update has no target project' }, { status: 422 });
		}
		const [target] = await db
			.select()
			.from(project)
			.where(and(eq(project.id, change.targetProjectId), eq(project.userId, locals.user.id)));
		if (!target) {
			return json({ error: 'Target project no longer exists' }, { status: 404 });
		}
		const updates: Record<string, unknown> = { updatedAt: new Date() };
		for (const key of ['name', 'type', 'shortDescription', 'description', 'active'] as const) {
			if (key in payload) updates[key] = payload[key];
		}
		const [updated] = await db
			.update(project)
			.set(updates)
			.where(eq(project.id, change.targetProjectId))
			.returning();
		await db
			.update(projectChange)
			.set({ status: 'applied', reviewedAt })
			.where(eq(projectChange.id, id));
		return json({ status: 'applied', project: updated });
	}

	if (change.action === 'status_update') {
		if (!change.targetProjectId) {
			return json({ error: 'Staged status has no target project' }, { status: 422 });
		}
		const [target] = await db
			.select({ id: project.id })
			.from(project)
			.where(and(eq(project.id, change.targetProjectId), eq(project.userId, locals.user.id)));
		if (!target) {
			return json({ error: 'Target project no longer exists' }, { status: 404 });
		}
		const bodyText = typeof payload.body === 'string' ? payload.body.trim() : '';
		const titleRaw = typeof payload.title === 'string' ? payload.title.trim() : '';
		const occurredAtRaw = typeof payload.occurredAt === 'string' ? payload.occurredAt : '';
		if (!bodyText) {
			return json({ error: 'Staged status is missing a body' }, { status: 422 });
		}
		const occurredAt = occurredAtRaw ? new Date(occurredAtRaw) : new Date();
		if (Number.isNaN(occurredAt.getTime())) {
			return json({ error: 'Staged status occurredAt is invalid' }, { status: 422 });
		}
		const [inserted] = await db
			.insert(projectStatus)
			.values({
				projectId: change.targetProjectId,
				title: titleRaw || null,
				body: bodyText,
				occurredAt
			})
			.returning();
		await db
			.update(projectChange)
			.set({ status: 'applied', reviewedAt })
			.where(eq(projectChange.id, id));
		return json({ status: 'applied', projectStatus: inserted });
	}

	return json({ error: `Unknown action ${change.action}` }, { status: 422 });
};
