<script lang="ts">
	import { enhance } from '$app/forms';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const categories = ['cafe', 'library', 'park', 'coworking', 'restaurant', 'bar', 'other'];
	let selectedCategory = $state(data.prefill.latitude ? 'cafe' : '');
</script>

<div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
	<header class="border-b border-gray-200 dark:border-gray-700 px-4 py-3" style="display: flex; align-items: center; gap: 1rem;">
		<a href="/" class="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
		</a>
		<h1 class="text-xl font-semibold">Add a Place</h1>
	</header>

	<div class="max-w-lg mx-auto px-4 py-8">
		<form method="POST" use:enhance class="space-y-4">
			<input type="hidden" name="mapboxId" value={data.prefill.mapboxId} />
			<input type="hidden" name="latitude" value={data.prefill.latitude} />
			<input type="hidden" name="longitude" value={data.prefill.longitude} />

			<div>
				<label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
				<input
					id="name"
					type="text"
					name="name"
					value={data.prefill.name}
					required
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label for="address" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Address</label>
				<input
					id="address"
					type="text"
					name="address"
					value={data.prefill.address}
					required
					class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<div>
				<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category</label>
				<div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
					{#each categories as cat}
						<button
							type="button"
							onclick={() => selectedCategory = cat}
							class="px-3 py-1.5 text-sm rounded-md border transition-colors {selectedCategory === cat ? 'bg-blue-100 dark:bg-blue-900/50 border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300' : 'border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-gray-400'}"
						>
							{cat}
						</button>
					{/each}
				</div>
				<input type="hidden" name="category" value={selectedCategory} />
			</div>

			{#if data.prefill.latitude && data.prefill.longitude}
				<p class="text-xs text-gray-500 dark:text-gray-400">
					Location: {data.prefill.latitude.toFixed(4)}, {data.prefill.longitude.toFixed(4)}
				</p>
			{/if}

			<button
				type="submit"
				class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
			>
				Add place
			</button>
		</form>
	</div>
</div>
