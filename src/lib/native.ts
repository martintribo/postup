/**
 * Native bridges (M10). Every function is a no-op on the web, so web code can call them freely.
 * Loaded lazily so the web bundle doesn't pay for Capacitor plugins.
 */
import { browser } from '$app/environment';

export function isNative(): boolean {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	return browser && !!(window as any).Capacitor?.isNativePlatform?.();
}

/** Register for push and send the device token to the server (join requests, chat). */
export async function registerPush(): Promise<void> {
	if (!isNative()) return;
	const { PushNotifications } = await import('@capacitor/push-notifications');
	const perm = await PushNotifications.requestPermissions();
	if (perm.receive !== 'granted') return;
	await PushNotifications.addListener('registration', async (t) => {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const platform = (window as any).Capacitor.getPlatform();
		await fetch('/api/devices', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ token: t.value, platform }) });
	});
	await PushNotifications.addListener('pushNotificationActionPerformed', (a) => {
		const url = a.notification.data?.url;
		if (typeof url === 'string' && url.startsWith('/')) location.href = url;
	});
	await PushNotifications.register();
}

/** Native location for "Where are you?"; falls back to the browser API. */
export async function currentPosition(): Promise<{ latitude: number; longitude: number } | null> {
	if (isNative()) {
		const { Geolocation } = await import('@capacitor/geolocation');
		const p = await Geolocation.getCurrentPosition({ enableHighAccuracy: false, timeout: 10000 });
		return { latitude: p.coords.latitude, longitude: p.coords.longitude };
	}
	if (!browser || !navigator.geolocation) return null;
	return new Promise((res) => navigator.geolocation.getCurrentPosition((p) => res({ latitude: p.coords.latitude, longitude: p.coords.longitude }), () => res(null), { timeout: 10000 }));
}

/** Deep links: universal/app links for /p/* and /projects/* open in-app. */
export async function listenDeepLinks(): Promise<void> {
	if (!isNative()) return;
	const { App } = await import('@capacitor/app');
	await App.addListener('appUrlOpen', ({ url }) => {
		const u = new URL(url);
		if (/^\/(p|projects|postups)\//.test(u.pathname)) location.href = u.pathname + u.search;
	});
}
