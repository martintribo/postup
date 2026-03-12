import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';
import { PUBLIC_MAPBOX_ACCESS_TOKEN } from '$env/static/public';
import { db } from '$lib/server/db';
import { place } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';
import { isCurrentlyOpen } from '$lib/server/places';

async function fetchGooglePhoto(name: string, lat: number, lng: number, googleApiKey: string): Promise<{ googlePlaceId: string; photoRef: string } | null> {
	try {
		const response = await fetch('https://places.googleapis.com/v1/places:searchText', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-Goog-Api-Key': googleApiKey,
				'X-Goog-FieldMask': 'places.id,places.photos'
			},
			body: JSON.stringify({
				textQuery: name,
				locationBias: {
					circle: { center: { latitude: lat, longitude: lng }, radius: 200 }
				},
				maxResultCount: 1
			})
		});

		if (!response.ok) return null;

		const data = await response.json();
		const gPlace = data.places?.[0];
		if (!gPlace?.photos?.[0]?.name) return null;

		return {
			googlePlaceId: gPlace.id,
			photoRef: gPlace.photos[0].name
		};
	} catch {
		return null;
	}
}

export const GET: RequestHandler = async ({ url }) => {
	const id = parseInt(url.searchParams.get('id') || '', 10);
	const tzOffsetParam = url.searchParams.get('tz');
	const tzOffset = tzOffsetParam ? parseInt(tzOffsetParam, 10) : undefined;

	if (isNaN(id)) {
		return json({ error: 'id required' }, { status: 400 });
	}

	const [existing] = await db.select().from(place).where(eq(place.id, id)).limit(1);
	if (!existing) {
		return json({ error: 'Place not found' }, { status: 404 });
	}

	const accessToken = privateEnv.MAPBOX_ACCESS_TOKEN || PUBLIC_MAPBOX_ACCESS_TOKEN;

	// 1. Refresh from Mapbox
	if (accessToken && existing.mapboxId) {
		try {
			const latOffset = 0.005;
			const lngOffset = 0.005 / Math.cos((existing.latitude * Math.PI) / 180);
			const bbox = `${existing.longitude - lngOffset},${existing.latitude - latOffset},${existing.longitude + lngOffset},${existing.latitude + latOffset}`;

			const params = new URLSearchParams({
				access_token: accessToken,
				limit: '25',
				language: 'en',
				bbox
			});

			const response = await fetch(
				`https://api.mapbox.com/search/searchbox/v1/category/cafe?${params.toString()}`
			);

			if (response.ok) {
				const data = await response.json();
				const match = (data.features || []).find(
					(f: any) => f.properties?.mapbox_id === existing.mapboxId
				);

				if (match) {
					const props = match.properties || {};
					const metadata = props.metadata || {};
					const coords = match.geometry?.coordinates || [existing.longitude, existing.latitude];

					await db.update(place)
						.set({
							name: props.name || existing.name,
							address: props.full_address || props.address || existing.address,
							latitude: coords[1],
							longitude: coords[0],
							openHours: metadata.open_hours?.periods || existing.openHours,
							website: metadata.website ?? existing.website,
							phone: metadata.phone ?? existing.phone,
							updatedAt: new Date()
						})
						.where(eq(place.id, id));
				}
			}
		} catch (err) {
			console.warn('Failed to refresh place from Mapbox:', err);
		}
	}

	// 2. Fetch photo from Google Places if we don't have one cached
	const googleApiKey = privateEnv.GOOGLE_PLACES_API_KEY;
	if (googleApiKey && !existing.photoRef) {
		const photo = await fetchGooglePhoto(existing.name, existing.latitude, existing.longitude, googleApiKey);
		if (photo) {
			await db.update(place)
				.set({
					googlePlaceId: photo.googlePlaceId,
					photoRef: photo.photoRef
				})
				.where(eq(place.id, id));
		}
	}

	// 3. Return the latest data
	const [updated] = await db.select().from(place).where(eq(place.id, id)).limit(1);
	if (!updated) {
		return json({ error: 'Place not found' }, { status: 404 });
	}

	let hours: { isOpen: boolean | null; closesAt: string | null; opensAt: string | null } = { isOpen: null, closesAt: null, opensAt: null };
	try {
		const periods = Array.isArray(updated.openHours) ? updated.openHours : null;
		if (periods) {
			hours = isCurrentlyOpen(periods as any, tzOffset);
		}
	} catch {
		// Bad hours data
	}

	return json({
		place: {
			id: updated.id,
			mapboxId: updated.mapboxId,
			name: updated.name,
			address: updated.address,
			latitude: updated.latitude,
			longitude: updated.longitude,
			category: updated.category,
			claimed: updated.createdBy !== null || updated.sessionId !== null,
			isOpen: hours.isOpen,
			closesAt: hours.closesAt,
			opensAt: hours.opensAt,
			website: updated.website,
			phone: updated.phone,
			photoRef: updated.photoRef
		}
	});
};
