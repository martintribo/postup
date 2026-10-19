import { and, eq, or } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { block, report, post, message, project, user } from '$lib/server/db/schema';
import { env } from '$env/dynamic/private';

export const REPORT_REASONS = ['spam', 'harassment', 'inappropriate', 'fake', 'unsafe', 'not_public', 'other'] as const;
export const TARGETS = ['user', 'post', 'message', 'project'] as const;

/** Everyone this user has blocked or been blocked by (blocks hide both ways). */
export async function blockedSet(userId: string | null | undefined): Promise<Set<string>> {
	if (!userId) return new Set();
	const rows = await db.select().from(block).where(or(eq(block.blockerId, userId), eq(block.blockedId, userId)));
	return new Set(rows.map((r) => (r.blockerId === userId ? r.blockedId : r.blockerId)));
}

export async function isBlockedBetween(a: string, b: string) {
	return (await blockedSet(a)).has(b);
}

export async function blockUser(blockerId: string, blockedId: string) {
	if (blockerId === blockedId) throw new Error("You can't block yourself");
	await db.insert(block).values({ blockerId, blockedId }).onConflictDoNothing();
}
export async function unblockUser(blockerId: string, blockedId: string) {
	await db.delete(block).where(and(eq(block.blockerId, blockerId), eq(block.blockedId, blockedId)));
}

export async function fileReport(r: { reporterId: string; targetType: string; targetId: string; reason: string; details?: string }) {
	if (!(TARGETS as readonly string[]).includes(r.targetType)) throw new Error('Bad target');
	if (!(REPORT_REASONS as readonly string[]).includes(r.reason)) throw new Error('Pick a reason');
	const [row] = await db
		.insert(report)
		.values({ reporterId: r.reporterId, targetType: r.targetType, targetId: String(r.targetId), reason: r.reason, details: r.details?.slice(0, 1000) || null })
		.returning();
	return row;
}

/** Admins: comma-separated usernames in ADMIN_USERNAMES (no UI to grant admin). */
export async function isAdmin(userId: string | null | undefined) {
	if (!userId) return false;
	const names = (env.ADMIN_USERNAMES || '').split(',').map((s) => s.trim()).filter(Boolean);
	if (!names.length) return false;
	const [u] = await db.select({ username: user.username }).from(user).where(eq(user.id, userId));
	return !!u && names.includes(u.username);
}

/** Admin action: hide the reported thing (or dismiss). */
export async function resolveReport(id: number, action: 'hide' | 'dismiss') {
	const [r] = await db.select().from(report).where(eq(report.id, id));
	if (!r) throw new Error('Not found');
	if (action === 'hide') {
		if (r.targetType === 'post') await db.update(post).set({ status: 'cancelled' }).where(eq(post.id, Number(r.targetId)));
		if (r.targetType === 'message') await db.update(message).set({ deletedAt: new Date() }).where(eq(message.id, Number(r.targetId)));
		if (r.targetType === 'project') await db.update(project).set({ hidden: true }).where(eq(project.id, Number(r.targetId)));
		// user: no ban system yet; admin hides their content individually (noted in plan).
	}
	await db.update(report).set({ status: action === 'hide' ? 'actioned' : 'dismissed', resolvedAt: new Date() }).where(eq(report.id, id));
}
