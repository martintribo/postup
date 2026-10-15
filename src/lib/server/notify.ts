import { eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { notification, user } from '$lib/server/db/schema';
import { flag } from '$lib/flags';
import { env } from '$env/dynamic/private';

/**
 * Record an in-app notification; optionally email it (ff email_alerts, D9).
 * No mail provider is wired yet: with EMAIL_WEBHOOK_URL set we POST {to, subject, text};
 * otherwise the email is only logged. Push (webpush/native) hooks in here later.
 */
export async function notify(n: { userId: string; type: string; postId?: number | null; actorId?: string | null; body: string }) {
	await db.insert(notification).values({ userId: n.userId, type: n.type, postId: n.postId ?? null, actorId: n.actorId ?? null, body: n.body });
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
