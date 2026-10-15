import { expect, it, vi } from 'vitest';

// Regression: config.ts called isTheme() before THEMES was declared. That throws
// ("Cannot access 'THEMES' before initialization") only when PUBLIC_THEME is set,
// which the Hub worktrees do and the test env did not.
vi.mock('$env/dynamic/public', () => ({ env: { PUBLIC_THEME: 'bold', PUBLIC_THEME_AUTO_DARK: '1' } }));

it('config imports with PUBLIC_THEME set', async () => {
	const { config, isTheme } = await import('./config');
	expect(config.theme).toBe('bold');
	expect(config.autoDark).toBe(true);
	expect(isTheme('nonsense')).toBe(false);
});
