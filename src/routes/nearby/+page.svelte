<script lang="ts">
	/** Nearby tab (mockup #quiet-feed, #quiet-feed-b, #empty-area, #offline). Root tab: no Back. No map. */
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { invalidateAll } from '$app/navigation';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import Welcome from '$lib/components/ui/Welcome.svelte';
	import ProjectCard from '$lib/components/ui/ProjectCard.svelte';
	import FeedCard from '$lib/components/feed/FeedCard.svelte';
	let { data } = $props();
	const me = $derived(data.user ? { name: data.user.displayName || data.user.username, href: resolve('/u/[username]', { username: data.user.username }) } : null);
	const empty = $derived(!data.anyLive && !data.projects.length);

	// #offline: keep what we had on screen, show the banner and Retry.
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
	const retry = (e: Event) => {
		e.preventDefault();
		if (navigator.onLine) invalidateAll();
	};
</script>

<div class="scr-quiet-feed" data-testid={data.anyLive ? 'nearby-feed' : 'nearby-projects'}>
	<TopBar title="Nearby" back={false}>
		{#snippet right()}
			{#if me}<a class="ib" href={me.href} aria-label="Profile"><Av name={me.name} src={data.user?.avatarUrl} size={30} /></a>{/if}
		{/snippet}
	</TopBar>
	<div class="pad fd">
		{#if offline}
			<div class="offl" role="status" data-testid="offline"><Icon name="wifi" size={16} /><span>You're offline · showing what we had</span><a class="lnk sm" href="/nearby" onclick={retry}>Retry</a></div>
		{:else}
			<Welcome id="feed" text="Post up at a cafe. See who's working nearby." />
		{/if}
		{#if empty}
			<!-- Mockup #empty-area, minus its map: no postups means no map (override F044/R1); Nearby never shows one. -->
			<div class="sp-h"><h2>Be the first here</h2></div>
			<p class="mu sm">No postups around {data.area} yet. Start one and people nearby will see it.</p>
			{#if data.cafes.length}
				<div class="cafes">
					{#each data.cafes as c (c.id)}
						<a class="lrow" href="/post?place={c.id}"><span class="ci"><Icon name="coffee" size={20} /></span><div class="lm"><b>{c.name}</b><div class="l2">{Number(c.mi).toFixed(1)} mi</div></div><Icon name="chev" size={18} class="mu" /></a>
					{/each}
				</div>
			{/if}
			<a class="btn lg" href="/post"><Icon name="plus" size={18} /> Post up</a>
		{:else}
			<div class="hero">
				<h1>Good things happen at cafes</h1>
				{#if data.anyLive}
					<p class="mu"><span class="stk">{#each data.who as w, i (i)}<Av name={w} size={24} />{/each}</span> {data.weekCount} {data.weekCount === 1 ? 'postup' : 'postups'} nearby this week</p>
				{:else}
					<p class="mu">What people are building</p>
				{/if}
			</div>
			<a class="btn lg" href="/post"><Icon name="plus" size={18} /> Post up</a>
			{#if data.anyLive}
				{#each data.items as it (it.kind + it.id)}<FeedCard {it} />{/each}
			{:else}
				{#each data.projects as c (c.id)}<ProjectCard {c} />{/each}
			{/if}
		{/if}
		<aside class="dside">
			<div class="dcta"><h2>Working somewhere today?</h2><p class="mu sm">Let people nearby know. Takes ten seconds.</p><a class="btn" href="/post"><Icon name="plus" size={18} /> Post up</a></div>
			{#if data.week.length}
				<div class="dcard">
					<h3>Cafes nearby</h3>
					{#each data.week as c (c.id)}
						<a class="lrow" href={resolve('/places/[id]', { id: String(c.id) })}><span class="ci"><Icon name="coffee" size={20} /></span><div class="lm"><b>{c.name}</b><div class="l2"><span class="stk">{#each c.who ?? [] as w, i (i)}<Av name={w} size={20} />{/each}</span> {c.n} this week</div></div><Icon name="chev" size={18} class="mu" /></a>
					{/each}
				</div>
			{/if}
			<a class="dmapc" href="/?mode=live"><div class="dmt dmt-tint"><span class="mk cafe" style="left:30%;top:34%"><span class="cp"><Icon name="coffee" size={15} /></span></span><span class="mk cafe" style="left:68%;top:58%"><span class="cp"><Icon name="coffee" size={15} /></span></span></div><div class="dml"><b>Open map</b><Icon name="chev" size={18} class="mu" /></div></a>
		</aside>
		{#if !empty}<p class="mu sm ctr">You're all caught up · <a class="lnk" href="/?mode=live">Map</a></p>{/if}
	</div>
</div>
