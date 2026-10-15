<script lang="ts">
	import { onMount } from 'svelte';
	import { enhance } from '$app/forms';
	import { env } from '$env/dynamic/public';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Seg from '$lib/components/ui/Seg.svelte';
	import GooglePlaceSearch from '$lib/components/GooglePlaceSearch.svelte';
	import { askSignIn } from '$lib/signin.svelte';
	import { clock } from '$lib/time';
	let { data, form } = $props();

	type Spot = { placeId: number | null; name: string; latitude: number; longitude: number; googlePlaceId?: string; note: string };
	const fromPlace = (p: (typeof data.places)[number]): Spot => ({ placeId: p.id, name: p.name, latitude: p.latitude, longitude: p.longitude, note: `${p.mi < 0.1 ? 'Here' : p.mi.toFixed(1) + ' mi'}${p.live ? ` · ${p.live} live` : ''}` });
	const initial = data.places.find((p) => p.id === data.placeId) ?? data.places[0];
	let spot = $state<Spot | null>(initial ? { ...fromPlace(initial), note: data.placeId ? fromPlace(initial).note : `Nearest · ${fromPlace(initial).note}` } : null);
	let activity = $state('');
	let projectId = $state<number | null>(data.attach?.id ?? data.mine[0]?.id ?? null);
	const untilAt = (() => { const d = new Date(Date.now() + 3.5 * 3600e3); d.setMinutes(0, 0, 0); if (d.getTime() < Date.now() + 3.5 * 3600e3) d.setHours(d.getHours() + 1); return d; })();
	let until = $state('2h');
	let join = $state('open');
	let when = $state('now');
	let picking = $state(false);
	let q = $state('');
	let busy = $state(false);
	const hasGoogle = !!env.PUBLIC_GOOGLE_MAPS_BROWSER_KEY;
	const list = $derived(data.places.filter((p) => !q || p.name.toLowerCase().includes(q.toLowerCase())));
	const KEY = 'pu.postdraft';

	onMount(() => {
		try {
			const d = JSON.parse(sessionStorage.getItem(KEY) || 'null');
			if (d) ({ spot, activity, projectId, until, join, when } = { ...{ spot, activity, projectId, until, join, when }, ...d });
		} catch { /* no draft */ }
	});
	function pick(s: Spot) { spot = s; picking = false; q = ''; }
	function save() { sessionStorage.setItem(KEY, JSON.stringify({ spot, activity, projectId, until, join, when })); }
</script>

<form
	class="formscr scr-post"
	method="POST"
	data-testid="post-form"
	use:enhance={({ cancel }) => {
		save();
		if (!data.signedIn) {
			cancel();
			askSignIn({ title: 'Almost there', sub: 'Sign in and your postup goes live.', next: '/post' + (data.attach ? `?project=${data.attach.id}` : '') });
			return;
		}
		busy = true;
		return async ({ result, update }) => {
			if (result.type === 'redirect') sessionStorage.removeItem(KEY);
			await update();
			busy = false;
		};
	}}
>
	<TopBar title="Post up" />
	<div class="pad form">
		{#if data.attach}
			<label>Project</label>
			<div class="field"><span class="ci sm pj"><Icon name="folder" size={16} /></span><div class="lm"><b>{data.attach.name}</b></div></div>
		{/if}
		<label>Where</label>
		<button type="button" class="field" onclick={() => (picking = true)} data-testid="where-field">
			<span class="ci sm"><Icon name="coffee" size={16} /></span>
			<div class="lm">{#if spot}<b>{spot.name}</b><span class="mu xs">{spot.note}</span>{:else}<b>Pick a cafe</b><span class="mu xs">Search or choose one nearby</span>{/if}</div>
			<span class="lnk sm">{spot ? 'Change' : 'Choose'}</span>
		</button>

		{#if !data.attach}
			<label for="wo">Working on</label>
			<input id="wo" class="in" name="activity" bind:value={activity} maxlength="140" placeholder="Level editor for the mod" />
			<div class="chips">
				{#each data.mine as p (p.id)}<button type="button" class="chip" class:on={projectId === p.id} onclick={() => (projectId = p.id)}>{p.name}</button>{/each}
				<a class="chip ad" href={data.signedIn ? '/projects/new?back=post' : '/login?next=%2Fprojects%2Fnew%3Fback%3Dpost'} onclick={save}><Icon name="plus" size={14} /> Project</a>
				<button type="button" class="chip" class:on={projectId === null} onclick={() => (projectId = null)}>None</button>
			</div>
		{:else}
			<label>When</label>
			<Seg name="when" bind:value={when} options={[{ v: 'now', label: 'Now' }, { v: 'earlier', label: 'I was here earlier' }]} />
			<input type="hidden" name="activity" value={activity} />
		{/if}

		<label>Until</label>
		<Seg name="until" bind:value={until} testid="until" options={[{ v: '1h', label: '1h' }, { v: '2h', label: '2h' }, { v: '3h', label: '3h' }, ...(data.attach ? [] : [{ v: 'at', label: clock(untilAt) }])]} />
		<input type="hidden" name="untilAt" value={untilAt.toISOString()} />
		{#if !data.attach}
			<label>Who can join</label>
			<Seg name="join" bind:value={join} options={[{ v: 'open', label: 'Anyone can join' }, { v: 'ask', label: 'Ask to join' }]} />
			<p class="mu xs">{join === 'ask' ? "People ask first. Your cafe stays hidden until you say yes." : "You'll get an alert whenever someone joins."}</p>
		{:else}
			<p class="mu xs">I was here earlier adds it to the cafe's recent activity.</p>
		{/if}
		{#if form?.message}<p class="err" role="alert">{form.message}</p>{/if}

		<input type="hidden" name="projectId" value={projectId ?? ''} />
		<input type="hidden" name="placeId" value={spot?.placeId ?? ''} />
		<input type="hidden" name="placeName" value={spot?.name ?? ''} />
		<input type="hidden" name="latitude" value={spot?.latitude ?? ''} />
		<input type="hidden" name="longitude" value={spot?.longitude ?? ''} />
		<input type="hidden" name="googlePlaceId" value={spot?.googlePlaceId ?? ''} />
	</div>
	<div class="cta"><button class="btn" disabled={busy || !spot} data-testid="post-submit">{busy ? 'Posting…' : 'Post up'} {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</button></div>
</form>

{#if picking}
	<div class="dim" onclick={() => (picking = false)} role="presentation"></div>
	<div class="bs tall" role="dialog" aria-modal="true" aria-label="Where are you?" data-testid="where-sheet">
		<span class="grab"></span>
		<h2>Where are you?</h2>
		{#if hasGoogle}
			<GooglePlaceSearch near={data.location} onSelect={(g) => pick({ placeId: null, name: g.name, latitude: g.latitude, longitude: g.longitude, googlePlaceId: g.googlePlaceId, note: g.address ?? '' })} />
		{:else}
			<label class="srch"><input class="in" placeholder="Search cafes" bind:value={q} /></label>
		{/if}
		<p class="sh">Nearby</p>
		{#each list as p (p.id)}
			<button type="button" class="lrow wr" onclick={() => pick(fromPlace(p))}><span class="ci sm"><Icon name="coffee" size={16} /></span><div class="lm"><b>{p.name}</b><span class="l2">{fromPlace(p).note}</span></div></button>
		{:else}
			<p class="mu sm">Search for your cafe above and it's added for everyone.</p>
		{/each}
	</div>
{/if}
