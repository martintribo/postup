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

	onMount(() => {
		// Initialize the map with provided coordinates
		map = L.map(mapContainer).setView([latitude, longitude], 13);

		// Add OpenStreetMap tiles
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution:
				'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			maxZoom: 19
		}).addTo(map);

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

