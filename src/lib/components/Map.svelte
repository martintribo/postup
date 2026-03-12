<script lang="ts">
	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import { env } from '$env/dynamic/public';
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
		isOpen: boolean | null;
		closesAt: string | null;
		opensAt: string | null;
		website: string | null;
		phone: string | null;
		photoRef: string | null;
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
	let userMarker: L.Marker | null = null;
	let nearbyCafes = $state<NearbyPlace[]>([]);
	let cafeIndex = new Map<string, NearbyPlace>(); // dedup by mapboxId
	let loadingPlaces = $state(false);
	let showSearchArea = $state(false);
	let hasDoneInitialFetch = false;

	// Open now filter
	let openNowFilter = $state(false);

	// Place search
	let searchQuery = $state('');
	let searchResults = $state<{ name: string; address: string; latitude: number; longitude: number }[]>([]);
	let showSearchResults = $state(false);
	let searchSelectedIndex = $state(-1);
	let searchDebounceTimer: ReturnType<typeof setTimeout> | null = null;
	let searchMarker: L.Marker | null = null;

	function mergeCafes(newCafes: NearbyPlace[]) {
		for (const cafe of newCafes) {
			cafeIndex.set(cafe.mapboxId, cafe);
		}
		nearbyCafes = Array.from(cafeIndex.values());
	}

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

	function createUserLocationIcon(): L.DivIcon {
		return L.divIcon({
			className: 'custom-user-marker',
			html: `<div style="width: 18px; height: 18px; border-radius: 50%; background-color: #3b82f6; border: 3px solid white; box-shadow: 0 0 0 2px rgba(59,130,246,0.3), 0 1px 4px rgba(0,0,0,0.3);"></div>`,
			iconSize: [18, 18],
			iconAnchor: [9, 9]
		});
	}

	function updateUserMarker() {
		if (!map) return;
		if (userMarker) map.removeLayer(userMarker);
		userMarker = L.marker([latitude, longitude], {
			icon: createUserLocationIcon(),
			zIndexOffset: 2000,
			interactive: false
		}).addTo(map);
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

	function createPlaceIcon(isOpen: boolean | null): L.DivIcon {
		// Green = open, gray = unknown, red-ish = closed
		const bgColor = isOpen === true ? '#059669' : isOpen === false ? '#9ca3af' : '#d1d5db';
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

	function buildPlacePopup(cafe: NearbyPlace): string {
		const link = cafe.claimed && cafe.id
			? `<a href="/places/${cafe.id}" style="color: #2563eb; text-decoration: underline; font-size: 0.75rem;">View profile</a>`
			: `<a href="/places/add?mapboxId=${encodeURIComponent(cafe.mapboxId || '')}&name=${encodeURIComponent(cafe.name)}&address=${encodeURIComponent(cafe.address)}&lat=${cafe.latitude}&lng=${cafe.longitude}" style="color: #059669; text-decoration: underline; font-size: 0.75rem;">Add to postup</a>`;

		let hoursLine = '';
		if (cafe.isOpen === true) {
			const detail = cafe.closesAt ? ` · closes ${cafe.closesAt}` : '';
			hoursLine = `<div style="font-size: 0.75rem; color: #059669; margin-bottom: 4px;">${cafe.closesAt ? 'Open' + detail : 'Open 24 hours'}</div>`;
		} else if (cafe.isOpen === false) {
			const parts = [];
			if (cafe.closesAt) parts.push(`closed ${cafe.closesAt}`);
			if (cafe.opensAt) parts.push(`opens ${cafe.opensAt}`);
			const detail = parts.length > 0 ? ` · ${parts.join(' · ')}` : '';
			hoursLine = `<div style="font-size: 0.75rem; color: #dc2626; margin-bottom: 4px;">Closed${detail}</div>`;
		}

		let contactLine = '';
		const contactParts = [];
		if (cafe.website) {
			const domain = cafe.website.replace(/^https?:\/\//, '').replace(/\/.*$/, '');
			contactParts.push(`<a href="${cafe.website}" target="_blank" rel="noopener noreferrer" style="color: #2563eb; text-decoration: underline;">${domain}</a>`);
		}
		if (cafe.phone) {
			contactParts.push(`<a href="tel:${cafe.phone}" style="color: #2563eb; text-decoration: underline;">${cafe.phone}</a>`);
		}
		if (contactParts.length > 0) {
			contactLine = `<div style="font-size: 0.75rem; margin-bottom: 4px;">${contactParts.join(' · ')}</div>`;
		}

		const photoLine = cafe.photoRef
			? `<img src="/api/places/photo?ref=${encodeURIComponent(cafe.photoRef)}" alt="${cafe.name}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 6px; margin-bottom: 6px;" />`
			: '';

		return `
			<div style="min-width: 200px; max-width: 260px;">
				${photoLine}
				<div style="font-weight: 600; margin-bottom: 2px;">${cafe.name}</div>
				<div style="font-size: 0.8rem; color: #666; margin-bottom: 4px;">${cafe.address}</div>
				${hoursLine}
				${contactLine}
				${link}
			</div>
		`;
	}

	function updatePlaceMarkers() {
		if (!map) return;
		const currentMap = map;
		placeMarkers.forEach((m) => currentMap.removeLayer(m));
		placeMarkers = [];

		const cafesToShow = openNowFilter ? nearbyCafes.filter((c) => c.isOpen === true) : nearbyCafes;

		cafesToShow.forEach((cafe) => {
			const marker = L.marker([cafe.latitude, cafe.longitude], {
				icon: createPlaceIcon(cafe.isOpen),
				zIndexOffset: 500
			}).addTo(currentMap);

			marker.bindPopup(buildPlacePopup(cafe));

			// Refresh data from Mapbox when the popup opens
			if (cafe.id) {
				const cafeId = cafe.id;
				marker.on('click', async () => {
					try {
						const tz = new Date().getTimezoneOffset();
						const res = await fetch(`/api/places/refresh?id=${cafeId}&tz=${tz}`);
						if (!res.ok) return;
						const data = await res.json();
						if (!data.place) return;
						const fresh = data.place as NearbyPlace;
						// Update the cached entry
						if (cafe.mapboxId) cafeIndex.set(cafe.mapboxId, fresh);
						// Update popup content and marker icon
						marker.setPopupContent(buildPlacePopup(fresh));
						marker.setIcon(createPlaceIcon(fresh.isOpen));
					} catch {
						// Keep showing stale data
					}
				});
			}

			placeMarkers.push(marker);
		});
	}

	function fitToContent(animate = false) {
		if (!map) return;

		// Collect all points: user location, posts, and cafes
		const points: L.LatLngExpression[] = [[latitude, longitude]];

		for (const p of posts) {
			points.push([p.latitude, p.longitude]);
		}
		for (const c of nearbyCafes) {
			points.push([c.latitude, c.longitude]);
		}

		if (points.length <= 1) {
			// No content besides user location — use default 40x40 mile bounds
			const bounds = calculateBounds(latitude, longitude);
			if (animate) {
				map.flyToBounds(bounds, { duration: 1.5 });
			} else {
				map.fitBounds(bounds);
			}
			return;
		}

		const bounds = L.latLngBounds(points).pad(0.1);
		if (animate) {
			map.flyToBounds(bounds, { duration: 1.5, maxZoom: 16 });
		} else {
			map.fitBounds(bounds, { maxZoom: 16 });
		}
	}

	async function searchThisArea() {
		if (!map) return;
		showSearchArea = false;
		loadingPlaces = true;
		try {
			const bounds = map.getBounds();
			const sw = bounds.getSouthWest();
			const ne = bounds.getNorthEast();
			const bbox = `${sw.lng},${sw.lat},${ne.lng},${ne.lat}`;
			const tz = new Date().getTimezoneOffset();
			const res = await fetch(`/api/places/nearby?bbox=${bbox}&tz=${tz}`);
			if (res.ok) {
				const data = await res.json();
				mergeCafes(data.places || []);
				updatePlaceMarkers();
			}
		} catch (err) {
			console.error('Failed to search area:', err);
		}
		loadingPlaces = false;
	}

	async function fetchNearbyCafes(lat: number, lng: number, animate = false) {
		if (!showPlaces) return;
		loadingPlaces = true;
		try {
			const tz = new Date().getTimezoneOffset();
			const res = await fetch(`/api/places/nearby?lat=${lat}&lng=${lng}&tz=${tz}`);
			if (res.ok) {
				const data = await res.json();
				mergeCafes(data.places || []);
				updatePlaceMarkers();
				fitToContent(animate);
			}
		} catch (err) {
			console.error('Failed to fetch nearby cafes:', err);
		}
		loadingPlaces = false;
		// Delay setting this so the initial fitToContent moveend doesn't trigger the button
		setTimeout(() => { hasDoneInitialFetch = true; }, 500);
	}

	// Place search
	async function searchPlaces(query: string) {
		if (query.length < 2) {
			searchResults = [];
			showSearchResults = false;
			return;
		}

		const accessToken = env.PUBLIC_MAPBOX_ACCESS_TOKEN;
		if (!accessToken) return;

		try {
			const params = new URLSearchParams({
				q: query,
				access_token: accessToken,
				limit: '5',
				language: 'en',
				types: 'poi,place,address'
			});

			if (latitude && longitude) {
				params.set('proximity', `${longitude},${latitude}`);
			}

			const response = await fetch(
				`https://api.mapbox.com/search/searchbox/v1/forward?${params.toString()}`
			);

			if (!response.ok) return;

			const data = await response.json();
			searchResults = (data.features || []).map((f: any) => ({
				name: f.properties?.name || 'Unknown',
				address: f.properties?.full_address || f.properties?.address || '',
				latitude: f.geometry?.coordinates?.[1] || 0,
				longitude: f.geometry?.coordinates?.[0] || 0
			}));
			showSearchResults = searchResults.length > 0;
			searchSelectedIndex = -1;
		} catch {
			searchResults = [];
			showSearchResults = false;
		}
	}

	function handleSearchInput(e: Event) {
		const target = e.target as HTMLInputElement;
		searchQuery = target.value;
		if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
		searchDebounceTimer = setTimeout(() => searchPlaces(searchQuery), 300);
	}

	function selectSearchResult(result: { name: string; address: string; latitude: number; longitude: number }) {
		searchQuery = result.name;
		showSearchResults = false;

		if (!map) return;

		// Remove previous search marker
		if (searchMarker) map.removeLayer(searchMarker);

		// Add a marker at the selected location
		searchMarker = L.marker([result.latitude, result.longitude], {
			icon: L.divIcon({
				className: 'custom-search-marker',
				html: `<div style="width: 36px; height: 36px; border-radius: 50%; background-color: #dc2626; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>`,
				iconSize: [36, 36],
				iconAnchor: [18, 36],
				popupAnchor: [0, -36]
			}),
			zIndexOffset: 1500
		}).addTo(map);

		searchMarker.bindPopup(`
			<div style="min-width: 180px;">
				<div style="font-weight: 600; margin-bottom: 2px;">${result.name}</div>
				<div style="font-size: 0.8rem; color: #666;">${result.address}</div>
			</div>
		`).openPopup();

		// Fly to the location and fetch cafes nearby
		map.flyTo([result.latitude, result.longitude], 15, { duration: 1.5 });

		// Fetch cafes around this location
		fetchNearbyCafes(result.latitude, result.longitude, false);
	}

	function handleSearchKeydown(e: KeyboardEvent) {
		if (!showSearchResults || searchResults.length === 0) return;

		if (e.key === 'ArrowDown') {
			e.preventDefault();
			searchSelectedIndex = Math.min(searchSelectedIndex + 1, searchResults.length - 1);
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			searchSelectedIndex = Math.max(searchSelectedIndex - 1, -1);
		} else if (e.key === 'Enter' && searchSelectedIndex >= 0) {
			e.preventDefault();
			selectSearchResult(searchResults[searchSelectedIndex]);
		} else if (e.key === 'Escape') {
			showSearchResults = false;
			searchSelectedIndex = -1;
		}
	}

	function handleSearchBlur() {
		setTimeout(() => { showSearchResults = false; }, 200);
	}

	function clearSearch() {
		searchQuery = '';
		searchResults = [];
		showSearchResults = false;
		if (searchMarker && map) {
			map.removeLayer(searchMarker);
			searchMarker = null;
		}
	}

	function toggleOpenNow() {
		openNowFilter = !openNowFilter;
		updatePlaceMarkers();
	}

	// Re-center map and fetch places when location changes
	let initialLoad = true;
	$effect(() => {
		if (map && latitude && longitude) {
			updateUserMarker();
			if (initialLoad) {
				initialLoad = false;
				return; // onMount handles initial load
			}
			fetchNearbyCafes(latitude, longitude, true);
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

		// Start with default bounds, then refine once cafes load
		const bounds = calculateBounds(latitude, longitude);
		map.fitBounds(bounds);

		updateUserMarker();
		updatePostMarkers();
		fetchNearbyCafes(latitude, longitude, false);

		// Show "Search this area" when user pans/zooms after initial load
		map.on('moveend', () => {
			if (hasDoneInitialFetch) {
				showSearchArea = true;
			}
		});

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

<div style="position: relative; width: 100%; height: 100%;">
	<div bind:this={mapContainer} class="map-container"></div>

	<!-- Search bar -->
	<div class="search-bar">
		<div class="search-input-wrapper">
			<svg xmlns="http://www.w3.org/2000/svg" class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
			<input
				type="text"
				value={searchQuery}
				oninput={handleSearchInput}
				onkeydown={handleSearchKeydown}
				onblur={handleSearchBlur}
				placeholder="Search for a place..."
				class="search-input"
				autocomplete="off"
			/>
			{#if searchQuery}
				<button type="button" onclick={clearSearch} class="search-clear" aria-label="Clear search">
					<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
				</button>
			{/if}
		</div>
		{#if showSearchResults && searchResults.length > 0}
			<ul class="search-results">
				{#each searchResults as result, index}
					<li>
						<button
							type="button"
							onclick={() => selectSearchResult(result)}
							class="search-result-item {searchSelectedIndex === index ? 'selected' : ''}"
						>
							<div class="search-result-name">{result.name}</div>
							{#if result.address}
								<div class="search-result-address">{result.address}</div>
							{/if}
						</button>
					</li>
				{/each}
			</ul>
		{/if}
	</div>

	<!-- Open now filter -->
	<button
		type="button"
		onclick={toggleOpenNow}
		class="open-now-btn {openNowFilter ? 'active' : ''}"
	>
		<div class="open-now-dot {openNowFilter ? 'active' : ''}"></div>
		Open now
	</button>

	{#if showSearchArea}
		<button
			type="button"
			onclick={searchThisArea}
			disabled={loadingPlaces}
			class="search-area-btn"
		>
			{#if loadingPlaces}
				Searching...
			{:else}
				Search this area
			{/if}
		</button>
	{/if}
</div>

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

	:global(.custom-search-marker),
	:global(.custom-coffee-marker),
	:global(.custom-place-marker),
	:global(.custom-user-marker) {
		background: transparent;
		border: none;
	}

	:global(.custom-coffee-marker .material-symbols-outlined) {
		font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
	}

	.search-bar {
		position: absolute;
		top: 12px;
		right: 12px;
		z-index: 1000;
		width: 280px;
	}

	.search-input-wrapper {
		display: flex;
		align-items: center;
		background: white;
		border: 1px solid #d1d5db;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
		overflow: hidden;
	}

	.search-icon {
		margin-left: 10px;
		color: #9ca3af;
		flex-shrink: 0;
	}

	.search-input {
		flex: 1;
		padding: 8px 8px;
		border: none;
		outline: none;
		font-size: 0.875rem;
		background: transparent;
		color: #111827;
	}

	.search-input::placeholder {
		color: #9ca3af;
	}

	.search-clear {
		padding: 6px 10px;
		background: none;
		border: none;
		color: #9ca3af;
		cursor: pointer;
		display: flex;
		align-items: center;
	}

	.search-clear:hover {
		color: #6b7280;
	}

	.search-results {
		margin-top: 4px;
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
		overflow: hidden;
		list-style: none;
		padding: 0;
	}

	.search-result-item {
		width: 100%;
		text-align: left;
		padding: 8px 12px;
		border: none;
		background: none;
		cursor: pointer;
		display: block;
	}

	.search-result-item:hover,
	.search-result-item.selected {
		background: #f3f4f6;
	}

	.search-result-name {
		font-size: 0.875rem;
		font-weight: 500;
		color: #111827;
	}

	.search-result-address {
		font-size: 0.75rem;
		color: #6b7280;
		margin-top: 1px;
	}

	@media (prefers-color-scheme: dark) {
		.search-input-wrapper {
			background: #1f2937;
			border-color: #374151;
		}

		.search-input {
			color: #f3f4f6;
		}

		.search-input::placeholder {
			color: #6b7280;
		}

		.search-results {
			background: #1f2937;
			border-color: #374151;
		}

		.search-result-item:hover,
		.search-result-item.selected {
			background: #374151;
		}

		.search-result-name {
			color: #f3f4f6;
		}

		.search-result-address {
			color: #9ca3af;
		}
	}

	.open-now-btn {
		position: absolute;
		top: 12px;
		right: 300px;
		z-index: 1000;
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 7px 14px;
		font-size: 0.875rem;
		font-weight: 500;
		color: #374151;
		background: white;
		border: 1px solid #d1d5db;
		border-radius: 9999px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
		cursor: pointer;
		transition: all 0.15s;
	}

	.open-now-btn:hover {
		border-color: #059669;
		color: #059669;
	}

	.open-now-btn.active {
		background: #ecfdf5;
		border-color: #059669;
		color: #059669;
	}

	.open-now-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #d1d5db;
		transition: background 0.15s;
	}

	.open-now-dot.active {
		background: #059669;
	}

	@media (max-width: 500px) {
		.open-now-btn {
			top: 52px;
			right: 12px;
		}
	}

	@media (prefers-color-scheme: dark) {
		.open-now-btn {
			background: #1f2937;
			border-color: #374151;
			color: #d1d5db;
		}

		.open-now-btn:hover {
			border-color: #059669;
			color: #34d399;
		}

		.open-now-btn.active {
			background: #064e3b;
			border-color: #059669;
			color: #34d399;
		}
	}

	.search-area-btn {
		position: absolute;
		top: 12px;
		left: 50%;
		transform: translateX(-50%);
		z-index: 1000;
		padding: 8px 16px;
		font-size: 0.875rem;
		font-weight: 500;
		color: #1e40af;
		background: white;
		border: 1px solid #bfdbfe;
		border-radius: 9999px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
		cursor: pointer;
		transition: all 0.15s;
	}

	.search-area-btn:hover {
		background: #eff6ff;
		border-color: #93c5fd;
	}

	.search-area-btn:disabled {
		color: #9ca3af;
		cursor: wait;
	}
</style>
