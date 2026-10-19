import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('home opens in Building when nobody is live, Live when someone is', async ({ page }) => {
	test.skip(process.env.PUBLIC_FF_FEED_HOME !== '1', 'flag off');
	const sql = postgres(process.env.DATABASE_URL!);
	await sql`update post set status='ended' where status='live'`;
	const tag = `feed-${Date.now()}`;
	// Keep the feed small and deterministic: push earlier test rows out of the 7-day window.
	await sql`update post set start_time = now() - interval '30 days' where status <> 'live'`;
	await sql`insert into post (name, activity, location, latitude, longitude, hours, created_at, start_time, ends_at, status)
		values ('Maya', ${tag}, 'Bean Theory', 33.976, -118.417, 2, now() - interval '1 day', now() - interval '1 day', now() - interval '22 hours', 'ended')`;

	await page.goto('/');
	await expect(page.getByTestId('home-building')).toBeVisible();
	await expect(page.getByRole('heading', { name: 'What people are building' })).toBeVisible();
	await expect(page.getByTestId('nearby-feed')).toHaveCount(0);
	await expect(page.getByText(/quiet/i)).toHaveCount(0);

	// Nearby with nobody live falls back to projects (mockup #quiet-feed, none live).
	await page.goto('/nearby');
	await expect(page.getByTestId('nearby-projects')).toBeVisible();
	await expect(page.getByText('What people are building')).toBeVisible();
	await expect(page.getByText(/quiet/i)).toHaveCount(0);

	await sql`insert into post (name, activity, location, latitude, longitude, hours, created_at, start_time, ends_at, status)
		values ('Sam', 'live now', 'Bean Theory', 33.976, -118.417, 2, now(), now(), now() + interval '2 hours', 'live')`;
	await page.goto('/');
	await expect(page.getByTestId('live-now')).toBeVisible();
	await expect(page.getByTestId('nearby-feed')).toHaveCount(0);
	// Someone live: Nearby is the photo feed of this week's postups.
	await page.goto('/nearby');
	await expect(page.getByTestId('nearby-feed')).toBeVisible();
	await expect(page.getByText(tag)).toBeVisible();
	await expect(page.getByText(/postups? nearby this week/)).toBeVisible();
	await sql`update post set status='ended' where activity='live now'`;

	const api = await page.request.get('/api/feed?lat=33.976&lng=-118.417');
	expect((await api.json()).items.length).toBeGreaterThan(0);
	await sql.end();
});
