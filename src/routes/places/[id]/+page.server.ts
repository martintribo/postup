import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import { zod4 } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { fail, error } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { place, placeReview, placeTag, post } from '$lib/server/db/schema';
import { desc, eq, sql, and } from 'drizzle-orm';

const reviewSchema = z.object({
	rating: z.number().int().min(1).max(5),
	text: z.string().optional(),
	wifiRating: z.number().int().min(1).max(5).optional(),
	noiseLevel: z.enum(['quiet', 'moderate', 'noisy']).optional(),
	hasOutlets: z.boolean().optional()
});

export const load: PageServerLoad = async (event) => {
	const id = parseInt(event.params.id, 10);
	if (isNaN(id)) throw error(404, 'Place not found');

	const [placeData] = await db.select().from(place).where(eq(place.id, id));
	if (!placeData) throw error(404, 'Place not found');

	const reviews = await db
		.select()
		.from(placeReview)
		.where(eq(placeReview.placeId, id))
		.orderBy(desc(placeReview.createdAt));

	const tags = await db
		.select()
		.from(placeTag)
		.where(eq(placeTag.placeId, id))
		.orderBy(desc(placeTag.votes));

	// Active posts at this place
	const now = new Date();
	const activePosts = await db
		.select()
		.from(post)
		.where(
			and(
				eq(post.placeId, id),
				sql`${post.startTime} + (${post.hours} || ' hours')::interval > ${now}`
			)
		)
		.orderBy(desc(post.createdAt));

	// Compute aggregate stats
	const totalRating = reviews.reduce((sum, r) => sum + r.rating, 0);
	const wifiRatings = reviews.filter((r) => r.wifiRating != null);
	const totalWifi = wifiRatings.reduce((sum, r) => sum + (r.wifiRating ?? 0), 0);
	const noiseCounts = { quiet: 0, moderate: 0, noisy: 0 };
	const outletYes = reviews.filter((r) => r.hasOutlets === true).length;
	const outletNo = reviews.filter((r) => r.hasOutlets === false).length;

	for (const r of reviews) {
		if (r.noiseLevel && r.noiseLevel in noiseCounts) {
			noiseCounts[r.noiseLevel as keyof typeof noiseCounts]++;
		}
	}

	const stats = {
		avgRating: reviews.length > 0 ? totalRating / reviews.length : 0,
		reviewCount: reviews.length,
		avgWifi: wifiRatings.length > 0 ? totalWifi / wifiRatings.length : 0,
		wifiCount: wifiRatings.length,
		noiseCounts,
		outletYes,
		outletNo,
		outletTotal: outletYes + outletNo
	};

	const reviewForm = await superValidate(zod4(reviewSchema));

	return {
		place: placeData,
		reviews,
		tags,
		activePosts,
		stats,
		reviewForm,
		anonymousSessionId: event.locals.anonymousSessionId
	};
};

export const actions: Actions = {
	createReview: async (event) => {
		const id = parseInt(event.params.id, 10);
		const form = await superValidate(event.request, zod4(reviewSchema));

		if (!form.valid) {
			return fail(400, { reviewForm: form });
		}

		await db.insert(placeReview).values({
			placeId: id,
			userId: event.locals.user?.id ?? null,
			sessionId: event.locals.anonymousSessionId,
			rating: form.data.rating,
			text: form.data.text || null,
			wifiRating: form.data.wifiRating ?? null,
			noiseLevel: form.data.noiseLevel ?? null,
			hasOutlets: form.data.hasOutlets ?? null
		});

		return { reviewForm: form };
	},
	deleteReview: async (event) => {
		const formData = await event.request.formData();
		const reviewId = parseInt(formData.get('reviewId') as string, 10);
		if (isNaN(reviewId)) return fail(400);

		const [review] = await db.select().from(placeReview).where(eq(placeReview.id, reviewId));
		if (!review) return fail(404);
		if (review.sessionId !== event.locals.anonymousSessionId) return fail(403);

		await db.delete(placeReview).where(eq(placeReview.id, reviewId));
		return { deleted: true };
	},
	addTag: async (event) => {
		const id = parseInt(event.params.id, 10);
		const formData = await event.request.formData();
		const tag = (formData.get('tag') as string)?.trim().toLowerCase();

		if (!tag || tag.length < 2 || tag.length > 30) {
			return fail(400, { message: 'Tag must be 2-30 characters' });
		}

		// Upsert: increment votes if exists, insert if not
		const [existing] = await db
			.select()
			.from(placeTag)
			.where(and(eq(placeTag.placeId, id), eq(placeTag.tag, tag)));

		if (existing) {
			await db.update(placeTag)
				.set({ votes: existing.votes + 1 })
				.where(eq(placeTag.id, existing.id));
		} else {
			await db.insert(placeTag).values({ placeId: id, tag, votes: 1 });
		}

		return { tagAdded: true };
	},
	voteTag: async (event) => {
		const formData = await event.request.formData();
		const tagId = parseInt(formData.get('tagId') as string, 10);
		if (isNaN(tagId)) return fail(400);

		const [tag] = await db.select().from(placeTag).where(eq(placeTag.id, tagId));
		if (!tag) return fail(404);

		await db.update(placeTag)
			.set({ votes: tag.votes + 1 })
			.where(eq(placeTag.id, tagId));

		return { voted: true };
	}
};
