import { expect, test } from '@playwright/test';
import { createHash } from 'node:crypto';
import postgres from 'postgres';

// Needs OAUTH_MOCK=1 and PUBLIC_FF_OAUTH=1 (dev only).
test('mock OAuth sign-in creates a user and claims anonymous posts', async ({ page, context }) => {
	test.skip(process.env.OAUTH_MOCK !== '1', 'mock provider off');
	const sql = postgres(process.env.DATABASE_URL!);
	await page.goto('/');
	const anon = (await context.cookies()).find((c) => c.name === 'anonymous-session')!;
	const anonId = createHash('sha256').update(anon.value).digest('hex');
	const uid = `e2e-${Date.now()}`;
	await sql`insert into post (name, activity, location, latitude, longitude, hours, session_id, created_at, start_time)
		values ('anon', 'testing', 'Cafe', 33.97, -118.41, 2, ${anonId}, now(), now())`;

	await page.goto('/login?next=/projects');
	await expect(page.getByTestId('signin-sheet')).toBeVisible();
	await page.goto(`/auth/mock?id=${uid}&name=Maya%20Test&next=/projects`);
	await expect(page).toHaveURL(/\/projects$/);

	const [acct] = await sql`select user_id from oauth_account where provider='mock' and provider_user_id=${uid}`;
	expect(acct).toBeTruthy();
	const [u] = await sql`select display_name, password_hash from "user" where id=${acct.user_id}`;
	expect(u.display_name).toBe('Maya Test');
	expect(u.password_hash).toBeNull();
	const claimed = await sql`select id from post where session_id=${anonId} and user_id=${acct.user_id}`;
	expect(claimed.length).toBe(1);

	// Signing in again with the same identity reuses the same user.
	await context.clearCookies();
	await page.goto(`/auth/mock?id=${uid}&name=Maya%20Test`);
	const accts = await sql`select user_id from oauth_account where provider_user_id=${uid}`;
	expect(accts.length).toBe(1);
	await sql.end();
});

test('password login still works for existing accounts', async ({ page }) => {
	const name = `pw${Date.now() % 1e8}`;
	await page.goto('/login');
	await page.getByRole('button', { name: /register|sign up|create/i }).first().click();
	await page.locator('input[name=username]').fill(name);
	await page.locator('input[name=password]').fill('secret123');
	await page.locator('form[action*=register] button[type=submit], form button[type=submit]').last().click();
	await expect(page).toHaveURL(/\/$/);
	await expect(page.getByText(name)).toBeVisible();
});
