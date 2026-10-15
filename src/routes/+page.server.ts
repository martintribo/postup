import { sanitizePosts } from '$lib/server/privacy';
import { blockedSet } from '$lib/server/safety';
import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import { zod4 } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { fail, redirect } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { post, project, place, user } from '$lib/server/db/schema';
import { inArray } from 'drizzle-orm';
import { listProjectCards, dayLabel } from '$lib/server/projects-view';
import * as auth from '$lib/server/auth';
import { and, desc, eq, sql } from 'drizzle-orm';
import { getUserLocation, reverseGeocode } from '$lib/server/location';
import { getNearbyFeed } from '$lib/server/feed';
import { flag } from '$lib/flags';
import { config } from '$lib/config';
import { notification } from '$lib/server/db/schema';
import { isNull } from 'drizzle-orm';
import { liveCondition, computeEndsAt, upsertGooglePlace } from '$lib/server/postups';

const postSchema = z.object({
	activity: z.string().min(1, 'Activity is required'),
	goals: z.string().optional(),
	location: z.string().min(1, 'Location is required'),
	latitude: z.number(),
	longitude: z.number(),
	hours: z.number().int().min(1, 'Hours must be at least 1').max(24, 'Hours cannot exceed 24'),
	projectId: z.number().int().optional(),
	placeId: z.number().int().optional(),
	googlePlaceId: z.string().optional()
});

async function getActivePosts(userLatitude: number, userLongitude: number, viewerId?: string | null) {
	const distanceInMiles = 200;

	const rows = await db
		.select()
		.from(post)
		.where(
			// Use SQL now() — postgres-js stringifies JS Date as Date.toString(), which PG rejects.
			sql`${liveCondition} AND (3959 * acos(cos(radians(${userLatitude})) * cos(radians(${post.latitude})) * cos(radians(${post.longitude}) - radians(${userLongitude})) + sin(radians(${userLatitude})) * sin(radians(${post.latitude})))) <= ${distanceInMiles}`
		)
		.orderBy(desc(post.createdAt));
	const blocked = await blockedSet(viewerId);
	return sanitizePosts(rows.filter((r) => !r.userId || !blocked.has(r.userId)), viewerId);
}

export const load: PageServerLoad = async (event) => {
	const anonymousSessionId = event.locals.anonymousSessionId;
	const { location: userLocation, source: locationSource, suggestUpdate } = await getUserLocation(event);

	const form = await superValidate(zod4(postSchema));
	const posts = await getActivePosts(userLocation.latitude, userLocation.longitude, event.locals.user?.id);
	const projects = await db
		.select()
		.from(project)
		.where(and(eq(project.active, true), eq(project.hidden, false)))
		.orderBy(desc(project.createdAt));

	// User's own projects for the post-up form
	const userId = event.locals.user?.id;
	const myProjects = userId
		? await db.select().from(project).where(sql`${project.userId} = ${userId} AND ${project.active} = true`).orderBy(desc(project.createdAt))
		: [];

	// M4: feed-first home when nobody nearby is live.
	const feed = flag('feed_home') && posts.length === 0 ? await getNearbyFeed(userLocation.latitude, userLocation.longitude, 30, event.locals.user?.id) : null;

	// M5: "You're live" banner for the signed-in poster.
	const [myLive] = event.locals.user
		? await db.select({ id: post.id, activity: post.activity }).from(post).where(and(eq(post.userId, event.locals.user.id), liveCondition)).orderBy(desc(post.startTime)).limit(1)
		: [];

	const [unread] = event.locals.user
		? await db.select({ n: sql<number>`count(*)::int` }).from(notification).where(and(eq(notification.userId, event.locals.user.id), isNull(notification.readAt)))
		: [];

	// Live-now panel: who is posted up (names, avatars) and cafes busy this week.
	const ids = [...new Set(posts.map((p) => p.userId).filter((x): x is string => !!x))];
	const people = ids.length
		? Object.fromEntries(
				(await db.select({ id: user.id, displayName: user.displayName, username: user.username, avatarUrl: user.avatarUrl }).from(user).where(inArray(user.id, ids))).map((u) => [
					u.id,
					{ name: u.displayName || u.username, avatarUrl: u.avatarUrl }
				])
			)
		: {};
	const lat = userLocation.latitude, lng = userLocation.longitude;
	const week = (await db.execute(sql`
		select pl.id, pl.name, count(*)::int as n,
			(array_agg(coalesce(u.display_name, u.username, p.name) order by p.start_time desc))[1:3] as who
		from ${post} p join ${place} pl on pl.id = p.place_id left join ${user} u on u.id = p.user_id
		where p.start_time > now() - interval '7 days' and p.join_mode <> 'ask'
			and (3959 * acos(least(1, cos(radians(${lat})) * cos(radians(pl.latitude)) * cos(radians(pl.longitude) - radians(${lng})) + sin(radians(${lat})) * sin(radians(pl.latitude))))) <= 25
		group by pl.id, pl.name order by n desc limit 5`)) as unknown as { id: number; name: string; n: number; who: string[] }[];

	const projectCards = (await listProjectCards('all', event.locals.user?.id)).slice(0, posts.length ? 6 : 12).map((c) => ({ ...c, when: dayLabel(c.lastAt) }));
	return {
		projectCards,
		areaName: config.launchArea.name,
		people,
		week: [...week],
		unread: unread?.n ?? 0,
		myLive: myLive ?? null,
		feed,
		location: userLocation,
		locationSource,
		suggestUpdate,
		form,
		posts,
		projects,
		myProjects,
		anonymousSessionId,
		userSessionId: event.locals.session?.id ?? null
	};
};

export const actions: Actions = {
	delete: async (event) => {
		if (!event.locals.user) {
			return fail(401, { message: 'You must be logged in' });
		}

		const formData = await event.request.formData();
		const postId = formData.get('postId');

		if (!postId || typeof postId !== 'string') {
			return fail(400, { message: 'Invalid post ID' });
		}

		try {
			const [existingPost] = await db
				.select()
				.from(post)
				.where(eq(post.id, parseInt(postId, 10)));

			if (!existingPost) {
				return fail(404, { message: 'Post not found' });
			}

			if (existingPost.sessionId !== event.locals.session?.id) {
				return fail(403, { message: 'Not authorized to delete this post' });
			}

			await db.delete(post).where(eq(post.id, parseInt(postId, 10)));

			// Reload posts after deletion
			const { location: userLocation } = await getUserLocation(event);
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude, event.locals.user?.id);
			return { posts };
		} catch (error) {
			console.error('Error deleting post:', error);
			return fail(500, { message: 'Failed to delete post' });
		}
	},
	setLocation: async (event) => {
		const formData = await event.request.formData();
		const latitude = parseFloat(formData.get('latitude') as string);
		const longitude = parseFloat(formData.get('longitude') as string);

		if (isNaN(latitude) || isNaN(longitude)) {
			return fail(400, { message: 'Invalid coordinates' });
		}

		// Reverse geocode to get a friendly name
		const geocodeResult = await reverseGeocode(latitude, longitude);
		const cityName = geocodeResult.locality || geocodeResult.neighborhood || geocodeResult.district;

		const locationData = { latitude, longitude, city: cityName || undefined };

		event.cookies.set(auth.userLocationCookieName, JSON.stringify(locationData), {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: auth.isSecureRequest(event),
			maxAge: 60 * 60 * 24 * 90 // 90 days
		});

		return { locationUpdated: true };
	},
	clearLocation: async (event) => {
		event.cookies.delete(auth.userLocationCookieName, { path: '/' });
		return { locationCleared: true };
	},
	create: async (event) => {
		if (!event.locals.user) {
			return fail(401, { message: 'You must be logged in to post up' });
		}

		const form = await superValidate(event.request, zod4(postSchema));
		const { location: userLocation } = await getUserLocation(event);

		if (!form.valid) {
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude, event.locals.user?.id);
			return fail(400, { form, posts });
		}

		try {
			// Reverse geocode to get neighborhood, locality, and district
			const geocodeResult = await reverseGeocode(form.data.latitude, form.data.longitude);

			let placeId = form.data.placeId ?? null;
			if (!placeId && form.data.googlePlaceId) {
				placeId = await upsertGooglePlace(
					{ googlePlaceId: form.data.googlePlaceId, name: form.data.location, latitude: form.data.latitude, longitude: form.data.longitude },
					event.locals.user!.id
				);
			}
			const startTime = new Date();
			const result = await db.insert(post).values({
				userId: event.locals.user!.id,
				joinMode: config.defaultJoinMode,
				placeId,
				projectId: form.data.projectId ?? null,
				startTime,
				endsAt: computeEndsAt(startTime, form.data.hours),
				name: event.locals.user!.username,
				activity: form.data.activity,
				goals: form.data.goals || null,
				location: form.data.location,
				latitude: form.data.latitude,
				longitude: form.data.longitude,
				hours: form.data.hours,
				neighborhood: geocodeResult.neighborhood,
				locality: geocodeResult.locality,
				district: geocodeResult.district,
				sessionId: event.locals.session?.id
			}).returning();

			// Reload posts after creating a new one
			const createdId = result[0]?.id ?? null;
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude, event.locals.user?.id);
			return { form, posts, createdId };
		} catch (error) {
			console.error('Error creating post:', error);
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude, event.locals.user?.id);
			return fail(500, {
				form,
				posts,
				message: 'Failed to create post'
			});
		}
	},
	logout: async (event) => {
		if (!event.locals.session) {
			return fail(401);
		}
		await auth.invalidateSession(event.locals.session.id);
		auth.deleteSessionTokenCookie(event);
		return redirect(302, '/');
	}
};

