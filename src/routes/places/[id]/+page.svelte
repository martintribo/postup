<script lang="ts">
	/** Cafe (mockups #cafe, #cafe-gfail). Desktop: map + right panel. Google details stay inside GCard. */
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import GCard from '$lib/components/ui/GCard.svelte';
	import MapPanel from '$lib/components/ui/MapPanel.svelte';
	import ShareSheet from '$lib/components/sheets/ShareSheet.svelte';
	import { clock } from '$lib/time';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	let shareOpen = $state(false);
	const p = $derived(data.place);
	const dist = $derived(data.miles < 0.1 ? 'Here' : `${data.miles < 10 ? data.miles.toFixed(1) : Math.round(data.miles)} mi`);
</script>

<MapPanel latitude={p.latitude} longitude={p.longitude} cls="scr-cafe">
	<div class="hero-img" class:nocover={!data.photo} data-testid="cafe-page">
		{#if data.photo}<img src={data.photo.src} alt="" />{/if}
		<div class="hg"></div>
		<TopBar clear href="/">
			{#snippet right()}<button class="ib fl" onclick={() => (shareOpen = true)} data-testid="share" aria-label="Share"><Icon name="share" size={20} /></button>{/snippet}
		</TopBar>
		<div class="hi-t"><h1>{p.name}</h1><p><Icon name="pin" size={14} /> {dist}</p></div>
		{#if data.photo?.who}<span class="fbadge tr"><Icon name="camera" size={12} /> {data.photo.who.split(' ')[0]}'s photo</span>{/if}
	</div>
	<div class="pad">
		{#if data.hereNow.length}
			<div class="sp-h"><h2>Here now</h2><span class="ok sm"><span class="dot"></span> {data.hereNow.length} live</span></div>
			<div class="grp">
				{#each data.hereNow as h (h.id)}
					<a class="lrow" href="/postups/{h.id}">
						<Av name={h.who} src={h.avatarUrl} size={44} />
						<div class="lm"><div class="l1"><b>{h.who.split(' ')[0]}</b><span class="dot"></span><span class="ok">Live</span></div><div class="l2"><span class="cl">{h.cafe}</span> · till {clock(h.endsAt)}</div>{#if h.project}<span class="tag">{h.project}</span>{/if}</div>
						<span class="pill sm2">{h.ask ? 'Ask' : 'Join'}</span>
					</a>
				{/each}
			</div>
		{/if}
		<GCard googlePlaceId={p.googlePlaceId} name={p.name} lat={p.latitude} lng={p.longitude} />
		{#if data.week.n}
			<p class="mu sm"><span class="stk">{#each data.week.who as w, i (i)}<Av name={w} size={20} />{/each}</span> {data.week.n} {data.week.n === 1 ? 'postup' : 'postups'} this week{#if data.week.regular}{' · '}<a class="cl" href="/projects/{data.week.regularId}">{data.week.regular}</a> regular{/if}</p>
		{/if}
	</div>
	<div class="cta"><a class="btn" href="/post?place={p.id}"><Icon name="plus" size={18} /> Post up here</a></div>
</MapPanel>
<ShareSheet bind:open={shareOpen} path="/places/{p.id}" text="Work from {p.name} on PostUp" />
