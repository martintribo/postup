import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { notificationSubscription } from '$lib/server/db/schema';
import { eq } from 'drizzle-orm';

export const POST: RequestHandler = async (event) => {
	try {
		const body = await event.request.json();
		const { endpoint } = body;
		
		if (!endpoint) {
			return json({ error: 'Endpoint is required' }, { status: 400 });
		}
		
		await db
			.delete(notificationSubscription)
			.where(eq(notificationSubscription.endpoint, endpoint));
		
		return json({ success: true });
	} catch (error) {
		console.error('Error unsubscribing from notifications:', error);
		return json({ error: 'Failed to unsubscribe' }, { status: 500 });
	}
};

