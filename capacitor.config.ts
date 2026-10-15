import type { CapacitorConfig } from '@capacitor/cli';

/**
 * PostUp native shell (M10).
 * CAP_MODE=remote (default for now): the app loads https://postup.now, with a bundled
 *   offline screen (app-shell/) as the fallback page. Ships today.
 * CAP_MODE=bundled (recommended target, D7): ship a static SPA build in webDir talking to
 *   https://postup.now/api/*. Needs the remaining server-loaded pages moved to /api calls.
 */
const mode = process.env.CAP_MODE === 'bundled' ? 'bundled' : 'remote';
const origin = process.env.CAP_SERVER_URL || 'https://postup.now';

const config: CapacitorConfig = {
	appId: process.env.CAP_APP_ID || 'now.postup.app',
	appName: 'PostUp',
	webDir: mode === 'bundled' ? 'build-app' : 'app-shell',
	server:
		mode === 'remote'
			? { url: origin, cleartext: origin.startsWith('http://'), errorPath: 'offline.html', allowNavigation: [new URL(origin).host] }
			: { androidScheme: 'https' },
	plugins: {
		PushNotifications: { presentationOptions: ['badge', 'sound', 'alert'] }
	}
};

export default config;
