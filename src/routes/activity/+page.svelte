<script lang="ts">
	/** Mockup #activity. */
	import { onMount } from 'svelte';
	let { data } = $props();
	onMount(() => {
		fetch('/api/notifications/read', { method: 'POST' });
	});
</script>

<main class="pu-page" data-testid="activity">
	<a href="/" class="pu-back">← Back</a>
	<h1>Activity</h1>
	{#if data.items.length === 0}
		<p class="pu-muted">Nothing yet. When someone joins or asks to join your postup, you'll see it here.</p>
	{:else}
		<ul>
			{#each data.items as n (n.id)}
				<li class:unread={!n.readAt}>
					{#if n.postId}<a href="/postups/{n.postId}">{n.body}</a>{:else}{n.body}{/if}
					<time class="pu-muted">{new Date(n.createdAt).toLocaleString([], { weekday: 'short', hour: 'numeric', minute: '2-digit' })}</time>
				</li>
			{/each}
		</ul>
	{/if}
</main>

<style>
	.pu-page { max-width: 640px; margin: 0 auto; padding: 20px 16px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	h1 { font-family: var(--pu-font-display); }
	.pu-back { color: var(--pu-muted); text-decoration: none; }
	.pu-muted { color: var(--pu-muted); font-size: 13px; display: block; }
	ul { list-style: none; padding: 0; display: grid; gap: 8px; }
	li { padding: 10px 12px; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); }
	li.unread { border-left: 4px solid var(--pu-accent); }
	a { color: inherit; }
</style>
