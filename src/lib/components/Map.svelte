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
		/** false = bare map (no search, filters or places panel), for the home live-now layout. */
		chrome?: boolean;
		onCafesLoaded?: (cafes: NearbyPlace[]) => void;
	}

	let { latitude, longitude, city, country, posts = [], showPlaces = true, chrome = true, onCafesLoaded }: Props = $props();

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
	let postMarkers: L.Layer[] = [];
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
	let showLeaders = $state(true);
	let googleReady = $state(false);
	let googleKeyMissing = $state(!googleMapsBrowserKey());
	let cardRowEls = $state<HTMLElement[]>([]);
	let leaderLines = $state.raw<{ n: number; x1: number; y1: number; x2: number; y2: number }[]>([]);
	let leaderRaf = 0;
	let leaderLoopHeld = false;
	let leaderLoopUntil = 0;

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

	function leaderTick() {
		leaderRaf = 0;
		updateLeaderLines();
		if (showLeaders && (leaderLoopHeld || performance.now() < leaderLoopUntil)) {
			leaderRaf = requestAnimationFrame(leaderTick);
		}
	}

	function startLeaderLoop() {
		if (!showLeaders) return;
		leaderLoopHeld = true;
		if (!leaderRaf) leaderRaf = requestAnimationFrame(leaderTick);
	}

	function bumpLeaderLoop(ms = 200) {
		if (!showLeaders) return;
		leaderLoopUntil = Math.max(leaderLoopUntil, performance.now() + ms);
		if (!leaderRaf) leaderRaf = requestAnimationFrame(leaderTick);
	}

	function releaseLeaderLoop() {
		leaderLoopHeld = false;
		bumpLeaderLoop(80);
	}

	function cancelLeaderLoop() {
		if (leaderRaf) cancelAnimationFrame(leaderRaf);
		leaderRaf = 0;
		leaderLoopHeld = false;
		leaderLoopUntil = 0;
	}

	function onPanelScroll() {
		bumpLeaderLoop(200);
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
		return document.documentElement.dataset.theme === 'night';
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
			html: `<div style="width: 18px; height: 18px; border-radius: 50%; background-color: var(--pu-accent); border: 3px solid white; box-shadow: 0 0 0 2px rgba(59,130,246,0.3), 0 1px 4px rgba(0,0,0,0.3);"></div>`,
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
			html: `<div style="width: 40px; height: 40px; border-radius: 50%; background-color: var(--pu-accent); display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"><span class="material-symbols-outlined" style="font-size: 24px; color: var(--pu-accent-text);">local_cafe</span></div>`,
			iconSize: [40, 40],
			iconAnchor: [20, 40],
			popupAnchor: [0, -40]
		});
	}

	// Mockup live pin: avatar with a pulse ring, count badge when several people share a spot.
	const PIN_COLORS = ['#7c3aed', '#e11d48', '#0891b2', '#d97706', '#2563eb', '#10a364', '#db2777', '#4f46e5'];
	function livePinIcon(name: string, count: number): L.DivIcon {
		const n = name || '?';
		const c = PIN_COLORS[[...n].reduce((a, ch) => (a * 31 + ch.charCodeAt(0)) >>> 0, 7) % PIN_COLORS.length];
		const safe = n[0].toUpperCase().replace(/[<>&"]/g, '');
		return L.divIcon({
			className: 'pu-live-pin',
			html: `<span class="mk live" style="position:relative;transform:none"><span class="pulse"></span><span class="av" style="--c:${c};width:34px;height:34px;font-size:14px">${safe}</span><em>${count > 1 ? count : ''}</em></span>`,
			iconSize: [34, 34],
			iconAnchor: [17, 17],
			popupAnchor: [0, -20]
		});
	}
	function cafePinIcon(): L.DivIcon {
		return L.divIcon({
			className: 'pu-cafe-pin',
			html: `<span class="mk cafe" style="position:relative;transform:none"><span class="cp"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v3M12 3v3"/></svg></span></span>`,
			iconSize: [32, 32],
			iconAnchor: [16, 16]
		});
	}

	function createPlaceIcon(isOpen: boolean | null): L.DivIcon {
		if (!chrome) return cafePinIcon();
		const bgColor = isOpen === true ? 'var(--pu-live)' : isOpen === false ? 'var(--pu-subtle)' : 'var(--pu-border)';
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
		if (!chrome) return cafePinIcon();
		const bgColor = isOpen === true ? 'var(--pu-live)' : isOpen === false ? 'var(--pu-subtle)' : 'var(--pu-muted)';
		const ring = highlighted ? '0 0 0 3px var(--pu-accent), 0 2px 8px rgba(0,0,0,0.35)' : '0 1px 3px rgba(0,0,0,0.3)';
		const scale = highlighted ? 'transform: scale(1.18);' : '';
		return L.divIcon({
			className: 'custom-place-marker numbered-place-marker',
			html: `<div data-n="${n}" style="width: 28px; height: 28px; border-radius: 50%; background-color: ${bgColor}; color: var(--pu-accent-text); font-weight: 700; font-size: 13px; display: flex; align-items: center; justify-content: center; box-shadow: ${ring}; cursor: pointer; ${scale}">${n}</div>`,
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

		const perSpot = new globalThis.Map<string, number>();
		posts.forEach((p) => {
			const k = `${p.latitude.toFixed(4)},${p.longitude.toFixed(4)}`;
			perSpot.set(k, (perSpot.get(k) ?? 0) + 1);
		});
		const drawn = new Set<string>();
		posts.forEach((postItem) => {
			const spot = `${postItem.latitude.toFixed(4)},${postItem.longitude.toFixed(4)}`;
			if (drawn.has(spot)) return;
			drawn.add(spot);
			// Ask-to-join with hidden cafe: show an area, not a pin (D2).
			const hidden = (postItem as Post & { cafeHidden?: boolean }).cafeHidden;
			const marker = (hidden
				? L.circle([postItem.latitude, postItem.longitude], { radius: 700, color: '#1f7a4d', weight: 1, fillOpacity: 0.15, className: 'pu-area-marker' })
				: L.marker([postItem.latitude, postItem.longitude], { icon: livePinIcon(postItem.name, perSpot.get(spot) ?? 1), zIndexOffset: 1000 })
			).addTo(currentMap);

			const endTime = getEndTime(postItem.startTime, postItem.hours);
			marker.bindPopup(`
				<div style="min-width: 200px;">
					<div style="font-weight: 600; margin-bottom: 4px;">${postItem.name}</div>
					<div style="font-size: 0.875rem; color: var(--pu-muted); margin-bottom: 4px;">${postItem.activity}</div>
					<div style="font-size: 0.875rem; color: var(--pu-muted); margin-bottom: 4px;">${postItem.location}</div>
					<div style="font-size: 0.75rem; color: var(--pu-subtle);">
						${formatDate(postItem.startTime)} – ${formatDate(endTime)}
					</div>
					<div style="font-size: 0.75rem; color: var(--pu-subtle); margin-top: 4px;">
						${postItem.hours} ${postItem.hours === 1 ? 'hour' : 'hours'}
					</div>
				</div>
			`);
			postMarkers.push(marker);
		});
	}

	function buildPlacePopup(cafe: NearbyPlace): string {
		const link = cafe.claimed && cafe.id
			? `<a href="/places/${cafe.id}" style="color: var(--pu-accent); text-decoration: underline; font-size: 0.75rem;">View profile</a>`
			: `<a href="/places/add?mapboxId=${encodeURIComponent(cafe.mapboxId || '')}&name=${encodeURIComponent(cafe.name)}&address=${encodeURIComponent(cafe.address)}&lat=${cafe.latitude}&lng=${cafe.longitude}" style="color: var(--pu-live); text-decoration: underline; font-size: 0.75rem;">Add to postup</a>`;

		let hoursLine = '';
		if (cafe.isOpen === true) {
			const detail = cafe.closesAt ? ` · closes ${cafe.closesAt}` : '';
			hoursLine = `<div style="font-size: 0.75rem; color: var(--pu-live); margin-bottom: 4px;">${cafe.closesAt ? 'Open' + detail : 'Open 24 hours'}</div>`;
		} else if (cafe.isOpen === false) {
			const parts = [];
			if (cafe.closesAt) parts.push(`closed ${cafe.closesAt}`);
			if (cafe.opensAt) parts.push(`opens ${cafe.opensAt}`);
			const detail = parts.length > 0 ? ` · ${parts.join(' · ')}` : '';
			hoursLine = `<div style="font-size: 0.75rem; color: var(--pu-danger); margin-bottom: 4px;">Closed${detail}</div>`;
		}

		let contactLine = '';
		const contactParts = [];
		if (cafe.website) {
			const domain = cafe.website.replace(/^https?:\/\//, '').replace(/\/.*$/, '');
			contactParts.push(`<a href="${cafe.website}" target="_blank" rel="noopener noreferrer" style="color: var(--pu-accent); text-decoration: underline;">${domain}</a>`);
		}
		if (cafe.phone) {
			contactParts.push(`<a href="tel:${cafe.phone}" style="color: var(--pu-accent); text-decoration: underline;">${cafe.phone}</a>`);
		}
		if (contactParts.length > 0) {
			contactLine = `<div style="font-size: 0.75rem; margin-bottom: 4px;">${contactParts.join(' · ')}</div>`;
		}

		return `
			<div style="min-width: 200px; max-width: 260px;">
				<div style="font-weight: 600; margin-bottom: 2px;">${cafe.name}</div>
				<div style="font-size: 0.8rem; color: var(--pu-muted); margin-bottom: 4px;">${cafe.address}</div>
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
					bumpLeaderLoop(500);
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
		void tick().then(() => bumpLeaderLoop(400));
		void fillMissingPlaceIds(panelPlaces).then(() => {
			computePanelPlaces();
			updatePlaceMarkers();
			void tick().then(() => bumpLeaderLoop(400));
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
				html: `<div style="width: 36px; height: 36px; border-radius: 50%; background-color: var(--pu-danger); display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.3);"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>`,
				iconSize: [36, 36],
				iconAnchor: [18, 36],
				popupAnchor: [0, -36]
			}),
			zIndexOffset: 1500
		}).addTo(map);

		searchMarker.bindPopup(`
			<div style="min-width: 180px;">
				<div style="font-weight: 600; margin-bottom: 2px;">${result.name}</div>
				<div style="font-size: 0.8rem; color: var(--pu-muted);">${result.address}</div>
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
		if (showLeaders) {
			void tick().then(() => bumpLeaderLoop(120));
		} else {
			cancelLeaderLoop();
			leaderLines = [];
		}
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
		// Basemap follows the active style (Night = dark tiles).
		const themeObserver = new MutationObserver(() => updateTileLayer(isDarkMode()));
		themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		const handleChange = () => updateTileLayer(isDarkMode());
		mediaQuery.addEventListener('change', handleChange);

		const bounds = calculateBounds(latitude, longitude);
		map.fitBounds(bounds);

		updateUserMarker();
		updatePostMarkers();
		fetchNearbyCafes(latitude, longitude, false);

		map.on('movestart zoomstart', startLeaderLoop);
		map.on('moveend zoomend', () => {
			releaseLeaderLoop();
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
			cancelLeaderLoop();
			mediaQuery.removeEventListener('change', handleChange);
			window.removeEventListener('resize', handleResize);
			resizeObserver.disconnect();
			map?.remove();
		};
	});
</script>

<div class="map-shell" class:bare={!chrome}>
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
		<div class="panel-list" onscroll={onPanelScroll}>
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
		stroke: var(--pu-accent);
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
		background: var(--pu-surface);
		border: 1px solid var(--pu-border);
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
		overflow: hidden;
	}

	.search-icon {
		margin-left: 10px;
		color: var(--pu-subtle);
		flex-shrink: 0;
	}

	.search-input {
		flex: 1;
		padding: 8px 8px;
		border: none;
		outline: none;
		font-size: 0.875rem;
		background: transparent;
		color: var(--pu-text);
	}

	.search-input::placeholder {
		color: var(--pu-subtle);
	}

	.search-clear {
		padding: 6px 10px;
		background: none;
		border: none;
		color: var(--pu-subtle);
		cursor: pointer;
		display: flex;
		align-items: center;
	}

	.search-clear:hover {
		color: var(--pu-muted);
	}

	.search-results {
		margin-top: 4px;
		background: var(--pu-surface);
		border: 1px solid var(--pu-border);
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
		background: var(--pu-surface-2);
	}

	.search-result-name {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--pu-text);
	}

	.search-result-address {
		font-size: 0.75rem;
		color: var(--pu-muted);
		margin-top: 1px;
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
		color: var(--pu-text);
		background: var(--pu-surface);
		border: 1px solid var(--pu-border);
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
		border-color: var(--pu-accent);
		color: var(--pu-accent);
	}

	.open-now-btn.active,
	.leaders-btn.active {
		background: var(--pu-accent-soft);
		border-color: var(--pu-accent);
		color: var(--pu-accent-hover);
	}

	.open-now-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--pu-border);
		transition: background 0.15s;
	}

	.open-now-dot.active {
		background: var(--pu-live);
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
		color: var(--pu-accent-hover);
		background: var(--pu-surface);
		border: 1px solid var(--pu-accent-soft);
		border-radius: 9999px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
		cursor: pointer;
		transition: all 0.15s;
	}

	.search-area-btn:hover {
		background: var(--pu-accent-soft);
		border-color: var(--pu-accent);
	}

	.search-area-btn:disabled {
		color: var(--pu-subtle);
		cursor: wait;
	}

	.places-panel {
		display: flex;
		flex-direction: column;
		min-height: 0;
		background: var(--pu-bg);
		border-left: 1px solid var(--pu-border);
		z-index: 500;
	}

	.panel-head {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		padding: 10px 12px 8px;
		border-bottom: 1px solid var(--pu-border);
		background: var(--pu-surface);
	}

	.panel-title {
		font-size: 0.9rem;
		font-weight: 650;
		color: var(--pu-text);
	}

	.panel-sub {
		font-size: 0.7rem;
		color: var(--pu-muted);
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
		background: var(--pu-accent-soft);
	}

	.num-badge {
		flex-shrink: 0;
		width: 22px;
		height: 22px;
		margin-top: 8px;
		border-radius: 50%;
		background: var(--pu-text);
		color: var(--pu-accent-text);
		font-size: 11px;
		font-weight: 700;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.card-wrap {
		flex: 1;
		min-width: 0;
		overflow: visible;
		border-radius: 8px;
	}

	.card-fallback {
		padding: 10px 12px;
		background: var(--pu-surface);
		border: 1px solid var(--pu-border);
		border-radius: 8px;
	}

	.card-fallback-name {
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--pu-text);
	}

	.card-fallback-addr {
		font-size: 0.75rem;
		color: var(--pu-muted);
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
		color: var(--pu-muted);
		text-align: center;
	}

	.map-shell.bare { grid-template-columns: 1fr; grid-template-rows: 1fr; }
	.map-shell.bare .places-panel,
	.map-shell.bare .search-bar,
	.map-shell.bare .open-now-btn,
	.map-shell.bare .leaders-btn,
	.map-shell.bare .leader-svg,
	.map-shell.bare .search-area-btn { display: none; }
	.map-shell.bare :global(.leaflet-control-zoom) { display: none; }

	@media (max-width: 768px) {
		.map-shell.bare { grid-template-rows: 1fr; }
		.map-shell {
			grid-template-columns: 1fr;
			grid-template-rows: 1fr min(42vh, 360px);
		}

		.places-panel {
			border-left: none;
			border-top: 1px solid var(--pu-border);
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


</style>
