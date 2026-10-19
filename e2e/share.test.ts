import { expect, test } from '@playwright/test';
import postgres from 'postgres';

test('shared postup and project links render previews and lead to join', async ({ page, browser }) => {
	test.skip(process.env.OAUTH_MOCK !== '1' || process.env.PUBLIC_FF_SHARE_LINKS !== '1', 'needs mock + share');
	const sql = postgres(process.env.DATABASE_URL!);
	const t = Date.now();
	await page.goto(`/auth/mock?id=sh-${t}&name=Maya%20Share`);
	const origin = new URL(page.url()).origin;
	await sql`insert into project (name, short_description, description, created_at, updated_at, user_id)
		select ${'Star Fox ' + t}, 'N64 mod', 'd', now(), now(), user_id from oauth_account where provider_user_id=${'sh-' + t}`;
	const [pr] = await sql`select id from project where name=${'Star Fox ' + t}`;
	await page.request.post('/?/create', { headers: { 'content-type': 'application/x-www-form-urlencoded', origin }, data: new URLSearchParams({ activity: `share-${t}`, location: 'Bean Theory', latitude: '33.976', longitude: '-118.417', hours: '2', projectId: String(pr.id) }).toString() });
	const [p] = await sql`select id, project_id from post where activity=${'share-' + t}`;
	if (!p.project_id) await sql`update post set project_id=${pr.id} where id=${p.id}`;

	await page.goto(`/postups/${p.id}?posted=1`);
	await expect(page.getByTestId('share')).toContainText('Invite friends');

	// A logged-out friend opens the link: SSR'd preview tags + invite copy.
	const ctx = await browser.newContext();
	const f = await ctx.newPage();
	const html = await (await f.request.get(`${origin}/p/${p.id}`)).text();
	expect(html).toMatch(/<meta property="og:title" content="Maya Share is working at Bean Theory/);
	expect(html).toContain(`share-${t}`);
	await f.goto(`${origin}/p/${p.id}`);
	await expect(f.getByTestId('invite')).toContainText('Join Maya?');
	// Signed out: Join opens the sign-in sheet over the invite (mockup #invite → #join-signin).
	await f.getByTestId('invite-join').click();
	await expect(f.getByTestId('signin-sheet')).toContainText("Sign in so Maya knows who's coming.");

	const proj = await (await f.request.get(`${origin}/projects/${pr.id}`)).text();
	expect(proj).toMatch(/og:title" content="Maya Share is building Star Fox/);
	await f.goto(`${origin}/projects/${pr.id}?s=1`);
	await expect(f.getByText('Live now · join them')).toBeVisible();
	await f.goto(`${origin}/projects/${pr.id}`);
	await f.getByTestId('share').click();
	await expect(f.getByTestId('share-sheet')).toContainText(`/projects/${pr.id}?s=1`);

	await sql`update post set status='ended' where id=${p.id}`;
	await f.goto(`${origin}/p/${p.id}`);
	await expect(f.getByTestId('invite-ended')).toBeVisible();
	await ctx.close();
	await sql.end();
});
