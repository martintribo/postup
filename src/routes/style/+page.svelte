<script lang="ts">
	/** M12 style pick: compare Fresh, Cozy, Night and Bold on real components. Choice is saved per browser for review; the default comes from PUBLIC_THEME. */
	import { THEMES, type Theme } from '$lib/config';
	import { saveTheme } from '$lib/theme';
	import NearbyFeed from '$lib/components/NearbyFeed.svelte';
	const sample = [
		{ kind: 'postup' as const, id: 1, at: new Date(Date.now() - 20 * 60000).toISOString(), who: 'Maya', username: null, avatarUrl: null, activity: 'Star Fox 64 mod', cafe: 'Bean Theory', placeId: null, projectName: 'Star Fox 64 mod', projectId: null, live: true, miles: 0.4, photo: null, joined: [] },
		{ kind: 'update' as const, id: 2, at: new Date(Date.now() - 26 * 3600000).toISOString(), projectId: 1, projectName: 'Tiny synth', title: 'First sound!', body: 'Got the oscillator working on the breadboard.', who: null, username: null, avatarUrl: null, photo: null }
	];
	const pick = (t: Theme) => saveTheme(t);
</script>

<div style="padding: 12px; display: flex; gap: 8px; position: relative; z-index: 600; background: var(--pu-surface)">
	<b>Style:</b>
	{#each THEMES as t (t)}<button onclick={() => pick(t)} data-testid="pick-{t}">{t}</button>{/each}
	<span style="color: var(--pu-muted)">Saved for this browser. Default for everyone is set with PUBLIC_THEME.</span>
</div>
<div style="position: relative; height: 80vh"><NearbyFeed items={sample} weekCount={6} onPostUp={() => {}} onOpenMap={() => {}} /></div>
