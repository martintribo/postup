import { env } from '$env/dynamic/public';

/** How far a cafe can be from the person and still count as "where you are". Best effort. [M1039] */
export function maxPostMiles(): number {
	const n = Number(env.PUBLIC_POST_MAX_MILES);
	return Number.isFinite(n) && n > 0 ? n : 0.5;
}

export interface LatLng {
	latitude: number;
	longitude: number;
}

export function milesBetween(a: LatLng, b: LatLng): number {
	const R = 3959;
	const dLat = ((b.latitude - a.latitude) * Math.PI) / 180;
	const dLon = ((b.longitude - a.longitude) * Math.PI) / 180;
	const h =
		Math.sin(dLat / 2) ** 2 +
		Math.cos((a.latitude * Math.PI) / 180) * Math.cos((b.latitude * Math.PI) / 180) * Math.sin(dLon / 2) ** 2;
	return R * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));
}

export type DistanceVerdict =
	| { ok: true; miles: number }
	| { ok: false; reason: 'denied' | 'far'; miles: number | null };

/**
 * Posting only works at a place you're at. A denied browser location blocks the post.
 * When the client didn't ask yet, the caller may pass a server guess as `here` with denied=false.
 */
export function distanceVerdict(here: LatLng | null, place: LatLng, opts?: { denied?: boolean; maxMiles?: number }): DistanceVerdict {
	if (opts?.denied || !here) return { ok: false, reason: 'denied', miles: null };
	const miles = milesBetween(here, place);
	const max = opts?.maxMiles ?? maxPostMiles();
	if (miles > max) return { ok: false, reason: 'far', miles };
	return { ok: true, miles };
}
