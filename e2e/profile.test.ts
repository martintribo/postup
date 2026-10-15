import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('profile, follow, settings and account deletion', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1', 'needs mock');
	const sql = postgres(process.env.DATABASE_URL!);
	const t = Date.now();
	await page.goto(`/auth/mock?id=prof-${t}&name=Prof%20Ile`);
	const origin = new URL(page.url()).origin;
	await page.request.post('/?/create', { headers: { 'content-type': 'application/x-www-form-urlencoded', origin }, data: new URLSearchParams({ activity: `prof-${t}`, location: 'Bean Theory', latitude: '33.976', longitude: '-118.417', hours: '2' }).toString() });

	await page.goto('/me');
	await expect(page.getByTestId('profile')).toContainText(`prof-${t}`);
	await page.getByTestId('edit-profile').click();
	await page.locator('input[name=displayName]').fill('Maya P');
	await page.locator('textarea[name=bio]').fill('Building N64 mods');
	await page.getByRole('button', { name: 'Save' }).click();
	await expect(page.getByTestId('saved')).toBeVisible();
	await page.goto('/me');
	await expect(page.getByText('Building N64 mods')).toBeVisible();
	const profileUrl = page.url();

	const fctx = await browser.newContext();
	const f = await fctx.newPage();
	await f.goto(`${origin}/auth/mock?id=fan-${t}&name=Fan`);
	await f.goto(profileUrl);
	await f.getByTestId('follow').click();
	await expect(f.getByTestId('follow')).toHaveText('Following');
	await expect(f.getByText('1 follower')).toBeVisible();

	// Delete: live postup cancelled, sign-in removed, profile 404.
	await page.goto('/settings');
	await page.getByRole('button', { name: 'Delete account…' }).click();
	await page.locator('input[name=confirm]').fill('DELETE');
	await page.getByRole('button', { name: 'Delete account' }).click();
	await expect(page).toHaveURL(/deleted=1/);
	const [acct] = await sql`select count(*)::int n from oauth_account where provider_user_id=${'prof-' + t}`;
	expect(acct.n).toBe(0);
	const [p] = await sql`select status from post where activity=${'prof-' + t}`;
	expect(p.status).toBe('cancelled');
	expect((await f.request.get(profileUrl)).status()).toBe(404);
	await fctx.close();
	await sql.end();
});
