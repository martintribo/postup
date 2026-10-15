import { expect, test } from '@playwright/test';

test('native endpoints: token exchange rejects junk, devices need auth, link files served', async ({ request, page }) => {
	expect((await request.post('/api/auth/native', { data: { provider: 'google', idToken: 'not-a-jwt' } })).status()).toBe(401);
	expect((await request.post('/api/devices', { data: { token: 'x', platform: 'android' } })).status()).toBe(401);
	const aasa = await (await request.get('/.well-known/apple-app-site-association')).json();
	expect(aasa.applinks).toBeDefined();
	expect(Array.isArray(await (await request.get('/.well-known/assetlinks.json')).json())).toBe(true);
	test.skip(process.env.OAUTH_MOCK !== '1', 'mock off');
	await page.goto('/auth/mock?id=dev-tok&name=Device');
	expect((await page.request.post('/api/devices', { data: { token: `fcm-${Date.now()}`, platform: 'android' } })).ok()).toBeTruthy();
});
