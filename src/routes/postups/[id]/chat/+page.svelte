<script lang="ts">
	/** Mockup #chat: header → postup, members strip, "Only people in this postup can see this chat.",
	 *  per-message ⋯ (#ov-msg: Copy, Report message, Block sender). Polls every 3s. Desktop: full page. */
	import { onMount, tick } from 'svelte';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import Sheet from '$lib/components/sheets/Sheet.svelte';
	import BlockSheet from '$lib/components/sheets/BlockSheet.svelte';
	import ShareSheet from '$lib/components/sheets/ShareSheet.svelte';
	import { gate } from '$lib/gate';
	import { clock } from '$lib/time';
	let { data } = $props();
	type Msg = { id: number; userId: string; name: string; avatarUrl: string | null; body: string; createdAt: string };
	// svelte-ignore state_referenced_locally
	let msgs = $state<Msg[]>(data.signedIn ? [...data.messages] : []);
	// svelte-ignore state_referenced_locally
	let canWrite = $state(data.signedIn ? data.canWrite : false);
	// svelte-ignore state_referenced_locally
	let members = $state(data.signedIn ? data.members : []);
	let text = $state('');
	let err = $state('');
	let picked = $state<Msg | null>(null);
	let msgOpen = $state(false);
	let blockOpen = $state(false);
	let copied = $state(false);
	let moreOpen = $state(false);
	let shareOpen = $state(false);
	const lastId = () => msgs.at(-1)?.id ?? 0;
	const p = $derived(data.signedIn ? data.postup : null);
	const title = $derived(!p ? 'Chat' : p.userId === (data.signedIn ? data.me : '') ? 'Your postup' : `${p.who.split(' ')[0]}'s postup`);

	async function poll() {
		const r = await fetch(`/api/postups/${data.postId}/messages?after=${lastId()}`);
		if (!r.ok) return;
		const d = await r.json();
		canWrite = d.canWrite;
		members = d.members ?? members;
		if (d.messages.length) {
			msgs = [...msgs, ...d.messages.filter((m: Msg) => !msgs.some((x) => x.id === m.id))];
			await tick();
			scrollTo({ top: document.body.scrollHeight });
		}
	}
	async function send(e: SubmitEvent) {
		e.preventDefault();
		err = '';
		const body = text.trim();
		if (!body) return;
		const r = await fetch(`/api/postups/${data.postId}/messages`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ body }) });
		if (!r.ok) err = (await r.json().catch(() => ({}))).error || 'Not sent';
		else text = '';
		await poll();
	}
	function options(m: Msg) {
		picked = m;
		msgOpen = true;
	}
	async function copyMsg() {
		if (picked) await navigator.clipboard?.writeText(picked.body).catch(() => {});
		msgOpen = false;
		copied = true;
		setTimeout(() => (copied = false), 1600);
	}
	onMount(() => {
		if (!data.signedIn) return gate('chat', `/postups/${data.postId}/chat`);
		scrollTo({ top: document.body.scrollHeight });
		const t = setInterval(poll, 3000);
		return () => clearInterval(t);
	});
</script>

<div class="chatscr" data-testid="chat">
	<TopBar {title} href={`/postups/${data.postId}`}>
		{#snippet right()}<button class="ib" onclick={() => (moreOpen = true)} aria-label="More" data-testid="more"><Icon name="more" size={20} /></button>{/snippet}
	</TopBar>
	{#if p}
		<a class="chhd" href="/postups/{p.id}">
			<span class="stk">{#each members.slice(0, 4) as m, i (i)}<Av name={m.name} src={m.avatarUrl} size={22} />{/each}</span>
			<span class="sm">{p.cafe} · till {clock(p.endsAt)} · {members.length} {members.length === 1 ? 'person' : 'people'}</span>
			<Icon name="chev" size={16} />
		</a>
	{/if}
	<div class="pad chat">
		<p class="xs mu ctr">Only people in this postup can see this chat.</p>
		{#each msgs as m (m.id)}
			{#if data.signedIn && m.userId === data.me}
				<div class="mg me"><p>{m.body}</p><span class="xs mu">{clock(m.createdAt)}</span></div>
			{:else}
				<div class="mg">
					<Av name={m.name} src={m.avatarUrl} size={30} />
					<div>
						<span class="xs mu"><b>{m.name.split(' ')[0]}</b> · {clock(m.createdAt)}</span>
						<div class="bub"><p>{m.body}</p><button class="ib xs2" onclick={() => options(m)} aria-label="Message options"><Icon name="more" size={16} /></button></div>
					</div>
				</div>
			{/if}
		{:else}
			{#if data.signedIn}<p class="mu sm ctr">Say hi and share where you're sitting.</p>{/if}
		{/each}
		{#if err}<p class="err" role="alert">{err}</p>{/if}
	</div>
	{#if canWrite}
		<form class="cbar" onsubmit={send}>
			<input class="in" bind:value={text} name="body" maxlength="1000" placeholder="Message" autocomplete="off" />
			<button class="btn sq" type="submit" aria-label="Send"><Icon name="send" size={18} /></button>
		</form>
	{:else if data.signedIn}
		<p class="cbar xs mu" data-testid="chat-readonly">This postup has ended. The chat stays readable until {new Date(data.readableUntil).toLocaleString('en-US', { weekday: 'short', hour: 'numeric', minute: '2-digit' })}.</p>
	{/if}
</div>

<Sheet bind:open={msgOpen} title="Message" testid="msg-sheet">
	<button class="lrow wr" onclick={copyMsg}><span class="ixi"><Icon name="copy" size={18} /></span><span class="lm">Copy</span></button>
	{#if picked}
		<a class="lrow wr dg" href="/report?type=message&id={picked.id}&name={encodeURIComponent(picked.name)}&uid={picked.userId}&back={encodeURIComponent(`/postups/${data.postId}/chat`)}"><span class="ixi"><Icon name="flag" size={18} /></span><span class="lm">Report message</span></a>
		<button class="lrow wr dg" onclick={() => { msgOpen = false; blockOpen = true; }}><span class="ixi"><Icon name="ban" size={18} /></span><span class="lm">Block sender</span></button>
	{/if}
	<button class="tx" onclick={() => (msgOpen = false)}>Cancel</button>
</Sheet>
{#if picked}<BlockSheet bind:open={blockOpen} userId={picked.userId} name={picked.name} onBlocked={() => { msgs = msgs.filter((m) => m.userId !== picked?.userId); }} />{/if}
<Sheet bind:open={moreOpen} title={p ? p.who.split(' ')[0] : 'Chat'} testid="more-sheet">
	<a class="lrow wr" href="/postups/{data.postId}"><span class="ixi"><Icon name="coffee" size={18} /></span><span class="lm">View postup</span></a>
	{#if p?.username}<a class="lrow wr" href="/u/{p.username}"><span class="ixi"><Icon name="user" size={18} /></span><span class="lm">View profile</span></a>{/if}
	<button class="lrow wr" onclick={() => { moreOpen = false; shareOpen = true; }}><span class="ixi"><Icon name="share" size={18} /></span><span class="lm">Share</span></button>
	<button class="tx" onclick={() => (moreOpen = false)}>Cancel</button>
</Sheet>
<ShareSheet bind:open={shareOpen} path="/p/{data.postId}" text={p ? `${p.who} is working at ${p.cafe}` : 'PostUp'} />
{#if copied}<div class="toast" role="status">Copied</div>{/if}
