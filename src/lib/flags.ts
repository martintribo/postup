import { env } from '$env/dynamic/public';

/** Feature flags. Each reads PUBLIC_FF_<NAME>. On phase/final every flag is ON by default;
 *  set PUBLIC_FF_<NAME>=0 to turn one off. */
const NAMES = ['oauth', 'projects_v2', 'agent_api', 'places_v2', 'feed_home', 'join', 'chat', 'webpush', 'email_alerts', 'share_links'] as const;
export type FlagName = (typeof NAMES)[number];

export function flag(name: FlagName): boolean {
	const v = env[`PUBLIC_FF_${name.toUpperCase()}`];
	if (v === undefined || v === '') return true;
	return !(v === '0' || v === 'false' || v === 'off');
}

export function allFlags(): Record<FlagName, boolean> {
	return Object.fromEntries(NAMES.map((n) => [n, flag(n)])) as Record<FlagName, boolean>;
}
