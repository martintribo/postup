import { error, redirect, type RequestEvent } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import { apple, google, mockEnabled, decodeIdToken, findOrCreateUser, claimAnonymous, type OAuthProfile } from '$lib/server/oauth';

async function finish(event: RequestEvent, profile: OAuthProfile) {
	const userId = await findOrCreateUser(profile, event.locals.user?.id);
	await claimAnonymous(userId, auth.getAnonymousSessionIdFromCookie(event));
	const token = auth.generateSessionToken();
	const session = await auth.createSession(token, userId);
	auth.setSessionTokenCookie(event, token, session.expiresAt);
	const next = event.cookies.get('oauth_next') || '/';
	for (const c of ['oauth_state', 'oauth_verifier', 'oauth_next']) event.cookies.delete(c, { path: '/' });
	redirect(302, next);
}

function checkState(event: RequestEvent, state: string | null) {
	const expected = event.cookies.get('oauth_state');
	if (!state || !expected || state !== expected) error(400, 'Sign-in expired, please try again');
}

export async function GET(event: RequestEvent) {
	const { provider } = event.params;
	const state = event.url.searchParams.get('state');
	checkState(event, state);

	if (provider === 'google') {
		const g = google(event.url.origin);
		const code = event.url.searchParams.get('code');
		const verifier = event.cookies.get('oauth_verifier');
		if (!g || !code || !verifier) error(400, 'Bad request');
		const tokens = await g.validateAuthorizationCode(code, verifier);
		const c = decodeIdToken(tokens.idToken()) as { sub: string; email?: string; name?: string; picture?: string };
		return finish(event, { provider: 'google', providerUserId: c.sub, email: c.email, name: c.name, avatarUrl: c.picture });
	}
	if (provider === 'mock' && mockEnabled()) {
		return finish(event, {
			provider: 'mock',
			providerUserId: event.url.searchParams.get('id') || 'mock-user-1',
			name: event.url.searchParams.get('name') || 'Mock User'
		});
	}
	error(404, 'Unknown provider');
}

/** Apple uses response_mode=form_post. */
export async function POST(event: RequestEvent) {
	if (event.params.provider !== 'apple') error(405);
	const form = await event.request.formData();
	checkState(event, form.get('state') as string | null);
	const a = apple(event.url.origin);
	const code = form.get('code') as string | null;
	if (!a || !code) error(400, 'Bad request');
	const tokens = await a.validateAuthorizationCode(code);
	const c = decodeIdToken(tokens.idToken()) as { sub: string; email?: string };
	let name: string | null = null;
	try {
		const u = JSON.parse((form.get('user') as string) || 'null'); // only sent on first sign-in
		if (u?.name) name = [u.name.firstName, u.name.lastName].filter(Boolean).join(' ');
	} catch {
		/* ignore */
	}
	return finish(event, { provider: 'apple', providerUserId: c.sub, email: c.email, name });
}
