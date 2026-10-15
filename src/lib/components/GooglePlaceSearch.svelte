<script lang="ts">
	/**
	 * "Where are you?" Google search (Places UI Kit PlaceAutocompleteElement).
	 * ToS: suggestions render inside Google's widget; we keep only place_id (+ coords for the map).
	 * Renders nothing when no browser key is set or the library fails to load.
	 */
	import { onMount } from 'svelte';
	import { loadGooglePlacesLibrary } from '$lib/google-maps';

	let {
		near,
		onSelect
	}: {
		near?: { latitude: number; longitude: number };
		onSelect: (p: { googlePlaceId: string; name: string; latitude: number; longitude: number; address?: string }) => void;
	} = $props();

	let host: HTMLDivElement;
	let state = $state<'loading' | 'ready' | 'off' | 'error'>('loading');

	onMount(async () => {
		const ok = await loadGooglePlacesLibrary();
		if (!ok) {
			state = 'off';
			return;
		}
		try {
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			const places: any = await window.google!.maps.importLibrary('places');
			const el = new places.PlaceAutocompleteElement({
				includedPrimaryTypes: ['cafe', 'coffee_shop', 'bakery', 'library', 'restaurant'],
				...(near ? { locationBias: { center: { lat: near.latitude, lng: near.longitude }, radius: 15000 } } : {})
			});
			el.setAttribute('data-testid', 'google-place-search');
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			el.addEventListener('gmp-select', async (ev: any) => {
				const place = ev.placePrediction.toPlace();
				await place.fetchFields({ fields: ['id', 'displayName', 'location', 'formattedAddress'] });
				onSelect({
					googlePlaceId: place.id,
					name: place.displayName,
					latitude: place.location.lat(),
					longitude: place.location.lng(),
					address: place.formattedAddress
				});
			});
			host.appendChild(el);
			state = 'ready';
		} catch (e) {
			console.warn('Google place search unavailable', e);
			state = 'error';
		}
	});
</script>

<div bind:this={host} class="pu-gsearch" data-state={state}>
	{#if state === 'error'}<p class="pu-gsearch-err">Google search is unavailable right now. Pick a nearby cafe instead.</p>{/if}
</div>

<style>
	.pu-gsearch-err { font-size: 13px; color: var(--pu-muted); margin: 4px 0; }
</style>
