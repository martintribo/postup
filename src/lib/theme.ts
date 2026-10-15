import { browser } from '$app/environment';
import { config, isTheme, type Theme } from '$lib/config';

export const THEME_KEY = 'pu-theme';

/** Precedence: ?theme= (preview) > saved choice > OS dark (if enabled) > PUBLIC_THEME default. */
export function resolveTheme(query: string | null): Theme {
	if (isTheme(query)) return query;
	if (browser) {
		const saved = localStorage.getItem(THEME_KEY);
		if (isTheme(saved)) return saved;
		if (config.autoDark && matchMedia('(prefers-color-scheme: dark)').matches) return 'night';
	}
	return config.theme;
}

export function saveTheme(t: Theme | null) {
	if (!browser) return;
	if (t) localStorage.setItem(THEME_KEY, t);
	else localStorage.removeItem(THEME_KEY);
	window.dispatchEvent(new CustomEvent('pu-theme'));
}
