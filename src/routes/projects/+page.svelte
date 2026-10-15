<script lang="ts">
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Welcome from '$lib/components/ui/Welcome.svelte';
	import ProjectCard from '$lib/components/ui/ProjectCard.svelte';
	let { data } = $props();
	const newHref = $derived(data.signedIn ? '/projects/new' : '/login?next=/projects/new');
	const chip = (f: string) => (data.signedIn || f === 'all' ? (f === 'all' ? '/projects' : `/projects?f=${f}`) : `/login?next=${encodeURIComponent(`/projects?f=${f}`)}`);
</script>

<div class="scr-projects" data-testid="projects-page">
	<TopBar title="Projects" back={false}>
		{#snippet right()}<a class="ib" href={newHref} aria-label="New project"><Icon name="plus" size={22} /></a>{/snippet}
	</TopBar>
	<div class="pad pjs">
		<Welcome id="projects" icon="folder" cls="pwel" text="See what people nearby are building. Follow along or post up to work on yours." />
		<div class="hero"><h1>Projects</h1><p class="mu">What people nearby are building</p></div>
		<a class="btn newp" href={newHref}><Icon name="plus" size={18} /> New project {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</a>
		<div class="chips pchips" role="tablist">
			<a class="chip" class:on={data.filter === 'all'} href={chip('all')} role="tab" aria-selected={data.filter === 'all'}>Nearby</a>
			<a class="chip" class:on={data.filter === 'following'} href={chip('following')} role="tab" aria-selected={data.filter === 'following'}>Following</a>
			<a class="chip" class:on={data.filter === 'mine'} href={chip('mine')} role="tab" aria-selected={data.filter === 'mine'}>Mine</a>
		</div>
		{#if data.cards.length}
			<div class="pgrid">
				{#each data.cards as c (c.id)}<ProjectCard {c} />{/each}
			</div>
		{:else}
			<div class="estate pgrid-empty">
				{#if data.filter === 'following'}
					<h2>Follow a project to keep up with it</h2>
					<p class="mu">Open any project and tap Follow. Its updates and postups show up here.</p>
					<a class="btn sec" href="/projects">See projects nearby</a>
				{:else}
					<h2>Building something? Share a project</h2>
					<p class="mu">Add what you're working on so people nearby can follow along and join you.</p>
					<a class="btn" href={newHref}><Icon name="plus" size={18} /> New project</a>
				{/if}
			</div>
		{/if}
		{#if data.pending}
			<a class="lrow card pgrid-note" href="/projects/agent"><span class="ci sm pj"><Icon name="spark" size={16} /></span><div class="lm"><b>Changes from your agent</b><div class="l2">{data.pending} waiting for review</div></div><Icon name="chev" size={18} class="mu" /></a>
		{/if}
	</div>
</div>
