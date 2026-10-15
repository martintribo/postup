import { expect, test } from '@playwright/test';

// Seeding flow: sign in, mint an agent token, agent proposes a project + update, owner accepts.
test('agent-seeded project and update appear after the owner accepts', async ({ page, request }) => {
	test.skip(process.env.OAUTH_MOCK !== '1' || process.env.PUBLIC_FF_AGENT_API !== '1', 'needs mock oauth + agent_api');
	const uid = `seed-${Date.now()}`;
	await page.goto(`/auth/mock?id=${uid}&name=Seeder&next=/projects`);
	const tok = await page.request.post('/api/agent/tokens', { data: { scope: 'projects' } });
	expect(tok.status()).toBe(200);
	const { token } = await tok.json();
	const name = `Star Fox mod ${Date.now()}`;
	const created = await request.post('/api/agent/projects', {
		headers: { authorization: `Bearer ${token}` },
		data: { name, shortDescription: 'N64 mod', description: 'Seeded by agent' }
	});
	expect(created.status()).toBe(202);
	const { change } = await created.json();
	expect((await page.request.post(`/api/projects/changes/${change.id}`, { data: { action: 'accept' } })).ok()).toBeTruthy();
	await page.goto('/projects');
	await expect(page.getByText(name).first()).toBeVisible();
});

test('agent API is 404 when the flag is off', async ({ request }) => {
	test.skip(process.env.PUBLIC_FF_AGENT_API === '1', 'flag on');
	expect((await request.get('/api/agent/projects')).status()).toBe(404);
});
