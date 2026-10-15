import { expect, test } from '@playwright/test';

test('home has title and description', async ({ page }) => {
	await page.goto('/');
	await expect(page).toHaveTitle(/PostUp/);
	await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /cafe/);
});

test('projects page hides hidden projects', async ({ page }) => {
	await page.goto('/projects');
	await expect(page.getByText('HIDDEN-E2E-PROJECT')).toHaveCount(0);
	await expect(page.getByText('Visible Seed Project')).toBeVisible();
});

test('theme override via ?theme=bold', async ({ page }) => {
	await page.goto('/?theme=bold');
	await expect(page.locator('html')).toHaveAttribute('data-theme', 'bold');
});
