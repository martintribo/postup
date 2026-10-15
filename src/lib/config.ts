import { env } from '$env/dynamic/public';

/**
 * Product defaults for decisions still pending with Martin (see implementation-plan.md).
 * Each can be overridden with a PUBLIC_* env var without a code change.
 */
// Declared before `config`: it calls isTheme() at import time (TDZ otherwise).
export const THEMES = ['fresh', 'cozy', 'night', 'bold'] as const;
export type Theme = (typeof THEMES)[number];

export function isTheme(t: string | null | undefined): t is Theme {
	return !!t && (THEMES as readonly string[]).includes(t);
}

export const config = {
	/** D1 launch area: Playa Vista / Westside LA (recommended default). */
	launchArea: {
		name: env.PUBLIC_LAUNCH_AREA_NAME || 'Westside, Los Angeles',
		latitude: Number(env.PUBLIC_LAUNCH_AREA_LAT || 33.9765),
		longitude: Number(env.PUBLIC_LAUNCH_AREA_LNG || -118.4176)
	},
	/** D8 style: Fresh by default; cozy | night | bold are the other candidates. */
	theme: (isTheme(env.PUBLIC_THEME) ? env.PUBLIC_THEME : 'fresh') as Theme,
	/** Use Night when the OS is in dark mode and nobody picked a style. Off by default. */
	autoDark: env.PUBLIC_THEME_AUTO_DARK === '1',
	/** Floating style switcher. Always on in `vite dev`; set PUBLIC_STYLE_SWITCHER=1 to show it on a preview build. */
	styleSwitcher: env.PUBLIC_STYLE_SWITCHER === '1'
};
