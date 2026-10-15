<script lang="ts">
	/** Mockup #chat. Polls every 3s (client-only, works in the native shell). */
	import { onMount, tick } from 'svelte';
	let { data } = $props();
	let msgs = $state([...data.messages]);
	let text = $state('');
	let err = $state('');
	let canWrite = $state(data.canWrite);
	let list: HTMLElement;
	const lastId = () => msgs.at(-1)?.id ?? 0;

	async function poll() {
		const r = await fetch(`/api/postups/${data.postup.id}/messages?after=${lastId()}`);
		if (!r.ok) return;
		const d = await r.json();
		canWrite = d.canWrite;
		if (d.messages.length) {
			msgs = [...msgs, ...d.messages.filter((m: { id: number }) => !msgs.some((x) => x.id === m.id))];
			await tick();
			list?.scrollTo({ top: list.scrollHeight });
		}
	}
	async function send(e: SubmitEvent) {
		e.preventDefault();
		err = '';
		const body = text.trim();
		if (!body) return;
		const r = await fetch(`/api/postups/${data.postup.id}/messages`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ body }) });
		if (!r.ok) err = (await r.json().catch(() => ({}))).error || 'Not sent';
		else text = '';
		await poll();
	}
	onMount(() => {
		list?.scrollTo({ top: list.scrollHeight });
		const t = setInterval(poll, 3000);
		return () => clearInterval(t);
	});
	async function report(id: number) {
		const r = await fetch('/api/reports', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ targetType: 'message', targetId: id, reason: 'inappropriate' }) });
		err = r.ok ? 'Reported. Thanks.' : 'Could not report';
	}
	const time = (iso: string) => new Date(iso).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
</script>

<main class="pu-chat" data-testid="chat">
	<header><a href="/postups/{data.postup.id}">←</a> <b>{data.postup.activity}</b></header>
	<ol bind:this={list}>
		{#each msgs as m (m.id)}
			<li class:mine={m.userId === data.me}>
				{#if m.userId !== data.me}<span class="who">{m.name}</span>{/if}
				<span class="bubble">{m.body}</span>
				<time>{time(m.createdAt)}{#if m.userId !== data.me} · <button class="rep" onclick={() => report(m.id)}>Report</button>{/if}</time>
			</li>
		{:else}
			<li class="empty">Say hi and share where you're sitting.</li>
		{/each}
	</ol>
	{#if canWrite}
		<form onsubmit={send}>
			<input bind:value={text} name="body" maxlength="1000" placeholder="Message" autocomplete="off" />
			<button type="submit">Send</button>
		</form>
	{:else}
		<p class="closed" data-testid="chat-readonly">This postup has ended. The chat is read-only until {new Date(data.readableUntil).toLocaleString([], { weekday: 'short', hour: 'numeric', minute: '2-digit' })}.</p>
	{/if}
	{#if err}<p class="err" role="alert">{err}</p>{/if}
</main>

<style>
	.pu-chat { display: grid; grid-template-rows: auto 1fr auto auto; height: 100dvh; max-width: 720px; margin: 0 auto; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	header { padding: 12px 16px; border-bottom: var(--pu-border-width) solid var(--pu-border); display: flex; gap: 10px; }
	header a { color: inherit; text-decoration: none; }
	ol { list-style: none; margin: 0; padding: 12px 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
	li { display: grid; justify-items: start; max-width: 80%; }
	li.mine { justify-self: end; justify-items: end; margin-left: auto; }
	.who { font-size: 12px; color: var(--pu-muted); }
	.bubble { padding: 8px 12px; border-radius: 16px; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); white-space: pre-wrap; word-break: break-word; }
	li.mine .bubble { background: var(--pu-accent); color: var(--pu-accent-text); border-color: var(--pu-accent); }
	time { font-size: 11px; color: var(--pu-muted); }
	.rep { background: none; border: 0; padding: 0; color: var(--pu-muted); font-size: 11px; text-decoration: underline; cursor: pointer; }
	.empty { color: var(--pu-muted); max-width: none; }
	form { display: flex; gap: 8px; padding: 10px 16px; border-top: var(--pu-border-width) solid var(--pu-border); }
	input { flex: 1; padding: 10px; border-radius: 999px; border: var(--pu-border-width) solid var(--pu-border); background: var(--pu-surface); color: var(--pu-text); }
	button { padding: 10px 16px; border-radius: 999px; border: 0; background: var(--pu-accent); color: var(--pu-accent-text); font-weight: 700; }
	.closed, .err { padding: 10px 16px; color: var(--pu-muted); margin: 0; }
	.err { color: #c62828; }
</style>
