<script lang="ts">
	import { env } from '$env/dynamic/public';

	interface SearchSuggestion {
		name: string;
		mapbox_id: string;
		feature_type: string;
		address?: string;
		full_address?: string;
		place_formatted?: string;
		context?: {
			country?: { name: string };
			region?: { name: string };
			place?: { name: string };
		};
	}

	interface Props {
		name: string;
		value: string;
		onSelect: (location: { name: string; latitude: number; longitude: number }) => void;
		proximity?: { latitude: number; longitude: number };
	}

	let { name, value = $bindable(''), onSelect, proximity }: Props = $props();

	let suggestions = $state<SearchSuggestion[]>([]);
	let showSuggestions = $state(false);
	let selectedIndex = $state(-1);
	let debounceTimer: ReturnType<typeof setTimeout> | null = null;
	let sessionToken = $state(crypto.randomUUID());

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
			// Using Mapbox Search Box API for POI/business search
			const params = new URLSearchParams({
				q: query,
				access_token: accessToken,
				session_token: sessionToken,
				limit: '8',
				types: 'poi,address,place'
			});

			// Add proximity parameter if user location is available
			if (proximity) {
				params.append('proximity', `${proximity.longitude},${proximity.latitude}`);
			}

			const response = await fetch(
				`https://api.mapbox.com/search/searchbox/v1/suggest?${params.toString()}`
			);

			if (!response.ok) {
				throw new Error(`Mapbox API error: ${response.status}`);
			}

			const data = await response.json();
			suggestions = data.suggestions || [];
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

	async function selectSuggestion(suggestion: SearchSuggestion) {
		const displayName = suggestion.name + (suggestion.place_formatted ? `, ${suggestion.place_formatted}` : '');
		value = displayName;
		showSuggestions = false;

		const accessToken = env.PUBLIC_MAPBOX_ACCESS_TOKEN;
		if (!accessToken) {
			console.error('Mapbox access token is not configured');
			return;
		}

		try {
			// Retrieve full details including coordinates
			const params = new URLSearchParams({
				access_token: accessToken,
				session_token: sessionToken
			});

			const response = await fetch(
				`https://api.mapbox.com/search/searchbox/v1/retrieve/${suggestion.mapbox_id}?${params.toString()}`
			);

			if (!response.ok) {
				throw new Error(`Mapbox retrieve error: ${response.status}`);
			}

			const data = await response.json();
			const feature = data.features?.[0];

			if (feature?.geometry?.coordinates) {
				const [longitude, latitude] = feature.geometry.coordinates;
				onSelect({
					name: displayName,
					latitude,
					longitude
				});
			}

			// Generate new session token for next search
			sessionToken = crypto.randomUUID();
		} catch (error) {
			console.error('Error retrieving location details:', error);
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
			{#each suggestions as suggestion, index (suggestion.mapbox_id)}
				<li>
					<button
						type="button"
						onclick={() => selectSuggestion(suggestion)}
						class="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none {selectedIndex === index
							? 'bg-gray-100 dark:bg-gray-700'
							: ''}"
					>
						<div class="text-sm font-medium text-gray-900 dark:text-gray-100">
							{suggestion.name}
						</div>
						{#if suggestion.place_formatted}
							<div class="text-xs text-gray-500 dark:text-gray-400">
								{suggestion.place_formatted}
							</div>
						{/if}
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>

