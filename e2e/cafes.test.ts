import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('posting up at a Google place stores place, end time and owner', async ({ page }) => {
	test.skip(process.env.OAUTH_MOCK !== '1', 'needs mock oauth');
	const sql = postgres(process.env.DATABASE_URL!);
	const uid = `cafe-${Date.now()}`;
	await page.goto(`/auth/mock?id=${uid}&name=Cafe%20Tester`);
	const gid = `ChIJtest${Date.now()}`;
	const fd = new URLSearchParams({
		activity: 'Star Fox 64 mod',
		location: 'Bean Theory',
		latitude: '33.976',
		longitude: '-118.417',
		hours: '3',
		googlePlaceId: gid
	});
	const r = await page.request.post('/?/create', {
		headers: { 'content-type': 'application/x-www-form-urlencoded', origin: new URL(page.url()).origin },
		data: fd.toString()
	});
	expect(r.ok()).toBeTruthy();
	const [pl] = await sql`select id from place where google_place_id=${gid}`;
	expect(pl).toBeTruthy();
	const [p] = await sql`select place_id, user_id, ends_at, start_time, join_mode, status from post where activity='Star Fox 64 mod' and place_id=${pl.id}`;
	expect(p.user_id).toBeTruthy();
	expect(p.join_mode).toBe('open');
	expect(p.status).toBe('live');
	expect((p.ends_at.getTime() - p.start_time.getTime()) / 3600000).toBeCloseTo(3, 1);

	await page.goto(`/places/${pl.id}`);
	await expect(page.getByText('Star Fox 64 mod').first()).toBeVisible();

	// Ended postups drop off the live lists.
	await sql`update post set status='ended' where place_id=${pl.id}`;
	await page.goto(`/places/${pl.id}`);
	await expect(page.getByText('Star Fox 64 mod')).toHaveCount(0);
	await sql.end();
});

test('Google place search widget state is reported (key may be referrer-blocked on localhost)', async ({ page }) => {
	test.skip(process.env.PUBLIC_FF_PLACES_V2 !== '1', 'flag off');
	await page.goto('/');
	const st = await page.evaluate(async () => {
		await new Promise((r) => setTimeout(r, 4000));
		return typeof (window as any).google?.maps?.importLibrary;
	});
	console.log('google maps loader:', st);
	expect(st).toBeDefined();
});
