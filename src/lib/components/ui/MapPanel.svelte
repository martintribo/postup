<script lang="ts">
	/** Desktop map screens (mockup #postup, #live, #joined, #cafe…): the map fills the page and the
	 *  phone screen sits in a 440px panel on the right. On phone it is just the screen.
	 *  Map (leaflet) needs window, so it loads in the browser only, and only on desktop. */
	import { onMount, type Snippet, type Component } from 'svelte';
	let { latitude = null, longitude = null, children, cls = '', showPlaces = true }: { latitude?: number | null; longitude?: number | null; children: Snippet; cls?: string; showPlaces?: boolean } = $props();
	let desk = $state(false);
	let MapC = $state<Component<{ latitude: number; longitude: number; chrome?: boolean; showPlaces?: boolean }> | null>(null);
	onMount(() => {
		const mq = matchMedia('(min-width: 1024px)');
		const set = async () => {
			desk = mq.matches;
			if (desk && !MapC) MapC = (await import('$lib/components/Map.svelte')).default as never;
		};
		set();
		mq.addEventListener('change', set);
		return () => mq.removeEventListener('change', set);
	});
</script>

<div class="mapscr {cls}">
	{#if desk && MapC && latitude != null && longitude != null}
		<div class="mapscr-map"><MapC {latitude} {longitude} {showPlaces} chrome={false} /></div>
	{/if}
	<div class="mpanel">{@render children()}</div>
</div>
