<script lang="ts">
	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import type { Post } from '$lib/server/db/schema';

	interface Props {
		latitude: number;
		longitude: number;
		city?: string;
		country?: string;
		posts?: Post[];
	}

	let { latitude, longitude, city, country, posts = [] }: Props = $props();

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
	let markers: L.Marker[] = [];

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
	 * Calculate bounds for a 40x40 square mile area centered on the given coordinates
	 */
	function calculateBounds(centerLat: number, centerLon: number): L.LatLngBounds {
		// 1 degree of latitude ≈ 69 miles
		// For 40 miles total (20 miles each direction): 20 / 69 ≈ 0.2899 degrees
		const latOffset = 20 / 69;

		// 1 degree of longitude ≈ 69 * cos(latitude) miles
		// For 40 miles total (20 miles each direction): 20 / (69 * cos(latitude))
		const lonOffset = 20 / (69 * Math.cos((centerLat * Math.PI) / 180));

		const north = centerLat + latOffset;
		const south = centerLat - latOffset;
		const east = centerLon + lonOffset;
		const west = centerLon - lonOffset;

		return L.latLngBounds([south, west], [north, east]);
	}

	/**
	 * Format date for display
	 */
	function formatDate(date: Date): string {
		return new Date(date).toLocaleString(undefined, {
			month: 'short',
			day: 'numeric',
			hour: 'numeric',
			minute: '2-digit'
		});
	}

	/**
	 * Calculate end time for a post
	 */
	function getEndTime(startTime: Date, hours: number): Date {
		return new Date(new Date(startTime).getTime() + hours * 60 * 60 * 1000);
	}

	/**
	 * Update post markers on the map
	 */
	function updatePostMarkers() {
		if (!map) return;
		const currentMap = map;

		// Remove existing markers
		markers.forEach((marker) => {
			currentMap.removeLayer(marker);
		});
		markers = [];

		// Add markers for each post
		posts.forEach((postItem) => {
			const marker = L.marker([postItem.latitude, postItem.longitude]).addTo(currentMap);

			const endTime = getEndTime(postItem.startTime, postItem.hours);
			const popupContent = `
				<div style="min-width: 200px;">
					<div style="font-weight: 600; margin-bottom: 4px;">${postItem.name}</div>
					<div style="font-size: 0.875rem; color: #555; margin-bottom: 4px;">${postItem.activity}</div>
					<div style="font-size: 0.875rem; color: #666; margin-bottom: 4px;">${postItem.location}</div>
					<div style="font-size: 0.75rem; color: #888;">
						${formatDate(postItem.startTime)} – ${formatDate(endTime)}
					</div>
					<div style="font-size: 0.75rem; color: #888; margin-top: 4px;">
						${postItem.hours} ${postItem.hours === 1 ? 'hour' : 'hours'}
					</div>
				</div>
			`;

			marker.bindPopup(popupContent);
			markers.push(marker);
		});
	}

	// Update markers when posts change
	$effect(() => {
		if (map && posts) {
			updatePostMarkers();
		}
	});

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

		// Add markers for posts
		updatePostMarkers();

		// Handle window resize to update map size
		const handleResize = () => {
			if (map) {
				map.invalidateSize();
			}
		};
		window.addEventListener('resize', handleResize);

		// Use ResizeObserver to detect container size changes (better for responsive layouts)
		const resizeObserver = new ResizeObserver(() => {
			const currentMap = map;
			if (currentMap) {
				// Small delay to ensure layout has settled
				setTimeout(() => {
					currentMap.invalidateSize();
				}, 100);
			}
		});
		resizeObserver.observe(mapContainer);

		return () => {
			if (mediaQuery.removeEventListener) {
				mediaQuery.removeEventListener('change', handleChange);
			} else {
				mediaQuery.removeListener(handleChange);
			}
			window.removeEventListener('resize', handleResize);
			resizeObserver.disconnect();
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
		height: 100%;
		overflow: hidden;
	}

	:global(.leaflet-container) {
		height: 100%;
		width: 100%;
	}
</style>

