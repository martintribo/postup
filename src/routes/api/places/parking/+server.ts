import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';
import { db } from '$lib/server/db';
import { place } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';
import OpenAI from 'openai';

const parkingSchema = {
	type: 'object' as const,
	properties: {
		hasParking: {
			type: 'boolean' as const,
			description: 'Whether any reviews mention parking availability'
		},
		parkingType: {
			type: 'string' as const,
			enum: ['onsite_lot', 'onsite_garage', 'street', 'nearby_lot', 'mixed', 'unknown'],
			description: 'The primary type of parking mentioned'
		},
		summary: {
			type: 'string' as const,
			description: 'A short (1-2 sentence) summary of what a visitor should know about parking at this place. Include any tips, costs, or difficulties mentioned in reviews.'
		},
		confidence: {
			type: 'string' as const,
			enum: ['high', 'medium', 'low'],
			description: 'How confident are you based on the review evidence'
		}
	},
	required: ['hasParking', 'parkingType', 'summary', 'confidence'] as const,
	additionalProperties: false as const
};

export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	const id = body.id;
	const rescan = body.rescan === true;
	const keyword = (body.keyword as string || 'parking').trim().toLowerCase();

	if (!id) {
		return json({ error: 'id required' }, { status: 400 });
	}

	const [existing] = await db.select().from(place).where(eq(place.id, id)).limit(1);
	if (!existing) {
		return json({ error: 'Place not found' }, { status: 404 });
	}

	// Return cached result unless rescan requested
	if (existing.parking && !rescan) {
		return json({ parking: existing.parking });
	}

	const googleKey = privateEnv.GOOGLE_PLACES_API_KEY;
	const openrouterKey = privateEnv.OPENROUTER_API_KEY;

	if (!googleKey || !openrouterKey) {
		return json({ error: 'API keys not configured' }, { status: 500 });
	}

	try {
		// 1. Get Google Place ID if we don't have it
		let googlePlaceId = existing.googlePlaceId;
		if (!googlePlaceId) {
			const searchRes = await fetch('https://places.googleapis.com/v1/places:searchText', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Goog-Api-Key': googleKey,
					'X-Goog-FieldMask': 'places.id'
				},
				body: JSON.stringify({
					textQuery: existing.name,
					locationBias: {
						circle: { center: { latitude: existing.latitude, longitude: existing.longitude }, radius: 200 }
					},
					maxResultCount: 1
				})
			});
			if (searchRes.ok) {
				const data = await searchRes.json();
				googlePlaceId = data.places?.[0]?.id || null;
				if (googlePlaceId) {
					await db.update(place).set({ googlePlaceId }).where(eq(place.id, id));
				}
			}
		}

		if (!googlePlaceId) {
			return json({ error: 'Could not find place on Google' }, { status: 404 });
		}

		// 2. Fetch reviews
		const reviewsRes = await fetch(`https://places.googleapis.com/v1/places/${googlePlaceId}`, {
			headers: {
				'X-Goog-Api-Key': googleKey,
				'X-Goog-FieldMask': 'reviews'
			}
		});

		if (!reviewsRes.ok) {
			return json({ error: 'Failed to fetch reviews' }, { status: 502 });
		}

		const reviewsData = await reviewsRes.json();
		const reviews = reviewsData.reviews || [];

		if (reviews.length === 0) {
			const noReviews = 'No reviews available to determine parking';
			await db.update(place).set({ parking: noReviews }).where(eq(place.id, id));
			return json({ parking: noReviews });
		}

		const allReviewTexts = reviews
			.map((r: any) => r.text?.text || r.originalText?.text || '')
			.filter((t: string) => t.length > 0);

		// Filter reviews to those mentioning the keyword
		const keywordRegex = new RegExp(`\\b${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\w*\\b`, 'i');
		const relevantReviews = allReviewTexts.filter((t: string) => keywordRegex.test(t));

		if (relevantReviews.length === 0) {
			const noMention = `No reviews mention "${keyword}"`;
			if (keyword === 'parking') {
				await db.update(place).set({ parking: noMention }).where(eq(place.id, id));
			}
			return json({ parking: noMention });
		}

		const reviewTexts = relevantReviews.join('\n---\n');

		// 3. Send to LLM via OpenRouter
		const client = new OpenAI({
			baseURL: 'https://openrouter.ai/api/v1',
			apiKey: openrouterKey
		});

		const completion = await client.chat.completions.create({
			model: 'google/gemini-2.0-flash-001',
			messages: [
				{
					role: 'system',
					content: `You extract information about "${keyword}" ONLY from what reviewers explicitly say. Do NOT guess or infer from the address, neighborhood, or type of business. Only report details that a reviewer actually described. Be concise (1-2 sentences).`
				},
				{
					role: 'user',
					content: `Look through these reviews for "${existing.name}" and extract ONLY what reviewers say about "${keyword}". Do not make assumptions.\n\nReviews:\n${reviewTexts}`
				}
			],
			response_format: {
				type: 'json_schema',
				json_schema: {
					name: 'parking_info',
					strict: true,
					schema: parkingSchema
				}
			}
		});

		const content = completion.choices[0]?.message?.content;
		if (!content) {
			return json({ error: 'No response from LLM' }, { status: 502 });
		}

		const parsed = JSON.parse(content);
		const parkingText = parsed.summary;

		// 4. Store in DB
		await db.update(place).set({ parking: parkingText }).where(eq(place.id, id));

		return json({ parking: parkingText, details: parsed });
	} catch (err) {
		console.error('Parking scan error:', err);
		return json({ error: 'Failed to analyze parking' }, { status: 500 });
	}
};
