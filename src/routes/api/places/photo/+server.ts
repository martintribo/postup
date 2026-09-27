import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';
import { error, redirect } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { place } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';
import { resolveLivePhoto, schedulePersonalArchive } from '$lib/server/place-photos';

export const GET: RequestHandler = async ({ url }) => {
	if (!privateEnv.GOOGLE_PLACES_API_KEY) {
		throw error(500, 'Google Places not configured');
	}

	const id = parseInt(url.searchParams.get('id') || '', 10);
	if (Number.isNaN(id)) {
		throw error(400, 'id required');
	}

	const [row] = await db.select().from(place).where(eq(place.id, id)).limit(1);
	if (!row) {
		throw error(404, 'Place not found');
	}

	const live = await resolveLivePhoto(row);
	if (!live) {
		throw error(404, 'No photo');
	}

	schedulePersonalArchive(row, live);

	throw redirect(302, live.photoUri);
};
