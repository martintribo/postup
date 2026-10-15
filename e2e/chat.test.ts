import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('group chat: members talk live, strangers blocked, read-only after end, closed after window', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1' || process.env.PUBLIC_FF_CHAT !== '1', 'needs mock + ff chat');
	const sql = postgres(process.env.DATABASE_URL!);
	const t = Date.now();
	await page.goto(`/auth/mock?id=co-${t}&name=Chat%20Owner`);
	const origin = new URL(page.url()).origin;
	await page.request.post('/?/create', {
		headers: { 'content-type': 'application/x-www-form-urlencoded', origin },
		data: new URLSearchParams({ activity: `chat-${t}`, location: 'Bean Theory', latitude: '33.976', longitude: '-118.417', hours: '2' }).toString()
	});
	const [p] = await sql`select id from post where activity=${'chat-' + t}`;

	const jctx = await browser.newContext();
	const j = await jctx.newPage();
	await j.goto(`${origin}/auth/mock?id=cj-${t}&name=Joiner`);
	await j.goto(`${origin}/postups/${p.id}`);
	await j.getByRole('button', { name: 'Join', exact: true }).click();
	await j.getByTestId('open-chat').click();
	await j.locator('input[name=body]').fill('Hi! By the window');
	await j.getByRole('button', { name: 'Send' }).click();
	await expect(j.getByText('Hi! By the window')).toBeVisible();

	await page.goto('/inbox');
	await expect(page.getByTestId('chat-unread')).toHaveText('1');
	await page.getByText(`chat-${t}`).click();
	await expect(page.getByText('Hi! By the window')).toBeVisible();
	await page.locator('input[name=body]').fill('On my way over');
	await page.getByRole('button', { name: 'Send' }).click();
	await expect(j.getByText('On my way over')).toBeVisible({ timeout: 8000 }); // arrives by polling

	const sctx = await browser.newContext();
	const s = await sctx.newPage();
	await s.goto(`${origin}/auth/mock?id=cs-${t}&name=Stranger`);
	expect((await s.request.get(`${origin}/api/postups/${p.id}/messages`)).status()).toBe(403);

	await sql`update post set status='ended', ends_at=now() - interval '1 hour' where id=${p.id}`;
	await j.reload();
	await expect(j.getByTestId('chat-readonly')).toBeVisible();
	expect((await j.request.post(`${origin}/api/postups/${p.id}/messages`, { data: { body: 'late' } })).status()).toBe(409);

	await sql`update post set ends_at=now() - interval '25 hours' where id=${p.id}`;
	expect((await j.request.get(`${origin}/api/postups/${p.id}/messages`)).status()).toBe(410);
	await jctx.close();
	await sctx.close();
	await sql.end();
});
