import { expect, test } from '@playwright/test';

test('offline banner, friendly 404, style picker', async ({ page, context }) => {
	await page.goto('/projects');
	await context.setOffline(true);
	await expect(page.getByTestId('offline')).toBeVisible();
	await context.setOffline(false);
	await expect(page.getByTestId('offline')).toHaveCount(0);

	const r = await page.goto('/postups/99999999');
	expect(r?.status()).toBe(404);
	await expect(page.getByTestId('error-page')).toContainText("This isn't here anymore");

	await page.goto('/style');
	await page.getByTestId('pick-bold').click();
	await page.goto('/projects');
	await expect(page.locator('html')).toHaveAttribute('data-theme', 'bold');
});
