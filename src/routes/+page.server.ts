import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import { zod4 } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { fail } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { post } from '$lib/server/db/schema';
import { desc, eq, sql, gt } from 'drizzle-orm';
import { env as privateEnv } from '$env/dynamic/private';
import { PUBLIC_MAPBOX_ACCESS_TOKEN } from '$env/static/public';
import { sendPushNotification } from '$lib/server/notifications';

const postSchema = z.object({
	name: z.string().min(1, 'Name is required'),
	activity: z.string().min(1, 'Activity is required'),
	location: z.string().min(1, 'Location is required'),
	latitude: z.number(),
	longitude: z.number(),
	hours: z.number().int().min(1, 'Hours must be at least 1').max(24, 'Hours cannot exceed 24')
});

interface GeoLocation {
	latitude: number;
	longitude: number;
	city?: string;
	country?: string;
}

async function getLocationFromIP(ip: string): Promise<GeoLocation | null> {
	try {
		// Using ip-api.com (free, no API key required)
		const response = await fetch(`http://ip-api.com/json/${ip}?fields=status,message,lat,lon,city,country`);
		const data = await response.json();

		if (data.status === 'success') {
			return {
				latitude: data.lat,
				longitude: data.lon,
				city: data.city,
				country: data.country
			};
		}
		return null;
	} catch (error) {
		console.error('Error fetching location:', error);
		return null;
	}
}

function getClientIP(event: { getClientAddress: () => string }): string {
	return event.getClientAddress();
}

function isLocalhost(ip: string): boolean {
	// Check for common localhost IPs
	const localhostIPs = ['127.0.0.1', '::1', 'localhost', '::ffff:127.0.0.1'];
	return localhostIPs.includes(ip) || ip.startsWith('127.') || ip.startsWith('::1');
}

interface ReverseGeocodeResult {
	neighborhood?: string;
	locality?: string;
	district?: string;
}

async function reverseGeocode(latitude: number, longitude: number): Promise<ReverseGeocodeResult> {
	const accessToken = privateEnv.MAPBOX_ACCESS_TOKEN || PUBLIC_MAPBOX_ACCESS_TOKEN;
	
	if (!accessToken) {
		console.error('Mapbox access token is not configured');
		return {};
	}

	try {
		const params = new URLSearchParams({
			longitude: longitude.toString(),
			latitude: latitude.toString(),
			types: 'neighborhood,locality,district',
			access_token: accessToken
		});

		const response = await fetch(
			`https://api.mapbox.com/search/geocode/v6/reverse?${params.toString()}`
		);

		if (!response.ok) {
			throw new Error(`Mapbox API error: ${response.status}`);
		}

		const data = await response.json();
		
		// Mapbox v6 response structure: features array with context array
		const features = data.features || [];
		const result: ReverseGeocodeResult = {};

		if (features.length > 0) {
			const feature = features[0];
			// Context is an array of objects with id and text properties
			const context = feature.properties?.context || feature.context || [];

			if (Array.isArray(context)) {
				for (const ctx of context) {
					// Context objects have id (e.g., "neighborhood.12345") and text (the name)
					if (ctx.id?.startsWith('neighborhood.')) {
						result.neighborhood = ctx.text;
					} else if (ctx.id?.startsWith('locality.')) {
						result.locality = ctx.text;
					} else if (ctx.id?.startsWith('district.')) {
						result.district = ctx.text;
					}
				}
			}
		}

		return result;
	} catch (error) {
		console.error('Error reverse geocoding:', error);
		return {};
	}
}

async function getActivePosts(userLatitude: number, userLongitude: number) {
	const now = new Date();
	// Haversine formula to calculate distance in miles
	// 3959 is the Earth's radius in miles
	const distanceInMiles = 200;
	
	return await db
		.select()
		.from(post)
		.where(
			sql`${post.startTime} + (${post.hours} || ' hours')::interval > ${now} AND (3959 * acos(cos(radians(${userLatitude})) * cos(radians(${post.latitude})) * cos(radians(${post.longitude}) - radians(${userLongitude})) + sin(radians(${userLatitude})) * sin(radians(${post.latitude})))) <= ${distanceInMiles}`
		)
		.orderBy(desc(post.createdAt));
}

async function getUserLocation(event: { getClientAddress: () => string }): Promise<GeoLocation> {
	const clientIP = getClientIP(event);
	
	// If localhost, default to Los Angeles
	if (isLocalhost(clientIP)) {
		return {
			latitude: 34.0522,
			longitude: -118.2437,
			city: 'Los Angeles',
			country: 'USA'
		};
	}

	const location = await getLocationFromIP(clientIP);

	// Fallback to default location (London) if geo IP fails
	const defaultLocation: GeoLocation = {
		latitude: 51.505,
		longitude: -0.09,
		city: 'London',
		country: 'UK'
	};

	return location || defaultLocation;
}

export const load: PageServerLoad = async (event) => {
	const anonymousSessionId = event.locals.anonymousSessionId;
	const userLocation = await getUserLocation(event);
	
	const form = await superValidate(zod4(postSchema));
	const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
	
	return {
		location: userLocation,
		form,
		posts,
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
			const userLocation = await getUserLocation(event);
			const posts = await getActivePosts(userLocation.latitude, userLocation.longitude);
			return { posts };
		} catch (error) {
			console.error('Error deleting post:', error);
			return fail(500, { message: 'Failed to delete post' });
		}
	},
	create: async (event) => {
		const form = await superValidate(event.request, zod4(postSchema));
		const userLocation = await getUserLocation(event);

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

			// Send push notification to all subscribers
			const notificationTitle = 'New Post!';
			const notificationBody = `${form.data.name} is ${form.data.activity} at ${form.data.location}`;
			// Don't await - send notifications asynchronously
			sendPushNotification(notificationTitle, notificationBody).catch((error) => {
				console.error('Error sending push notification:', error);
			});

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
	}
};

