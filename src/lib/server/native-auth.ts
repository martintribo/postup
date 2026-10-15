import { createRemoteJWKSet, jwtVerify, type JWTVerifyGetKey } from 'jose';
import { env } from '$env/dynamic/private';

const JWKS = {
	google: createRemoteJWKSet(new URL('https://www.googleapis.com/oauth2/v3/certs')),
	apple: createRemoteJWKSet(new URL('https://appleid.apple.com/auth/keys'))
};
const ISS = { google: ['https://accounts.google.com', 'accounts.google.com'], apple: ['https://appleid.apple.com'] };

function audiences(provider: 'google' | 'apple') {
	const raw = provider === 'google' ? `${env.GOOGLE_CLIENT_ID || ''},${env.GOOGLE_IOS_CLIENT_ID || ''},${env.GOOGLE_ANDROID_CLIENT_ID || ''}` : `${env.APPLE_BUNDLE_ID || ''},${env.APPLE_CLIENT_ID || ''}`;
	return raw.split(',').map((s) => s.trim()).filter(Boolean);
}

/** Verify an ID token from native Sign in with Apple / Google. Throws on any problem. */
export async function verifyNativeIdToken(provider: 'google' | 'apple', idToken: string, jwks: JWTVerifyGetKey = JWKS[provider]) {
	const aud = audiences(provider);
	if (!aud.length) throw new Error(`${provider} native sign-in is not configured`);
	const { payload } = await jwtVerify(idToken, jwks, { issuer: ISS[provider], audience: aud });
	if (!payload.sub) throw new Error('No subject');
	return { sub: payload.sub, email: (payload.email as string | undefined) ?? null, name: (payload.name as string | undefined) ?? null, picture: (payload.picture as string | undefined) ?? null };
}
