import { config } from '$lib/config';

export interface GeoLocation {
	latitude: number;
	longitude: number;
	city?: string;
	country?: string;
	source: 'edge' | 'ip' | 'default';
}

/**
 * Best guess at where the visitor is, used only until the browser grants location.
 * Order: Vercel edge geo headers -> ip-api on the real client IP -> launch area.
 * The old code looked up the serverless function's own IP when headers were missing,
 * which is the likely cause of the Clarksville, TN default on prod.
 */
export async function guessLocation(
	headers: Headers,
	clientAddress: string,
	fetcher: typeof fetch = fetch
): Promise<GeoLocation> {
	const lat = Number(headers.get('x-vercel-ip-latitude'));
	const lng = Number(headers.get('x-vercel-ip-longitude'));
	if (headers.get('x-vercel-ip-latitude') && Number.isFinite(lat) && Number.isFinite(lng)) {
		const city = headers.get('x-vercel-ip-city');
		return {
			latitude: lat,
			longitude: lng,
			city: city ? decodeURIComponent(city) : undefined,
			country: headers.get('x-vercel-ip-country') ?? undefined,
			source: 'edge'
		};
	}

	const forwarded = headers.get('x-forwarded-for')?.split(',')[0]?.trim();
	const ip = forwarded || clientAddress;
	if (ip && !isPrivate(ip)) {
		try {
			const r = await fetcher(`http://ip-api.com/json/${ip}?fields=status,lat,lon,city,country`);
			const d = await r.json();
			if (d.status === 'success') {
				return { latitude: d.lat, longitude: d.lon, city: d.city, country: d.country, source: 'ip' };
			}
		} catch {
			/* fall through */
		}
	}

	const a = config.launchArea;
	return { latitude: a.latitude, longitude: a.longitude, city: a.name, source: 'default' };
}

export function isPrivate(ip: string): boolean {
	return (
		ip === 'localhost' ||
		ip.startsWith('127.') ||
		ip === '::1' ||
		ip.startsWith('::ffff:127.') ||
		ip.startsWith('10.') ||
		ip.startsWith('192.168.') ||
		/^172\.(1[6-9]|2\d|3[01])\./.test(ip) ||
		ip.startsWith('100.') ||
		ip.startsWith('fc') ||
		ip.startsWith('fd')
	);
}
