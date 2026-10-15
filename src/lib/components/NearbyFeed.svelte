<script lang="ts">
	/** Nearby feed (mockup #quiet-feed): shown instead of the map when nobody nearby is live. */
	import { onMount } from 'svelte';
	import type { FeedItem } from '$lib/server/feed';

	let {
		items,
		weekCount,
		onPostUp,
		onOpenMap
	}: { items: FeedItem[]; weekCount: number; onPostUp: () => void; onOpenMap: () => void } = $props();

	let showWelcome = $state(false);
	onMount(() => {
		showWelcome = localStorage.getItem('pu.welcome.feed') !== '1';
	});
	function dismiss() {
		localStorage.setItem('pu.welcome.feed', '1');
		showWelcome = false;
	}
	function rel(iso: string) {
		const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
		if (m < 60) return `${Math.max(m, 1)}m ago`;
		const h = Math.round(m / 60);
		if (h < 24) return h < 6 ? `${h}h ago` : 'earlier today';
		const d = Math.round(h / 24);
		return d === 1 ? 'yesterday' : `${d} days ago`;
	}
	const initial = (s: string) => (s.trim()[0] || '?').toUpperCase();
</script>

<section class="pu-feed" data-testid="nearby-feed">
	<header class="pu-feed-head">
		<div>
			<h2>Nearby</h2>
			<p class="pu-muted">Good things happen at cafes{weekCount ? ` · ${weekCount} postup${weekCount === 1 ? '' : 's'} this week` : ''}</p>
		</div>
		<button type="button" class="pu-link" onclick={onOpenMap} data-testid="open-map">Open map</button>
	</header>

	{#if showWelcome}
		<div class="pu-welcome" data-testid="feed-welcome">
			<span>Post up at a cafe and see who's working nearby.</span>
			<button type="button" class="pu-x" onclick={dismiss} aria-label="Dismiss">×</button>
		</div>
	{/if}

	<button type="button" class="pu-cta" onclick={onPostUp} data-testid="feed-postup"><span>Post up</span></button>

	{#if items.length === 0}
		<div class="pu-card pu-empty" data-testid="feed-empty">
			<b>Be the first here this week.</b>
			<p class="pu-muted">Pick a cafe, say what you're working on, and people nearby can join you.</p>
		</div>
	{:else}
		<ul class="pu-list">
			{#each items as it (it.kind + it.id)}
				<li class="pu-card">
					{#if it.kind === 'postup'}
						<div class="pu-row">
							<span class="pu-av" aria-hidden="true">
								{#if it.avatarUrl}<img src={it.avatarUrl} alt="" />{:else}{initial(it.who)}{/if}
							</span>
							<div class="pu-body">
								<div><b>{it.who}</b> {it.live ? 'is posted up' : 'posted up'} at
									{#if it.placeId}<a href="/places/{it.placeId}">{it.cafe}</a>{:else}{it.cafe}{/if}
									{#if it.live}<span class="pu-live">Live</span>{/if}
								</div>
								<div class="pu-act">{it.activity}</div>
								<div class="pu-muted pu-meta">
									{rel(it.at)}{#if it.projectName} · <a href="/projects/{it.projectId}">{it.projectName}</a>{/if}
								</div>
							</div>
						</div>
					{:else}
						<div class="pu-row">
							<span class="pu-av pu-av-proj" aria-hidden="true">{initial(it.projectName)}</span>
							<div class="pu-body">
								<div><a href="/projects/{it.projectId}"><b>{it.projectName}</b></a> update</div>
								{#if it.title}<div class="pu-act">{it.title}</div>{/if}
								<div class="pu-clamp">{it.body}</div>
								<div class="pu-muted pu-meta">{rel(it.at)}</div>
							</div>
						</div>
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
</section>

<style>
	.pu-feed { position: absolute; inset: 0; overflow-y: auto; padding: 16px; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); z-index: 500; }
	.pu-feed-head { display: flex; justify-content: space-between; align-items: flex-start; max-width: 720px; margin: 0 auto 10px; }
	h2 { margin: 0; font-family: var(--pu-font-display); font-size: 26px; }
	.pu-muted { color: var(--pu-muted); margin: 2px 0 0; font-size: 14px; }
	.pu-link { white-space: nowrap; background: none; border: var(--pu-border-width) solid var(--pu-border); border-radius: 999px; padding: 6px 12px; color: var(--pu-text); cursor: pointer; }
	.pu-welcome, .pu-cta, .pu-list, .pu-empty { max-width: 720px; margin-left: auto; margin-right: auto; }
	.pu-welcome { display: flex; justify-content: space-between; gap: 8px; padding: 10px 12px; margin-bottom: 10px; border-radius: var(--pu-radius); background: var(--pu-surface); border: var(--pu-border-width) dashed var(--pu-border); }
	.pu-x { background: none; border: 0; font-size: 18px; cursor: pointer; color: var(--pu-muted); }
	.pu-cta span { color: var(--pu-accent-text); }
	.pu-cta { display: block; width: 100%; padding: 14px; margin-bottom: 14px; font-weight: 700; font-size: 16px; border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); background: var(--pu-accent); color: var(--pu-accent-text); box-shadow: var(--pu-shadow); cursor: pointer; }
	.pu-list { list-style: none; padding: 0; display: grid; gap: 10px; }
	@media (min-width: 1024px) { .pu-list, .pu-cta, .pu-welcome, .pu-empty, .pu-feed-head { max-width: 1040px; } .pu-list { grid-template-columns: 1fr 1fr; } }
	.pu-card { background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); box-shadow: var(--pu-shadow); padding: 12px; }
	.pu-row { display: flex; gap: 10px; }
	.pu-av { flex: 0 0 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; font-weight: 700; background: var(--pu-accent); color: var(--pu-accent-text); overflow: hidden; }
	.pu-av img { width: 100%; height: 100%; object-fit: cover; }
	.pu-av-proj { border-radius: 10px; background: var(--pu-border); color: var(--pu-text); }
	.pu-body { min-width: 0; }
	.pu-act { font-weight: 600; margin-top: 2px; }
	.pu-meta { font-size: 13px; }
	.pu-clamp { display: -webkit-box; -webkit-line-clamp: 3; line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
	.pu-live { margin-left: 6px; font-size: 11px; font-weight: 700; padding: 1px 6px; border-radius: 999px; background: var(--pu-live); color: #fff; }
	a { color: inherit; }
</style>
