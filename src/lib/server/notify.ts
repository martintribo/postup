import { eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { notification, user } from '$lib/server/db/schema';
import { flag } from '$lib/flags';
import { env } from '$env/dynamic/private';
import { sendPush } from '$lib/server/push';

/**
 * Record an in-app notification; optionally email it (ff email_alerts, D9).
 * No mail provider is wired yet: with EMAIL_WEBHOOK_URL set we POST {to, subject, text};
 * otherwise the email is only logged. Push (webpush/native) hooks in here later.
 */
/** Settings toggles (mockup #settings). Defaults: everything on except "people you follow post up". */
export const NOTIFY_DEFAULTS = { requests: true, joins: true, messages: true, follows: false } as const;
export type NotifyPrefs = Record<keyof typeof NOTIFY_DEFAULTS, boolean>;
const PREF_FOR: Record<string, keyof NotifyPrefs> = { join_request: 'requests', joined: 'joins', left: 'joins', message: 'messages', follow_posted: 'follows' };

export function prefsOf(raw: Partial<NotifyPrefs> | null | undefined): NotifyPrefs {
	return { ...NOTIFY_DEFAULTS, ...(raw ?? {}) };
}

export async function notify(n: { userId: string; type: string; postId?: number | null; actorId?: string | null; body: string }) {
	await db.insert(notification).values({ userId: n.userId, type: n.type, postId: n.postId ?? null, actorId: n.actorId ?? null, body: n.body });
	// The Activity list always gets the row; a switched-off toggle only silences push and email.
	const key = PREF_FOR[n.type];
	if (key) {
		const [u] = await db.select({ p: user.notifyPrefs }).from(user).where(eq(user.id, n.userId));
		if (!prefsOf(u?.p)[key]) return;
	}
	await sendPush(n.userId, n.body, n.postId ? `/postups/${n.postId}` : '/activity').catch((e) => console.error('push failed', e));
	if (!flag('email_alerts')) return;
	const [u] = await db.select({ email: user.email }).from(user).where(eq(user.id, n.userId));
	if (!u?.email) return;
	const msg = { to: u.email, subject: 'PostUp', text: n.body };
	if (env.EMAIL_WEBHOOK_URL) {
		await fetch(env.EMAIL_WEBHOOK_URL, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(msg) }).catch((e) => console.error('email failed', e));
	} else {
		console.info('[email_alerts] would send', { to: '<redacted>', type: n.type });
	}
}
