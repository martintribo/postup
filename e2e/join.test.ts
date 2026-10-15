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
	await expect(sam.page.getByRole('alert')).toContainText(/why you want to join/);
	await sam.page.locator('textarea[name=reason]').fill('Also building a mod, happy to pair');
	await sam.page.getByRole('button', { name: 'Ask to join' }).click();
	await expect(sam.page.getByTestId('requested')).toBeVisible();

	await page.goto('/');
	await expect(page.getByTestId('unread')).toHaveText('2');
	await page.goto(`/postups/${askP.id}`);
	await expect(page.getByTestId('requests')).toContainText('Also building a mod');
	await page.getByRole('button', { name: 'Accept' }).click();
	await expect(page.getByTestId('requests')).toContainText('is joining');

	await sam.page.reload();
	await expect(sam.page.getByTestId('joined')).toBeVisible();
	await expect(sam.page.getByText('Bean Theory').first()).toBeVisible();
	await sam.page.goto(`${origin}/activity`);
	await expect(sam.page.getByText(/You're in!/)).toBeVisible();

	// Capacity 1 now reached: a third person sees "full".
	const kim = await as(browser, origin, `kim-${t}`, 'Kim');
	await kim.page.goto(`${origin}/postups/${askP.id}`);
	await expect(kim.page.getByTestId('full')).toBeVisible();

	// Owner removes Sam; Sam's alert says so.
	await page.reload();
	await page.getByRole('button', { name: 'Remove' }).click();
	await expect(page.getByTestId('requests')).toHaveCount(0);
	const [n] = await sql`select n.type from notification n join oauth_account o on o.user_id=n.user_id where o.provider_user_id=${'sam-' + t} order by n.id desc limit 1`;
	expect(n.type).toBe('removed');

	await page.goto(`/activity`);
	await expect(page.getByText(/asked to join/)).toBeVisible();
	await expect(page.getByText(/is joining you/)).toBeVisible();
	for (const x of [sam, kim]) await x.ctx.close();
	await sql.end();
});
