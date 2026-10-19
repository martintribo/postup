<script lang="ts">
	/** Mockups #profile / #me: live card, avatar, bio, "N postups · since Sep", Follow or Edit profile,
	 *  regular cafes, projects, past postups. ⋯ → Share / Report / Block. Gear → Settings (yours). */
	import { invalidateAll } from '$app/navigation';
	import { enhance } from '$app/forms';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import Sheet from '$lib/components/sheets/Sheet.svelte';
	import ShareSheet from '$lib/components/sheets/ShareSheet.svelte';
	import BlockSheet from '$lib/components/sheets/BlockSheet.svelte';
	import { askSignIn } from '$lib/signin.svelte';
	import { clock } from '$lib/time';
	let { data } = $props();
	const p = $derived(data.profile);
	const first = $derived(p.name.split(' ')[0]);
	let moreOpen = $state(false);
	let shareOpen = $state(false);
	let blockOpen = $state(false);
	let editOpen = $state(false);
	let busy = $state(false);
	let now = $state(Date.now());
	const since = $derived(p.since ? new Date(p.since).toLocaleDateString('en-US', { month: 'short', ...(new Date(p.since).getFullYear() !== new Date().getFullYear() ? { year: 'numeric' } : {}) }) : null);
	const day = (iso: string) => {
		const d = new Date(iso);
		const days = Math.floor((now - d.getTime()) / 86400e3);
		if (days < 1) return 'Today';
		if (days < 2) return 'Yesterday';
		if (days < 7) return d.toLocaleDateString('en-US', { weekday: 'short' });
		return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
	};
	const updated = (iso: string) => { const d = day(iso); return `Updated ${d === 'Today' || d === 'Yesterday' ? d.toLowerCase() : d}`; };
	const ring = $derived.by(() => {
		if (!p.live) return { p: 0, t: '' };
		const total = new Date(p.live.endsAt).getTime() - new Date(p.live.startTime).getTime();
		const left = Math.max(0, new Date(p.live.endsAt).getTime() - now);
		const m = Math.round(left / 60000);
		return { p: total > 0 ? left / total : 0, t: `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}` };
	});
	async function follow() {
		if (!data.signedIn) { askSignIn({ title: `Follow ${first}`, sub: 'Sign in to follow along.', next: `/u/${p.username}` }); return; }
		busy = true;
		await fetch('/api/follows', { method: data.following ? 'DELETE' : 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ targetType: 'user', targetId: p.id }) });
		await invalidateAll();
		busy = false;
	}
</script>

<div class="acctscr scr-profile" data-testid="profile">
	<TopBar>
		{#snippet right()}
			{#if data.isMe}<a class="ib" href="/settings" aria-label="Settings" data-testid="settings-link"><Icon name="settings" size={20} /></a>
			{:else}<button class="ib" onclick={() => (moreOpen = true)} aria-label="More" data-testid="more"><Icon name="more" size={20} /></button>{/if}
		{/snippet}
	</TopBar>
	<div class="pad prof">
		{#if p.live}
			<a class="card livec sm2c" href="/postups/{p.live.id}" data-testid="profile-live">
				{#if data.isMe}<div class="ring sm" style="--p:{ring.p.toFixed(2)}"><b>{ring.t}</b></div>{:else}<span class="dot"></span>{/if}
				<div class="lm"><b>{data.isMe ? `You're live at ${p.live.cafe}` : `Live at ${p.live.cafe}`}</b><span class="mu sm">Till {clock(p.live.endsAt)}{#if data.isMe && data.requests} · {data.requests} {data.requests === 1 ? 'request' : 'requests'}{:else if p.live.project} · {p.live.project}{/if}</span></div>
			</a>
		{/if}
		<div class="phd">
			<Av name={p.name} src={p.avatarUrl} size={88} />
			<h1>{first}</h1>
			{#if p.bio}<p class="mu">{p.bio}</p>{/if}
			<p class="mu sm">{p.postCount} {p.postCount === 1 ? 'postup' : 'postups'}{#if since} · since {since}{/if}</p>
			{#if data.isMe}
				<button class="btn sec" onclick={() => (editOpen = true)} data-testid="edit-profile"><Icon name="edit" size={16} /> Edit profile</button>
			{:else}
				<button class="btn" class:sec={data.following} disabled={busy} onclick={follow} data-testid="follow">{data.following ? 'Following' : 'Follow'} {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</button>
			{/if}
		</div>
		{#if p.cafes.length}
			<h3 class="sh">Regular cafes</h3>
			<div class="chips">{#each p.cafes as c (c.id)}<a class="chip" href="/places/{c.id}">{c.name}</a>{/each}</div>
		{/if}
		{#if p.projects.length}
			<h3 class="sh">Projects</h3>
			<div class="grp">{#each p.projects as pr (pr.id)}<a class="lrow" href="/projects/{pr.id}"><span class="ci sm pj"><Icon name="folder" size={16} /></span><div class="lm"><b class="sm">{pr.name}</b><span class="l2">{updated(pr.updatedAt)}</span></div></a>{/each}</div>
		{/if}
		{#if p.posts.length}
			<h3 class="sh">Past postups</h3>
			<div class="grp">{#each p.posts.slice(0, 8) as po (po.id)}<a class="lrow" href={po.placeId ? `/places/${po.placeId}` : `/postups/${po.id}`}><span class="ci sm"><Icon name="coffee" size={16} /></span><div class="lm"><b class="sm">{po.activity}</b><span class="l2">{po.where} · {day(po.at)}</span></div></a>{/each}</div>
		{:else if data.isMe}
			<a class="btn" href="/post">Post up</a>
		{/if}
	</div>
</div>

<Sheet bind:open={moreOpen} title={first} testid="more-sheet">
	<button class="lrow wr" onclick={() => { moreOpen = false; shareOpen = true; }}><span class="ixi"><Icon name="share" size={18} /></span><span class="lm">Share</span></button>
	{#if data.signedIn}
		<a class="lrow wr dg" href="/report?type=user&id={p.id}&uid={p.id}&back={encodeURIComponent(`/u/${p.username}`)}"><span class="ixi"><Icon name="flag" size={18} /></span><span class="lm">Report</span></a>
		<button class="lrow wr dg" onclick={() => { moreOpen = false; blockOpen = true; }}><span class="ixi"><Icon name="ban" size={18} /></span><span class="lm">Block {first}</span></button>
	{/if}
	<button class="tx" onclick={() => (moreOpen = false)}>Cancel</button>
</Sheet>
<ShareSheet bind:open={shareOpen} path="/u/{p.username}" text="{first} on PostUp" />
<BlockSheet bind:open={blockOpen} userId={p.id} name={p.name} />
{#if data.isMe}
	<Sheet bind:open={editOpen} title="Edit profile" testid="edit-sheet">
		<form method="POST" action="/settings?/save" class="form" use:enhance={() => async ({ result, update }) => { if (result.type === 'success') { editOpen = false; await invalidateAll(); } else await update(); }}>
			<label for="ep-name">Name</label>
			<input id="ep-name" class="in" name="displayName" value={p.name} maxlength="50" />
			<label for="ep-bio">About you</label>
			<textarea id="ep-bio" class="in" name="bio" rows="3" maxlength="300" placeholder="What you're building, when you're usually out">{p.bio ?? ''}</textarea>
			<button class="btn">Save</button>
		</form>
		<button class="tx" onclick={() => (editOpen = false)}>Cancel</button>
	</Sheet>
{/if}
