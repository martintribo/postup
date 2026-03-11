<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let sortBy = $state<'distance' | 'rating' | 'reviews'>('distance');
	let filterCategory = $state<string | null>(null);
	let filterNoise = $state<string | null>(null);
	let searchQuery = $state('');

	const categories = ['cafe', 'library', 'park', 'coworking', 'restaurant', 'bar', 'other'];
	const noiseLevels = ['quiet', 'moderate', 'noisy'];

	const filteredPlaces = $derived.by(() => {
		let result = [...data.places];

		if (searchQuery) {
			const q = searchQuery.toLowerCase();
			result = result.filter((p) => p.name.toLowerCase().includes(q) || p.address.toLowerCase().includes(q));
		}
		if (filterCategory) {
			result = result.filter((p) => p.category === filterCategory);
		}

		if (sortBy === 'rating') {
			result.sort((a, b) => b.avgRating - a.avgRating);
		} else if (sortBy === 'reviews') {
			result.sort((a, b) => b.reviewCount - a.reviewCount);
		}
		// default is distance, already sorted by server

		return result;
	});

	function renderStars(rating: number): string {
		const full = Math.round(rating);
		return '\u2605'.repeat(full) + '\u2606'.repeat(5 - full);
	}
</script>

<div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
	<header class="border-b border-gray-200 dark:border-gray-700 px-4 py-3" style="display: flex; align-items: center; gap: 1rem;">
		<a href="/" class="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
		</a>
		<h1 class="text-xl font-semibold">Places</h1>
	</header>

	<div style="display: flex; flex-direction: row; min-height: calc(100vh - 57px);">
		<!-- Filters sidebar -->
		<aside class="border-r border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800/50" style="width: 16rem; flex-shrink: 0;">
			<div class="space-y-5">
				<!-- Search -->
				<div>
					<label for="search" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Search</label>
					<input
						id="search"
						type="text"
						bind:value={searchQuery}
						placeholder="Find a place..."
						class="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
					/>
				</div>

				<!-- Sort -->
				<div>
					<p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Sort by</p>
					<div class="space-y-1">
						{#each [['distance', 'Nearest'], ['rating', 'Highest rated'], ['reviews', 'Most reviewed']] as [value, label]}
							<button
								type="button"
								onclick={() => sortBy = value as typeof sortBy}
								class="block w-full text-left px-3 py-1.5 text-sm rounded-md transition-colors {sortBy === value ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 font-medium' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'}"
							>
								{label}
							</button>
						{/each}
					</div>
				</div>

				<!-- Category filter -->
				<div>
					<div style="display: flex; align-items: center; justify-content: space-between;">
						<p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Category</p>
						{#if filterCategory}
							<button type="button" onclick={() => filterCategory = null} class="text-xs text-blue-600 dark:text-blue-400 hover:underline mb-1.5">Clear</button>
						{/if}
					</div>
					<div style="display: flex; flex-wrap: wrap; gap: 0.375rem;">
						{#each categories as cat}
							<button
								type="button"
								onclick={() => filterCategory = filterCategory === cat ? null : cat}
								class="px-2.5 py-1 text-xs rounded-full border transition-colors {filterCategory === cat ? 'bg-blue-100 dark:bg-blue-900/50 border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300' : 'border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-gray-400'}"
							>
								{cat}
							</button>
						{/each}
					</div>
				</div>

				<!-- Placeholder: future filters -->
				<div class="pt-4 border-t border-gray-200 dark:border-gray-700">
					<p class="text-xs text-gray-400 dark:text-gray-500 italic">More filters coming: wifi quality, noise level, outlets</p>
				</div>
			</div>
		</aside>

		<!-- Main content -->
		<main class="flex-1 p-6">
			{#if filteredPlaces.length === 0}
				<div class="text-center py-16">
					<div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
							<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
						</svg>
					</div>
					<h3 class="text-lg font-medium text-gray-700 dark:text-gray-300 mb-1">No places yet</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">Be the first to add a place — post up somewhere and create a place profile!</p>
				</div>
			{:else}
				<div class="grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));">
					{#each filteredPlaces as p (p.id)}
						<a
							href="/places/{p.id}"
							class="block p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 hover:border-blue-300 dark:hover:border-blue-600 hover:shadow-md transition-all"
						>
							<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem;">
								<div class="min-w-0 flex-1">
									<h3 class="font-semibold text-gray-900 dark:text-gray-100 truncate">{p.name}</h3>
									<p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5 truncate">{p.address}</p>
								</div>
								{#if p.category}
									<span class="px-2 py-0.5 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 flex-shrink-0">
										{p.category}
									</span>
								{/if}
							</div>

							<div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.75rem;" class="text-sm">
								{#if p.reviewCount > 0}
									<span class="text-amber-500" title="{p.avgRating.toFixed(1)} stars">{renderStars(p.avgRating)}</span>
									<span class="text-gray-500 dark:text-gray-400">{p.reviewCount} {p.reviewCount === 1 ? 'review' : 'reviews'}</span>
								{:else}
									<span class="text-gray-400 dark:text-gray-500 italic">No reviews yet</span>
								{/if}
							</div>

							<div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;" class="text-xs text-gray-500 dark:text-gray-400">
								<span>{p.distance.toFixed(1)} mi away</span>
								{#if p.avgWifi > 0}
									<span>WiFi: {p.avgWifi.toFixed(1)}/5</span>
								{/if}
							</div>

							{#if p.tags.length > 0}
								<div style="display: flex; flex-wrap: wrap; gap: 0.25rem; margin-top: 0.5rem;">
									{#each p.tags.slice(0, 4) as tag}
										<span class="px-1.5 py-0.5 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
											{tag}
										</span>
									{/each}
									{#if p.tags.length > 4}
										<span class="text-xs text-gray-400">+{p.tags.length - 4}</span>
									{/if}
								</div>
							{/if}
						</a>
					{/each}
				</div>
			{/if}
		</main>
	</div>
</div>
