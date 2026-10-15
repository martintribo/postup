import { env } from '$env/dynamic/public';

/** Feature flags. Each reads PUBLIC_FF_<NAME>=1. Off by default, so prod is unchanged until set. */
const NAMES = ['oauth', 'projects_v2', 'agent_api', 'places_v2', 'feed_home', 'join', 'chat', 'webpush', 'email_alerts', 'share_links'] as const;
export type FlagName = (typeof NAMES)[number];

export function flag(name: FlagName): boolean {
	const v = env[`PUBLIC_FF_${name.toUpperCase()}`];
	return v === '1' || v === 'true';
}

export function allFlags(): Record<FlagName, boolean> {
	return Object.fromEntries(NAMES.map((n) => [n, flag(n)])) as Record<FlagName, boolean>;
}
