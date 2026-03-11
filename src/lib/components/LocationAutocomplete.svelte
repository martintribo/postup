<script lang="ts">
	import { env } from '$env/dynamic/public';

	interface SearchFeature {
		properties: {
			name: string;
			full_address?: string;
			address?: string;
			mapbox_id?: string;
			feature_type?: string;
			[key: string]: unknown;
		};
		geometry: {
			type: string;
			coordinates: [number, number]; // [longitude, latitude]
		};
	}

	interface Props {
		name: string;
		value: string;
		onSelect: (location: { name: string; latitude: number; longitude: number }) => void;
		proximity?: { latitude: number; longitude: number };
	}

	let { name, value = $bindable(''), onSelect, proximity }: Props = $props();

	let inputElement: HTMLInputElement;
	let suggestions = $state<SearchFeature[]>([]);
	let showSuggestions = $state(false);
	let selectedIndex = $state(-1);
	let debounceTimer: ReturnType<typeof setTimeout> | null = null;

	async function searchLocations(query: string) {
		if (query.length < 2) {
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
			const params = new URLSearchParams({
				q: query,
				access_token: accessToken,
				limit: '7',
				language: 'en',
				types: 'poi,address'
			});

			if (proximity) {
				params.append('proximity', `${proximity.longitude},${proximity.latitude}`);
			}

			const response = await fetch(
				`https://api.mapbox.com/search/searchbox/v1/forward?${params.toString()}`
			);

			if (!response.ok) {
				throw new Error(`Mapbox API error: ${response.status}`);
			}

			const data = await response.json();
			suggestions = data.features || [];
			showSuggestions = suggestions.length > 0;
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

		if (debounceTimer) clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => searchLocations(value), 300);
	}

	function displayName(feature: SearchFeature): string {
		const props = feature.properties;
		if (props.name && props.full_address && !props.full_address.startsWith(props.name)) {
			return `${props.name}, ${props.full_address}`;
		}
		return props.full_address || props.name || 'Unknown location';
	}

	function selectSuggestion(feature: SearchFeature) {
		const label = displayName(feature);
		value = label;
		showSuggestions = false;

		const [longitude, latitude] = feature.geometry.coordinates;
		onSelect({ name: label, latitude, longitude });
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
		setTimeout(() => { showSuggestions = false; }, 200);
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
		placeholder="Search for a place or address..."
		class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
		autocomplete="off"
	/>
	{#if showSuggestions && suggestions.length > 0}
		<ul
			class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg max-h-60 overflow-auto"
		>
			{#each suggestions as feature, index (feature.properties.mapbox_id || index.toString())}
				<li>
					<button
						type="button"
						onclick={() => selectSuggestion(feature)}
						class="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none {selectedIndex === index ? 'bg-gray-100 dark:bg-gray-700' : ''}"
					>
						<div class="text-sm font-medium text-gray-900 dark:text-gray-100">
							{feature.properties.name}
						</div>
						{#if feature.properties.full_address}
							<div class="text-xs text-gray-500 dark:text-gray-400">
								{feature.properties.full_address}
							</div>
						{/if}
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>
