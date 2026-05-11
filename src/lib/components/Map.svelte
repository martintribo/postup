<script lang="ts">
	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import { env } from '$env/dynamic/public';
	import { forceSimulation, forceX, forceY, forceCollide, type SimulationNodeDatum } from 'd3-force';
	import type { Post } from '$lib/server/db/schema';

	export interface NearbyPlace {
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

	// Photo cards overlay — responsive sizing
	function getCardConfig() {
		if (typeof window === 'undefined') return { limit: 5, w: 140, h: 110 };
		const w = window.innerWidth;
		if (w < 480) return { limit: 6, w: 70, h: 72 };
		if (w < 768) return { limit: 8, w: 90, h: 92 };
		return { limit: 10, w: 130, h: 118 };
	}

	let cardConfig = $state(getCardConfig());
	$effect(() => {
		if (typeof window === 'undefined') return;
		const onResize = () => { cardConfig = getCardConfig(); updatePhotoCards(); };
		window.addEventListener('resize', onResize);
		return () => window.removeEventListener('resize', onResize);
	});

	const PHOTO_CARD_LIMIT = $derived(cardConfig.limit);
	const CARD_W = $derived(cardConfig.w);
	const CARD_H = $derived(cardConfig.h);

	interface PhotoCard extends SimulationNodeDatum {
		cafe: NearbyPlace;
		anchorX: number;
		anchorY: number;
	}

	let photoCards = $state<PhotoCard[]>([]);
	let photoOverlay: HTMLDivElement;
	let photoFetchQueue = new Set<number>();
	let springRAF: number | null = null;
	let draggedCard: PhotoCard | null = $state(null);
	let dragOffsetX = 0;
	let dragOffsetY = 0;
	let dragStartX = 0;
	let dragStartY = 0;
	let didDrag = false;

	function startSpringLoop() {
		if (springRAF) return;
		const tick = () => {
			if (photoCards.length === 0) { springRAF = null; return; }
			const rect = mapContainer?.getBoundingClientRect();
			if (!rect || !map) { springRAF = requestAnimationFrame(tick); return; }

			let moved = false;
			const minAnchorDist = CARD_H * 0.7 + 20;

			// Get all visible marker screen positions
			const allMarkers = placeMarkers.map((m) => {
				const pt = map!.latLngToContainerPoint(m.getLatLng());
				return { x: pt.x, y: pt.y };
			});

			for (const card of photoCards) {
				// Update anchor to current screen position of the marker
				const pt = map.latLngToContainerPoint([card.cafe.latitude, card.cafe.longitude]);
				const prevAx = card.anchorX;
				const prevAy = card.anchorY;
				card.anchorX = pt.x;
				card.anchorY = pt.y;

				// Shift card position by the same delta so it moves with the map
				const adx = card.anchorX - prevAx;
				const ady = card.anchorY - prevAy;
				if (Math.abs(adx) > 0.1 || Math.abs(ady) > 0.1) {
					card.x = (card.x ?? 0) + adx;
					card.y = (card.y ?? 0) + ady;
					moved = true;
				}

				// Skip physics for the card being dragged
				if (card === draggedCard) continue;

				let tx = card.x ?? 0;
				let ty = card.y ?? 0;
				const cx = tx + CARD_W / 2;
				const cy = ty + CARD_H / 2;

				// Pull toward anchor (gentle)
				const dax = card.anchorX - cx;
				const day = card.anchorY - cy;
				const anchorDist = Math.hypot(dax, day);
				if (anchorDist > minAnchorDist) {
					tx += dax * 0.03;
					ty += day * 0.03;
				}

				// Push away from other cards (rect-to-rect)
				for (const other of photoCards) {
					if (other === card) continue;
					const ox = other.x ?? 0;
					const oy = other.y ?? 0;
					const overlapX = (CARD_W + 8) - Math.abs((tx + CARD_W / 2) - (ox + CARD_W / 2));
					const overlapY = (CARD_H + 8) - Math.abs((ty + CARD_H / 2) - (oy + CARD_H / 2));
					if (overlapX > 0 && overlapY > 0) {
						const docx = (tx + CARD_W / 2) - (ox + CARD_W / 2);
						const docy = (ty + CARD_H / 2) - (oy + CARD_H / 2);
						const dist = Math.hypot(docx, docy) || 1;
						const push = Math.min(overlapX, overlapY) * 0.4;
						tx += (docx / dist) * push;
						ty += (docy / dist) * push;
					}
				}

				// Push away from all marker icons (rect-to-point with padding)
				const padX = CARD_W / 2 + 18;
				const padY = CARD_H / 2 + 18;
				for (const mp of allMarkers) {
					const dx = mp.x - (tx + CARD_W / 2);
					const dy = mp.y - (ty + CARD_H / 2);
					const overlapX = padX - Math.abs(dx);
					const overlapY = padY - Math.abs(dy);
					if (overlapX > 0 && overlapY > 0) {
						const dist = Math.hypot(dx, dy) || 1;
						const push = Math.min(overlapX, overlapY) * 0.5;
						tx -= (dx / dist) * push;
						ty -= (dy / dist) * push;
					}
				}

				// Clamp to container
				tx = Math.max(4, Math.min(rect.width - CARD_W - 4, tx));
				ty = Math.max(4, Math.min(rect.height - CARD_H - 4, ty));

				if (Math.abs(tx - (card.x ?? 0)) > 0.3 || Math.abs(ty - (card.y ?? 0)) > 0.3) {
					card.x = tx;
					card.y = ty;
					moved = true;
				}
			}
			if (moved) {
				photoCards = [...photoCards];
			}
			springRAF = requestAnimationFrame(tick);
		};
		springRAF = requestAnimationFrame(tick);
	}

	async function ensurePhotos(cafes: NearbyPlace[]): Promise<NearbyPlace[]> {
		// Pick cafes that already have photos first
		const withPhotos = cafes.filter((c) => c.photoRef);
		if (withPhotos.length >= PHOTO_CARD_LIMIT) return withPhotos.slice(0, PHOTO_CARD_LIMIT);

		// Need more — fetch photos for cafes without them
		const needPhotos = cafes.filter((c) => !c.photoRef && c.id && !photoFetchQueue.has(c.id));
		const needed = PHOTO_CARD_LIMIT - withPhotos.length;
		const toFetch = needPhotos.slice(0, needed);

		const tz = new Date().getTimezoneOffset();
		const fetched: NearbyPlace[] = [];

		await Promise.all(
			toFetch.map(async (cafe) => {
				if (!cafe.id) return;
				photoFetchQueue.add(cafe.id);
				try {
					const res = await fetch(`/api/places/refresh?id=${cafe.id}&tz=${tz}`);
					if (!res.ok) return;
					const data = await res.json();
					if (data.place?.photoRef) {
						// Update in cafeIndex
						const fresh = data.place as NearbyPlace;
						if (cafe.mapboxId) cafeIndex.set(cafe.mapboxId, fresh);
						fetched.push(fresh);
					}
				} catch {
					// skip
				}
			})
		);

		return [...withPhotos, ...fetched].slice(0, PHOTO_CARD_LIMIT);
	}

	function getVisibleCafes(): NearbyPlace[] {
		if (!map) return [];
		const bounds = map.getBounds();
		const cafesToShow = openNowFilter ? nearbyCafes.filter((c) => c.isOpen === true) : nearbyCafes;
		return cafesToShow.filter((c) => bounds.contains([c.latitude, c.longitude]));
	}

	/** Find the best direction and distance of free space around a point, considering all obstacles */
	function findFreeSpace(px: number, py: number, obstacles: { x: number; y: number }[], containerW: number, containerH: number) {
		const cardDiag = Math.hypot(CARD_W, CARD_H);
		const minRequired = cardDiag * 0.8; // minimum free space to show a card
		const probeCount = 12; // check 12 directions (every 30°)
		const probeMax = cardDiag * 1.5;

		let bestAngle = 0;
		let bestDist = 0;

		for (let i = 0; i < probeCount; i++) {
			const angle = (i * 2 * Math.PI) / probeCount;
			// How far can we go in this direction before hitting an obstacle or edge?
			let maxDist = probeMax;

			// Check container edges
			const cos = Math.cos(angle);
			const sin = Math.sin(angle);
			if (cos > 0) maxDist = Math.min(maxDist, (containerW - CARD_W / 2 - px) / cos);
			else if (cos < 0) maxDist = Math.min(maxDist, (CARD_W / 2 - px) / cos);
			if (sin > 0) maxDist = Math.min(maxDist, (containerH - CARD_H / 2 - py) / sin);
			else if (sin < 0) maxDist = Math.min(maxDist, (CARD_H / 2 - py) / sin);
			maxDist = Math.max(0, maxDist);

			// Check distance to nearest obstacle in this direction
			for (const obs of obstacles) {
				const dx = obs.x - px;
				const dy = obs.y - py;
				// Project obstacle onto this direction
				const proj = dx * cos + dy * sin;
				if (proj <= 0) continue; // behind us
				// Perpendicular distance
				const perp = Math.abs(dx * sin - dy * cos);
				if (perp < 30) { // obstacle is roughly in this direction
					maxDist = Math.min(maxDist, proj);
				}
			}

			if (maxDist > bestDist) {
				bestDist = maxDist;
				bestAngle = angle;
			}
		}

		return { angle: bestAngle, dist: bestDist, enough: bestDist >= minRequired };
	}

	function updatePhotoCards() {
		if (!map) return;
		const currentMap = map;
		const containerRect = mapContainer.getBoundingClientRect();
		const cw = containerRect.width;
		const ch = containerRect.height;

		const visible = getVisibleCafes();

		// Get screen positions of ALL visible cafe markers
		const allMarkerPoints = visible.map((c) => {
			const pt = currentMap.latLngToContainerPoint([c.latitude, c.longitude]);
			return { x: pt.x, y: pt.y };
		});

		// Score each cafe with a photo by how much free space it has
		const candidates = visible.filter((c) => c.photoRef).map((cafe) => {
			const pt = currentMap.latLngToContainerPoint([cafe.latitude, cafe.longitude]);
			// Obstacles = all OTHER markers (exclude self)
			const obstacles = allMarkerPoints.filter((mp) =>
				Math.abs(mp.x - pt.x) > 1 || Math.abs(mp.y - pt.y) > 1
			);
			const space = findFreeSpace(pt.x, pt.y, obstacles, cw, ch);
			return { cafe, pt, space };
		});

		// Only keep ones with enough space, sorted by most space first
		const viable = candidates
			.filter((c) => c.space.enough)
			.sort((a, b) => b.space.dist - a.space.dist)
			.slice(0, PHOTO_CARD_LIMIT);

		if (viable.length === 0) {
			photoCards = [];
			return;
		}

		// Place each card in its best free-space direction
		const placedCards: { x: number; y: number }[] = [];
		const nodes: PhotoCard[] = viable.map((v) => {
			const offsetDist = Math.min(v.space.dist * 0.6, CARD_H + 50);
			let bestAngle = v.space.angle;

			// Also avoid already-placed cards
			if (placedCards.length > 0) {
				const obstacles = [...allMarkerPoints, ...placedCards];
				const refined = findFreeSpace(v.pt.x, v.pt.y, obstacles, cw, ch);
				if (refined.enough) bestAngle = refined.angle;
			}

			const x = v.pt.x + Math.cos(bestAngle) * offsetDist - CARD_W / 2;
			const y = v.pt.y + Math.sin(bestAngle) * offsetDist - CARD_H / 2;
			placedCards.push({ x: x + CARD_W / 2, y: y + CARD_H / 2 });

			return {
				cafe: v.cafe,
				anchorX: v.pt.x,
				anchorY: v.pt.y,
				x,
				y
			};
		});

		// Custom force to keep cards away from ALL marker icons (rect-to-point)
		const avoidPadX = CARD_W / 2 + 18;
		const avoidPadY = CARD_H / 2 + 18;
		function forceAvoidAnchors(strength: number) {
			return function(alpha: number) {
				for (const node of nodes) {
					for (const mp of allMarkerPoints) {
						const dx = mp.x - ((node.x ?? 0) + CARD_W / 2);
						const dy = mp.y - ((node.y ?? 0) + CARD_H / 2);
						const overlapX = avoidPadX - Math.abs(dx);
						const overlapY = avoidPadY - Math.abs(dy);
						if (overlapX > 0 && overlapY > 0) {
							const dist = Math.hypot(dx, dy) || 1;
							const push = Math.min(overlapX, overlapY) * strength * alpha;
							node.x! -= (dx / dist) * push;
							node.y! -= (dy / dist) * push;
						}
					}
				}
			};
		}

		// d3-force to prevent overlap — no directional bias so cards settle 360° around markers
		const sim = forceSimulation(nodes)
			.force('x', forceX<PhotoCard>((d) => d.anchorX).strength(0.1))
			.force('y', forceY<PhotoCard>((d) => d.anchorY).strength(0.1))
			.force('collide', forceCollide<PhotoCard>(Math.max(CARD_W, CARD_H) / 2 + 12))
			.force('avoidAnchors', forceAvoidAnchors(1.5))
			.stop();

		// Run simulation synchronously
		for (let i = 0; i < 200; i++) sim.tick();

		// Clamp to container bounds
		for (const node of nodes) {
			node.x = Math.max(4, Math.min(containerRect.width - CARD_W - 4, node.x!));
			node.y = Math.max(4, Math.min(containerRect.height - CARD_H - 4, node.y!));
		}

		photoCards = nodes;
		startSpringLoop();
	}

	async function loadAndShowPhotoCards() {
		if (!map) return;
		const visible = getVisibleCafes();
		// Sort by distance from center of map
		const center = map.getCenter();
		const sorted = [...visible].sort((a, b) => {
			const da = Math.hypot(a.latitude - center.lat, a.longitude - center.lng);
			const db = Math.hypot(b.latitude - center.lat, b.longitude - center.lng);
			return da - db;
		});

		await ensurePhotos(sorted.slice(0, 20)); // try fetching photos for visible cafes
		// Re-read nearbyCafes since ensurePhotos may have updated cafeIndex
		nearbyCafes = Array.from(cafeIndex.values());
		updatePhotoCards();
	}

	function mergeCafes(newCafes: NearbyPlace[]) {
		for (const cafe of newCafes) {
			cafeIndex.set(cafe.mapboxId, cafe);
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

		let parkingLine = '';
		if (cafe.parking) {
			parkingLine = `<div style="font-size: 0.75rem; color: #6b7280; margin-bottom: 4px; display: flex; align-items: start; gap: 4px;">
				<span style="flex-shrink: 0;">🅿️</span>
				<span>${cafe.parking}</span>
			</div>`;
		}
		const scanSection = cafe.id ? `
			<div style="margin-top: 6px; border-top: 1px solid #f3f4f6; padding-top: 6px;">
				<div style="display: flex; gap: 4px; align-items: center;">
					<input id="scan-kw-${cafe.id}" type="text" value="parking" placeholder="keyword" style="flex: 1; font-size: 0.7rem; padding: 2px 6px; border: 1px solid #e5e7eb; border-radius: 4px; outline: none; min-width: 0;" />
					<button onclick="window.__scanParking(${cafe.id}, this, ${cafe.parking ? 'true' : 'false'}, document.getElementById('scan-kw-${cafe.id}').value)" style="font-size: 0.7rem; color: #6b7280; background: none; border: 1px solid #e5e7eb; border-radius: 4px; padding: 2px 6px; cursor: pointer; white-space: nowrap;">Scan</button>
				</div>
			</div>` : '';

		return `
			<div style="min-width: 200px; max-width: 260px;">
				${photoLine}
				<div style="font-weight: 600; margin-bottom: 2px;">${cafe.name}</div>
				<div style="font-size: 0.8rem; color: #666; margin-bottom: 4px;">${cafe.address}</div>
				${hoursLine}
				${parkingLine}
				${contactLine}
				${link}
				${scanSection}
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

		// Update photo cards (sync repositioning for ones with photos already)
		updatePhotoCards();
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
		photoCards = []; // clear old cards while loading
		photoFetchQueue.clear();
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
				await loadAndShowPhotoCards();
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
				// Fetch photos for display cards after markers are placed
				loadAndShowPhotoCards();
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

	function getHoursLeft(closesAt: string | null): string | null {
		if (!closesAt) return null;
		// Parse "5 PM", "2 AM", "11:30 PM" etc.
		const match = closesAt.match(/^(\d+)(?::(\d+))?\s*(AM|PM)$/i);
		if (!match) return null;
		let h = parseInt(match[1]);
		const m = match[2] ? parseInt(match[2]) : 0;
		const ampm = match[3].toUpperCase();
		if (ampm === 'PM' && h < 12) h += 12;
		if (ampm === 'AM' && h === 12) h = 0;

		const now = new Date();
		const closeMinutes = h * 60 + m;
		const nowMinutes = now.getHours() * 60 + now.getMinutes();

		let diff = closeMinutes - nowMinutes;
		if (diff <= 0) diff += 24 * 60; // closes after midnight

		const hours = Math.floor(diff / 60);
		const mins = diff % 60;
		if (hours === 0) return `${mins}m`;
		if (mins === 0) return `${hours}h`;
		return `${hours}h`;
	}

	function startDrag(card: PhotoCard, clientX: number, clientY: number) {
		const rect = mapContainer.getBoundingClientRect();
		draggedCard = card;
		dragOffsetX = clientX - rect.left - (card.x ?? 0);
		dragOffsetY = clientY - rect.top - (card.y ?? 0);
		dragStartX = clientX;
		dragStartY = clientY;
		didDrag = false;
	}

	function onDragMove(clientX: number, clientY: number) {
		if (!draggedCard) return;
		if (!didDrag && Math.hypot(clientX - dragStartX, clientY - dragStartY) > 5) {
			didDrag = true;
			if (map) map.dragging.disable();
		}
		if (!didDrag) return;
		const rect = mapContainer.getBoundingClientRect();
		draggedCard.x = Math.max(4, Math.min(rect.width - CARD_W - 4, clientX - rect.left - dragOffsetX));
		draggedCard.y = Math.max(4, Math.min(rect.height - CARD_H - 4, clientY - rect.top - dragOffsetY));
		photoCards = [...photoCards];
	}

	function endDrag() {
		const wasDrag = didDrag;
		const card = draggedCard;
		draggedCard = null;
		didDrag = false;
		if (map) map.dragging.enable();

		// If it was a click (not a drag), open the popup
		if (!wasDrag && card && map) {
			const marker = placeMarkers.find((m) => {
				const ll = m.getLatLng();
				return Math.abs(ll.lat - card.cafe.latitude) < 0.0001 && Math.abs(ll.lng - card.cafe.longitude) < 0.0001;
			});
			if (marker) marker.openPopup();
		}
	}

	function toggleOpenNow() {
		openNowFilter = !openNowFilter;
		updatePlaceMarkers();
		loadAndShowPhotoCards();
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
		// Global handler for parking scan button in popups
		(window as any).__scanParking = async (placeId: number, btn: HTMLButtonElement, rescan: boolean, keyword?: string) => {
			btn.textContent = 'Scanning...';
			btn.disabled = true;
			try {
				const res = await fetch('/api/places/parking', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ id: placeId, rescan: true, keyword: keyword || 'parking' })
				});
				if (res.ok) {
					const data = await res.json();
					// Update the cafe in our index
					for (const [key, cafe] of cafeIndex) {
						if (cafe.id === placeId) {
							cafe.parking = data.parking;
							cafeIndex.set(key, cafe);
							break;
						}
					}
					nearbyCafes = Array.from(cafeIndex.values());

					// Update the popup content
					const marker = placeMarkers.find((m) => {
						const ll = m.getLatLng();
						const cafe = Array.from(cafeIndex.values()).find(c => c.id === placeId);
						return cafe && Math.abs(ll.lat - cafe.latitude) < 0.0001 && Math.abs(ll.lng - cafe.longitude) < 0.0001;
					});
					if (marker) {
						const cafe = Array.from(cafeIndex.values()).find(c => c.id === placeId);
						if (cafe) marker.setPopupContent(buildPlacePopup(cafe));
					}
				} else {
					btn.textContent = 'Scan failed';
				}
			} catch {
				btn.textContent = 'Scan failed';
			}
		};

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
			loadAndShowPhotoCards();
		});

		// Drag move/end listeners (window-level so drag works outside the card)
		const onMouseMove = (e: MouseEvent) => {
			if (draggedCard) onDragMove(e.clientX, e.clientY);
		};
		const onMouseUp = () => { if (draggedCard) endDrag(); };
		const onTouchMove = (e: TouchEvent) => {
			const t = e.touches[0];
			if (draggedCard && t) onDragMove(t.clientX, t.clientY);
		};
		const onTouchEnd = () => { if (draggedCard) endDrag(); };
		window.addEventListener('mousemove', onMouseMove);
		window.addEventListener('mouseup', onMouseUp);
		window.addEventListener('touchmove', onTouchMove, { passive: true });
		window.addEventListener('touchend', onTouchEnd);

		const handleResize = () => map?.invalidateSize();
		window.addEventListener('resize', handleResize);

		const resizeObserver = new ResizeObserver(() => {
			setTimeout(() => map?.invalidateSize(), 100);
		});
		resizeObserver.observe(mapContainer);

		return () => {
			mediaQuery.removeEventListener('change', handleChange);
			window.removeEventListener('mousemove', onMouseMove);
			window.removeEventListener('mouseup', onMouseUp);
			window.removeEventListener('touchmove', onTouchMove);
			window.removeEventListener('touchend', onTouchEnd);
			window.removeEventListener('resize', handleResize);
			resizeObserver.disconnect();
			if (springRAF) cancelAnimationFrame(springRAF);
			map?.remove();
		};
	});
</script>

<div style="position: relative; width: 100%; height: 100%;">
	<div bind:this={mapContainer} class="map-container"></div>

	<!-- Photo cards overlay -->
	<div bind:this={photoOverlay} class="photo-overlay">
		<!-- Leader lines — rendered inside overlay so they're visible, but behind cards via DOM order -->
		<svg class="photo-lines">
			{#each photoCards as card}
				<line
					x1={card.anchorX}
					y1={card.anchorY - 15}
					x2={(card.x ?? 0) + CARD_W / 2}
					y2={(card.y ?? 0) + CARD_H / 2}
					stroke="rgba(59,130,246,0.45)"
					stroke-width="1.5"
				/>
			{/each}
		</svg>
		{#each photoCards as card (card.cafe.id)}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div
				class="photo-card {draggedCard === card ? 'dragging' : ''}"
				style="left: {card.x}px; top: {card.y}px; width: {CARD_W}px; height: {CARD_H}px;"
				onwheel={(e) => {
					e.preventDefault();
					mapContainer.dispatchEvent(new WheelEvent('wheel', e));
				}}
				onmousedown={(e) => {
					e.preventDefault();
					startDrag(card, e.clientX, e.clientY);
				}}
				ontouchstart={(e) => {
					const t = e.touches[0];
					if (t) startDrag(card, t.clientX, t.clientY);
				}}
			>
				<div class="photo-card-inner">
					<img
						src="/api/places/photo?ref={encodeURIComponent(card.cafe.photoRef || '')}"
						alt={card.cafe.name}
						class="photo-card-img"
					/>
					<div class="photo-card-label">
						<span class="photo-card-name">{card.cafe.name}</span>
					</div>
				</div>
				<div class="photo-card-stats">
					{#if card.cafe.isOpen === true}
						{@const hoursLeft = getHoursLeft(card.cafe.closesAt)}
						<span class="stat open" title={card.cafe.closesAt ? `Closes ${card.cafe.closesAt}` : 'Open'}>
							{#if hoursLeft}{hoursLeft}{:else}24h{/if}
						</span>
					{:else if card.cafe.isOpen === false}
						<span class="stat closed">Closed</span>
					{:else}
						<span class="stat unknown">--</span>
					{/if}
					<span class="stat-sep"></span>
					<span class="stat popularity" title="Popularity (coming soon)">
						--
					</span>
				</div>
			</div>
		{/each}
	</div>

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

	.photo-overlay {
		position: absolute;
		inset: 0;
		z-index: 800;
		pointer-events: none;
		overflow: hidden;
	}

	.photo-lines {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
	}

	.photo-card {
		position: absolute;
		pointer-events: auto;
		border-radius: 8px;
		overflow: hidden;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
		border: 2px solid rgba(59, 130, 246, 0.6);
		cursor: pointer;
		transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
		padding: 0;
		background: white;
		display: flex;
		flex-direction: column;
	}

	.photo-card:hover {
		transform: scale(1.05);
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
		border-color: #3b82f6;
		z-index: 10;
		cursor: grab;
	}

	.photo-card.dragging {
		cursor: grabbing;
		transform: scale(1.08);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
		z-index: 20;
		opacity: 0.9;
	}

	.photo-card-inner {
		position: relative;
		flex: 1;
		min-height: 0;
		overflow: hidden;
	}

	.photo-card-img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.photo-card-label {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		padding: 3px 5px;
		background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
		display: flex;
		align-items: baseline;
		gap: 3px;
	}

	.photo-card-name {
		font-size: 0.6rem;
		font-weight: 600;
		color: white;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		flex: 1;
		line-height: 1.2;
	}

	.photo-card-stats {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;
		padding: 2px 4px;
		background: rgba(255, 255, 255, 0.95);
		flex-shrink: 0;
	}

	.stat {
		font-size: 0.55rem;
		font-weight: 700;
		letter-spacing: 0.02em;
	}

	.stat.open {
		color: #059669;
	}

	.stat.closed {
		color: #dc2626;
	}

	.stat.unknown, .stat.popularity {
		color: #9ca3af;
	}

	.stat-sep {
		width: 1px;
		height: 8px;
		background: #e5e7eb;
	}

	@media (max-width: 479px) {
		.photo-card-label {
			padding: 2px 3px;
			gap: 2px;
		}

		.photo-card-name {
			font-size: 0.5rem;
		}

		.stat {
			font-size: 0.5rem;
		}
	}

	@media (prefers-color-scheme: dark) {
		.photo-card {
			border-color: #374151;
			background: #1f2937;
		}

		.photo-card-stats {
			background: rgba(31, 41, 55, 0.95);
		}

		.stat-sep {
			background: #374151;
		}
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
