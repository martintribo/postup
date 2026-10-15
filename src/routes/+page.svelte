<script lang="ts">
	/** Home (mockup #home / #quiet): map with a "Live now" panel. Phone: sheet under the map. Desktop: floating side panel. */
	import { onMount } from 'svelte';
	import Map from '$lib/components/Map.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import { enhance } from '$app/forms';

	let { data } = $props();
	let mounted = $state(false);
	let setLocationForm: HTMLFormElement;
	let lat = $state(''), lng = $state('');

	const projectName = $derived(Object.fromEntries((data.projects ?? []).map((p) => [p.id, p.name])) as Record<number, string>);
	const live = $derived(
		(data.posts ?? []).map((p) => {
			const who = (p.userId && data.people?.[p.userId]) || { name: p.name, avatarUrl: null };
			const end = p.endsAt ? new Date(p.endsAt) : new Date(new Date(p.startTime).getTime() + p.hours * 3600e3);
			return { id: p.id, who, cafe: p.location, placeId: p.placeId, project: p.projectId ? projectName[p.projectId] : null, projectId: p.projectId, till: till(end) };
		})
	);
	function till(d: Date) {
		return d.toLocaleTimeString([], { hour: 'numeric', minute: d.getMinutes() ? '2-digit' : undefined }).replace(' ', '').toLowerCase();
	}
	function locate() {
		navigator.geolocation?.getCurrentPosition((pos) => {
			lat = String(pos.coords.latitude);
			lng = String(pos.coords.longitude);
			queueMicrotask(() => setLocationForm.requestSubmit());
		});
	}
	onMount(() => {
		mounted = true;
		if (data.locationSource !== 'precise' && navigator.geolocation) locate();
	});
</script>

<form bind:this={setLocationForm} method="POST" action="?/setLocation" use:enhance hidden>
	<input type="hidden" name="latitude" value={lat} />
	<input type="hidden" name="longitude" value={lng} />
</form>

<div class="home" data-testid="home">
	<div class="map hmap">
		{#if mounted}
			<Map latitude={data.location.latitude} longitude={data.location.longitude} city={data.location.city} country={data.location.country} posts={data.posts} chrome={false} />
		{/if}
		<div class="mtop">
			<span class="brand"><Icon name="coffee" size={16} /> postup</span>
			<button class="ib fl" onclick={locate} aria-label="Locate me"><Icon name="locate" size={20} /></button>
		</div>
	</div>

	<section class="sheet-p livep" data-testid="live-now">
		<span class="grab"></span>
		{#if data.myLive}
			<a class="lrow you-live" href="/postups/{data.myLive.id}">
				<span class="ci"><span class="dot"></span></span>
				<div class="lm"><b>You're live</b><div class="l2">{data.myLive.activity}</div></div>
				<Icon name="chev" size={18} class="mu" />
			</a>
		{/if}
		{#if live.length}
			<div class="sp-h"><h2>Live now</h2><span class="mu sm">{live.length} nearby</span></div>
			{#each live as p (p.id)}
				<a class="lrow" href="/postups/{p.id}">
					<Av name={p.who.name} src={p.who.avatarUrl} size={44} />
					<div class="lm">
						<div class="l1"><b>{p.who.name}</b><span class="dot"></span><span class="ok">Live</span></div>
						<div class="l2">{p.cafe} · till {p.till}</div>
						{#if p.project}<span class="tag">{p.project}</span>{/if}
					</div>
					<Icon name="chev" size={18} class="mu" />
				</a>
			{/each}
		{:else}
			<div class="sp-h"><h2>Working somewhere good today?</h2></div>
			<p class="mu sm">Post up and people nearby can come work with you.</p>
			<a class="btn" href="/post"><Icon name="plus" size={18} /> Post up</a>
		{/if}
		{#if data.week?.length}
			<div class="sp-h" style="margin-top:12px"><h3>This week</h3></div>
			{#each data.week as c (c.id)}
				<a class="lrow" href="/places/{c.id}">
					<span class="ci"><Icon name="coffee" size={20} /></span>
					<div class="lm">
						<b>{c.name}</b>
						<div class="l2"><span class="stk">{#each c.who ?? [] as w, i (i)}<Av name={w} size={20} />{/each}</span> {c.n} {c.n === 1 ? 'postup' : 'postups'}</div>
					</div>
					<Icon name="chev" size={18} class="mu" />
				</a>
			{/each}
		{/if}
		{#if live.length}<a class="btn" href="/post"><Icon name="plus" size={18} /> Post up</a>{/if}
	</section>
</div>
