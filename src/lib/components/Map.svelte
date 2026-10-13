<script lang="ts">
	import { onMount, tick } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import { env } from '$env/dynamic/public';
	import type { Post } from '$lib/server/db/schema';
	import PlaceDetailsCard from '$lib/components/PlaceDetailsCard.svelte';
	import { googleMapsBrowserKey, loadGooglePlacesLibrary } from '$lib/google-maps';

	export interface NearbyPlace {
		id?: number;
		mapboxId: string | null;
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
		googlePlaceId: string | null;
		parking: string | null;
	}

	interface Props {
		latitude: number;
		longitude: number;
		city?: string;
		country?: string;
		posts?: Post[];
		showPlaces?: boolean;
		onCafesLoaded?: (cafes: NearbyPlace[]) => void;
	}

	let { latitude, longitude, city, country, posts = [], showPlaces = true, onCafesLoaded }: Props = $props();

	delete (L.Icon.Default.prototype as any)._getIconUrl;
	L.Icon.Default.mergeOptions({
		iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
		iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
		shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png'
	});

	const STADIA_ATTRIBUTION =
		'&copy; <a href="https://stadiamaps.com/attribution/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>';

	let mapContainer: HTMLDivElement;
	let mapPane: HTMLDivElement;
	let map: L.Map | null = null;
	let tileLayer: L.TileLayer | null = null;
	let postMarkers: L.Marker[] = [];
	let placeMarkers: L.Marker[] = [];
	let numberedMarkerByN = new Map<number, L.Marker>();
	let userMarker: L.Marker | null = null;
	let nearbyCafes = $state<NearbyPlace[]>([]);
	let cafeIndex = new Map<string, NearbyPlace>();
	let loadingPlaces = $state(false);
	let showSearchArea = $state(false);
	let hasDoneInitialFetch = false;

	let openNowFilter = $state(false);

	let searchQuery = $state('');
	let searchResults = $state<{ name: string; address: string; latitude: number; longitude: number }[]>([]);
	let showSearchResults = $state(false);
	let searchSelectedIndex = $state(-1);
	let searchDebounceTimer: ReturnType<typeof setTimeout> | null = null;
	let searchMarker: L.Marker | null = null;

	function panelLimit(): number {
		if (typeof window === 'undefined') return 8;
		const w = window.innerWidth;
		if (w < 480) return 6;
		if (w < 768) return 8;
		return 10;
	}

	let cardLimit = $state(panelLimit());
	let panelPlaces = $state<NearbyPlace[]>([]);
	let highlightedN = $state<number | null>(null);
	let showLeaders = $state(false);
	let googleReady = $state(false);
	let googleKeyMissing = $state(!googleMapsBrowserKey());
	let cardRowEls = $state<HTMLElement[]>([]);
	let leaderLines = $state<{ n: number; x1: number; y1: number; x2: number; y2: number }[]>([]);

	function cafeKey(cafe: NearbyPlace): string {
		if (cafe.mapboxId) return cafe.mapboxId;
		if (cafe.id) return `id:${cafe.id}`;
		return `${cafe.latitude},${cafe.longitude}`;
	}

	function getVisibleCafes(): NearbyPlace[] {
		if (!map) return [];
		const bounds = map.getBounds();
		const cafesToShow = openNowFilter ? nearbyCafes.filter((c) => c.isOpen === true) : nearbyCafes;
		return cafesToShow.filter((c) => bounds.contains([c.latitude, c.longitude]));
	}

	function computePanelPlaces() {
		if (!map) {
			panelPlaces = [];
			return;
		}
		const visible = getVisibleCafes();
		const center = map.getCenter();
		const sorted = [...visible].sort((a, b) => {
			const da = Math.hypot(a.latitude - center.lat, a.longitude - center.lng);
			const db = Math.hypot(b.latitude - center.lat, b.longitude - center.lng);
			return da - db;
		});
		panelPlaces = sorted.slice(0, cardLimit);
	}

	function updateLeaderLines() {
		if (!showLeaders || !map || !mapPane) {
			leaderLines = [];
			return;
		}
		const mapRect = mapPane.getBoundingClientRect();
		const lines: { n: number; x1: number; y1: number; x2: number; y2: number }[] = [];
		for (let i = 0; i < panelPlaces.length; i++) {
			const cafe = panelPlaces[i];
			const n = i + 1;
			const pt = map.latLngToContainerPoint([cafe.latitude, cafe.longitude]);
			const el = cardRowEls[i];
			if (!el) continue;
			const cr = el.getBoundingClientRect();
			const x1 = pt.x;
			const y1 = pt.y;
			let x2 = cr.left - mapRect.left;
			let y2 = cr.top + cr.height / 2 - mapRect.top;
			if (cr.top >= mapRect.bottom - 8) {
				x2 = cr.left + Math.min(48, cr.width / 2) - mapRect.left;
				y2 = mapRect.height;
			} else {
				x2 = Math.min(mapRect.width, Math.max(0, x2));
			}
			lines.push({ n, x1, y1, x2, y2 });
		}
		leaderLines = lines;
	}

	function mergeCafes(newCafes: NearbyPlace[]) {
		for (const cafe of newCafes) {
			cafeIndex.set(cafeKey(cafe), cafe);
		}
		nearbyCafes = Array.from(cafeIndex.values());
		onCafesLoaded?.(nearbyCafes);
	}

	function isDarkMode(): boolean {
		if (typeof window === 'undefined') return false;
		return window.matchMedia('(prefers-color-scheme: dark)').matches;
	}

	function getTileLayerUrl(isDark: boolean): string {
		if (isDark) {
			return 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png';
		}
		return 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png';
	}

	function updateTileLayer(isDark: boolean) {
		if (!map) return;
		if (tileLayer) map.removeLayer(tileLayer);
		tileLayer = L.tileLayer(getTileLayerUrl(isDark), {
			maxZoom: 20,
			attribution: STADIA_ATTRIBUTION
		}).addTo(map);
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

	function createNumberedIcon(n: number, isOpen: boolean | null, highlighted: boolean): L.DivIcon {
		const bgColor = isOpen === true ? '#059669' : isOpen === false ? '#9ca3af' : '#4b5563';
		const ring = highlighted ? '0 0 0 3px #2563eb, 0 2px 8px rgba(0,0,0,0.35)' : '0 1px 3px rgba(0,0,0,0.3)';
		const scale = highlighted ? 'transform: scale(1.18);' : '';
		return L.divIcon({
			className: 'custom-place-marker numbered-place-marker',
			html: `<div data-n="${n}" style="width: 28px; height: 28px; border-radius: 50%; background-color: ${bgColor}; color: white; font-weight: 700; font-size: 13px; display: flex; align-items: center; justify-content: center; box-shadow: ${ring}; cursor: pointer; ${scale}">${n}</div>`,
			iconSize: [28, 28],
			iconAnchor: [14, 28],
			popupAnchor: [0, -28]
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

		return `
			<div style="min-width: 200px; max-width: 260px;">
				<div style="font-weight: 600; margin-bottom: 2px;">${cafe.name}</div>
				<div style="font-size: 0.8rem; color: #666; margin-bottom: 4px;">${cafe.address}</div>
				${hoursLine}
				${contactLine}
				${link}
			</div>
		`;
	}

	function panelIndexForCafe(cafe: NearbyPlace): number {
		return panelPlaces.findIndex((p) => cafeKey(p) === cafeKey(cafe));
	}

	function setHighlight(n: number | null) {
		highlightedN = n;
		numberedMarkerByN.forEach((marker, num) => {
			const cafe = panelPlaces[num - 1];
			if (!cafe) return;
			marker.setIcon(createNumberedIcon(num, cafe.isOpen, n === num));
			marker.setZIndexOffset(n === num ? 800 : 600);
		});
		if (showLeaders) updateLeaderLines();
	}

	function updatePlaceMarkers() {
		if (!map) return;
		const currentMap = map;
		placeMarkers.forEach((m) => currentMap.removeLayer(m));
		placeMarkers = [];
		numberedMarkerByN = new Map();

		const cafesToShow = openNowFilter ? nearbyCafes.filter((c) => c.isOpen === true) : nearbyCafes;

		cafesToShow.forEach((cafe) => {
			const idx = panelIndexForCafe(cafe);
			const n = idx >= 0 ? idx + 1 : null;
			const highlighted = n !== null && highlightedN === n;
			const icon = n
				? createNumberedIcon(n, cafe.isOpen, highlighted)
				: createPlaceIcon(cafe.isOpen);
			const marker = L.marker([cafe.latitude, cafe.longitude], {
				icon,
				zIndexOffset: n ? 600 : 500
			}).addTo(currentMap);

			marker.bindPopup(buildPlacePopup(cafe));

			if (n) {
				numberedMarkerByN.set(n, marker);
				marker.on('mouseover', () => setHighlight(n));
				marker.on('mouseout', () => {
					if (highlightedN === n) setHighlight(null);
				});
				marker.on('click', () => {
					setHighlight(n);
					cardRowEls[n - 1]?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
				});
			}

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
						cafeIndex.set(cafeKey(fresh), fresh);
						nearbyCafes = Array.from(cafeIndex.values());
						marker.setPopupContent(buildPlacePopup(fresh));
					} catch {
						// Keep showing stale data
					}
				});
			}

			placeMarkers.push(marker);
		});
	}

	const placeIdFetchAttempted = new Set<number>();

	async function fillMissingPlaceIds(cafes: NearbyPlace[]) {
		const missing = cafes
			.filter((c) => c.id && !c.googlePlaceId && !placeIdFetchAttempted.has(c.id))
			.slice(0, cardLimit);
		if (missing.length === 0) return;
		for (const c of missing) if (c.id) placeIdFetchAttempted.add(c.id);
		const tz = new Date().getTimezoneOffset();
		await Promise.all(
			missing.map(async (cafe) => {
				try {
					const res = await fetch(`/api/places/refresh?id=${cafe.id}&tz=${tz}`);
					if (!res.ok) return;
					const data = await res.json();
					if (data.place) cafeIndex.set(cafeKey(data.place), data.place);
				} catch {
					// leave without place_id
				}
			})
		);
		nearbyCafes = Array.from(cafeIndex.values());
	}

	function refreshPanelAndMarkers() {
		computePanelPlaces();
		updatePlaceMarkers();
		void tick().then(updateLeaderLines);
		void fillMissingPlaceIds(panelPlaces).then(() => {
			computePanelPlaces();
			updatePlaceMarkers();
			void tick().then(updateLeaderLines);
		});
	}

	function fitToContent(animate = false) {
		if (!map) return;

		const points: L.LatLngExpression[] = [[latitude, longitude]];

		for (const p of posts) {
			points.push([p.latitude, p.longitude]);
		}
		for (const c of nearbyCafes) {
			points.push([c.latitude, c.longitude]);
		}

		if (points.length <= 1) {
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
				refreshPanelAndMarkers();
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
				refreshPanelAndMarkers();
				fitToContent(animate);
			}
		} catch (err) {
			console.error('Failed to fetch nearby cafes:', err);
		}
		loadingPlaces = false;
		setTimeout(() => { hasDoneInitialFetch = true; }, 500);
	}

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

		if (searchMarker) map.removeLayer(searchMarker);

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

		map.flyTo([result.latitude, result.longitude], 15, { duration: 1.5 });
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
		refreshPanelAndMarkers();
	}

	function toggleLeaders() {
		showLeaders = !showLeaders;
		void tick().then(updateLeaderLines);
	}

	function onCardEnter(n: number) {
		setHighlight(n);
	}

	function onCardLeave(n: number) {
		if (highlightedN === n) setHighlight(null);
	}

	function onCardActivate(n: number) {
		setHighlight(n);
		const marker = numberedMarkerByN.get(n);
		if (marker && map) {
			marker.openPopup();
			const ll = marker.getLatLng();
			map.panTo(ll, { animate: true });
		}
	}

	let initialLoad = true;
	$effect(() => {
		if (map && latitude && longitude) {
			updateUserMarker();
			if (initialLoad) {
				initialLoad = false;
				return;
			}
			fetchNearbyCafes(latitude, longitude, true);
		}
	});

	$effect(() => {
		if (map && posts) {
			updatePostMarkers();
		}
	});

	onMount(() => {
		googleKeyMissing = !googleMapsBrowserKey();
		void loadGooglePlacesLibrary().then((ok) => {
			googleReady = ok;
		});

		map = L.map(mapContainer);

		const darkMode = isDarkMode();
		updateTileLayer(darkMode);

		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		const handleChange = (e: MediaQueryListEvent) => updateTileLayer(e.matches);
		mediaQuery.addEventListener('change', handleChange);

		const bounds = calculateBounds(latitude, longitude);
		map.fitBounds(bounds);

		updateUserMarker();
		updatePostMarkers();
		fetchNearbyCafes(latitude, longitude, false);

		map.on('moveend', () => {
			if (hasDoneInitialFetch) {
				showSearchArea = true;
			}
			refreshPanelAndMarkers();
		});

		const handleResize = () => {
			cardLimit = panelLimit();
			map?.invalidateSize();
			refreshPanelAndMarkers();
		};
		window.addEventListener('resize', handleResize);

		const resizeObserver = new ResizeObserver(() => {
			setTimeout(() => {
				map?.invalidateSize();
				updateLeaderLines();
			}, 100);
		});
		resizeObserver.observe(mapPane);

		return () => {
			mediaQuery.removeEventListener('change', handleChange);
			window.removeEventListener('resize', handleResize);
			resizeObserver.disconnect();
			map?.remove();
		};
	});
</script>

<div class="map-shell">
	<div bind:this={mapPane} class="map-pane">
		<div bind:this={mapContainer} class="map-container"></div>

		<svg class="leader-svg" aria-hidden="true">
			{#if showLeaders}
				{#each leaderLines as line (line.n)}
					<line
						x1={line.x1}
						y1={line.y1}
						x2={line.x2}
						y2={line.y2}
						class={highlightedN === line.n ? 'leader-on' : 'leader-off'}
					/>
				{/each}
			{/if}
		</svg>

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
					{#each searchResults as result, index (`${result.latitude},${result.longitude}:${result.name}`)}
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

		<button
			type="button"
			onclick={toggleOpenNow}
			class="open-now-btn {openNowFilter ? 'active' : ''}"
		>
			<div class="open-now-dot {openNowFilter ? 'active' : ''}"></div>
			Open now
		</button>

		<button
			type="button"
			onclick={toggleLeaders}
			class="leaders-btn {showLeaders ? 'active' : ''}"
			aria-pressed={showLeaders}
		>
			Leader lines
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

	<aside class="places-panel" aria-label="Place details">
		<div class="panel-head">
			<div class="panel-title">Places</div>
			<div class="panel-sub">
				{#if loadingPlaces}
					Loading…
				{:else}
					{panelPlaces.length} of {cardLimit} in view
				{/if}
			</div>
		</div>
		{#if googleKeyMissing}
			<div class="panel-banner">
				Needs <code>PUBLIC_GOOGLE_MAPS_BROWSER_KEY</code> (referrer-restricted to
				dev-vm ports and postup.now) to load Google Place Details cards. Numbered
				markers use our stored coordinates.
			</div>
		{:else if !googleReady}
			<div class="panel-banner">Loading Google Place Details…</div>
		{/if}
		<div class="panel-list">
			{#each panelPlaces as cafe, i (cafeKey(cafe))}
				{@const n = i + 1}
				<div
					class="panel-row {highlightedN === n ? 'is-hot' : ''}"
					bind:this={cardRowEls[i]}
					onmouseenter={() => onCardEnter(n)}
					onmouseleave={() => onCardLeave(n)}
					onclick={() => onCardActivate(n)}
					onkeydown={(e) => {
						if (e.key === 'Enter' || e.key === ' ') {
							e.preventDefault();
							onCardActivate(n);
						}
					}}
					role="button"
					tabindex="0"
				>
					<div class="num-badge" aria-hidden="true">{n}</div>
					<div class="card-wrap">
						{#if googleReady && cafe.googlePlaceId}
							<PlaceDetailsCard placeId={cafe.googlePlaceId} />
						{:else}
							<div class="card-fallback">
								<div class="card-fallback-name">{cafe.name}</div>
								<div class="card-fallback-addr">{cafe.address}</div>
								{#if !cafe.googlePlaceId}
									<div class="card-fallback-note">No stored Google place_id</div>
								{/if}
							</div>
						{/if}
					</div>
				</div>
			{/each}
			{#if panelPlaces.length === 0 && !loadingPlaces}
				<div class="panel-empty">No cafes in this view. Search this area or pan the map.</div>
			{/if}
		</div>
	</aside>
</div>

<style>
	.map-shell {
		display: grid;
		grid-template-columns: 1fr 340px;
		width: 100%;
		height: 100%;
		min-height: 0;
	}

	.map-pane {
		position: relative;
		min-width: 0;
		min-height: 0;
	}

	.map-container {
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	:global(.leaflet-container) {
		height: 100%;
		width: 100%;
	}

	.leader-svg {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 450;
		clip-path: inset(0 0 28px 0);
	}

	.leader-off {
		stroke: rgba(37, 99, 235, 0.4);
		stroke-width: 1.5;
	}

	.leader-on {
		stroke: #2563eb;
		stroke-width: 2.5;
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

	.open-now-btn,
	.leaders-btn {
		position: absolute;
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

	.open-now-btn {
		top: 12px;
		right: 300px;
	}

	.leaders-btn {
		top: 52px;
		right: 12px;
	}

	.open-now-btn:hover,
	.leaders-btn:hover {
		border-color: #2563eb;
		color: #2563eb;
	}

	.open-now-btn.active,
	.leaders-btn.active {
		background: #eff6ff;
		border-color: #2563eb;
		color: #1d4ed8;
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

	.places-panel {
		display: flex;
		flex-direction: column;
		min-height: 0;
		background: #f9fafb;
		border-left: 1px solid #e5e7eb;
		z-index: 500;
	}

	.panel-head {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		padding: 10px 12px 8px;
		border-bottom: 1px solid #e5e7eb;
		background: white;
	}

	.panel-title {
		font-size: 0.9rem;
		font-weight: 650;
		color: #111827;
	}

	.panel-sub {
		font-size: 0.7rem;
		color: #6b7280;
	}

	.panel-banner {
		margin: 8px 12px 0;
		padding: 8px 10px;
		font-size: 0.75rem;
		line-height: 1.35;
		color: #92400e;
		background: #fffbeb;
		border: 1px solid #fde68a;
		border-radius: 8px;
	}

	.panel-banner code {
		font-size: 0.7rem;
	}

	.panel-list {
		flex: 1;
		overflow: auto;
		padding: 8px;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.panel-row {
		display: flex;
		align-items: stretch;
		gap: 8px;
		cursor: pointer;
		border-radius: 10px;
		padding: 2px;
	}

	.panel-row.is-hot {
		background: #dbeafe;
	}

	.num-badge {
		flex-shrink: 0;
		width: 22px;
		height: 22px;
		margin-top: 8px;
		border-radius: 50%;
		background: #111827;
		color: white;
		font-size: 11px;
		font-weight: 700;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.card-wrap {
		flex: 1;
		min-width: 0;
		overflow: hidden;
		border-radius: 8px;
	}

	.card-fallback {
		padding: 10px 12px;
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 8px;
	}

	.card-fallback-name {
		font-size: 0.85rem;
		font-weight: 600;
		color: #111827;
	}

	.card-fallback-addr {
		font-size: 0.75rem;
		color: #6b7280;
		margin-top: 2px;
	}

	.card-fallback-note {
		font-size: 0.7rem;
		color: #b45309;
		margin-top: 4px;
	}

	.panel-empty {
		padding: 16px 8px;
		font-size: 0.8rem;
		color: #6b7280;
		text-align: center;
	}

	@media (max-width: 768px) {
		.map-shell {
			grid-template-columns: 1fr;
			grid-template-rows: 1fr min(42vh, 360px);
		}

		.places-panel {
			border-left: none;
			border-top: 1px solid #e5e7eb;
			border-radius: 16px 16px 0 0;
			box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.12);
		}

		.open-now-btn {
			top: 52px;
			right: 12px;
		}

		.leaders-btn {
			top: 92px;
			right: 12px;
		}
	}

	@media (prefers-color-scheme: dark) {
		.open-now-btn,
		.leaders-btn {
			background: #1f2937;
			border-color: #374151;
			color: #d1d5db;
		}

		.open-now-btn:hover,
		.leaders-btn:hover {
			border-color: #60a5fa;
			color: #93c5fd;
		}

		.open-now-btn.active,
		.leaders-btn.active {
			background: #1e3a5f;
			border-color: #3b82f6;
			color: #93c5fd;
		}

		.places-panel {
			background: #111827;
			border-color: #374151;
		}

		.panel-head {
			background: #1f2937;
			border-color: #374151;
		}

		.panel-title {
			color: #f3f4f6;
		}

		.card-fallback {
			background: #1f2937;
			border-color: #374151;
		}

		.card-fallback-name {
			color: #f3f4f6;
		}

		.panel-row.is-hot {
			background: #1e3a5f;
		}
	}
</style>
