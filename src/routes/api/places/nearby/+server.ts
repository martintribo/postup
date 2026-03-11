import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';
import { PUBLIC_MAPBOX_ACCESS_TOKEN } from '$env/static/public';
import { db } from '$lib/server/db';
import { place } from '$lib/server/db/schema';
import { sql, inArray } from 'drizzle-orm';

export interface NearbyPlace {
	id?: number; // our DB id, if it exists
	mapboxId: string;
	name: string;
	address: string;
	latitude: number;
	longitude: number;
	category: string | null;
	distance?: number;
	claimed: boolean; // whether it exists in our DB
}

export const GET: RequestHandler = async ({ url }) => {
	const lat = parseFloat(url.searchParams.get('lat') || '');
	const lng = parseFloat(url.searchParams.get('lng') || '');

	if (isNaN(lat) || isNaN(lng)) {
		return json({ error: 'lat and lng required' }, { status: 400 });
	}

	const accessToken = privateEnv.MAPBOX_ACCESS_TOKEN || PUBLIC_MAPBOX_ACCESS_TOKEN;
	if (!accessToken) {
		return json({ error: 'Mapbox not configured' }, { status: 500 });
	}

	try {
		// Use Mapbox Search Box API category search for cafes
		const params = new URLSearchParams({
			access_token: accessToken,
			proximity: `${lng},${lat}`,
			limit: '25',
			language: 'en'
		});

		const response = await fetch(
			`https://api.mapbox.com/search/searchbox/v1/category/cafe?${params.toString()}`
		);

		if (!response.ok) {
			console.error('Mapbox category search error:', response.status, await response.text());
			return json({ error: 'Failed to search places' }, { status: 502 });
		}

		const data = await response.json();
		const features = data.features || [];

		// Check which of these cafes already exist in our DB by mapbox_id
		const mapboxIds = features
			.map((f: any) => f.properties?.mapbox_id)
			.filter(Boolean);

		let existingPlaces: { id: number; mapboxId: string | null }[] = [];
		if (mapboxIds.length > 0) {
			existingPlaces = await db
				.select({ id: place.id, mapboxId: place.mapboxId })
				.from(place)
				.where(inArray(place.mapboxId, mapboxIds));
		}

		const existingMap = new Map(existingPlaces.map((p) => [p.mapboxId, p.id]));

		const places: NearbyPlace[] = features.map((f: any) => {
			const props = f.properties || {};
			const coords = f.geometry?.coordinates || [0, 0]; // [lng, lat]
			const mbId = props.mapbox_id || '';

			return {
				id: existingMap.get(mbId) ?? undefined,
				mapboxId: mbId,
				name: props.name || 'Unknown',
				address: props.full_address || props.address || '',
				latitude: coords[1],
				longitude: coords[0],
				category: 'cafe',
				claimed: existingMap.has(mbId)
			};
		});

		return json({ places });
	} catch (err) {
		console.error('Places search error:', err);
		return json({ error: 'Internal error' }, { status: 500 });
	}
};
