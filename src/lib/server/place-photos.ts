import { env } from '$env/dynamic/private';
import { db } from '$lib/server/db';
import { place, type Place } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';
import { archiveConfigured, putArchiveObject } from '$lib/server/photo-archive';

const MONTH_MS = 30 * 24 * 60 * 60 * 1000;
const uriCache = new Map<number, { uri: string; name: string; exp: number }>();

function googleKey(): string | null {
	return env.GOOGLE_PLACES_API_KEY || null;
}

async function placeDetailsPhotoName(googlePlaceId: string, key: string): Promise<string | null> {
	const res = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(googlePlaceId)}`, {
		headers: {
			'X-Goog-Api-Key': key,
			'X-Goog-FieldMask': 'photos'
		}
	});
	if (!res.ok) return null;
	const data = (await res.json()) as { photos?: { name?: string }[] };
	return data.photos?.[0]?.name || null;
}

async function searchTextPhoto(
	name: string,
	lat: number,
	lng: number,
	key: string
): Promise<{ googlePlaceId: string; photoName: string } | null> {
	const res = await fetch('https://places.googleapis.com/v1/places:searchText', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-Goog-Api-Key': key,
			'X-Goog-FieldMask': 'places.id,places.photos'
		},
		body: JSON.stringify({
			textQuery: name,
			locationBias: { circle: { center: { latitude: lat, longitude: lng }, radius: 200 } },
			maxResultCount: 1
		})
	});
	if (!res.ok) return null;
	const data = (await res.json()) as {
		places?: { id?: string; photos?: { name?: string }[] }[];
	};
	const gPlace = data.places?.[0];
	const photoName = gPlace?.photos?.[0]?.name;
	const id = gPlace?.id;
	if (!id || !photoName) return null;
	return { googlePlaceId: id, photoName };
}

async function mediaPhotoUri(photoName: string, key: string): Promise<string | null> {
	const url = `https://places.googleapis.com/v1/${photoName}/media?maxWidthPx=800&skipHttpRedirect=true`;
	const res = await fetch(url, { headers: { 'X-Goog-Api-Key': key } });
	if (!res.ok) return null;
	const data = (await res.json()) as { photoUri?: string };
	return data.photoUri || null;
}

export async function resolveLivePhoto(row: Place): Promise<{ name: string; photoUri: string } | null> {
	const key = googleKey();
	if (!key) return null;

	const cached = uriCache.get(row.id);
	if (cached && cached.exp > Date.now()) {
		return { name: cached.name, photoUri: cached.uri };
	}

	let photoName: string | null = null;
	let googlePlaceId = row.googlePlaceId;

	if (googlePlaceId) {
		photoName = await placeDetailsPhotoName(googlePlaceId, key);
	}
	if (!photoName) {
		const found = await searchTextPhoto(row.name, row.latitude, row.longitude, key);
		if (found) {
			googlePlaceId = found.googlePlaceId;
			photoName = found.photoName;
		}
	}
	if (!photoName) return null;

	const photoUri = await mediaPhotoUri(photoName, key);
	if (!photoUri) return null;

	uriCache.set(row.id, { uri: photoUri, name: photoName, exp: Date.now() + 60 * 60 * 1000 });

	if (googlePlaceId !== row.googlePlaceId || photoName !== row.photoRef) {
		await db
			.update(place)
			.set({
				googlePlaceId: googlePlaceId ?? row.googlePlaceId,
				photoRef: photoName,
				updatedAt: new Date()
			})
			.where(eq(place.id, row.id));
	}

	return { name: photoName, photoUri };
}

function shouldArchive(row: Place, photoName: string): boolean {
	if (!archiveConfigured()) return false;
	if (row.photoArchiveKey && row.photoRef === photoName) return false;
	if (row.photoArchivedAt && Date.now() - row.photoArchivedAt.getTime() < MONTH_MS) return false;
	return true;
}

async function headEtag(url: string): Promise<string | null> {
	try {
		const res = await fetch(url, { method: 'HEAD' });
		return res.headers.get('etag');
	} catch {
		return null;
	}
}

export function schedulePersonalArchive(row: Place, photo: { name: string; photoUri: string }) {
	if (!shouldArchive(row, photo.name)) return;
	void archivePlacePhoto(row, photo).catch((err) => {
		console.warn('personal photo archive failed', row.id, err);
	});
}

async function archivePlacePhoto(row: Place, photo: { name: string; photoUri: string }) {
	const etag = await headEtag(photo.photoUri);
	if (etag && row.photoEtag === etag && row.photoArchiveKey) {
		await db
			.update(place)
			.set({ photoRef: photo.name, photoArchivedAt: new Date(), updatedAt: new Date() })
			.where(eq(place.id, row.id));
		return;
	}

	const res = await fetch(photo.photoUri);
	if (!res.ok) return;
	const buf = new Uint8Array(await res.arrayBuffer());
	const contentType = res.headers.get('content-type') || 'image/jpeg';
	const gotEtag = res.headers.get('etag') || etag;
	const key = `places/${row.id}/${photo.name.replace(/[^A-Za-z0-9._-]+/g, '_').slice(-80)}.jpg`;
	await putArchiveObject(key, buf, contentType, gotEtag);
	await db
		.update(place)
		.set({
			photoRef: photo.name,
			photoArchiveKey: key,
			photoArchivedAt: new Date(),
			photoEtag: gotEtag,
			updatedAt: new Date()
		})
		.where(eq(place.id, row.id));
}
