<script lang="ts">
	import { env } from '$env/dynamic/public';

	interface LocationSuggestion {
		id?: string;
		type?: string;
		text?: string;
		place_name?: string;
		properties?: {
			full_address?: string;
			coordinates?: {
				latitude: number;
				longitude: number;
				accuracy?: string;
			};
			[key: string]: unknown;
		};
		geometry?: {
			type: string;
			coordinates: [number, number]; // [longitude, latitude]
		};
		center?: [number, number]; // [longitude, latitude] - fallback for v5 compatibility
	}

	interface Props {
		name: string;
		value: string;
		onSelect: (location: { name: string; latitude: number; longitude: number }) => void;
	}

	let { name, value = $bindable(''), onSelect }: Props = $props();

	let inputElement: HTMLInputElement;
	let suggestions = $state<LocationSuggestion[]>([]);
	let showSuggestions = $state(false);
	let selectedIndex = $state(-1);
	let debounceTimer: ReturnType<typeof setTimeout> | null = null;

	async function searchLocations(query: string) {
		if (query.length < 3) {
			suggestions = [];
			showSuggestions = false;
			return;
		}

		const accessToken = env.PUBLIC_MAPBOX_ACCESS_TOKEN;
		if (!accessToken) {
			console.error('Mapbox access token is not configured');
			return;
		}

		try {
			// Using Mapbox Geocoding API v6
			const params = new URLSearchParams({
				q: query,
				access_token: accessToken,
				limit: '5'
			});
			const response = await fetch(
				`https://api.mapbox.com/search/geocode/v6/forward?${params.toString()}`
			);
			
			if (!response.ok) {
				throw new Error(`Mapbox API error: ${response.status}`);
			}
			
			const data = await response.json();
			console.log('Mapbox API response:', data);
			
			// Handle both FeatureCollection and direct features array
			const features = data.features || data || [];
			console.log('Parsed features:', features);
			
			suggestions = features;
			showSuggestions = true;
			selectedIndex = -1;
		} catch (error) {
			console.error('Error searching locations:', error);
			suggestions = [];
			showSuggestions = false;
		}
	}

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		value = target.value;

		if (debounceTimer) {
			clearTimeout(debounceTimer);
		}

		debounceTimer = setTimeout(() => {
			searchLocations(value);
		}, 300);
	}

	function selectSuggestion(suggestion: LocationSuggestion) {
		const placeName = suggestion.properties?.full_address || suggestion.place_name || suggestion.text || '';
		value = placeName;
		showSuggestions = false;
		
		// Mapbox v6 has coordinates in properties.coordinates
		const coords = suggestion.properties?.coordinates;
		if (coords && typeof coords.latitude === 'number' && typeof coords.longitude === 'number') {
			onSelect({
				name: placeName,
				latitude: coords.latitude,
				longitude: coords.longitude
			});
		} else if (suggestion.geometry?.coordinates) {
			// Fallback to geometry.coordinates [longitude, latitude]
			const [longitude, latitude] = suggestion.geometry.coordinates;
			onSelect({
				name: placeName,
				latitude,
				longitude
			});
		} else if (suggestion.center) {
			// Fallback to center [longitude, latitude]
			const [longitude, latitude] = suggestion.center;
			onSelect({
				name: placeName,
				latitude,
				longitude
			});
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!showSuggestions || suggestions.length === 0) return;

		if (e.key === 'ArrowDown') {
			e.preventDefault();
			selectedIndex = Math.min(selectedIndex + 1, suggestions.length - 1);
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			selectedIndex = Math.max(selectedIndex - 1, -1);
		} else if (e.key === 'Enter' && selectedIndex >= 0) {
			e.preventDefault();
			selectSuggestion(suggestions[selectedIndex]);
		} else if (e.key === 'Escape') {
			showSuggestions = false;
			selectedIndex = -1;
		}
	}

	function handleBlur() {
		// Delay to allow click events on suggestions to fire
		setTimeout(() => {
			showSuggestions = false;
		}, 200);
	}
</script>

<div class="relative">
	<input
		name={name}
		bind:this={inputElement}
		type="text"
		bind:value
		oninput={handleInput}
		onkeydown={handleKeydown}
		onblur={handleBlur}
		placeholder="Search for a location..."
		class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
		autocomplete="off"
	/>
	{#if showSuggestions && suggestions.length > 0}
		<ul
			class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg max-h-60 overflow-auto"
		>
			{#each suggestions as suggestion, index (suggestion.id || index.toString())}
				<li>
					<button
						type="button"
						onclick={() => selectSuggestion(suggestion)}
						class="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none {selectedIndex === index
							? 'bg-gray-100 dark:bg-gray-700'
							: ''}"
					>
						<div class="text-sm text-gray-900 dark:text-gray-100">
							{suggestion.properties?.full_address || suggestion.place_name || suggestion.text || 'Unknown location'}
						</div>
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>

