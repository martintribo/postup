import type { PageServerLoad, Actions } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import { zod4 } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { fail } from '@sveltejs/kit';
import { db } from '$lib/server/db';
import { post } from '$lib/server/db/schema';

const postSchema = z.object({
	name: z.string().min(1, 'Name is required'),
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

export const load: PageServerLoad = async (event) => {
	const clientIP = getClientIP(event);
	
	// If localhost, default to Los Angeles
	if (isLocalhost(clientIP)) {
		const losAngelesLocation: GeoLocation = {
			latitude: 34.0522,
			longitude: -118.2437,
			city: 'Los Angeles',
			country: 'USA'
		};
		const form = await superValidate(zod4(postSchema));
		return {
			location: losAngelesLocation,
			form
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

	const form = await superValidate(zod4(postSchema));
	
	return {
		location: location || defaultLocation,
		form
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event.request, zod4(postSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		try {
			const result = await db.insert(post).values({
				name: form.data.name,
				location: form.data.location,
				latitude: form.data.latitude,
				longitude: form.data.longitude,
				hours: form.data.hours
			}).returning();

			return { form };
		} catch (error) {
			console.error('Error creating post:', error);
			return fail(500, {
				form,
				message: 'Failed to create post'
			});
		}
	}
};

