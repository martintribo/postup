import { env } from '$env/dynamic/public';

/**
 * Product defaults for decisions still pending with Martin (see implementation-plan.md).
 * Each can be overridden with a PUBLIC_* env var without a code change.
 */
export const config = {
	/** D1 launch area: Playa Vista / Westside LA (recommended default). */
	launchArea: {
		name: env.PUBLIC_LAUNCH_AREA_NAME || 'Westside, Los Angeles',
		latitude: Number(env.PUBLIC_LAUNCH_AREA_LAT || 33.9765),
		longitude: Number(env.PUBLIC_LAUNCH_AREA_LNG || -118.4176)
	},
	/** D8 style: Fresh by default; 'bold' is the other candidate. */
	theme: (env.PUBLIC_THEME || 'fresh') as Theme
};

export const THEMES = ['fresh', 'bold'] as const;
export type Theme = (typeof THEMES)[number];

export function isTheme(t: string | null | undefined): t is Theme {
	return !!t && (THEMES as readonly string[]).includes(t);
}
