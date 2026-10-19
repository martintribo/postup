import { sanitizePosts } from '$lib/server/privacy';
import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import { zod4 } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { fail, error } from '@sveltejs/kit';
import { liveCondition } from '$lib/server/postups';
import { db } from '$lib/server/db';
import { place, placeReview, placeTag, post, user, project } from '$lib/server/db/schema';
import { desc, eq, sql, and, inArray } from 'drizzle-orm';
import { getUserLocation } from '$lib/server/location';
import { firstImage } from '$lib/server/projects-view';

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
	const activePostsRaw = await db
		.select()
		.from(post)
		.where(
			and(
				eq(post.placeId, id),
				// Use SQL now() — postgres-js stringifies JS Date as Date.toString(), which PG rejects.
				liveCondition
			)
		)
		.orderBy(desc(post.createdAt));
	// D2: ask-mode postups hidden from this cafe's page unless you're the poster or approved.
	const activePosts = (await sanitizePosts(activePostsRaw, event.locals.user?.id)).filter((p) => !('cafeHidden' in p && p.cafeHidden));

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

	const ids = [...new Set(activePosts.map((p) => p.userId).filter((x): x is string => !!x))];
	const names = ids.length ? Object.fromEntries((await db.select({ id: user.id, n: sql<string>`coalesce(${user.displayName}, ${user.username})`, a: user.avatarUrl }).from(user).where(inArray(user.id, ids))).map((u) => [u.id, u])) : {};
	const projIds = [...new Set(activePosts.map((p) => p.projectId).filter((x): x is number => !!x))];
	const projNames = projIds.length ? Object.fromEntries((await db.select({ id: project.id, name: project.name }).from(project).where(inArray(project.id, projIds))).map((r) => [r.id, r.name])) : {};
	const hereNow = activePosts.map((p) => ({ id: p.id, who: (p.userId && names[p.userId]?.n) || p.name, avatarUrl: (p.userId && names[p.userId]?.a) || null, project: p.projectId ? projNames[p.projectId] ?? null : null, cafe: placeData.name, projectId: p.projectId, endsAt: (p.endsAt ?? new Date(p.startTime.getTime() + p.hours * 3600e3)).toISOString(), ask: p.joinMode === 'ask' }));
	const [wk] = (await db.execute(sql`select count(*)::int as n, (array_agg(coalesce(u.display_name, u.username, p.name) order by p.start_time desc))[1:3] as who,
		(select pr.name from post p2 join project pr on pr.id = p2.project_id where p2.place_id = ${id} and p2.start_time > now() - interval '30 days' group by pr.name order by count(*) desc limit 1) as regular,
		(select p2.project_id from post p2 where p2.place_id = ${id} and p2.project_id is not null and p2.start_time > now() - interval '30 days' group by p2.project_id order by count(*) desc limit 1) as "regularId"
		from post p left join "user" u on u.id = p.user_id where p.place_id = ${id} and p.start_time > now() - interval '7 days' and p.join_mode <> 'ask'`)) as unknown as { n: number; who: string[] | null; regular: string | null; regularId: number | null }[];
	// Hero: distance from you, and the latest user/project photo taken here (never Google's).
	const { location } = await getUserLocation(event);
	const R = Math.PI / 180;
	const miles = 3959 * Math.acos(Math.min(1, Math.cos(location.latitude * R) * Math.cos(placeData.latitude * R) * Math.cos((placeData.longitude - location.longitude) * R) + Math.sin(location.latitude * R) * Math.sin(placeData.latitude * R)));
	// A spot photo someone took here wins; else the cover of a project worked on here.
	const [ph] = (await db.execute(sql`select p2.photo_url, pr.description, coalesce(u.display_name, u.username) as who from post p2 left join project pr on pr.id = p2.project_id and pr.hidden = false left join "user" u on u.id = p2.user_id
		where p2.place_id = ${id} and (p2.photo_url is not null or pr.description like '%![%') order by (p2.photo_url is not null) desc, p2.start_time desc limit 1`)) as unknown as { photo_url: string | null; description: string | null; who: string | null }[];
	const photo = ph ? { src: ph.photo_url ?? firstImage(ph.description ?? ''), who: ph.who } : null;
	return {
		title: placeData.name,
		miles,
		photo: photo?.src ? photo : null,
		hereNow,
		week: { n: wk?.n ?? 0, who: wk?.who ?? [], regular: wk?.regular ?? null, regularId: wk?.regularId ?? null },
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
