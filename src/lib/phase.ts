import { env } from '$env/dynamic/public';

/** Product phase. This branch ships phase 0 (smallest MVP). PUBLIC_PHASE=1 or 2 turns later work back on. */
export type Phase = 0 | 1 | 2;

export function phase(): Phase {
	const v = env.PUBLIC_PHASE;
	if (v === '1') return 1;
	if (v === '2') return 2;
	return 0;
}
