<script lang="ts">
	/** Mockup feed_card (#quiet-feed / #quiet-feed-b): photo or tinted tile, who · when · distance, what, tags, joined, Post up here. */
	import { resolve } from '$app/paths';
	import type { FeedItem } from '$lib/server/feed';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	let { it }: { it: FeedItem & { when: string } } = $props();
	let photoOk = $state(true);
	const COLORS = ['#7c3aed', '#e11d48', '#0891b2', '#d97706', '#2563eb', '#10a364', '#db2777', '#4f46e5'];
	const tint = $derived(COLORS[[...(it.who || '?')].reduce((a, ch) => (a * 31 + ch.charCodeAt(0)) >>> 0, 7) % COLORS.length]);
	const dist = $derived(it.kind === 'postup' && it.miles != null ? (it.miles < 0.1 ? 'here' : `${it.miles < 10 ? it.miles.toFixed(1) : Math.round(it.miles)} mi`) : '');
	const profile = $derived(it.username ? resolve('/u/[username]', { username: it.username }) : null);
	const cafeHref = $derived(it.kind === 'postup' && it.placeId ? resolve('/places/[id]', { id: String(it.placeId) }) : null);
	const projHref = $derived(it.projectId ? resolve('/projects/[id]', { id: String(it.projectId) }) : null);
	const mediaHref = $derived(it.kind === 'update' ? projHref : (cafeHref ?? resolve('/postups/[id]', { id: String(it.id) })));
</script>

<article class="fc" data-testid="feed-card">
	{#if it.photo && photoOk}
		<a class="fm" href={mediaHref}><img src={it.photo} alt="" loading="lazy" onerror={() => (photoOk = false)} /><span class="fbadge"><Icon name="camera" size={12} /> {it.kind === 'update' ? it.projectName : `${(it.who || '').split(' ')[0]}'s`} photo</span></a>
	{:else if it.kind === 'postup'}
		<a class="fm fb" style="--c:{tint}" href={mediaHref} aria-label={it.cafe}><span><Icon name="coffee" size={28} /></span></a>
	{/if}
	<div class="fbd">
		<div class="fh">
			{#if profile}<a class="fh lk2" href={profile}><Av name={it.who} src={it.avatarUrl} size={28} /><b>{it.who}</b></a>{:else}<Av name={it.who || it.projectName} src={it.avatarUrl} size={28} /><b>{it.who || it.projectName}</b>{/if}
			<span class="mu sm">· {it.when}{dist ? ` · ${dist}` : ''}</span>
		</div>
		<p class="fw">{it.kind === 'postup' ? it.activity : it.title || it.body}</p>
		<div class="fmeta">
			{#if it.projectName && projHref}<a class="tag" href={projHref}>{it.projectName}</a>{/if}
			{#if it.kind === 'update'}<span class="mu sm">Update</span>
			{:else if cafeHref}<a class="cl sm" href={cafeHref}><Icon name="pin" size={13} /> {it.cafe}</a>
			{:else}<span class="mu sm"><Icon name="pin" size={13} /> {it.cafe}</span>{/if}
		</div>
		<div class="fa">
			{#if it.kind === 'postup' && it.joined.length}
				<span class="soc"><span class="stk">{#each it.joined.slice(0, 3) as n, i (i)}<Av name={n} size={20} />{/each}</span><span class="mu sm">{it.joined.length} joined</span></span>
			{:else}<span></span>{/if}
			{#if it.kind === 'postup'}<a class="pill" href={it.placeId ? `/post?place=${it.placeId}` : '/post'}>Post up here</a>{/if}
		</div>
	</div>
</article>
