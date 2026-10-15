import { error, redirect } from '@sveltejs/kit';
import { apple, google, mockEnabled, generateCodeVerifier, generateState } from '$lib/server/oauth';
import type { RequestHandler } from './$types';

const cookieOpts = { path: '/', httpOnly: true, secure: false, maxAge: 600, sameSite: 'lax' } as const;

export const GET: RequestHandler = async (event) => {
	const { provider } = event.params;
	const next = event.url.searchParams.get('next') || '/';
	const origin = event.url.origin;
	const state = generateState();
	event.cookies.set('oauth_state', state, cookieOpts);
	event.cookies.set('oauth_next', next.startsWith('/') ? next : '/', cookieOpts);

	if (provider === 'google') {
		const g = google(origin);
		if (!g) error(404, 'Google sign-in is not configured');
		const verifier = generateCodeVerifier();
		event.cookies.set('oauth_verifier', verifier, cookieOpts);
		redirect(302, g.createAuthorizationURL(state, verifier, ['openid', 'profile', 'email']).toString());
	}
	if (provider === 'apple') {
		const a = apple(origin);
		if (!a) error(404, 'Apple sign-in is not configured');
		// Apple posts the callback cross-site, so the state cookie must be SameSite=None.
		event.cookies.set('oauth_state', state, { ...cookieOpts, sameSite: 'none', secure: true });
		const url = a.createAuthorizationURL(state, ['name', 'email']);
		url.searchParams.set('response_mode', 'form_post');
		redirect(302, url.toString());
	}
	if (provider === 'mock' && mockEnabled()) {
		const id = event.url.searchParams.get('id') || 'mock-user-1';
		const name = event.url.searchParams.get('name') || 'Mock User';
		redirect(302, `/auth/mock/callback?state=${state}&id=${encodeURIComponent(id)}&name=${encodeURIComponent(name)}`);
	}
	error(404, 'Unknown provider');
};
