import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('home opens on the Nearby feed when nobody is live, map when someone is', async ({ page }) => {
	test.skip(process.env.PUBLIC_FF_FEED_HOME !== '1', 'flag off');
	const sql = postgres(process.env.DATABASE_URL!);
	await sql`update post set status='ended' where status='live'`;
	const tag = `feed-${Date.now()}`;
	await sql`insert into post (name, activity, location, latitude, longitude, hours, created_at, start_time, ends_at, status)
		values ('Maya', ${tag}, 'Bean Theory', 33.976, -118.417, 2, now() - interval '1 day', now() - interval '1 day', now() - interval '22 hours', 'ended')`;

	await page.goto('/');
	await expect(page.getByTestId('nearby-feed')).toBeVisible();
	await expect(page.getByText(tag)).toBeVisible();
	await expect(page.getByText(/postups? this week/)).toBeVisible();
	await expect(page.getByText(/quiet/i)).toHaveCount(0);
	await expect(page.getByTestId('feed-welcome')).toBeVisible();
	await page.getByRole('button', { name: 'Dismiss' }).click();
	await page.reload();
	await expect(page.getByTestId('feed-welcome')).toHaveCount(0);

	await page.getByTestId('open-map').click();
	await expect(page.getByTestId('nearby-feed')).toHaveCount(0);

	await sql`insert into post (name, activity, location, latitude, longitude, hours, created_at, start_time, ends_at, status)
		values ('Sam', 'live now', 'Bean Theory', 33.976, -118.417, 2, now(), now(), now() + interval '2 hours', 'live')`;
	await page.goto('/');
	await expect(page.getByTestId('nearby-feed')).toHaveCount(0);
	await sql`update post set status='ended' where activity='live now'`;

	const api = await page.request.get('/api/feed?lat=33.976&lng=-118.417');
	expect((await api.json()).items.length).toBeGreaterThan(0);
	await sql.end();
});
