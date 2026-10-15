import { describe, expect, it, vi } from 'vitest';
vi.mock('$env/dynamic/private', () => ({ env: { GOOGLE_IOS_CLIENT_ID: 'ios-client' } }));
import { SignJWT, generateKeyPair, exportJWK, createLocalJWKSet } from 'jose';
import { verifyNativeIdToken } from './native-auth';

describe('verifyNativeIdToken', async () => {
	const { publicKey, privateKey } = await generateKeyPair('RS256');
	const jwk = { ...(await exportJWK(publicKey)), kid: 'k1', alg: 'RS256' };
	const jwks = createLocalJWKSet({ keys: [jwk] });
	const sign = (claims: Record<string, unknown>) =>
		new SignJWT(claims).setProtectedHeader({ alg: 'RS256', kid: 'k1' }).setIssuedAt().setExpirationTime('5m').sign(privateKey);
	it('accepts a valid Google token for our iOS client', async () => {
		const t = await sign({ iss: 'https://accounts.google.com', aud: 'ios-client', sub: 'g-123', email: 'a@b.c' });
		expect((await verifyNativeIdToken('google', t, jwks)).sub).toBe('g-123');
	});
	it('rejects a token for another app', async () => {
		const t = await sign({ iss: 'https://accounts.google.com', aud: 'someone-else', sub: 'g-1' });
		await expect(verifyNativeIdToken('google', t, jwks)).rejects.toThrow();
	});
});
