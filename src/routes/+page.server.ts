import type { PageServerLoad } from './$types';

interface GeoLocation {
	latitude: number;
	longitude: number;
	city?: string;
	country?: string;
}

async function getLocationFromIP(ip: string): Promise<GeoLocation | null> {
	try {
		// Using ip-api.com (free, no API key required)
		const response = await fetch(`http://ip-api.com/json/${ip}?fields=status,message,lat,lon,city,country`);
		const data = await response.json();

		if (data.status === 'success') {
			return {
				latitude: data.lat,
				longitude: data.lon,
				city: data.city,
				country: data.country
			};
		}
		return null;
	} catch (error) {
		console.error('Error fetching location:', error);
		return null;
	}
}

function getClientIP(event: { getClientAddress: () => string }): string {
	return event.getClientAddress();
}

function isLocalhost(ip: string): boolean {
	// Check for common localhost IPs
	const localhostIPs = ['127.0.0.1', '::1', 'localhost', '::ffff:127.0.0.1'];
	return localhostIPs.includes(ip) || ip.startsWith('127.') || ip.startsWith('::1');
}

export const load: PageServerLoad = async (event) => {
	const clientIP = getClientIP(event);
	
	// If localhost, default to Los Angeles
	if (isLocalhost(clientIP)) {
		const losAngelesLocation: GeoLocation = {
			latitude: 34.0522,
			longitude: -118.2437,
			city: 'Los Angeles',
			country: 'USA'
		};
		return {
			location: losAngelesLocation
		};
	}

	const location = await getLocationFromIP(clientIP);

	// Fallback to default location (London) if geo IP fails
	const defaultLocation: GeoLocation = {
		latitude: 51.505,
		longitude: -0.09,
		city: 'London',
		country: 'UK'
	};

	return {
		location: location || defaultLocation
	};
};

