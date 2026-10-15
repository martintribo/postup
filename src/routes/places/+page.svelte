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

<div class="min-h-screen bg-surface text-ink">
	<header class="border-b border-line px-4 py-3" style="display: flex; align-items: center; gap: 1rem;">
		<a href="/" class="text-muted hover:text-ink transition-colors">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
		</a>
		<h1 class="text-xl font-semibold">Places</h1>
	</header>

	<div class="flex flex-col md:flex-row" style="min-height: calc(100vh - 57px);">
		<!-- Filters sidebar -->
		<aside class="w-full md:w-64 md:shrink-0 border-b md:border-b-0 md:border-r border-line p-4 bg-bg">
			<div class="space-y-5">
				<!-- Search -->
				<div>
					<label for="search" class="block text-sm font-medium text-ink mb-1.5">Search</label>
					<input
						id="search"
						type="text"
						bind:value={searchQuery}
						placeholder="Find a place..."
						class="w-full px-3 py-1.5 text-sm border border-line rounded-md bg-surface text-ink focus:ring-2 focus:ring-brand focus:border-brand"
					/>
				</div>

				<!-- Sort -->
				<div>
					<p class="text-sm font-medium text-ink mb-1.5">Sort by</p>
					<div class="space-y-1">
						{#each [['distance', 'Nearest'], ['rating', 'Highest rated'], ['reviews', 'Most reviewed']] as [value, label]}
							<button
								type="button"
								onclick={() => sortBy = value as typeof sortBy}
								class="block w-full text-left px-3 py-1.5 text-sm rounded-md transition-colors {sortBy === value ? 'bg-brand-soft text-brand font-medium' : 'text-muted hover:bg-surface-2 '}"
							>
								{label}
							</button>
						{/each}
					</div>
				</div>

				<!-- Category filter -->
				<div>
					<div style="display: flex; align-items: center; justify-content: space-between;">
						<p class="text-sm font-medium text-ink mb-1.5">Category</p>
						{#if filterCategory}
							<button type="button" onclick={() => filterCategory = null} class="text-xs text-brand hover:underline mb-1.5">Clear</button>
						{/if}
					</div>
					<div style="display: flex; flex-wrap: wrap; gap: 0.375rem;">
						{#each categories as cat}
							<button
								type="button"
								onclick={() => filterCategory = filterCategory === cat ? null : cat}
								class="px-2.5 py-1 text-xs rounded-full border transition-colors {filterCategory === cat ? 'bg-brand-soft border-brand text-brand ' : 'border-line text-muted hover:border-line'}"
							>
								{cat}
							</button>
						{/each}
					</div>
				</div>

				<!-- Placeholder: future filters -->
				<div class="pt-4 border-t border-line">
					<p class="text-xs text-subtle italic">More filters coming: wifi quality, noise level, outlets</p>
				</div>
			</div>
		</aside>

		<!-- Main content -->
		<main class="flex-1 p-6">
			{#if filteredPlaces.length === 0}
				<div class="text-center py-16">
					<div class="w-16 h-16 mx-auto mb-4 rounded-full bg-surface-2 flex items-center justify-center">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-subtle" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
							<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
						</svg>
					</div>
					<h3 class="text-lg font-medium text-ink mb-1">Find your spot</h3>
					<p class="text-sm text-muted">Search for a cafe, or post up somewhere and add it here.</p>
				</div>
			{:else}
				<div class="grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));">
					{#each filteredPlaces as p (p.id)}
						<a
							href="/places/{p.id}"
							class="block p-4 border border-line rounded-lg bg-surface hover:border-brand hover:shadow-md transition-all"
						>
							<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem;">
								<div class="min-w-0 flex-1">
									<h3 class="font-semibold text-ink truncate">{p.name}</h3>
									<p class="text-sm text-muted mt-0.5 truncate">{p.address}</p>
								</div>
								{#if p.category}
									<span class="px-2 py-0.5 text-xs rounded-full bg-surface-2 text-muted flex-shrink-0">
										{p.category}
									</span>
								{/if}
							</div>

							<div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.75rem;" class="text-sm">
								{#if p.reviewCount > 0}
									<span class="text-ink" title="{p.avgRating.toFixed(1)} stars">{renderStars(p.avgRating)}</span>
									<span class="text-muted">{p.reviewCount} {p.reviewCount === 1 ? 'review' : 'reviews'}</span>
								{:else}
									<span class="text-subtle italic">Leave a review</span>
								{/if}
							</div>

							<div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;" class="text-xs text-muted">
								<span>{p.distance.toFixed(1)} mi away</span>
								{#if p.avgWifi > 0}
									<span>WiFi: {p.avgWifi.toFixed(1)}/5</span>
								{/if}
							</div>

							{#if p.tags.length > 0}
								<div style="display: flex; flex-wrap: wrap; gap: 0.25rem; margin-top: 0.5rem;">
									{#each p.tags.slice(0, 4) as tag}
										<span class="px-1.5 py-0.5 text-xs bg-surface-2 text-muted rounded">
											{tag}
										</span>
									{/each}
									{#if p.tags.length > 4}
										<span class="text-xs text-subtle">+{p.tags.length - 4}</span>
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
