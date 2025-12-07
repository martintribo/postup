<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="container mx-auto px-4 py-8">
	<h1 class="text-4xl font-bold mb-4">Welcome to SvelteKit</h1>
	<p class="text-lg text-gray-600 mb-8">
		Visit <a href="https://svelte.dev/docs/kit" class="text-blue-600 hover:underline">svelte.dev/docs/kit</a> to read the documentation
	</p>

	<div class="mb-8">
		<h2 class="text-2xl font-semibold mb-4">Map View</h2>
		{#if data.location}
			<Map
				latitude={data.location.latitude}
				longitude={data.location.longitude}
				city={data.location.city}
				country={data.location.country}
			/>
		{:else}
			<p class="text-gray-500">Loading map...</p>
		{/if}
	</div>
</div>
