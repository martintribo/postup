import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { notificationSubscription } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';

export const POST: RequestHandler = async (event) => {
	try {
		const body = await event.request.json();
		const { endpoint, keys } = body;
		
		if (!endpoint || !keys || !keys.p256dh || !keys.auth) {
			return json({ error: 'Invalid subscription data' }, { status: 400 });
		}
		
		const sessionId = event.locals.anonymousSessionId;
		
		// Check if subscription already exists
		const existing = await db
			.select()
			.from(notificationSubscription)
			.where(eq(notificationSubscription.endpoint, endpoint))
			.limit(1);
		
		if (existing.length > 0) {
			// Update existing subscription
			await db
				.update(notificationSubscription)
				.set({
					p256dh: keys.p256dh,
					auth: keys.auth,
					sessionId: sessionId
				})
				.where(eq(notificationSubscription.endpoint, endpoint));
		} else {
			// Create new subscription
			await db.insert(notificationSubscription).values({
				endpoint,
				p256dh: keys.p256dh,
				auth: keys.auth,
				sessionId: sessionId
			});
		}
		
		return json({ success: true });
	} catch (error) {
		console.error('Error subscribing to notifications:', error);
		return json({ error: 'Failed to subscribe' }, { status: 500 });
	}
};

