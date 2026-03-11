import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import { zod4 } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { fail, redirect } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { post, project } from '$lib/server/db/schema';
import * as auth from '$lib/server/auth';
import { desc, eq, sql } from 'drizzle-orm';
import { getUserLocation, reverseGeocode } from '$lib/server/location';

const postSchema = z.object({
	name: z.string().min(1, 'Name is required'),
	activity: z.string().min(1, 'Activity is required'),
	location: z.string().min(1, 'Location is required'),
	latitude: z.number(),
	longitude: z.number(),
	hours: z.number().int().min(1, 'Hours must be at least 1').max(24, 'Hours cannot exceed 24')
});

async function getActivePosts(userLatitude: number, userLongitude: number) {
	const now = new Date();
	const distanceInMiles = 200;

	return await db
		.select()
		.from(post)
		.where(
			sql`${post.startTime} + (${post.hours} || ' hours')::interval > ${now} AND (3959 * acos(cos(radians(${userLatitude})) * cos(radians(${post.latitude})) * cos(radians(${post.longitude}) - radians(${userLongitude})) + sin(radians(${userLatitude})) * sin(radians(${post.latitude})))) <= ${distanceInMiles}`
		)
		.orderBy(desc(post.createdAt));
}

export const load: PageServerLoad = async (event) => {
	const anonymousSessionId = event.locals.anonymousSessionId;
	const { location: userLocation, source: locationSource, suggestUpdate } = await getUserLocation(event);

	const form = await superValidate(zod4(postSchema));
	const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
	const projects = await db
		.select()
		.from(project)
		.where(eq(project.active, true))
		.orderBy(desc(project.createdAt));

	return {
		location: userLocation,
		locationSource,
		suggestUpdate,
		form,
		posts,
		projects,
		anonymousSessionId
	};
};

export const actions: Actions = {
	delete: async (event) => {
		const formData = await event.request.formData();
		const postId = formData.get('postId');
		const anonymousSessionId = event.locals.anonymousSessionId;

		if (!postId || typeof postId !== 'string') {
			return fail(400, { message: 'Invalid post ID' });
		}

		try {
			// Verify that the post belongs to the current session
			const [existingPost] = await db
				.select()
				.from(post)
				.where(eq(post.id, parseInt(postId, 10)));

			if (!existingPost) {
				return fail(404, { message: 'Post not found' });
			}

			if (existingPost.sessionId !== anonymousSessionId) {
				return fail(403, { message: 'Not authorized to delete this post' });
			}

			await db.delete(post).where(eq(post.id, parseInt(postId, 10)));

			// Reload posts after deletion
			const { location: userLocation } = await getUserLocation(event);
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
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
		const form = await superValidate(event.request, zod4(postSchema));
		const { location: userLocation } = await getUserLocation(event);

		if (!form.valid) {
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
			return fail(400, { form, posts });
		}

		try {
			// Reverse geocode to get neighborhood, locality, and district
			const geocodeResult = await reverseGeocode(form.data.latitude, form.data.longitude);
			const anonymousSessionId = event.locals.anonymousSessionId;

			const result = await db.insert(post).values({
				name: form.data.name,
				activity: form.data.activity,
				location: form.data.location,
				latitude: form.data.latitude,
				longitude: form.data.longitude,
				hours: form.data.hours,
				neighborhood: geocodeResult.neighborhood,
				locality: geocodeResult.locality,
				district: geocodeResult.district,
				sessionId: anonymousSessionId
			}).returning();

			// Reload posts after creating a new one
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
			return { form, posts };
		} catch (error) {
			console.error('Error creating post:', error);
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
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

