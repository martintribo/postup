import { createHash } from 'node:crypto';
import { Apple, GitHub, Google, generateCodeVerifier, generateState, decodeIdToken } from 'arctic';
import { env } from '$env/dynamic/private';
import { eq, and, isNull } from 'drizzle-orm';
import { db } from '$lib/server/db';
import * as table from '$lib/server/db/schema';
import { encodeBase32LowerCase } from '@oslojs/encoding';

export type Provider = 'google' | 'apple' | 'x' | 'github' | 'mock';

/** Shown on the phase 0 sign-in sheet, in this order. [M1039] */
export const VERIFIED_PROVIDERS = ['apple', 'google', 'x', 'github'] as const;

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

export function github(origin: string) {
	if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) return null;
	return new GitHub(env.GITHUB_CLIENT_ID, env.GITHUB_CLIENT_SECRET, redirectUri(origin, 'github'));
}

/** X (Twitter) OAuth 2.0. Arctic has no X client; this is the authorize URL plus PKCE. */
export function x(origin: string) {
	if (!env.X_CLIENT_ID || !env.X_CLIENT_SECRET) return null;
	return { origin, clientId: env.X_CLIENT_ID, clientSecret: env.X_CLIENT_SECRET, redirectUri: redirectUri(origin, 'x') };
}

export function xAuthorizeURL(client: NonNullable<ReturnType<typeof x>>, state: string, verifier: string) {
	const url = new URL('https://twitter.com/i/oauth2/authorize');
	url.searchParams.set('response_type', 'code');
	url.searchParams.set('client_id', client.clientId);
	url.searchParams.set('redirect_uri', client.redirectUri);
	url.searchParams.set('scope', 'users.read tweet.read');
	url.searchParams.set('state', state);
	url.searchParams.set('code_challenge', createHash('sha256').update(verifier).digest('base64url'));
	url.searchParams.set('code_challenge_method', 'S256');
	return url;
}

export async function xProfile(client: NonNullable<ReturnType<typeof x>>, code: string, verifier: string): Promise<OAuthProfile> {
	const body = new URLSearchParams({
		grant_type: 'authorization_code',
		code,
		redirect_uri: client.redirectUri,
		code_verifier: verifier
	});
	const tokenRes = await fetch('https://api.x.com/2/oauth2/token', {
		method: 'POST',
		headers: {
			'content-type': 'application/x-www-form-urlencoded',
			authorization: `Basic ${Buffer.from(`${client.clientId}:${client.clientSecret}`).toString('base64')}`
		},
		body
	});
	if (!tokenRes.ok) throw new Error('X sign-in failed');
	const token = (await tokenRes.json()) as { access_token?: string };
	if (!token.access_token) throw new Error('X sign-in failed');
	const meRes = await fetch('https://api.x.com/2/users/me?user.fields=name,profile_image_url,username', {
		headers: { authorization: `Bearer ${token.access_token}` }
	});
	if (!meRes.ok) throw new Error('X sign-in failed');
	const me = (await meRes.json()) as { data?: { id?: string; name?: string; username?: string; profile_image_url?: string } };
	if (!me.data?.id) throw new Error('X sign-in failed');
	return { provider: 'x', providerUserId: me.data.id, name: me.data.name || me.data.username || null, avatarUrl: me.data.profile_image_url ?? null };
}

export async function githubProfile(client: NonNullable<ReturnType<typeof github>>, code: string): Promise<OAuthProfile> {
	const tokens = await client.validateAuthorizationCode(code);
	const res = await fetch('https://api.github.com/user', {
		headers: { authorization: `Bearer ${tokens.accessToken()}`, accept: 'application/vnd.github+json', 'user-agent': 'postup' }
	});
	if (!res.ok) throw new Error('GitHub sign-in failed');
	const u = (await res.json()) as { id?: number; name?: string | null; login?: string; avatar_url?: string };
	if (!u.id) throw new Error('GitHub sign-in failed');
	return { provider: 'github', providerUserId: String(u.id), name: u.name || u.login || null, avatarUrl: u.avatar_url ?? null };
}

/** Env vars still needed before this provider can complete sign-in. */
export function missingProviderEnv(p: Provider): string[] {
	if (p === 'google') return ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET'].filter((k) => !env[k]);
	if (p === 'apple') return ['APPLE_CLIENT_ID', 'APPLE_TEAM_ID', 'APPLE_KEY_ID', 'APPLE_PRIVATE_KEY'].filter((k) => !env[k]);
	if (p === 'github') return ['GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET'].filter((k) => !env[k]);
	if (p === 'x') return ['X_CLIENT_ID', 'X_CLIENT_SECRET'].filter((k) => !env[k]);
	return [];
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
	if (x(origin)) out.push('x');
	if (github(origin)) out.push('github');
	if (mockEnabled()) out.push('mock');
	return out;
}

/** Phase 0 always offers the four verified providers. Unconfigured ones explain which env vars are missing. */
export function verifiedProviderIds(): Provider[] {
	const out: Provider[] = [...VERIFIED_PROVIDERS];
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
