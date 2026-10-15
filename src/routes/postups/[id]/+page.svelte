<script lang="ts">
	/** Mockups #live, #post-edit, #ov-endlive, #postup-ended, #postup-cancelled, #posted. */
	import { invalidateAll } from '$app/navigation';
	import { onMount } from 'svelte';
	let { data } = $props();
	const p = $derived(data.postup);
	let now = $state(Date.now());
	let editing = $state(false);
	let confirmEnd = $state(false);
	let err = $state('');
	let activity = $state('');
	let note = $state('');
	let joinMode = $state<'open' | 'ask'>('open');
	onMount(() => {
		const t = setInterval(() => (now = Date.now()), 30000);
		return () => clearInterval(t);
	});
	const left = $derived(Math.max(0, Math.round((new Date(p.endsAt).getTime() - now) / 60000)));
	const leftText = $derived(left >= 60 ? `${Math.floor(left / 60)}h ${left % 60}m left` : `${left}m left`);
	const until = $derived(new Date(p.endsAt).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }));
	const who = $derived(p.displayName || p.name);
	const cafe = $derived(p.placeName || p.location);

	async function act(body: object) {
		err = '';
		const r = await fetch(`/api/postups/${p.id}`, { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
		if (!r.ok) err = (await r.json().catch(() => ({}))).error || 'Something went wrong';
		editing = false;
		confirmEnd = false;
		await invalidateAll();
	}
	function startEdit() {
		activity = p.activity;
		note = p.note ?? '';
		joinMode = p.joinMode;
		editing = true;
	}
</script>

<main class="pu-page" data-testid="postup-page" data-state={p.state}>
	<a href="/" class="pu-back">← Back</a>
	{#if p.state === 'live'}
		{#if data.isOwner}<div class="pu-live-badge" data-testid="you-are-live">You're live</div>{/if}
		<h1>{who} <span class="pu-muted">at</span> {#if p.placeId}<a href="/places/{p.placeId}">{cafe}</a>{:else}{cafe}{/if}</h1>
		<p class="pu-act">{p.activity}</p>
		{#if p.note}<p class="pu-muted">{p.note}</p>{/if}
		{#if p.projectName}<p class="pu-muted">For <a href="/projects#p{p.projectId}">{p.projectName}</a></p>{/if}
		<p class="pu-time" data-testid="time-left">Here till {until} · {leftText}</p>
		<p class="pu-muted">{p.joinMode === 'ask' ? 'Ask to join' : 'Anyone can join'}{p.capacity ? ` · up to ${p.capacity}` : ''}</p>

		{#if data.isOwner}
			{#if editing}
				<form class="pu-card" onsubmit={(e) => { e.preventDefault(); act({ action: 'edit', activity, note, joinMode }); }}>
					<label>Working on <input bind:value={activity} maxlength="140" name="activity" /></label>
					<label>Note <input bind:value={note} maxlength="280" name="note" placeholder="Optional" /></label>
					<fieldset><legend>Who can join</legend>
						<label><input type="radio" bind:group={joinMode} value="open" /> Anyone</label>
						<label><input type="radio" bind:group={joinMode} value="ask" /> Ask to join</label>
					</fieldset>
					<div class="pu-row"><button class="pu-btn pu-primary" type="submit">Save</button><button class="pu-btn" type="button" onclick={() => (editing = false)}>Cancel</button></div>
				</form>
			{:else if confirmEnd}
				<div class="pu-card" data-testid="confirm-end">
					<b>End your postup now?</b>
					<p class="pu-muted">People nearby will stop seeing it.</p>
					<div class="pu-row"><button class="pu-btn pu-danger" onclick={() => act({ action: 'end' })}>End postup</button><button class="pu-btn" onclick={() => (confirmEnd = false)}>Keep going</button></div>
				</div>
			{:else}
				<div class="pu-row">
					<button class="pu-btn pu-primary" onclick={() => act({ action: 'extend', hours: 1 })}>+1 hour</button>
					<button class="pu-btn" onclick={startEdit}>Edit</button>
					<button class="pu-btn" onclick={() => (confirmEnd = true)}>End</button>
				</div>
			{/if}
		{/if}
	{:else if p.state === 'ended'}
		<h1>This postup has ended</h1>
		<p class="pu-muted">{who} was at {cafe} working on “{p.activity}”.</p>
		<a class="pu-btn pu-primary" href="/">See who's around now</a>
	{:else}
		<h1>This postup was cancelled</h1>
		<p class="pu-muted">{who} isn't at {cafe} after all.</p>
		<a class="pu-btn pu-primary" href="/">See who's around now</a>
	{/if}
	{#if err}<p class="pu-err" role="alert">{err}</p>{/if}
</main>

<style>
	.pu-page { max-width: 640px; margin: 0 auto; padding: 20px 16px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); display: grid; gap: 10px; align-content: start; }
	h1 { font-family: var(--pu-font-display); font-size: 26px; margin: 0; }
	.pu-back { color: var(--pu-muted); text-decoration: none; }
	.pu-muted { color: var(--pu-muted); margin: 0; }
	.pu-act { font-size: 18px; font-weight: 600; margin: 0; }
	.pu-time { font-weight: 700; margin: 0; }
	.pu-live-badge { justify-self: start; padding: 3px 10px; border-radius: 999px; background: var(--pu-live); color: #fff; font-weight: 700; font-size: 13px; }
	.pu-row { display: flex; gap: 8px; flex-wrap: wrap; }
	.pu-card { display: grid; gap: 8px; padding: 12px; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); box-shadow: var(--pu-shadow); }
	.pu-card input:not([type='radio']) { width: 100%; }
	.pu-btn { display: inline-block; text-align: center; padding: 10px 14px; border-radius: calc(var(--pu-radius) - 4px); border: var(--pu-border-width) solid var(--pu-border); background: var(--pu-surface); color: var(--pu-text); font-weight: 600; cursor: pointer; text-decoration: none; }
	.pu-primary { background: var(--pu-accent); color: var(--pu-accent-text); }
	.pu-danger { background: #c62828; color: #fff; border-color: #c62828; }
	.pu-err { color: #c62828; }
	a { color: inherit; }
</style>
