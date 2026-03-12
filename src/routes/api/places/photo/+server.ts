import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';
import { error } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ url }) => {
	const photoRef = url.searchParams.get('ref');
	if (!photoRef) {
		throw error(400, 'ref required');
	}

	const key = privateEnv.GOOGLE_PLACES_API_KEY;
	if (!key) {
		throw error(500, 'Google Places not configured');
	}

	const response = await fetch(
		`https://places.googleapis.com/v1/${photoRef}/media?maxWidthPx=400&key=${key}`
	);

	if (!response.ok) {
		throw error(502, 'Failed to fetch photo');
	}

	const contentType = response.headers.get('content-type') || 'image/jpeg';
	const body = await response.arrayBuffer();

	return new Response(body, {
		headers: {
			'content-type': contentType,
			'cache-control': 'public, max-age=86400'
		}
	});
};
