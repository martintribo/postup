<script lang="ts">
	/** Mockups #profile / #me. */
	import { invalidateAll } from '$app/navigation';
	import ReportSheet from '$lib/components/ReportSheet.svelte';
	let { data } = $props();
	const p = $derived(data.profile);
	let reporting = $state(false);
	async function toggleFollow() {
		await fetch('/api/follows', { method: data.following ? 'DELETE' : 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ targetType: 'user', targetId: p.id }) });
		await invalidateAll();
	}
</script>

<main class="pu-page" data-testid="profile">
	<a href="/" class="m">← Back</a>
	<header>
		<span class="av">{#if p.avatarUrl}<img src={p.avatarUrl} alt="" />{:else}{p.name[0]?.toUpperCase()}{/if}</span>
		<div>
			<h1>{p.name}</h1>
			<p class="m">@{p.username} · {p.followers} follower{p.followers === 1 ? '' : 's'}</p>
		</div>
	</header>
	{#if p.bio}<p>{p.bio}</p>{/if}
	<div class="row">
		{#if data.isMe}
			<a class="btn" href="/settings" data-testid="edit-profile">Edit profile & settings</a>
		{:else if data.signedIn}
			<button class="btn primary" onclick={toggleFollow} data-testid="follow">{data.following ? 'Following' : 'Follow'}</button>
			<button class="btn" onclick={() => (reporting = !reporting)}>Report</button>
		{/if}
	</div>
	{#if reporting}<ReportSheet targetType="user" targetId={p.id} blockUserId={p.id} blockName={p.name} onDone={() => (reporting = false)} />{/if}

	{#if p.projects.length}
		<h2>Projects</h2>
		<ul>{#each p.projects as pr (pr.id)}<li><a href="/projects/{pr.id}"><b>{pr.name}</b></a> <span class="m">{pr.short}</span></li>{/each}</ul>
	{/if}
	<h2>Postups</h2>
	{#if p.posts.length}
		<ul>{#each p.posts as po (po.id)}<li><a href="/postups/{po.id}">{po.activity}</a> <span class="m">· {po.where} · {new Date(po.at).toLocaleDateString([], { month: 'short', day: 'numeric' })}</span></li>{/each}</ul>
	{:else}
		<p class="m">No postups yet.</p>
	{/if}
</main>

<style>
	.pu-page { max-width: 640px; margin: 0 auto; padding: 20px 16px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	header { display: flex; gap: 12px; align-items: center; margin-top: 10px; }
	h1 { font-family: var(--pu-font-display); margin: 0; }
	.av { width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; background: var(--pu-accent); color: var(--pu-accent-text); font-size: 26px; font-weight: 700; overflow: hidden; }
	.av img { width: 100%; height: 100%; object-fit: cover; }
	.m { color: var(--pu-muted); text-decoration: none; margin: 0; }
	.row { display: flex; gap: 8px; margin: 10px 0; }
	.btn { padding: 8px 14px; border-radius: 999px; border: var(--pu-border-width) solid var(--pu-border); background: var(--pu-surface); color: var(--pu-text); font-weight: 600; text-decoration: none; cursor: pointer; }
	.primary { background: var(--pu-accent); color: var(--pu-accent-text); }
	ul { list-style: none; padding: 0; display: grid; gap: 6px; }
	li { padding: 8px 10px; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); }
	a { color: inherit; }
</style>
