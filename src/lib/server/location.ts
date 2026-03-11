import type { RequestEvent } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import { env as privateEnv } from '$env/dynamic/private';
import { PUBLIC_MAPBOX_ACCESS_TOKEN } from '$env/static/public';

export interface GeoLocation {
	latitude: number;
	longitude: number;
	city?: string;
	country?: string;
}

export interface ReverseGeocodeResult {
	neighborhood?: string;
	locality?: string;
	district?: string;
}

export async function getLocationFromIP(ip: string): Promise<GeoLocation | null> {
	try {
		const response = await fetch(`http://ip-api.com/json/${ip}?fields=status,message,lat,lon,city,country`);
		const data = await response.json();
		if (data.status === 'success') {
			return { latitude: data.lat, longitude: data.lon, city: data.city, country: data.country };
		}
		return null;
	} catch (error) {
		console.error('Error fetching location:', error);
		return null;
	}
}

export function getClientIP(event: { getClientAddress: () => string }): string {
	return event.getClientAddress();
}

export function isLocalhost(ip: string): boolean {
	const localhostIPs = ['127.0.0.1', '::1', 'localhost', '::ffff:127.0.0.1'];
	return localhostIPs.includes(ip) || ip.startsWith('127.') || ip.startsWith('::1');
}

export function haversineDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
	const R = 3959;
	const dLat = (lat2 - lat1) * Math.PI / 180;
	const dLon = (lon2 - lon1) * Math.PI / 180;
	const a = Math.sin(dLat / 2) ** 2 +
		Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
		Math.sin(dLon / 2) ** 2;
	return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export async function reverseGeocode(latitude: number, longitude: number): Promise<ReverseGeocodeResult> {
	const accessToken = privateEnv.MAPBOX_ACCESS_TOKEN || PUBLIC_MAPBOX_ACCESS_TOKEN;
	if (!accessToken) {
		console.error('Mapbox access token is not configured');
		return {};
	}

	try {
		const params = new URLSearchParams({
			longitude: longitude.toString(),
			latitude: latitude.toString(),
			types: 'neighborhood,locality,district',
			access_token: accessToken
		});

		const response = await fetch(`https://api.mapbox.com/search/geocode/v6/reverse?${params.toString()}`);
		if (!response.ok) throw new Error(`Mapbox API error: ${response.status}`);

		const data = await response.json();
		const features = data.features || [];
		const result: ReverseGeocodeResult = {};

		if (features.length > 0) {
			const context = features[0].properties?.context || features[0].context || [];
			if (Array.isArray(context)) {
				for (const ctx of context) {
					if (ctx.id?.startsWith('neighborhood.')) result.neighborhood = ctx.text;
					else if (ctx.id?.startsWith('locality.')) result.locality = ctx.text;
					else if (ctx.id?.startsWith('district.')) result.district = ctx.text;
				}
			}
		}
		return result;
	} catch (error) {
		console.error('Error reverse geocoding:', error);
		return {};
	}
}

function getStoredLocation(event: RequestEvent): GeoLocation | null {
	const cookie = event.cookies.get(auth.userLocationCookieName);
	if (!cookie) return null;
	try {
		const parsed = JSON.parse(cookie);
		if (typeof parsed.latitude === 'number' && typeof parsed.longitude === 'number') {
			return parsed;
		}
	} catch {}
	return null;
}

export async function getUserLocation(event: RequestEvent): Promise<{ location: GeoLocation; source: 'precise' | 'ip' | 'default'; suggestUpdate: boolean }> {
	const stored = getStoredLocation(event);
	const clientIP = getClientIP(event);

	let ipLocation: GeoLocation | null = null;
	if (isLocalhost(clientIP)) {
		ipLocation = { latitude: 34.0522, longitude: -118.2437, city: 'Los Angeles', country: 'USA' };
	} else {
		ipLocation = await getLocationFromIP(clientIP);
	}

	const fallback: GeoLocation = ipLocation || { latitude: 51.505, longitude: -0.09, city: 'London', country: 'UK' };

	if (stored) {
		const suggestUpdate = ipLocation
			? haversineDistance(stored.latitude, stored.longitude, ipLocation.latitude, ipLocation.longitude) > 25
			: false;
		return { location: stored, source: 'precise', suggestUpdate };
	}

	return { location: fallback, source: ipLocation ? 'ip' : 'default', suggestUpdate: false };
}
