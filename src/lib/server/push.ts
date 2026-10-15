import { eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { deviceToken } from '$lib/server/db/schema';
import { env } from '$env/dynamic/private';
import { importPKCS8, SignJWT } from 'jose';

/**
 * Native push via FCM HTTP v1 (covers Android and, with APNs key uploaded to Firebase, iOS).
 * Needs FCM_PROJECT_ID, FCM_CLIENT_EMAIL, FCM_PRIVATE_KEY. Without them this is a no-op.
 */
let cached: { token: string; exp: number } | null = null;
async function accessToken() {
	if (cached && cached.exp > Date.now() + 60_000) return cached.token;
	const key = await importPKCS8((env.FCM_PRIVATE_KEY || '').replace(/\\n/g, '\n'), 'RS256');
	const now = Math.floor(Date.now() / 1000);
	const assertion = await new SignJWT({ scope: 'https://www.googleapis.com/auth/firebase.messaging' })
		.setProtectedHeader({ alg: 'RS256' })
		.setIssuer(env.FCM_CLIENT_EMAIL!)
		.setAudience('https://oauth2.googleapis.com/token')
		.setIssuedAt(now)
		.setExpirationTime(now + 3600)
		.sign(key);
	const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion }) });
	const d = await r.json();
	cached = { token: d.access_token, exp: Date.now() + d.expires_in * 1000 };
	return cached.token;
}

export async function sendPush(userId: string, body: string, url: string) {
	if (!env.FCM_PROJECT_ID || !env.FCM_CLIENT_EMAIL || !env.FCM_PRIVATE_KEY) return;
	const tokens = await db.select().from(deviceToken).where(eq(deviceToken.userId, userId));
	if (!tokens.length) return;
	const at = await accessToken();
	for (const t of tokens) {
		const r = await fetch(`https://fcm.googleapis.com/v1/projects/${env.FCM_PROJECT_ID}/messages:send`, {
			method: 'POST',
			headers: { authorization: `Bearer ${at}`, 'content-type': 'application/json' },
			body: JSON.stringify({ message: { token: t.token, notification: { title: 'PostUp', body }, data: { url } } })
		});
		if (r.status === 404 || r.status === 400) await db.delete(deviceToken).where(eq(deviceToken.token, t.token));
	}
}
