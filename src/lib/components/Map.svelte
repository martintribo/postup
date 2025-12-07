<script lang="ts">
	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';

	interface Props {
		latitude: number;
		longitude: number;
		city?: string;
		country?: string;
	}

	let { latitude, longitude, city, country }: Props = $props();

	// Fix for default marker icon in Vite
	delete (L.Icon.Default.prototype as any)._getIconUrl;
	L.Icon.Default.mergeOptions({
		iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
		iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png'
	});

	let mapContainer: HTMLDivElement;
	let map: L.Map | null = null;

	/**
	 * Calculate bounds for a 50x50 square mile area centered on the given coordinates
	 */
	function calculateBounds(centerLat: number, centerLon: number): L.LatLngBounds {
		// 1 degree of latitude ≈ 69 miles
		// For 50 miles total (25 miles each direction): 25 / 69 ≈ 0.3623 degrees
		const latOffset = 25 / 69;

		// 1 degree of longitude ≈ 69 * cos(latitude) miles
		// For 50 miles total (25 miles each direction): 25 / (69 * cos(latitude))
		const lonOffset = 25 / (69 * Math.cos((centerLat * Math.PI) / 180));

		const north = centerLat + latOffset;
		const south = centerLat - latOffset;
		const east = centerLon + lonOffset;
		const west = centerLon - lonOffset;

		return L.latLngBounds([south, west], [north, east]);
	}

	onMount(() => {
		// Initialize the map
		map = L.map(mapContainer);

		// Add OpenStreetMap tiles
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution:
				'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			maxZoom: 19
		}).addTo(map);

		// Calculate bounds for 50x50 square mile area
		const bounds = calculateBounds(latitude, longitude);
		map.fitBounds(bounds);

		// Create popup text
		const popupText = city && country 
			? `You are near ${city}, ${country}`
			: city 
				? `You are near ${city}`
				: 'Your location';

		// Add a marker
		L.marker([latitude, longitude])
			.addTo(map)
			.bindPopup(popupText)
			.openPopup();

		return () => {
			if (map) {
				map.remove();
			}
		};
	});
</script>

<div bind:this={mapContainer} class="map-container"></div>

<style>
	.map-container {
		width: 100%;
		height: 500px;
		border-radius: 0.5rem;
		overflow: hidden;
		box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
	}

	:global(.leaflet-container) {
		height: 100%;
		width: 100%;
	}
</style>

