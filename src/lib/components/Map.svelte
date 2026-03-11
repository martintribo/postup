<script lang="ts">
	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import type { Post } from '$lib/server/db/schema';

	interface NearbyPlace {
		id?: number;
		mapboxId: string;
		name: string;
		address: string;
		latitude: number;
		longitude: number;
		category: string | null;
		claimed: boolean;
	}

	interface Props {
		latitude: number;
		longitude: number;
		city?: string;
		country?: string;
		posts?: Post[];
		showPlaces?: boolean;
	}

	let { latitude, longitude, city, country, posts = [], showPlaces = true }: Props = $props();

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
	let postMarkers: L.Marker[] = [];
	let placeMarkers: L.Marker[] = [];
	let nearbyCafes = $state<NearbyPlace[]>([]);
	let loadingPlaces = $state(false);

	function isDarkMode(): boolean {
		if (typeof window === 'undefined') return false;
		return window.matchMedia('(prefers-color-scheme: dark)').matches;
	}

	function getTileLayerUrl(isDark: boolean): string {
		if (isDark) {
			return 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
		}
		return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	}

	function updateTileLayer(isDark: boolean) {
		if (!map) return;
		if (tileLayer) map.removeLayer(tileLayer);
		tileLayer = L.tileLayer(getTileLayerUrl(isDark), { maxZoom: 19 }).addTo(map);
	}

	function calculateBounds(centerLat: number, centerLon: number): L.LatLngBounds {
		const latOffset = 20 / 69;
		const lonOffset = 20 / (69 * Math.cos((centerLat * Math.PI) / 180));
		return L.latLngBounds(
			[centerLat - latOffset, centerLon - lonOffset],
			[centerLat + latOffset, centerLon + lonOffset]
		);
	}

	function formatDate(date: Date): string {
		return new Date(date).toLocaleString(undefined, {
			month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit'
		});
	}

	function getEndTime(startTime: Date, hours: number): Date {
		return new Date(new Date(startTime).getTime() + hours * 60 * 60 * 1000);
	}

	function createPostIcon(): L.DivIcon {
		return L.divIcon({
			className: 'custom-coffee-marker',
			html: `<div style="width: 40px; height: 40px; border-radius: 50%; background-color: #2563eb; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"><span class="material-symbols-outlined" style="font-size: 24px; color: white;">local_cafe</span></div>`,
			iconSize: [40, 40],
			iconAnchor: [20, 40],
			popupAnchor: [0, -40]
		});
	}

	function createPlaceIcon(claimed: boolean): L.DivIcon {
		const bgColor = claimed ? '#059669' : '#9ca3af';
		const icon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>`;
		return L.divIcon({
			className: 'custom-place-marker',
			html: `<div style="width: 30px; height: 30px; border-radius: 50%; background-color: ${bgColor}; display: flex; align-items: center; justify-content: center; box-shadow: 0 1px 3px rgba(0,0,0,0.3); cursor: pointer;">${icon}</div>`,
			iconSize: [30, 30],
			iconAnchor: [15, 30],
			popupAnchor: [0, -30]
		});
	}

	function updatePostMarkers() {
		if (!map) return;
		const currentMap = map;
		postMarkers.forEach((m) => currentMap.removeLayer(m));
		postMarkers = [];

		posts.forEach((postItem) => {
			const marker = L.marker([postItem.latitude, postItem.longitude], {
				icon: createPostIcon(),
				zIndexOffset: 1000
			}).addTo(currentMap);

			const endTime = getEndTime(postItem.startTime, postItem.hours);
			marker.bindPopup(`
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
			`);
			postMarkers.push(marker);
		});
	}

	function updatePlaceMarkers() {
		if (!map) return;
		const currentMap = map;
		placeMarkers.forEach((m) => currentMap.removeLayer(m));
		placeMarkers = [];

		nearbyCafes.forEach((cafe) => {
			const marker = L.marker([cafe.latitude, cafe.longitude], {
				icon: createPlaceIcon(cafe.claimed),
				zIndexOffset: 500
			}).addTo(currentMap);

			const link = cafe.claimed && cafe.id
				? `<a href="/places/${cafe.id}" style="color: #2563eb; text-decoration: underline; font-size: 0.75rem;">View profile</a>`
				: `<a href="/places/add?mapboxId=${encodeURIComponent(cafe.mapboxId)}&name=${encodeURIComponent(cafe.name)}&address=${encodeURIComponent(cafe.address)}&lat=${cafe.latitude}&lng=${cafe.longitude}" style="color: #059669; text-decoration: underline; font-size: 0.75rem;">Add to postup</a>`;

			marker.bindPopup(`
				<div style="min-width: 180px;">
					<div style="font-weight: 600; margin-bottom: 2px;">${cafe.name}</div>
					<div style="font-size: 0.8rem; color: #666; margin-bottom: 6px;">${cafe.address}</div>
					${link}
				</div>
			`);
			placeMarkers.push(marker);
		});
	}

	async function fetchNearbyCafes(lat: number, lng: number) {
		if (!showPlaces) return;
		loadingPlaces = true;
		try {
			const res = await fetch(`/api/places/nearby?lat=${lat}&lng=${lng}`);
			if (res.ok) {
				const data = await res.json();
				nearbyCafes = data.places || [];
				updatePlaceMarkers();
			}
		} catch (err) {
			console.error('Failed to fetch nearby cafes:', err);
		}
		loadingPlaces = false;
	}

	// Re-center map and fetch places when location changes
	$effect(() => {
		if (map && latitude && longitude) {
			const bounds = calculateBounds(latitude, longitude);
			map.flyToBounds(bounds, { duration: 1.5 });
			fetchNearbyCafes(latitude, longitude);
		}
	});

	// Update post markers when posts change
	$effect(() => {
		if (map && posts) {
			updatePostMarkers();
		}
	});

	onMount(() => {
		map = L.map(mapContainer, { attributionControl: false });

		const darkMode = isDarkMode();
		updateTileLayer(darkMode);

		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		const handleChange = (e: MediaQueryListEvent) => updateTileLayer(e.matches);
		mediaQuery.addEventListener('change', handleChange);

		const bounds = calculateBounds(latitude, longitude);
		map.fitBounds(bounds);

		updatePostMarkers();
		fetchNearbyCafes(latitude, longitude);

		const handleResize = () => map?.invalidateSize();
		window.addEventListener('resize', handleResize);

		const resizeObserver = new ResizeObserver(() => {
			setTimeout(() => map?.invalidateSize(), 100);
		});
		resizeObserver.observe(mapContainer);

		return () => {
			mediaQuery.removeEventListener('change', handleChange);
			window.removeEventListener('resize', handleResize);
			resizeObserver.disconnect();
			map?.remove();
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

	:global(.custom-coffee-marker),
	:global(.custom-place-marker) {
		background: transparent;
		border: none;
	}

	:global(.custom-coffee-marker .material-symbols-outlined) {
		font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
	}
</style>
