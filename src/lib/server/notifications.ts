import webpush from 'web-push';
import { db } from './db';
import { notificationSubscription } from './db/schema';
import { eq } from 'drizzle-orm';
import { env } from '$env/dynamic/private';

// Initialize web-push with VAPID keys
// Note: Update the email address to your contact email
if (env.VAPID_PUBLIC_KEY && env.VAPID_PRIVATE_KEY) {
	webpush.setVapidDetails(
		env.VAPID_CONTACT_EMAIL || 'mailto:your-email@example.com',
		env.VAPID_PUBLIC_KEY,
		env.VAPID_PRIVATE_KEY
	);
}

export async function sendPushNotification(
	title: string,
	body: string,
	url?: string
) {
	try {
		// Get all active subscriptions
		const subscriptions = await db.select().from(notificationSubscription);
		
		const payload = JSON.stringify({
			title,
			body,
			url: url || '/'
		});
		
		// Send notification to all subscribers
		const promises = subscriptions.map(async (sub) => {
			try {
				await webpush.sendNotification(
					{
						endpoint: sub.endpoint,
						keys: {
							p256dh: sub.p256dh,
							auth: sub.auth
						}
					},
					payload
				);
			} catch (error: any) {
				// If subscription is invalid, remove it from database
				if (error.statusCode === 410 || error.statusCode === 404) {
					await db
						.delete(notificationSubscription)
						.where(eq(notificationSubscription.endpoint, sub.endpoint));
				} else {
					console.error('Error sending notification:', error);
				}
			}
		});
		
		await Promise.allSettled(promises);
	} catch (error) {
		console.error('Error in sendPushNotification:', error);
	}
}

