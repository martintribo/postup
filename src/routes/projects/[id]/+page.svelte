<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import { shareLink } from '$lib/share';
	import { clock } from '$lib/time';
	let { data } = $props();
	const p = $derived(data.project);
	const gate = (to: string) => (data.signedIn ? to : `/login?next=${encodeURIComponent(to)}`);
	const KIND: Record<string, string> = { software: 'Code', code: 'Code', game: 'Game', art: 'Art', hardware: 'Hardware', writing: 'Writing', other: 'Project' };
	let shareMsg = $state('');
	async function share() {
		const r = await shareLink(`/projects/${p.id}?s=1`, data.title);
		shareMsg = r === 'copied' ? 'Link copied' : '';
		if (shareMsg) setTimeout(() => (shareMsg = ''), 2000);
	}
	async function toggleFollow() {
		await fetch('/api/follows', { method: data.following ? 'DELETE' : 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ targetType: 'project', targetId: p.id }) });
		await invalidateAll();
	}
	const postups = $derived(`${data.stats.total} ${data.stats.total === 1 ? 'postup' : 'postups'}`);
</script>

{#if data.landing}
<div class="scr-invite-project" data-testid="invite-project">
	<header class="nb"><span class="ib"></span><b class="brand2"><Icon name="coffee" size={16} /> postup</b><span class="nr"></span></header>
	<div class="pad done inv">
		{#if p.cover}<img class="invimg" src={p.cover} alt="" />{/if}
		{#if p.owner}<div class="pair"><Av name={p.owner} src={p.ownerAvatar} size={56} /></div>{/if}
		<h1>{p.owner ? `${p.owner.split(' ')[0]} is building ${p.name}` : p.name}</h1>
		<p class="mu">{p.short || 'See updates, follow, or join the next postup.'}</p>
		<a class="btn" href="/projects/{p.id}">See updates</a>
		<a class="btn sec" href={gate(`/projects/${p.id}`)}>Follow <Icon name="lock" size={14} class="lk" /></a>
		{#if data.liveId}<a class="lnk sm" href="/postups/{data.liveId}">Live now · join them</a>{:else if data.stats.weekCafe}<a class="lnk sm" href="/projects/{p.id}">Usually at {data.stats.weekCafe}</a>{/if}
		<p class="mu sm">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p>
	</div>
</div>
{:else}
<div class="scr-project" data-testid="project-page">
	<div class="hero-img sm" class:nocover={!p.cover}>
		{#if p.cover}<img src={p.cover} alt="" />{/if}
		<div class="hg"></div>
		<TopBar clear href="/projects">
			{#snippet right()}<button class="ib fl" onclick={share} aria-label="Share"><Icon name="share" size={20} /></button>{/snippet}
		</TopBar>
		<div class="hi-t">
			<span class="tag lt">{KIND[p.type ?? ''] ?? 'Project'}</span>
			<h1>{p.name}</h1>
			<p>{#if p.owner}by <a class="cl" href="/u/{p.ownerUsername}">{p.owner}</a> · {/if}{postups}</p>
		</div>
	</div>
	{#if shareMsg}<p class="toast" role="status">{shareMsg}</p>{/if}

	<div class="pad">
		<div class="row2">
			{#if data.isOwner}
				<a class="btn sec" href="/projects/{p.id}/update"><Icon name="edit" size={16} /> Update</a>
			{:else if data.signedIn}
				<button class="btn sec" onclick={toggleFollow} data-testid="follow-project">{data.following ? 'Following' : 'Follow'}</button>
			{:else}
				<a class="btn sec" href={gate(`/projects/${p.id}`)}><Icon name="star" size={16} /> Follow <Icon name="lock" size={14} class="lk" /></a>
			{/if}
			<a class="btn" href={gate(`/post?project=${p.id}`)}><Icon name="plus" size={16} /> Post up {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</a>
		</div>

		<aside class="pside">
			<div class="dcard">
				{#if p.owner}<div class="fh"><Av name={p.owner} src={p.ownerAvatar} size={44} /><div class="lm"><b>{p.owner}</b><span class="mu sm">Owner · {postups}</span></div></div>{/if}
				<p class="sm">{p.about}</p>
				<a class="btn" href={gate(`/post?project=${p.id}`)}><Icon name="plus" size={18} /> Post up for this {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</a>
				{#if data.isOwner}
					<a class="btn sec" href="/projects/{p.id}/update"><Icon name="edit" size={16} /> Post update</a>
				{:else if data.signedIn}
					<button class="btn sec" onclick={toggleFollow}>{data.following ? 'Following' : 'Follow'}</button>
				{:else}
					<a class="btn sec" href={gate(`/projects/${p.id}`)}><Icon name="star" size={16} /> Follow <Icon name="lock" size={14} class="lk" /></a>
				{/if}
			</div>
			<div class="dcard">
				<h3>This week</h3>
				{#if data.stats.week}
					<p class="mu sm"><span class="stk">{#each data.stats.who as w, i (i)}<Av name={w} size={22} />{/each}</span> {data.stats.week} {data.stats.week === 1 ? 'postup' : 'postups'}{#if data.stats.weekCafe} · {data.stats.weekCafe}{/if}</p>
				{:else}
					<p class="mu sm">Post up for {p.name} and it shows here.</p>
				{/if}
			</div>
		</aside>

		<p class="about-ph">{p.about}</p>

		{#if data.live.length}
			<div class="sp-h"><h2>Live</h2></div>
			{#each data.live as l (l.id)}
				<a class="lrow card" href="/postups/{l.id}">
					<Av name={l.who} src={l.avatarUrl} size={40} />
					<div class="lm"><b>{l.who}</b><div class="l2">{l.cafe} · till {clock(l.endsAt)}</div></div>
					<span class="ok sm"><span class="dot"></span> Live</span>
				</a>
			{/each}
		{/if}

		<div class="sp-h"><h2>Updates</h2></div>
		{#if data.updates.length}
			<div class="tl">
				{#each data.updates as u (u.id)}
					<div class="ti">
						<b>{u.title || u.body.split('\n')[0]}</b>
						<span class="mu sm">{u.when}{#if u.placeName} · at {u.placeName}{/if}</span>
						{#if u.title && u.body}<p class="sm">{u.body}</p>{/if}
						{#if u.image}<img src={u.image} alt="" loading="lazy" />{/if}
					</div>
				{/each}
			</div>
		{:else if data.isOwner}
			<a class="lrow card" href="/projects/{p.id}/update"><span class="ci sm pj"><Icon name="edit" size={16} /></span><div class="lm"><b>Post your first update</b><div class="l2">A line and a photo is plenty.</div></div><Icon name="chev" size={18} class="mu" /></a>
		{:else}
			<p class="mu sm">Follow {p.name} to hear when {p.owner || 'the owner'} posts an update.</p>
		{/if}
	</div>
</div>
{/if}
