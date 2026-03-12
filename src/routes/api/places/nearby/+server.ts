import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';
import { PUBLIC_MAPBOX_ACCESS_TOKEN } from '$env/static/public';
import { db } from '$lib/server/db';
import { place } from '$lib/server/db/schema';
import { and, gte, lte, eq } from 'drizzle-orm';
import { isCurrentlyOpen, type OpenPeriod } from '$lib/server/places';

export interface NearbyPlace {
	id: number;
	mapboxId: string | null;
	name: string;
	address: string;
	latitude: number;
	longitude: number;
	category: string | null;
	distance?: number;
	claimed: boolean;
	isOpen: boolean | null;
	closesAt: string | null;
	opensAt: string | null;
	website: string | null;
	phone: string | null;
	photoRef: string | null;
}

/** Upsert Mapbox results into the place table. Returns nothing — we query DB separately. */
async function upsertMapboxResults(features: any[]) {
	if (features.length === 0) return;

	for (const f of features) {
		const props = f.properties || {};
		const coords = f.geometry?.coordinates || [0, 0];
		const mbId = props.mapbox_id || '';
		if (!mbId) continue;

		const metadata = props.metadata || {};
		const periods = metadata.open_hours?.periods || null;
		const website = metadata.website || null;
		const phone = metadata.phone || null;

		// Check if exists
		const [existing] = await db
			.select({ id: place.id })
			.from(place)
			.where(eq(place.mapboxId, mbId))
			.limit(1);

		if (existing) {
			// Update with fresh data from Mapbox
			await db.update(place)
				.set({
					name: props.name || 'Unknown',
					address: props.full_address || props.address || '',
					latitude: coords[1],
					longitude: coords[0],
					category: 'cafe',
					openHours: periods,
					website,
					phone,
					updatedAt: new Date()
				})
				.where(eq(place.mapboxId, mbId));
		} else {
			// Insert new place
			await db.insert(place).values({
				name: props.name || 'Unknown',
				address: props.full_address || props.address || '',
				latitude: coords[1],
				longitude: coords[0],
				mapboxId: mbId,
				category: 'cafe',
				openHours: periods,
				website,
				phone
			});
		}
	}
}

/** Query all places from DB within a bounding box */
async function queryPlacesInBounds(swLat: number, swLng: number, neLat: number, neLng: number) {
	return db
		.select()
		.from(place)
		.where(
			and(
				gte(place.latitude, swLat),
				lte(place.latitude, neLat),
				gte(place.longitude, swLng),
				lte(place.longitude, neLng)
			)
		);
}

/** Query all places from DB within a radius (used for lat/lng proximity queries) */
async function queryPlacesNearby(lat: number, lng: number, radiusMiles: number = 20) {
	// Approximate bounding box for the radius
	const latOffset = radiusMiles / 69;
	const lonOffset = radiusMiles / (69 * Math.cos((lat * Math.PI) / 180));
	return queryPlacesInBounds(
		lat - latOffset,
		lng - lonOffset,
		lat + latOffset,
		lng + lonOffset
	);
}

export const GET: RequestHandler = async ({ url }) => {
	const lat = parseFloat(url.searchParams.get('lat') || '');
	const lng = parseFloat(url.searchParams.get('lng') || '');
	const tzOffsetParam = url.searchParams.get('tz');
	const tzOffset = tzOffsetParam ? parseInt(tzOffsetParam, 10) : undefined;
	const openOnly = url.searchParams.get('open') === 'true';
	const bbox = url.searchParams.get('bbox');

	if (!bbox && (isNaN(lat) || isNaN(lng))) {
		return json({ error: 'lat/lng or bbox required' }, { status: 400 });
	}

	const accessToken = privateEnv.MAPBOX_ACCESS_TOKEN || PUBLIC_MAPBOX_ACCESS_TOKEN;

	// 1. Try to fetch fresh data from Mapbox (non-blocking — failures fall back to DB cache)
	if (accessToken) {
		try {
			const params = new URLSearchParams({
				access_token: accessToken,
				limit: '25',
				language: 'en'
			});

			if (bbox) {
				params.set('bbox', bbox);
			} else {
				params.set('proximity', `${lng},${lat}`);
			}

			const response = await fetch(
				`https://api.mapbox.com/search/searchbox/v1/category/cafe?${params.toString()}`
			);

			if (response.ok) {
				const data = await response.json();
				const features = data.features || [];
				await upsertMapboxResults(features);
			} else {
				console.warn('Mapbox category search error:', response.status);
			}
		} catch (err) {
			console.warn('Mapbox fetch failed, serving from DB cache:', err);
		}
	}

	try {
		// 2. Query our DB for ALL places in the area
		let dbPlaces;
		if (bbox) {
			const [swLng, swLat, neLng, neLat] = bbox.split(',').map(Number);
			dbPlaces = await queryPlacesInBounds(swLat, swLng, neLat, neLng);
		} else {
			dbPlaces = await queryPlacesNearby(lat, lng);
		}

		// 3. Compute open/closed status from stored openHours and return
		const places: NearbyPlace[] = dbPlaces.map((p) => {
			let hours: { isOpen: boolean | null; closesAt: string | null; opensAt: string | null } = { isOpen: null, closesAt: null, opensAt: null };
			try {
				const periods = Array.isArray(p.openHours) ? (p.openHours as OpenPeriod[]) : null;
				if (periods) {
					hours = isCurrentlyOpen(periods, tzOffset);
				}
			} catch {
				// Bad hours data — treat as unknown
			}

			return {
				id: p.id,
				mapboxId: p.mapboxId,
				name: p.name,
				address: p.address,
				latitude: p.latitude,
				longitude: p.longitude,
				category: p.category,
				claimed: p.createdBy !== null || p.sessionId !== null,
				isOpen: hours.isOpen,
				closesAt: hours.closesAt,
				opensAt: hours.opensAt,
				website: p.website,
				phone: p.phone,
				photoRef: p.photoRef
			};
		});

		const filtered = openOnly ? places.filter((p) => p.isOpen === true) : places;

		return json({ places: filtered });
	} catch (err) {
		console.error('Places search error:', err);
		return json({ error: 'Internal error' }, { status: 500 });
	}
};
