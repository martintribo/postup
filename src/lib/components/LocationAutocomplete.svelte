<script lang="ts">
	import { onMount } from 'svelte';

	interface LocationSuggestion {
		display_name: string;
		lat: string;
		lon: string;
	}

	interface Props {
		value: string;
		onSelect: (location: { name: string; latitude: number; longitude: number }) => void;
	}

	let { value = $bindable(''), onSelect }: Props = $props();

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

		try {
			// Using Nominatim (OpenStreetMap's geocoding service) - free, no API key required
			const response = await fetch(
				`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`,
				{
					headers: {
						'User-Agent': 'PostUp App' // Required by Nominatim
					}
				}
			);
			const data = await response.json();
			suggestions = data;
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
		value = suggestion.display_name;
		showSuggestions = false;
		onSelect({
			name: suggestion.display_name,
			latitude: parseFloat(suggestion.lat),
			longitude: parseFloat(suggestion.lon)
		});
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
			{#each suggestions as suggestion, index}
				<li>
					<button
						type="button"
						onclick={() => selectSuggestion(suggestion)}
						class="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none {selectedIndex === index
							? 'bg-gray-100 dark:bg-gray-700'
							: ''}"
					>
						<div class="text-sm text-gray-900 dark:text-gray-100">{suggestion.display_name}</div>
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>

