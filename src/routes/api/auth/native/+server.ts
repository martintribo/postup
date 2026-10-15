import { json } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import { findOrCreateUser, claimAnonymous } from '$lib/server/oauth';
import { verifyNativeIdToken } from '$lib/server/native-auth';
import type { RequestHandler } from './$types';

/** Native Sign in with Apple / Google: the app sends the provider ID token, we start a session. */
export const POST: RequestHandler = async (event) => {
	const { provider, idToken, name } = await event.request.json().catch(() => ({}));
	if ((provider !== 'google' && provider !== 'apple') || typeof idToken !== 'string') return json({ error: 'provider and idToken required' }, { status: 400 });
	let claims;
	try {
		claims = await verifyNativeIdToken(provider, idToken);
	} catch (e) {
		return json({ error: (e as Error).message }, { status: 401 });
	}
	const userId = await findOrCreateUser({ provider, providerUserId: claims.sub, email: claims.email, name: claims.name || name || null, avatarUrl: claims.picture }, event.locals.user?.id);
	await claimAnonymous(userId, auth.getAnonymousSessionIdFromCookie(event));
	const token = auth.generateSessionToken();
	const session = await auth.createSession(token, userId);
	auth.setSessionTokenCookie(event, token, session.expiresAt);
	return json({ ok: true, expiresAt: session.expiresAt.toISOString() });
};
