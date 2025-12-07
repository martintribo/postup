<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="flex flex-col lg:flex-row h-screen w-screen overflow-hidden bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
	<!-- Map Container - Full width on vertical, flexible on horizontal -->
	<div class="flex-1 min-h-0 lg:min-w-0">
		{#if data.location}
			<Map
				latitude={data.location.latitude}
				longitude={data.location.longitude}
				city={data.location.city}
				country={data.location.country}
			/>
		{:else}
			<div class="h-full flex items-center justify-center">
				<p class="text-gray-500 dark:text-gray-400">Loading map...</p>
			</div>
		{/if}
	</div>

	<!-- Sidebar - Bottom half on vertical, right bar on horizontal -->
	<aside class="w-full lg:w-80 xl:w-96 h-1/2 lg:h-full border-t lg:border-t-0 lg:border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-y-auto">
		<div class="p-4">
			<h2 class="text-2xl font-semibold mb-4">List Content</h2>
			<ul class="space-y-2">
				<!-- Placeholder list items -->
				<li class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
					<div class="font-medium">Item 1</div>
					<div class="text-sm text-gray-600 dark:text-gray-400">Description for item 1</div>
				</li>
				<li class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
					<div class="font-medium">Item 2</div>
					<div class="text-sm text-gray-600 dark:text-gray-400">Description for item 2</div>
				</li>
				<li class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
					<div class="font-medium">Item 3</div>
					<div class="text-sm text-gray-600 dark:text-gray-400">Description for item 3</div>
				</li>
				<li class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
					<div class="font-medium">Item 4</div>
					<div class="text-sm text-gray-600 dark:text-gray-400">Description for item 4</div>
				</li>
				<li class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
					<div class="font-medium">Item 5</div>
					<div class="text-sm text-gray-600 dark:text-gray-400">Description for item 5</div>
				</li>
			</ul>
		</div>
	</aside>
</div>
