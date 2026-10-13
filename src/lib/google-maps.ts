import { env } from '$env/dynamic/public';
import { browser } from '$app/environment';

declare global {
	interface Window {
		google?: {
			maps: {
				importLibrary: (name: string, ...rest: unknown[]) => Promise<unknown>;
			};
		};
	}
}

let loadPromise: Promise<boolean> | null = null;

/** Browser key for Maps JS / Places UI Kit. Empty until Martin adds a referrer-restricted key. */
export function googleMapsBrowserKey(): string {
	return env.PUBLIC_GOOGLE_MAPS_BROWSER_KEY?.trim() ?? '';
}

/**
 * Load Maps JS API (weekly) and `places` (UI Kit custom elements).
 * Returns false when no PUBLIC_GOOGLE_MAPS_BROWSER_KEY is set — do not create Cloud resources.
 */
export function loadGooglePlacesLibrary(): Promise<boolean> {
	if (!browser) return Promise.resolve(false);
	const key = googleMapsBrowserKey();
	if (!key) return Promise.resolve(false);
	if (loadPromise) return loadPromise;

	loadPromise = new Promise((resolve) => {
		const g = window as Window & { google?: { maps?: Record<string, unknown> } };
		const existing = g.google?.maps?.importLibrary as
			| ((name: string) => Promise<unknown>)
			| undefined;
		if (typeof existing === 'function') {
			existing('places')
				.then(() => resolve(true))
				.catch(() => resolve(false));
			return;
		}

		const apiName = 'The Google Maps JavaScript API';
		const ns = 'google';
		const importName = 'importLibrary';
		const callbackName = '__ib__';
		const doc = document;
		const win = window as unknown as Record<string, unknown>;
		win[ns] = win[ns] || {};
		const googleNs = win[ns] as { maps?: Record<string, unknown> };
		const maps = (googleNs.maps = googleNs.maps || {});
		const libraries = new Set<string>();
		const params = new URLSearchParams();
		let boot: Promise<void> | null = null;

		const start = () =>
			(boot ||= new Promise<void>((ok, fail) => {
				const script = doc.createElement('script');
				params.set('libraries', [...libraries].join(','));
				params.set('key', key);
				params.set('v', 'weekly');
				params.set('loading', 'async');
				params.set('callback', `${ns}.maps.${callbackName}`);
				script.src = `https://maps.googleapis.com/maps/api/js?${params}`;
				(maps as Record<string, unknown>)[callbackName] = ok;
				script.onerror = () => fail(new Error(`${apiName} could not load.`));
				script.nonce = doc.querySelector<HTMLScriptElement>('script[nonce]')?.nonce || '';
				doc.head.append(script);
			}));

		maps[importName] = (lib: string, ...rest: unknown[]) => {
			libraries.add(lib);
			return start().then(() => {
				const fn = maps[importName] as (name: string, ...r: unknown[]) => Promise<unknown>;
				return fn(lib, ...rest);
			});
		};

		(maps[importName] as (name: string) => Promise<unknown>)('places')
			.then(() => resolve(true))
			.catch((err) => {
				console.warn('Google Maps JS failed to load', err);
				loadPromise = null;
				resolve(false);
			});
	});

	return loadPromise;
}
