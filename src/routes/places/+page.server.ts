import type { PageServerLoad } from './$types';
import { db } from '$lib/server/db';
import { place, placeReview, placeTag, post } from '$lib/server/db/schema';
import { desc, eq, sql, avg, count } from 'drizzle-orm';
import { getUserLocation } from '$lib/server/location';

export const load: PageServerLoad = async (event) => {
	const { location } = await getUserLocation(event);

	const places = await db
		.select({
			id: place.id,
			name: place.name,
			address: place.address,
			latitude: place.latitude,
			longitude: place.longitude,
			category: place.category,
			createdAt: place.createdAt,
			avgRating: sql<number>`coalesce(avg(${placeReview.rating}), 0)`.as('avg_rating'),
			reviewCount: sql<number>`count(distinct ${placeReview.id})`.as('review_count'),
			avgWifi: sql<number>`coalesce(avg(${placeReview.wifiRating}), 0)`.as('avg_wifi'),
			distance: sql<number>`(3959 * acos(cos(radians(${location.latitude})) * cos(radians(${place.latitude})) * cos(radians(${place.longitude}) - radians(${location.longitude})) + sin(radians(${location.latitude})) * sin(radians(${place.latitude}))))`.as('distance')
		})
		.from(place)
		.leftJoin(placeReview, eq(placeReview.placeId, place.id))
		.groupBy(place.id)
		.orderBy(sql`distance`);

	// Get tags for all places
	const allTags = await db
		.select()
		.from(placeTag)
		.orderBy(desc(placeTag.votes));

	// Group tags by place
	const tagsByPlace = new Map<number, typeof allTags>();
	for (const tag of allTags) {
		const existing = tagsByPlace.get(tag.placeId) || [];
		existing.push(tag);
		tagsByPlace.set(tag.placeId, existing);
	}

	const placesWithTags = places.map((p) => ({
		...p,
		avgRating: Number(p.avgRating),
		avgWifi: Number(p.avgWifi),
		reviewCount: Number(p.reviewCount),
		distance: Number(p.distance),
		tags: (tagsByPlace.get(p.id) || []).map((t) => t.tag)
	}));

	return {
		places: placesWithTags,
		location
	};
};
