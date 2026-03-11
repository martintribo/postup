import type { PageServerLoad, Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { place } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';

export const load: PageServerLoad = async ({ url }) => {
	return {
		prefill: {
			mapboxId: url.searchParams.get('mapboxId') || '',
			name: url.searchParams.get('name') || '',
			address: url.searchParams.get('address') || '',
			latitude: parseFloat(url.searchParams.get('lat') || '0'),
			longitude: parseFloat(url.searchParams.get('lng') || '0')
		}
	};
};

export const actions: Actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const name = (formData.get('name') as string)?.trim();
		const address = (formData.get('address') as string)?.trim();
		const mapboxId = (formData.get('mapboxId') as string)?.trim() || null;
		const category = (formData.get('category') as string)?.trim() || 'cafe';
		const latitude = parseFloat(formData.get('latitude') as string);
		const longitude = parseFloat(formData.get('longitude') as string);

		if (!name || !address || isNaN(latitude) || isNaN(longitude)) {
			return fail(400, { message: 'Name, address, and coordinates are required' });
		}

		// Check if place already exists by mapboxId
		if (mapboxId) {
			const [existing] = await db.select().from(place).where(eq(place.mapboxId, mapboxId));
			if (existing) {
				throw redirect(302, `/places/${existing.id}`);
			}
		}

		const [newPlace] = await db.insert(place).values({
			name,
			address,
			latitude,
			longitude,
			mapboxId,
			category,
			sessionId: event.locals.anonymousSessionId,
			createdBy: event.locals.user?.id ?? null
		}).returning();

		throw redirect(302, `/places/${newPlace.id}`);
	}
};
