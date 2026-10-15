<script lang="ts">
	import { goto } from '$app/navigation';
	import NearbyFeed from '$lib/components/NearbyFeed.svelte';
	let { data } = $props();
</script>

<NearbyFeed items={data.feed.items} weekCount={data.feed.weekCount} onPostUp={() => goto('/post')} onOpenMap={() => goto('/')} />
