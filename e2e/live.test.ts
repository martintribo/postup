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
	await expect(page.getByTestId('ring-left')).toHaveText(/^(1:5\d|2:00)$/);

	await page.getByRole('button', { name: '+30 min' }).click();
	await expect(page.getByTestId('ring-left')).toHaveText(/^(2:2\d|2:30)$/);
	const [p2] = await sql`select ends_at from post where id=${p.id}`;
	expect(Math.round((p2.ends_at - p.ends_at) / 60000)).toBe(30);

	// Edit is the post form (mockup #post-edit); Save returns to You're live.
	await page.getByRole('link', { name: 'Edit' }).click();
	await expect(page.getByTestId('post-form').getByText('Edit postup')).toBeVisible();
	await page.locator('input[name=activity]').fill('Writing more tests');
	await page.getByRole('radio', { name: 'Ask to join' }).click();
	await page.getByRole('button', { name: 'Save' }).click();
	await expect(page.getByTestId('you-are-live')).toBeVisible();
	await expect(page.getByRole('radio', { name: 'Ask to join' })).toHaveAttribute('aria-checked', 'true');
	const [p4] = await sql`select activity, join_mode from post where id=${p.id}`;
	expect(p4).toMatchObject({ activity: 'Writing more tests', join_mode: 'ask' });

	// Someone else cannot manage it.
	const other = await browser.newContext();
	const op = await other.newPage();
	await op.goto(`${origin}/auth/mock?id=other-${uid}&name=Other`);
	const forbidden = await op.request.patch(`${origin}/api/postups/${p.id}`, { data: { action: 'end' } });
	expect(forbidden.status()).toBe(403);
	await other.close();

	await page.getByRole('button', { name: 'End postup' }).click();
	await page.getByTestId('confirm-end').click();
	await expect(page.getByText('This postup ended')).toBeVisible();
	const [p3] = await sql`select status from post where id=${p.id}`;
	expect(p3.status).toBe('ended');

	await sql`update post set status='cancelled' where id=${p.id}`;
	await page.reload();
	await expect(page.getByText(/cancelled this postup/)).toBeVisible();
	await sql.end();
});
