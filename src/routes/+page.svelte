<script lang="ts">
	/** Home (mockup #home): one URL, Live (map) and Building (projects). The mode sticks for this visit. */
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { invalidateAll } from '$app/navigation';
	import Map from '$lib/components/Map.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import { enhance } from '$app/forms';
	import Welcome from '$lib/components/ui/Welcome.svelte';
	import ProjectCard from '$lib/components/ui/ProjectCard.svelte';

	let { data } = $props();
	let mounted = $state(false);
	let setLocationForm: HTMLFormElement | undefined;
	let lat = $state(''), lng = $state('');
	function grabForm(node: HTMLFormElement) {
		setLocationForm = node;
	}

	const projectName = $derived(Object.fromEntries((data.projects ?? []).map((p) => [p.id, p.name])) as Record<number, string>);
	const live = $derived(
		(data.posts ?? []).map((p) => {
			const who = (p.userId && data.people?.[p.userId]) || { name: p.name, avatarUrl: null };
			const end = p.endsAt ? new Date(p.endsAt) : new Date(new Date(p.startTime).getTime() + p.hours * 3600e3);
			return { id: p.id, who, cafe: p.location, placeId: p.placeId, project: p.projectId ? projectName[p.projectId] : null, projectId: p.projectId, till: till(end) };
		})
	);
	const newest = $derived(live[0]);
	const area = $derived(data.location.city || data.areaName);

	// Null until the user picks a mode or this visit locks the default. A later live postup must not flip the page.
	let picked = $state<'live' | 'building' | null>(null);
	const mode = $derived.by((): 'live' | 'building' => {
		if (picked) return picked;
		const q = page.url.searchParams.get('mode');
		if (q === 'live' || q === 'building') return q;
		return live.length ? 'live' : 'building';
	});

	function till(d: Date) {
		return d.toLocaleTimeString([], { hour: 'numeric', minute: d.getMinutes() ? '2-digit' : undefined }).replace(' ', '').toLowerCase();
	}
	function firstName(name: string) {
		return name.trim().split(/\s+/)[0] || name;
	}
	function setMode(next: 'live' | 'building') {
		picked = next;
		const url = new URL(page.url);
		url.searchParams.set('mode', next);
		history.replaceState(history.state, '', `${url.pathname}${url.search}`);
	}
	function locate() {
		navigator.geolocation?.getCurrentPosition((pos) => {
			lat = String(pos.coords.latitude);
			lng = String(pos.coords.longitude);
			queueMicrotask(() => setLocationForm?.requestSubmit());
		});
	}
	onMount(() => {
		mounted = true;
		if (picked === null) picked = mode;
		if (data.locationSource !== 'precise' && navigator.geolocation) locate();
		const id = setInterval(() => {
			if (mode === 'building' && document.visibilityState === 'visible') invalidateAll();
		}, 20000);
		return () => clearInterval(id);
	});
</script>

{#snippet modeSwitch(which: string)}
	<div class="hsw hsw-{which}" role="tablist" aria-label="Home mode">
		<button type="button" role="tab" aria-selected={mode === 'live'} class:on={mode === 'live'} onclick={() => setMode('live')}>Live</button>
		<button type="button" role="tab" aria-selected={mode === 'building'} class:on={mode === 'building'} onclick={() => setMode('building')}>Building</button>
	</div>
{/snippet}

<form {@attach grabForm} method="POST" action="?/setLocation" use:enhance hidden>
	<input type="hidden" name="latitude" value={lat} />
	<input type="hidden" name="longitude" value={lng} />
</form>

{#if mode === 'building'}
	<div class="home-building" data-testid="home-building">
		<header class="nb hnb">
			<b class="brand2"><Icon name="coffee" size={16} /> postup</b>
			{@render modeSwitch('bar')}
			<span class="nr"></span>
		</header>
		<div class="pad hbld">
			{#if newest}
				<div class="hban" data-testid="live-banner">
					<span class="dot"></span>
					<span class="who"><Av name={newest.who.name} src={newest.who.avatarUrl} size={22} /> <b>{firstName(newest.who.name)}</b> just posted up nearby</span>
					<button type="button" class="lnk sm" onclick={() => setMode('live')}>See map</button>
				</div>
			{/if}
			<Welcome id="home" text="Post up at a cafe. See who's working nearby." />
			<div class="hbh">
				<h1>What people are building</h1>
				<a class="lnk sm" href={resolve('/projects')}>See all projects</a>
			</div>
			{#if data.projectCards?.length}
				<div class="hpg">
					{#each data.projectCards as c (c.id)}<ProjectCard {c} />{/each}
				</div>
			{:else}
				<div class="estate"><h2>Be the first here</h2><p class="mu">Post up at a cafe or share what you're building, and people nearby will see it.</p></div>
			{/if}
			<a class="btn sec hall" href={resolve('/projects')}><Icon name="folder" size={18} /> See all projects</a>
			<a class="btn lg hpost" href={resolve('/post')}><Icon name="plus" size={18} /> Post up</a>
			{#if data.week?.length}
				<div class="grp hwk">
					<h3 class="sh">This week</h3>
					{#each data.week as c (c.id)}
						<a class="lrow" href={resolve('/places/[id]', { id: String(c.id) })}>
							<span class="ci"><Icon name="coffee" size={20} /></span>
							<div class="lm">
								<b>{c.name}</b>
								<div class="l2"><span class="stk">{#each c.who ?? [] as w, i (i)}<Av name={w} size={20} />{/each}</span> {c.n} {c.n === 1 ? 'postup' : 'postups'}</div>
							</div>
							<Icon name="chev" size={18} class="mu" />
						</a>
					{/each}
				</div>
			{/if}
		</div>
	</div>
{:else}
	<div class="home" data-testid="home">
		<div class="map hmap">
			{#if mounted}
				<Map latitude={data.location.latitude} longitude={data.location.longitude} city={data.location.city} country={data.location.country} posts={data.posts} chrome={false} />
			{/if}
			<div class="mtop">
				<span class="brand hbr"><Icon name="coffee" size={16} /> postup</span>
				{@render modeSwitch('ph')}
				<span class="area-chip"><Icon name="pin" size={16} /> {area}</span>
				<button class="ib fl" onclick={locate} aria-label="Locate me"><Icon name="locate" size={20} /></button>
			</div>
		</div>

		<section class="sheet-p livep" data-testid="live-now">
			<span class="grab"></span>
			{@render modeSwitch('dk')}
			{#if data.myLive}
				<a class="lrow you-live" data-testid="live-bar" href={resolve('/postups/[id]', { id: String(data.myLive.id) })}>
					<span class="ci"><span class="dot"></span></span>
					<div class="lm"><b>You're live</b><div class="l2">{data.myLive.activity}</div></div>
					<Icon name="chev" size={18} class="mu" />
				</a>
			{/if}
			{#if live.length}
				<div class="sp-h"><h2>Live now</h2><span class="mu sm">{live.length} nearby</span></div>
				{#each live as p (p.id)}
					<a class="lrow" href={resolve('/postups/[id]', { id: String(p.id) })}>
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
				<div class="hinv">
					<h2>Working somewhere today?</h2>
					<p class="mu sm">Post up and people nearby will see you on the map.</p>
					<a class="btn" href={resolve('/post')}><Icon name="plus" size={18} /> Post up</a>
				</div>
			{/if}
			{#if data.week?.length}
				<div class="sp-h" style="margin-top:12px"><h3>This week</h3></div>
				{#each data.week as c (c.id)}
					<a class="lrow" href={resolve('/places/[id]', { id: String(c.id) })}>
						<span class="ci"><Icon name="coffee" size={20} /></span>
						<div class="lm">
							<b>{c.name}</b>
							<div class="l2"><span class="stk">{#each c.who ?? [] as w, i (i)}<Av name={w} size={20} />{/each}</span> {c.n} {c.n === 1 ? 'postup' : 'postups'}</div>
						</div>
						<Icon name="chev" size={18} class="mu" />
					</a>
				{/each}
			{/if}
		</section>
	</div>
{/if}
