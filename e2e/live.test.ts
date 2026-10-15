import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('poster sees You are live, extends, edits, and ends; others cannot', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1', 'needs mock oauth');
	const sql = postgres(process.env.DATABASE_URL!);
	const uid = `live-${Date.now()}`;
	await page.goto(`/auth/mock?id=${uid}&name=Live%20Owner`);
	const origin = new URL(page.url()).origin;
	const r = await page.request.post('/?/create', {
		headers: { 'content-type': 'application/x-www-form-urlencoded', origin },
		data: new URLSearchParams({ activity: 'Writing tests', location: 'Bean Theory', latitude: '33.976', longitude: '-118.417', hours: '2' }).toString()
	});
	expect(r.ok()).toBeTruthy();
	const [p] = await sql`select p.id, p.ends_at from post p join oauth_account o on o.user_id=p.user_id where o.provider_user_id=${uid}`;

	await page.goto('/');
	await expect(page.getByTestId('live-bar')).toBeVisible();
	await page.getByTestId('live-bar').click();
	await expect(page.getByTestId('you-are-live')).toBeVisible();
	await expect(page.getByTestId('time-left')).toContainText(/1h 5\dm left|2h 0m left/);

	await page.getByRole('button', { name: '+1 hour' }).click();
	await expect(page.getByTestId('time-left')).toContainText(/2h 5\dm left|3h 0m left/);
	const [p2] = await sql`select ends_at from post where id=${p.id}`;
	expect(Math.round((p2.ends_at - p.ends_at) / 60000)).toBe(60);

	await page.getByRole('button', { name: 'Edit' }).click();
	await page.locator('input[name=activity]').fill('Writing more tests');
	await page.getByLabel('Ask to join').check();
	await page.getByRole('button', { name: 'Save' }).click();
	await expect(page.getByText('Writing more tests')).toBeVisible();
	await expect(page.getByText('Ask to join')).toBeVisible();

	// Someone else cannot manage it.
	const other = await browser.newContext();
	const op = await other.newPage();
	await op.goto(`${origin}/auth/mock?id=other-${uid}&name=Other`);
	const forbidden = await op.request.patch(`${origin}/api/postups/${p.id}`, { data: { action: 'end' } });
	expect(forbidden.status()).toBe(403);
	await other.close();

	await page.getByRole('button', { name: 'End', exact: true }).click();
	await page.getByRole('button', { name: 'End postup' }).click();
	await expect(page.getByText('This postup has ended')).toBeVisible();
	const [p3] = await sql`select status from post where id=${p.id}`;
	expect(p3.status).toBe('ended');

	await sql`update post set status='cancelled' where id=${p.id}`;
	await page.reload();
	await expect(page.getByText('This postup was cancelled')).toBeVisible();
	await sql.end();
});
