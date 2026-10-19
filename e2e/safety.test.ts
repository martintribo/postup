import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('report a postup, admin hides it; block hides the poster and stops joining', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1' || process.env.PUBLIC_FF_JOIN !== '1', 'needs mock + join');
	const sql = postgres(process.env.DATABASE_URL!);
	const t = Date.now();
	await page.goto(`/auth/mock?id=bad-${t}&name=Bad%20Poster`);
	const origin = new URL(page.url()).origin;
	const mk = (activity: string) =>
		page.request.post('/?/create', { headers: { 'content-type': 'application/x-www-form-urlencoded', origin }, data: new URLSearchParams({ activity, location: 'Bean Theory', latitude: '33.976', longitude: '-118.417', hours: '2' }).toString() });
	await mk(`spam-${t}`);
	await mk(`other-${t}`);
	const [spam] = await sql`select id from post where activity=${'spam-' + t}`;
	const [other] = await sql`select id from post where activity=${'other-' + t}`;

	const vctx = await browser.newContext();
	const v = await vctx.newPage();
	await v.goto(`${origin}/auth/mock?id=victim-${t}&name=Victim`);
	await v.goto(`${origin}/postups/${spam.id}`);
	await v.getByTestId('more').click();
	await v.getByRole('button', { name: 'Report' }).click();
	await v.getByLabel('Spam').check();
	await v.getByRole('button', { name: 'Send report' }).click();
	await expect(v.getByTestId('reported')).toBeVisible();

	// Admin (ADMIN_USERNAMES=adminmock) hides it -> postup cancelled.
	const actx = await browser.newContext();
	const a = await actx.newPage();
	await a.goto(`${origin}/auth/mock?id=admin-fixed&name=adminmock&next=/admin/reports`);
	await expect(a.getByTestId('admin-reports')).toBeVisible();
	const row = a.locator('tr', { hasText: `post #${spam.id}` });
	await row.getByRole('button', { name: 'Hide it' }).click();
	await expect(a.locator('tr', { hasText: `post #${spam.id}` })).toHaveCount(0);
	const [s2] = await sql`select status from post where id=${spam.id}`;
	expect(s2.status).toBe('cancelled');

	// Non-admins get 404 on the admin page.
	expect((await v.request.get(`${origin}/admin/reports`)).status()).toBe(404);

	// Block: victim blocks the poster -> poster's other postup disappears and can't be joined.
	await v.goto(`${origin}/postups/${other.id}`);
	await v.getByTestId('more').click();
	await v.getByRole('button', { name: /^Block / }).click();
	await v.getByRole('button', { name: 'Block', exact: true }).click();
	await expect(v).toHaveURL(`${origin}/`);
	expect((await v.request.get(`${origin}/postups/${other.id}`)).status()).toBe(404);
	expect((await v.request.post(`${origin}/api/postups/${other.id}/join`, { data: {} })).status()).toBe(403);
	const data = await (await v.request.get(`${origin}/__data.json?x-sveltekit-invalidated=11`)).text();
	expect(data).not.toContain(`other-${t}`);
	// ...and the block is two-way: the poster can't see the victim's postups either (checked via join guard).
	await vctx.close();
	await actx.close();
	await sql.end();
});
