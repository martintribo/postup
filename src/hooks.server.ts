import type { Handle } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';

const handleAuth: Handle = async ({ event, resolve }) => {
	event.locals.agent = null;

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
