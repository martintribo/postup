// Service Worker for Push Notifications
self.addEventListener('push', (event) => {
	const data = event.data?.json() || {};
	const title = data.title || 'New Post';
	const options = {
		body: data.body || 'Someone posted up!',
		icon: '/favicon.svg',
		badge: '/favicon.svg',
		data: data.url || '/',
		tag: 'post-notification',
		requireInteraction: false
	};

	event.waitUntil(
		self.registration.showNotification(title, options)
	);
});

self.addEventListener('notificationclick', (event) => {
	event.notification.close();
	
	const urlToOpen = event.notification.data || '/';
	
	event.waitUntil(
		clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
			// Check if there's already a window/tab open with the target URL
			for (const client of clientList) {
				if (client.url === urlToOpen && 'focus' in client) {
					return client.focus();
				}
			}
			// If not, open a new window/tab
			if (clients.openWindow) {
				return clients.openWindow(urlToOpen);
			}
		})
	);
});

