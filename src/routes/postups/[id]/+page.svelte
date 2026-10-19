<script lang="ts">
	/** One postup. Owner: #live / #posted (?posted=1); edit is /post?edit=<id> (#post-edit).
	 *  Others: #postup, #postup-ask + #ask sheet, #requested, #joined, #postup-full, #postup-ended, #postup-cancelled.
	 *  Signed out: Join / Ask open the sign-in sheet (#join-signin, #ask-signin) and pick up after sign-in. */
	import { invalidateAll, goto, replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import Seg from '$lib/components/ui/Seg.svelte';
	import MapPanel from '$lib/components/ui/MapPanel.svelte';
	import ReportSheet from '$lib/components/ReportSheet.svelte';
	import PhotoPick from '$lib/components/ui/PhotoPick.svelte';
	import { enhance } from '$app/forms';
	import { askSignIn } from '$lib/signin.svelte';
	import { shareLink } from '$lib/share';
	import { clock } from '$lib/time';
	let { data } = $props();
	const p = $derived(data.postup);
	const who = $derived(p.displayName || p.name);
	const first = $derived(who.split(' ')[0]);
	const cafe = $derived(p.placeName || p.location);
	const until = $derived(clock(p.endsAt));
	let now = $state(Date.now());
	let sheet = $state<'' | 'ask' | 'more' | 'dirs' | 'end' | 'leave' | 'block' | 'report' | 'share'>('');
	let reason = $state('');
	let err = $state('');
	let busy = $state(false);
	let copied = $state(false);
	let joinMode = $state<string>('open');
	$effect(() => { joinMode = p.joinMode; });
	const posted = $derived(page.url.searchParams.get('posted') === '1');
	const peek = $derived(page.url.searchParams.get('view') === '1');
	const shareUrl = $derived(`${page.url.origin}/p/${p.id}`);

	const view = $derived.by(() => {
		if (p.state === 'ended') return 'ended';
		if (p.state === 'cancelled') return 'cancelled';
		if (data.isOwner) return posted ? 'posted' : 'live';
		const st = data.myRequest?.status;
		if (st === 'approved' && !peek) return 'joined';
		if (st === 'pending' && !peek) return 'requested';
		if (data.full && !st) return 'full';
		return 'postup';
	});

	// Ring: share of the postup left, and h:mm left.
	const total = $derived(new Date(p.endsAt).getTime() - new Date(p.startTime).getTime());
	const leftMs = $derived(Math.max(0, new Date(p.endsAt).getTime() - now));
	const leftMin = $derived(Math.round(leftMs / 60000));
	const ring = $derived(total > 0 ? Math.min(1, leftMs / total) : 0);
	const leftText = $derived(`${Math.floor(leftMin / 60)}:${String(leftMin % 60).padStart(2, '0')}`);
	const dist = $derived(data.miles == null ? null : data.miles < 0.1 ? 'Here' : `${data.miles < 10 ? data.miles.toFixed(1) : Math.round(data.miles)} mi · ${Math.max(1, Math.round(data.miles * 20))} min walk`);
	const ago = (iso: string) => { const m = Math.round((now - new Date(iso).getTime()) / 60000); return m < 1 ? 'just now' : m < 60 ? `${m} min ago` : `${Math.round(m / 60)}h ago`; };
	const joinLine = $derived.by(() => {
		const j = data.joiners;
		const names = j.length === 0 ? '' : j.length === 1 ? `${j[0].name.split(' ')[0]} is joining` : `${j[0].name.split(' ')[0]} and ${j.length - 1} more are joining`;
		const mode = p.joinMode === 'ask' ? `${first} approves who joins` : 'Anyone can join';
		return names ? `${names} · ${mode}` : mode;
	});
	const apple = $derived(`https://maps.apple.com/?q=${encodeURIComponent(cafe)}${p.latitude != null ? `&ll=${p.latitude},${p.longitude}` : ''}`);
	const google = $derived(p.latitude != null ? `https://www.google.com/maps/dir/?api=1&destination=${p.latitude},${p.longitude}` : `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(cafe)}`);

	async function call(url: string, method: string, body?: object) {
		err = '';
		busy = true;
		const r = await fetch(url, { method, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
		busy = false;
		if (!r.ok) { err = (await r.json().catch(() => ({}))).error || 'Something went wrong'; return false; }
		sheet = '';
		await invalidateAll();
		return true;
	}
	const act = (body: object) => call(`/api/postups/${p.id}`, 'PATCH', body);
	const join = () => call(`/api/postups/${p.id}/join`, 'POST', { reason });
	const leave = async () => { if (await call(`/api/postups/${p.id}/join`, 'DELETE')) goto(`/postups/${p.id}`, { replaceState: true, invalidateAll: true }); };
	const decide = (rid: number, action: string) => call(`/api/postups/${p.id}/requests/${rid}`, 'PATCH', { action });

	function onJoin() {
		if (!data.signedIn) {
			const ask = p.joinMode === 'ask';
			askSignIn({ title: ask ? `Ask ${first}` : `Join ${first}`, sub: ask ? `Sign in so ${first} knows who's asking.` : `Sign in so ${first} knows who's coming.`, next: `/postups/${p.id}?${ask ? 'ask' : 'join'}=1` });
			return;
		}
		if (p.joinMode === 'ask') sheet = 'ask';
		else join();
	}
	async function follow() {
		if (!data.signedIn) { askSignIn({ title: `Follow ${first}`, sub: `Sign in to see when ${first} posts up next.`, next: `/postups/${p.id}` }); return; }
		await call('/api/follows', data.following ? 'DELETE' : 'POST', { targetType: 'user', targetId: p.userId });
	}
	async function block() {
		await fetch('/api/blocks', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ userId: p.userId }) });
		location.href = '/';
	}
	async function share() {
		const r = await shareLink(`/p/${p.id}`, `${who} is working at ${cafe} till ${until}`);
		if (r === 'copied') { copied = true; setTimeout(() => (copied = false), 2000); }
	}
	async function copy() {
		await navigator.clipboard?.writeText(shareUrl).catch(() => {});
		copied = true;
		setTimeout(() => (copied = false), 2000);
	}
	async function setMode(v: string) {
		if (v !== p.joinMode) await act({ action: 'edit', joinMode: v });
	}

	onMount(() => {
		const t = setInterval(() => (now = Date.now()), 30000);
		// Back from the sign-in sheet: carry on with what they tapped.
		const u = page.url;
		if (data.signedIn && !data.isOwner && !data.myRequest && p.state === 'live' && !data.full) {
			if (u.searchParams.get('join') === '1' && p.joinMode === 'open') join();
			if (u.searchParams.get('ask') === '1' || (u.searchParams.get('join') === '1' && p.joinMode === 'ask')) sheet = 'ask';
		}
		if (u.searchParams.has('join') || u.searchParams.has('ask')) { const c = new URL(u); c.searchParams.delete('join'); c.searchParams.delete('ask'); replaceState(c, {}); }
		return () => clearInterval(t);
	});
</script>

<svelte:window onkeydown={(e) => e.key === 'Escape' && (sheet = '')} />

{#snippet whoRow(dim = false)}
	<a class="who lk2" class:dimmed={dim} href={p.username ? `/u/${p.username}` : undefined}>
		<Av name={who} src={p.avatarUrl} size={64} />
		<div><h1>{first}</h1>{#if dim}<p class="mu">{cafe}</p>{:else}<p class="ok"><span class="dot"></span> Live · till {until}</p>{/if}</div>
	</a>
{/snippet}

{#snippet moreBtns(withShare = true)}
	{#if withShare && data.shareEnabled}<button class="ib" onclick={share} aria-label="Share"><Icon name="share" size={20} /></button>{/if}
	{#if !data.isOwner}<button class="ib" onclick={() => (sheet = 'more')} aria-label="More" data-testid="more"><Icon name="more" size={20} /></button>{/if}
{/snippet}

{#if view === 'posted'}
	<main class="fullscr" data-testid="postup-page" data-state={p.state}>
		<TopBar back={false}>{#snippet right()}<a class="ib" href="/" aria-label="Close"><Icon name="x" size={22} /></a>{/snippet}</TopBar>
		<div class="pad done" data-testid="posted">
			<div class="okc"><Icon name="check" size={30} /></div>
			<h1>You're posted up</h1>
			<p class="mu">{cafe} · till {until}{#if p.projectName}<br /><a class="tag" href="/projects/{p.projectId}">{p.projectName}</a>{/if}</p>
			{#if data.shareEnabled}
				<div class="link"><span>{shareUrl.replace(/^https?:\/\//, '')}</span><button class="pill" onclick={copy}><Icon name="copy" size={14} /> {copied ? 'Copied' : 'Copy'}</button></div>
				<button class="btn" onclick={share} data-testid="share"><Icon name="share" size={18} /> Invite friends</button>
			{/if}
			{#if p.photoUrl}
				<img class="spotph" src={p.photoUrl} alt="Your spot" />
			{:else}
				<form method="POST" action="?/photo" enctype="multipart/form-data" use:enhance onchange={(e) => (e.currentTarget as HTMLFormElement).requestSubmit()} data-testid="spot-photo">
					<PhotoPick name="photo" label="Add a photo of your spot" />
				</form>
			{/if}
			<div class="lnks"><a class="lnk" href="/postups/{p.id}" data-testid="manage">Manage postup</a><a class="lnk" href="/">Map</a>{#if p.placeId}<a class="lnk" href="/places/{p.placeId}">Cafe</a>{/if}{#if p.projectId}<a class="lnk" href="/projects/{p.projectId}">Project</a>{/if}</div>
		</div>
	</main>
{:else if view === 'requested'}
	<main class="fullscr" data-testid="postup-page" data-state={p.state}>
		<TopBar back={false}>{#snippet right()}<a class="ib" href="/" aria-label="Close"><Icon name="x" size={22} /></a>{/snippet}</TopBar>
		<div class="pad done" data-testid="join-box">
			<div class="okc"><Icon name="nav" size={30} /></div>
			<h1 data-testid="requested">Request sent</h1>
			<p class="mu">{first} gets an alert and can say yes or no.<br />We'll let you know.</p>
			<a class="btn" href="/nearby">See who else is nearby</a>
			<div class="lnks"><a class="lnk" href="/postups/{p.id}?view=1">View postup</a><button class="lnk dg" onclick={leave}>Cancel request</button></div>
			{#if err}<p class="err" role="alert">{err}</p>{/if}
		</div>
	</main>
{:else}
<MapPanel latitude={data.center.latitude} longitude={data.center.longitude} showPlaces={!data.hideCafe} cls="scr-postup">
	<div class="scrin" data-testid="postup-page" data-state={p.state}>
	{#if view === 'live'}
		<TopBar title="You're live">{#snippet right()}{#if data.shareEnabled}<button class="ib" onclick={share} aria-label="Share" data-testid="share"><Icon name="share" size={20} /></button>{/if}{/snippet}</TopBar>
		<div class="pad" data-testid="you-are-live">
			<div class="card livec">
				<div class="ring" style="--p:{ring.toFixed(2)}"><b data-testid="ring-left">{leftText}</b><span class="xs mu">left</span></div>
				<div class="lm"><b>{#if p.placeId}<a href="/places/{p.placeId}">{cafe}</a>{:else}{cafe}{/if}</b><span class="mu sm" data-testid="time-left">Till {until}</span>{#if p.projectName}<a class="tag" href="/projects/{p.projectId}">{p.projectName}</a>{/if}</div>
			</div>
			<div class="row2">
				<button class="btn sec" disabled={busy} onclick={() => act({ action: 'extend', minutes: 30 })}><Icon name="clock" size={16} /> +30 min</button>
				<a class="btn sec" href="/post?edit={p.id}"><Icon name="edit" size={16} /> Edit</a>
			</div>
			<label class="lab" for="jm">Who can join</label>
			<Seg name="jm" bind:value={joinMode} onchange={setMode} options={[{ v: 'open', label: 'Anyone can join' }, { v: 'ask', label: 'Ask to join' }]} />
			{#if data.requests.length}
				<div class="sp-h"><h2>Requests</h2><span class="mu sm">{data.requests.length}</span></div>
				<div data-testid="requests">
				{#each data.requests as r (r.id)}
					<div class="card req">
						<div class="fh"><Av name={r.name} src={r.avatarUrl} size={36} /><b>{r.name.split(' ')[0]}</b><span class="mu sm">· {ago(r.createdAt)}</span></div>
						{#if r.reason}<p>"{r.reason}"</p>{/if}
						<div class="row2"><button class="btn sec" onclick={() => decide(r.id, 'decline')}>Decline</button><button class="btn" onclick={() => decide(r.id, 'approve')}>Approve</button></div>
					</div>
				{/each}
				</div>
			{/if}
			{#if data.joiners.length}
				<div class="sp-h"><h2>Joined</h2><span class="mu sm">{data.joiners.length}{p.capacity ? ` of ${p.capacity}` : ''}</span></div>
				{#each data.joiners as j (j.id)}
					<div class="lrow card"><Av name={j.name} src={j.avatarUrl} size={40} /><div class="lm"><b>{j.name.split(' ')[0]}</b><div class="l2">On the way · {ago(j.at)}</div></div><button class="tx sm" onclick={() => decide(j.id, 'remove')} aria-label="Remove {j.name}"><Icon name="x" size={16} /></button></div>
				{/each}
			{/if}
			{#if data.chatEnabled}<a class="btn sec" href="/postups/{p.id}/chat" data-testid="open-chat"><Icon name="chat" size={18} /> Group chat</a>{/if}
			<button class="tx dg" onclick={() => (sheet = 'end')}>End postup</button>
			{#if err}<p class="err" role="alert">{err}</p>{/if}
		</div>
	{:else if view === 'joined'}
		<TopBar back={false}>{#snippet right()}<a class="ib" href="/" aria-label="Close"><Icon name="x" size={22} /></a>{/snippet}</TopBar>
		<div class="pad done" data-testid="join-box">
			<div class="pair"><Av name={page.data.user?.displayName || page.data.user?.username || 'You'} src={page.data.user?.avatarUrl} size={56} /><Av name={who} src={p.avatarUrl} size={56} /></div>
			<h1 data-testid="joined">You're joining {first}</h1>
			<p class="mu">{#if p.placeId}<a class="cl" href="/places/{p.placeId}">{cafe}</a>{:else}{cafe}{/if} · till {until}</p>
			{#if data.chatEnabled}<a class="btn sec" href="/postups/{p.id}/chat" data-testid="open-chat"><Icon name="chat" size={18} /> Group chat</a>{/if}
			<button class="btn" onclick={() => (sheet = 'dirs')} data-testid="directions"><Icon name="nav" size={18} /> Directions</button>
			<p class="mu sm">{first}'s been told you're coming.</p>
			<div class="lnks"><a class="lnk" href="/">Back to map</a>{#if p.placeId}<a class="lnk" href="/places/{p.placeId}">Cafe</a>{/if}{#if p.projectId}<a class="lnk" href="/projects/{p.projectId}">Project</a>{/if}<button class="lnk dg" onclick={() => (sheet = 'leave')}>Leave</button></div>
			{#if err}<p class="err" role="alert">{err}</p>{/if}
		</div>
	{:else if view === 'postup'}
		<TopBar title="Postup">{#snippet right()}{@render moreBtns()}{/snippet}</TopBar>
		<div class="pad">
			{@render whoRow()}
			<a class="card" href={p.projectId ? `/projects/${p.projectId}` : undefined}>
				{#if p.projectName}<div class="ch"><span class="tag">{p.projectName}</span><span class="chv"><Icon name="chev" size={18} /></span></div>{/if}
				<p>{p.goals || p.activity}</p>
			</a>
			<a class="lrow card" href={p.placeId ? `/places/${p.placeId}` : undefined}>
				<span class="ci"><Icon name="coffee" size={20} /></span>
				<div class="lm"><b>{cafe}</b>{#if dist}<div class="l2">{dist}</div>{:else if data.hideCafe}<div class="l2">You'll see the cafe once {first} says yes</div>{/if}</div>
				{#if p.placeId}<span class="chv"><Icon name="chev" size={18} /></span>{/if}
			</a>
			<p class="mu sm" data-testid="join-explainer">
				{#if data.joiners.length}<span class="stk">{#each data.joiners.slice(0, 3) as j (j.id)}<Av name={j.name} src={j.avatarUrl} size={22} />{/each}</span>{:else if p.joinMode === 'ask'}<Icon name="lock" size={14} />{/if}
				{joinLine}
			</p>
			{#if data.myRequest?.status === 'declined'}<p class="mu sm">{first} isn't taking more people this time.</p>{/if}
			{#if err}<p class="err" role="alert">{err}</p>{/if}
		</div>
		{#if data.joinEnabled}
			<div class="cta" data-testid="join-box">
				{#if data.myRequest?.status === 'pending'}
					<button class="btn sec" onclick={leave}>Cancel request</button>
				{:else if data.myRequest?.status === 'approved'}
					<a class="btn" href="/postups/{p.id}">You're joining</a>
				{:else if data.myRequest?.status !== 'declined'}
					<button class="btn" disabled={busy} onclick={onJoin} data-testid="join">{p.joinMode === 'ask' ? 'Ask to join' : 'Join'} {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</button>
				{/if}
			</div>
		{/if}
	{:else}
		<TopBar title="Postup">{#snippet right()}{@render moreBtns(false)}{/snippet}</TopBar>
		<div class="pad">
			{@render whoRow(true)}
			<div class="estate" data-testid={view === 'full' ? 'full' : 'postup-over'}>
				<span class="ci"><Icon name={view === 'full' ? 'users' : view === 'ended' ? 'clock' : 'x'} size={22} /></span>
				{#if view === 'ended'}<h2>This postup ended</h2><p class="mu">{first} wrapped up at {until}.</p>
				{:else if view === 'full'}<h2>This postup is full</h2><p class="mu">{first} isn't taking more people right now.</p>
				{:else}<h2>{first} cancelled this postup</h2><p class="mu">Plans change. Others are working nearby.</p>{/if}
				<a class="btn" href="/nearby">See what's nearby</a>
				{#if !data.isOwner && p.userId}<button class="lnk sm" onclick={follow} data-testid="follow">{data.following ? `Following ${first}` : `Follow ${first} for next time`}</button>{/if}
			</div>
		</div>
	{/if}
	</div>
</MapPanel>
{/if}

{#if sheet}
	<div class="dim" onclick={() => (sheet = '')} role="presentation"></div>
	<div class="bs" role="dialog" aria-modal="true" data-testid="sheet-{sheet}">
		<span class="grab"></span>
		{#if sheet === 'ask'}
			<h2>Ask to join</h2>
			<p class="mu">Tell {first} a little about you. They'll get an alert.</p>
			<textarea class="in" rows="3" name="reason" maxlength="280" bind:value={reason} placeholder="Working on something similar, happy to share a table…"></textarea>
			<button class="btn" disabled={busy || !reason.trim()} onclick={join}><Icon name="spark" size={18} /> Send request</button>
			{#if err}<p class="err" role="alert">{err}</p>{/if}
			<button class="tx" onclick={() => (sheet = '')}>Cancel</button>
		{:else if sheet === 'more'}
			<h2>{first}</h2>
			{#if p.username}<a class="lrow wr" href="/u/{p.username}"><span class="ixi"><Icon name="users" size={18} /></span><span class="lm">View profile</span></a>{/if}
			{#if data.shareEnabled}<button class="lrow wr" onclick={() => { sheet = ''; share(); }}><span class="ixi"><Icon name="share" size={18} /></span><span class="lm">Share</span></button>{/if}
			{#if data.signedIn}
				<button class="lrow wr dg" onclick={() => (sheet = 'report')}><span class="ixi"><Icon name="flag" size={18} /></span><span class="lm">Report</span></button>
				{#if p.userId}<button class="lrow wr dg" onclick={() => (sheet = 'block')}><span class="ixi"><Icon name="x" size={18} /></span><span class="lm">Block {first}</span></button>{/if}
			{/if}
			<button class="tx" onclick={() => (sheet = '')}>Cancel</button>
		{:else if sheet === 'report'}
			<ReportSheet targetType="post" targetId={p.id} blockUserId={p.userId} blockName={who} onDone={() => (sheet = '')} />
		{:else if sheet === 'block'}
			<h2>Block {first}?</h2>
			<p class="mu">You won't see each other's postups or messages. {first} won't be told.</p>
			<button class="btn danger" onclick={block}>Block</button>
			<button class="tx" onclick={() => (sheet = '')}>Cancel</button>
		{:else if sheet === 'dirs'}
			<h2>{cafe}</h2>
			{#if dist}<p class="mu">{dist}</p>{/if}
			<a class="sso" href={apple} target="_blank" rel="noopener" onclick={() => (sheet = '')}>Open in Apple Maps</a>
			<a class="sso" href={google} target="_blank" rel="noopener" onclick={() => (sheet = '')}>Open in Google Maps</a>
			<button class="tx" onclick={() => (sheet = '')}>Cancel</button>
		{:else if sheet === 'end'}
			<h2>End your postup?</h2>
			<p class="mu">{data.joiners.length ? `${data.joiners.map((j) => j.name.split(' ')[0]).join(', ')} and anyone waiting will get an alert.` : 'Anyone waiting will get an alert.'}</p>
			<button class="btn danger" disabled={busy} onclick={() => act({ action: 'end' })} data-testid="confirm-end">End now</button>
			<button class="tx" onclick={() => (sheet = '')}>Keep going</button>
		{:else if sheet === 'leave'}
			<h2>Leave {first}'s postup?</h2>
			<p class="mu">{first} will get an alert.</p>
			<button class="btn danger" disabled={busy} onclick={leave}>Leave</button>
			<button class="tx" onclick={() => (sheet = '')}>Stay</button>
		{/if}
	</div>
{/if}
{#if copied}<div class="toast" role="status">Link copied</div>{/if}
