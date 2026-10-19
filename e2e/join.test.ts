import { expect, test, type Browser } from '@playwright/test';
import postgres from 'postgres';

async function as(browser: Browser, origin: string, id: string, name: string) {
	const ctx = await browser.newContext();
	const page = await ctx.newPage();
	await page.goto(`${origin}/auth/mock?id=${id}&name=${encodeURIComponent(name)}`);
	return { ctx, page };
}

test('open join and ask-to-join with approval, alerts, cafe hidden until approved', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1' || process.env.PUBLIC_FF_JOIN !== '1', 'needs mock oauth + ff join');
	const sql = postgres(process.env.DATABASE_URL!);
	const t = Date.now();
	await page.goto(`/auth/mock?id=owner-${t}&name=Maya%20Owner`);
	const origin = new URL(page.url()).origin;
	const create = (activity: string) =>
		page.request.post('/?/create', {
			headers: { 'content-type': 'application/x-www-form-urlencoded', origin },
			data: new URLSearchParams({ activity, location: 'Bean Theory', latitude: '33.976', longitude: '-118.417', hours: '2' }).toString()
		});
	await create(`open-${t}`);
	await create(`ask-${t}`);
	const [openP] = await sql`select id from post where activity=${'open-' + t}`;
	const [askP] = await sql`select id from post where activity=${'ask-' + t}`;
	await sql`update post set join_mode='ask', capacity=1, neighborhood='Playa Vista' where id=${askP.id}`;

	// Open mode: instant join, poster alerted.
	const sam = await as(browser, origin, `sam-${t}`, 'Sam Joiner');
	await sam.page.goto(`${origin}/postups/${openP.id}`);
	await sam.page.getByRole('button', { name: 'Join', exact: true }).click();
	await expect(sam.page.getByTestId('joined')).toBeVisible();

	// Ask mode: cafe hidden, reason required, then approval reveals cafe.
	await sam.page.goto(`${origin}/postups/${askP.id}`);
	await expect(sam.page.getByText('a cafe in Playa Vista')).toBeVisible();
	await expect(sam.page.getByText('Bean Theory')).toHaveCount(0);
	await sam.page.getByRole('button', { name: 'Ask to join' }).click();
	await expect(sam.page.getByRole('button', { name: 'Send request' })).toBeDisabled();
	await sam.page.locator('textarea[name=reason]').fill('Also building a mod, happy to pair');
	await sam.page.getByRole('button', { name: 'Send request' }).click();
	await expect(sam.page.getByTestId('requested')).toBeVisible();

	await page.goto('/');
	// Mockup nav shows a dot, not a count; the two alerts are checked in the DB.
	await expect(page.getByTestId('unread').first()).toBeAttached();
	const [{ n: alerts }] = await sql`select count(*)::int as n from notification n join oauth_account o on o.user_id=n.user_id where o.provider_user_id=${'owner-' + t} and n.read_at is null`;
	expect(alerts).toBe(2);
	await page.goto(`/postups/${askP.id}`);
	await expect(page.getByTestId('requests')).toContainText('Also building a mod');
	await page.getByRole('button', { name: 'Approve' }).click();
	await expect(page.getByTestId('requests')).toHaveCount(0);
	await expect(page.getByText('On the way')).toBeVisible();

	await sam.page.reload();
	await expect(sam.page.getByTestId('joined')).toBeVisible();
	await expect(sam.page.getByTestId('join-box').getByText('Bean Theory')).toBeVisible();
	await sam.page.goto(`${origin}/activity`);
	await expect(sam.page.getByText(/You're in!/)).toBeVisible();

	// Capacity 1 now reached: a third person sees "full".
	const kim = await as(browser, origin, `kim-${t}`, 'Kim');
	await kim.page.goto(`${origin}/postups/${askP.id}`);
	await expect(kim.page.getByTestId('full')).toBeVisible();

	// Owner removes Sam; Sam's alert says so.
	await page.reload();
	await page.getByRole('button', { name: /^Remove / }).click();
	await expect(page.getByText('On the way')).toHaveCount(0);
	const [n] = await sql`select n.type from notification n join oauth_account o on o.user_id=n.user_id where o.provider_user_id=${'sam-' + t} order by n.id desc limit 1`;
	expect(n.type).toBe('removed');

	await page.goto(`/activity`);
	await expect(page.getByText(/asked to join/)).toBeVisible();
	await expect(page.getByText(/is joining you/)).toBeVisible();
	for (const x of [sam, kim]) await x.ctx.close();
	await sql.end();
});

test('ask-to-join postups never leak the cafe on home or the cafe page', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1' || process.env.PUBLIC_FF_JOIN !== '1', 'needs mock oauth + ff join');
	const sql = postgres(process.env.DATABASE_URL!);
	const t = Date.now();
	await sql`update post set status='ended' where status='live'`;
	await sql`insert into place (name, address, latitude, longitude, created_at, updated_at) values (${'Secret Cafe ' + t}, 'x', 33.97612, -118.41734, now(), now())`;
	const [pl] = await sql`select id from place where name=${'Secret Cafe ' + t}`;
	await page.goto(`/auth/mock?id=own2-${t}&name=Owner2`);
	const [u] = await sql`select user_id from oauth_account where provider_user_id=${'own2-' + t}`;
	await sql`insert into post (name, activity, location, latitude, longitude, hours, created_at, start_time, ends_at, status, join_mode, neighborhood, place_id, user_id)
		values ('Owner2', ${'hush-' + t}, ${'Secret Cafe ' + t}, 33.97612, -118.41734, 2, now(), now(), now() + interval '2 hours', 'live', 'ask', 'Playa Vista', ${pl.id}, ${u.user_id})`;

	const ctx = await browser.newContext();
	const s = await ctx.newPage();
	const origin = new URL(page.url()).origin;
	const html = await (await s.request.get(`${origin}/__data.json?x-sveltekit-invalidated=11`)).text();
	expect(html).toContain('a cafe in Playa Vista');
	expect(html).not.toContain('Secret Cafe ' + t);
	expect(html).not.toContain('33.97612');
	const cafe = await (await s.request.get(`${origin}/places/${pl.id}`)).text();
	expect(cafe).not.toContain('hush-' + t);
	// The poster still sees their own exact postup.
	const own = await (await page.request.get('/places/' + pl.id)).text();
	expect(own).toContain('hush-' + t);
	await sql`update post set status='ended' where activity=${'hush-' + t}`;
	await ctx.close();
	await sql.end();
});
