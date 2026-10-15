<script lang="ts">
	import { goto } from '$app/navigation';
	import NearbyFeed from '$lib/components/NearbyFeed.svelte';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Welcome from '$lib/components/ui/Welcome.svelte';
	import ProjectCard from '$lib/components/ui/ProjectCard.svelte';
	let { data } = $props();
</script>

{#if data.feed.items.length}
	<NearbyFeed items={data.feed.items} weekCount={data.feed.weekCount} onPostUp={() => goto('/post')} onOpenMap={() => goto('/')} area={data.area} />
{:else}
	<div class="scr-projects" data-testid="nearby-projects">
		<TopBar title="Nearby" back={false} />
		<div class="pad pjs">
			<Welcome id="feed" text="Post up at a cafe. See who's working nearby." cls="pwel" />
			<p class="mu area-ph">Near {data.area} · recent projects from people who post up around here</p>
			<div class="hero"><h1>What people are building</h1><p class="mu">Near {data.area} · recent projects from people who post up around here</p></div>
			<a class="btn newp" href="/post"><Icon name="plus" size={18} /> Post up</a>
			{#if data.projects.length}
				<div class="pgrid">{#each data.projects as c (c.id)}<ProjectCard {c} />{/each}</div>
			{:else}
				<div class="estate pgrid-empty"><h2>Be the first here</h2><p class="mu">Post up at a cafe and people nearby will see it.</p><a class="btn" href="/post"><Icon name="plus" size={18} /> Post up</a></div>
			{/if}
		</div>
	</div>
{/if}
