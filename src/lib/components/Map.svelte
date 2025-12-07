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
	let tileLayer: L.TileLayer | null = null;

	/**
	 * Detect if the system prefers dark mode
	 */
	function isDarkMode(): boolean {
		if (typeof window === 'undefined') return false;
		return window.matchMedia('(prefers-color-scheme: dark)').matches;
	}

	/**
	 * Get the appropriate tile layer URL based on dark mode preference
	 */
	function getTileLayerUrl(isDark: boolean): string {
		if (isDark) {
			// CartoDB Dark Matter - a popular dark map style
			return 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
		} else {
			// OpenStreetMap standard tiles for light mode
			return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
		}
	}

	/**
	 * Update the tile layer based on dark mode preference
	 */
	function updateTileLayer(isDark: boolean) {
		if (!map) return;

		// Remove existing tile layer
		if (tileLayer) {
			map.removeLayer(tileLayer);
		}

		// Add new tile layer
		tileLayer = L.tileLayer(getTileLayerUrl(isDark), {
			maxZoom: 19
		}).addTo(map);
	}

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
		// Initialize the map with attribution control disabled
		map = L.map(mapContainer, {
			attributionControl: false
		});

		// Detect initial dark mode preference
		const darkMode = isDarkMode();
		updateTileLayer(darkMode);

		// Listen for changes in system dark mode preference
		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		const handleChange = (e: MediaQueryListEvent) => {
			updateTileLayer(e.matches);
		};

		// Modern browsers
		if (mediaQuery.addEventListener) {
			mediaQuery.addEventListener('change', handleChange);
		} else {
			// Fallback for older browsers
			mediaQuery.addListener(handleChange);
		}

		// Calculate bounds for 50x50 square mile area
		const bounds = calculateBounds(latitude, longitude);
		map.fitBounds(bounds);

		return () => {
			if (mediaQuery.removeEventListener) {
				mediaQuery.removeEventListener('change', handleChange);
			} else {
				mediaQuery.removeListener(handleChange);
			}
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

