import type { Handle } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import { flag } from '$lib/flags';

const handleAuth: Handle = async ({ event, resolve }) => {
	event.locals.agent = null;

	// Agent API (seeding projects from agents) stays dark until ff agent_api is on.
	if ((event.url.pathname.startsWith('/api/agent/') || event.url.pathname.startsWith('/agent/')) && !flag('agent_api')) {
		return new Response('Not found', { status: 404 });
	}

	if (event.url.pathname.startsWith('/api/agent/')) {
		const header = event.request.headers.get('authorization') ?? '';
		const match = header.match(/^Bearer\s+(.+)$/i);
		if (match) {
			event.locals.agent = await auth.validateAgentToken(match[1].trim());
		}
	}

	const sessionToken = event.cookies.get(auth.sessionCookieName);

	if (!sessionToken) {
		event.locals.user = null;
		event.locals.session = null;
		// Auto-generate anonymous session if user doesn't have authenticated session
		event.locals.anonymousSessionId = auth.getOrCreateAnonymousSession(event);
		return resolve(event);
	}

	const { session, user } = await auth.validateSessionToken(sessionToken);

	if (session) {
		auth.setSessionTokenCookie(event, sessionToken, session.expiresAt);
		// Use authenticated session ID for anonymous session
		event.locals.anonymousSessionId = session.id;
	} else {
		auth.deleteSessionTokenCookie(event);
		// Auto-generate anonymous session if session is invalid
		event.locals.anonymousSessionId = auth.getOrCreateAnonymousSession(event);
	}

	event.locals.user = user;
	event.locals.session = session;
	return resolve(event);
};

export const handle: Handle = handleAuth;
