<script lang="ts">
	/** Mockup #offline. */
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	let offline = $state(false);
	onMount(() => {
		const set = () => (offline = !navigator.onLine);
		set();
		addEventListener('online', set);
		addEventListener('offline', set);
		return () => {
			removeEventListener('online', set);
			removeEventListener('offline', set);
		};
	});
</script>

<!-- Nearby draws its own in-feed banner (mockup #offline). -->
{#if offline && page.url.pathname !== '/nearby'}
	<div class="pu-offline" role="status" data-testid="offline">You're offline. Showing what we last loaded.</div>
{/if}

<style>
	.pu-offline { position: fixed; left: 0; right: 0; top: 0; z-index: 2000; padding: 8px 12px; text-align: center; background: #333; color: #fff; font: 600 14px var(--pu-font); }
</style>
