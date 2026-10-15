import { Apple, Google, generateCodeVerifier, generateState, decodeIdToken } from 'arctic';
import { env } from '$env/dynamic/private';
import { eq, and, isNull } from 'drizzle-orm';
import { db } from '$lib/server/db';
import * as table from '$lib/server/db/schema';
import { encodeBase32LowerCase } from '@oslojs/encoding';

export type Provider = 'google' | 'apple' | 'mock';

export interface OAuthProfile {
	provider: Provider;
	providerUserId: string;
	email?: string | null;
	name?: string | null;
	avatarUrl?: string | null;
}

function redirectUri(origin: string, p: Provider) {
	return `${env.OAUTH_REDIRECT_ORIGIN || origin}/auth/${p}/callback`;
}

export function google(origin: string) {
	if (!env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) return null;
	return new Google(env.GOOGLE_CLIENT_ID, env.GOOGLE_CLIENT_SECRET, redirectUri(origin, 'google'));
}

export function apple(origin: string) {
	if (!env.APPLE_CLIENT_ID || !env.APPLE_TEAM_ID || !env.APPLE_KEY_ID || !env.APPLE_PRIVATE_KEY) return null;
	const pem = env.APPLE_PRIVATE_KEY.replace(/\\n/g, '\n')
		.replace(/-----[^-]+-----/g, '')
		.replace(/\s/g, '');
	const key = Uint8Array.from(atob(pem), (c) => c.charCodeAt(0));
	return new Apple(env.APPLE_CLIENT_ID, env.APPLE_TEAM_ID, env.APPLE_KEY_ID, key, redirectUri(origin, 'apple'));
}

/** Dev/test-only provider so sign-in can be exercised without real credentials. Never on in prod. */
export function mockEnabled() {
	return env.OAUTH_MOCK === '1' && env.VERCEL_ENV !== 'production';
}

export function availableProviders(origin: string): Provider[] {
	const out: Provider[] = [];
	if (apple(origin)) out.push('apple');
	if (google(origin)) out.push('google');
	if (mockEnabled()) out.push('mock');
	return out;
}

export { generateCodeVerifier, generateState, decodeIdToken };

function slug(s: string) {
	return s.toLowerCase().replace(/[^a-z0-9_-]+/g, '').slice(0, 20) || 'user';
}

async function uniqueUsername(base: string) {
	const b = slug(base);
	for (let i = 0; i < 20; i++) {
		const u = i === 0 ? b : `${b}${Math.floor(Math.random() * 10000)}`;
		const hit = await db.select({ id: table.user.id }).from(table.user).where(eq(table.user.username, u));
		if (!hit.length) return u;
	}
	return `${b}${Date.now()}`;
}

/**
 * Find the user for this identity, or link it to the signed-in user, or create a new one.
 * Email matching is deliberately NOT used to merge accounts (Apple relay emails, takeover risk).
 */
export async function findOrCreateUser(p: OAuthProfile, currentUserId?: string | null): Promise<string> {
	const [linked] = await db
		.select()
		.from(table.oauthAccount)
		.where(and(eq(table.oauthAccount.provider, p.provider), eq(table.oauthAccount.providerUserId, p.providerUserId)));
	if (linked) return linked.userId;

	let userId = currentUserId ?? null;
	if (!userId) {
		userId = encodeBase32LowerCase(crypto.getRandomValues(new Uint8Array(15)));
		const username = await uniqueUsername(p.name || p.email?.split('@')[0] || 'user');
		await db.insert(table.user).values({
			id: userId,
			username,
			passwordHash: null,
			displayName: p.name ?? null,
			email: p.email ?? null,
			avatarUrl: p.avatarUrl ?? null
		});
	}
	await db.insert(table.oauthAccount).values({
		provider: p.provider,
		providerUserId: p.providerUserId,
		userId,
		email: p.email ?? null
	});
	return userId;
}

/** Give a newly signed-in user ownership of what they posted anonymously from this browser. */
export async function claimAnonymous(userId: string, anonymousSessionId: string | null) {
	if (!anonymousSessionId) return;
	await db
		.update(table.post)
		.set({ userId })
		.where(and(eq(table.post.sessionId, anonymousSessionId), isNull(table.post.userId)));
	await db
		.update(table.project)
		.set({ userId })
		.where(and(eq(table.project.sessionId, anonymousSessionId), isNull(table.project.userId)));
}
