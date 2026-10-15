<script lang="ts">
	/** Google place card slot (mockup .gcard). Shows the UI Kit card; on error/timeout the mockup failure st with Open in Maps + Retry. */
	import { onMount } from 'svelte';
	import Icon from './Icon.svelte';
	import PlaceDetailsCard from '$lib/components/PlaceDetailsCard.svelte';
	import { loadGooglePlacesLibrary } from '$lib/google-maps';
	let { googlePlaceId, name, lat, lng }: { googlePlaceId: string | null; name: string; lat: number; lng: number } = $props();
	let st = $state<'loading' | 'ok' | 'fail'>('loading');
	let attempt = $state(0);
	const maps = $derived(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(name)}&query_place_id=${googlePlaceId ?? ''}&center=${lat},${lng}`);
	async function load() {
		st = 'loading';
		if (!googlePlaceId) { st = 'fail'; return; }
		const ok = await loadGooglePlacesLibrary().catch(() => false);
		if (!ok) { st = 'fail'; return; }
		st = 'ok';
		attempt++;
	}
	function watch(node: HTMLElement) {
		const el = () => node.querySelector('gmp-place-details-compact');
		const fail = () => (st = 'fail');
		const t = setTimeout(() => { const e = el() as HTMLElement | null; if (!e || !e.shadowRoot?.childElementCount) fail(); }, 9000);
		node.addEventListener('gmp-error', fail, true);
		return { destroy: () => { clearTimeout(t); node.removeEventListener('gmp-error', fail, true); } };
	}
	onMount(load);
</script>

{#if st === 'fail'}
	<div class="gcard fail" data-testid="gcard-fail">
		<div class="gph"><Icon name="image" size={22} /></div>
		<div class="lm"><b class="sm">Details unavailable</b><span class="mu xs">Couldn't load photos and hours right now.</span>
			<span class="row3"><a class="lnk xs" href={maps} target="_blank" rel="noopener"><Icon name="nav" size={13} /> Open in Maps</a><button type="button" class="lnk xs" onclick={load}><Icon name="refresh" size={13} /> Retry</button></span>
		</div>
	</div>
{:else if st === 'ok' && googlePlaceId}
	{#key attempt}<div class="gcard ok" use:watch data-testid="gcard"><PlaceDetailsCard placeId={googlePlaceId} /></div>{/key}
{:else}
	<div class="gcard"><div class="gph"><Icon name="image" size={22} /></div><div><b class="sm">Loading details…</b><div class="mu xs">Photos, rating and hours from Google</div></div></div>
{/if}
