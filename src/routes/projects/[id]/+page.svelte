<script lang="ts">
	import ShareButton from '$lib/components/ShareButton.svelte';
	let { data } = $props();
	const p = $derived(data.project);
</script>

<main class="pu-page" data-testid="project-page">
	<a href="/projects" class="back">← Projects</a>
	<h1>{p.name}</h1>
	{#if p.owner}<p class="m">by {p.owner}</p>{/if}
	<p>{p.short}</p>
	<div class="row">
		{#if data.liveId}<a class="cta" href="/postups/{data.liveId}">Join {p.owner || 'them'} now</a>{/if}
		<ShareButton path="/projects/{p.id}" text={data.title} />
	</div>
	<h2>Updates</h2>
	{#each data.updates as u (u.id)}
		<article>
			{#if u.title}<b>{u.title}</b>{/if}
			<p>{u.body}</p>
			<time class="m">{new Date(u.at).toLocaleDateString([], { month: 'short', day: 'numeric' })}</time>
		</article>
	{:else}
		<p class="m">No updates yet.</p>
	{/each}
</main>

<style>
	.pu-page { max-width: 680px; margin: 0 auto; padding: 20px 16px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	h1 { font-family: var(--pu-font-display); margin: 8px 0 0; }
	.back, .m { color: var(--pu-muted); text-decoration: none; }
	.row { display: flex; gap: 8px; flex-wrap: wrap; }
	.cta { padding: 10px 14px; border-radius: calc(var(--pu-radius) - 4px); background: var(--pu-accent); color: var(--pu-accent-text); font-weight: 700; text-decoration: none; }
	article { padding: 10px 12px; margin: 8px 0; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); }
	article p { margin: 4px 0; white-space: pre-wrap; }
</style>
