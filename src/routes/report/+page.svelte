<script lang="ts">
	/** Mockup #report (reason + optional details) → #reported ("Thanks for telling us", Block too, Done). */
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import BlockSheet from '$lib/components/sheets/BlockSheet.svelte';
	import { gate } from '$lib/gate';
	let { data } = $props();
	const REASONS: [string, string][] = [['spam', 'Spam or fake'], ['harassment', 'Harassment'], ['inappropriate', 'Inappropriate photo'], ['not_public', 'Not at a public place'], ['other', 'Something else']];
	let reason = $state('');
	let details = $state('');
	let done = $state(false);
	let busy = $state(false);
	let err = $state('');
	let blockOpen = $state(false);
	const first = $derived(data.target.name?.split(' ')[0] ?? '');
	async function send(e: SubmitEvent) {
		e.preventDefault();
		if (!data.signedIn) return gate('report', page.url.pathname + page.url.search);
		busy = true;
		err = '';
		const r = await fetch('/api/reports', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ targetType: data.target.type, targetId: data.target.id, reason, details }) });
		busy = false;
		if (!r.ok) { err = (await r.json().catch(() => ({}))).error || 'Not sent'; return; }
		done = true;
	}
	onMount(() => { if (!data.signedIn) gate('report', page.url.pathname + page.url.search); });
</script>

{#if done}
	<div class="acctscr" data-testid="reported">
		<TopBar back={false}>{#snippet right()}<a class="ib" href={data.back} aria-label="Close"><Icon name="x" size={22} /></a>{/snippet}</TopBar>
		<div class="pad done">
			<div class="okc"><Icon name="flag" size={30} /></div>
			<h1>Thanks for telling us</h1>
			<p class="mu">We'll review it. They won't know you reported them.</p>
			{#if data.target.uid && first}<button class="btn sec" onclick={() => (blockOpen = true)}><Icon name="ban" size={18} /> Block {first} too</button>{/if}
			<a class="btn" href={data.back}>Done</a>
		</div>
	</div>
	{#if data.target.uid}<BlockSheet bind:open={blockOpen} userId={data.target.uid} name={data.target.name ?? ''} />{/if}
{:else}
	<form class="acctscr fullform scr-report" onsubmit={send} data-testid="report-form">
		<TopBar title="Report" href={data.back} />
		<div class="pad form">
			<h2>What's wrong?</h2>
			<div class="grp" role="radiogroup">
				{#each REASONS as [v, label] (v)}
					<label class="lrow tgr"><span class="lm sm">{label}</span><input type="radio" name="reason" value={v} class="rd" bind:group={reason} /></label>
				{/each}
			</div>
			<label for="rd-details">Anything else? <span class="mu">optional</span></label>
			<textarea id="rd-details" class="in" rows="3" name="details" maxlength="1000" placeholder="Add details" bind:value={details}></textarea>
			{#if err}<p class="err" role="alert">{err}</p>{/if}
		</div>
		<div class="cta"><button class="btn" disabled={busy || !reason}>Send report {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</button></div>
	</form>
{/if}
