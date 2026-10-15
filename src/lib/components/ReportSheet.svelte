<script lang="ts">
	/** Mockups #report / #reported / #ov-block. */
	let { targetType, targetId, blockUserId = null, blockName = '', onDone }: { targetType: string; targetId: string | number; blockUserId?: string | null; blockName?: string; onDone?: () => void } = $props();
	const REASONS: [string, string][] = [['spam', 'Spam'], ['harassment', 'Harassment'], ['inappropriate', 'Inappropriate'], ['fake', 'Fake or misleading'], ['unsafe', 'Made me feel unsafe'], ['other', 'Something else']];
	let reason = $state('');
	let details = $state('');
	let alsoBlock = $state(false);
	let done = $state(false);
	let err = $state('');
	async function submit(e: SubmitEvent) {
		e.preventDefault();
		err = '';
		const r = await fetch('/api/reports', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ targetType, targetId, reason, details }) });
		if (!r.ok) {
			err = (await r.json().catch(() => ({}))).error || 'Not sent';
			return;
		}
		if (alsoBlock && blockUserId) await fetch('/api/blocks', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ userId: blockUserId }) });
		done = true;
	}
</script>

<div class="pu-card" data-testid="report-sheet">
	{#if done}
		<b data-testid="reported">Thanks, we'll take a look.</b>
		<p class="m">{alsoBlock ? `You won't see ${blockName} anymore.` : 'Reports are private.'}</p>
		<button type="button" class="pu-btn" onclick={() => onDone?.()}>Done</button>
	{:else}
		<form onsubmit={submit}>
			<b>What's wrong?</b>
			{#each REASONS as [v, l] (v)}<label><input type="radio" bind:group={reason} value={v} name="reason" /> {l}</label>{/each}
			<textarea bind:value={details} maxlength="1000" placeholder="Anything else (optional)"></textarea>
			{#if blockUserId}<label><input type="checkbox" bind:checked={alsoBlock} /> Also block {blockName}</label>{/if}
			<div class="row"><button class="pu-btn pu-danger" type="submit" disabled={!reason}>Send report</button><button type="button" class="pu-btn" onclick={() => onDone?.()}>Cancel</button></div>
			{#if err}<p class="err" role="alert">{err}</p>{/if}
		</form>
	{/if}
</div>

<style>
	.pu-card { display: grid; gap: 8px; padding: 12px; background: var(--pu-surface); color: var(--pu-text); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); }
	form { display: grid; gap: 6px; }
	textarea { width: 100%; min-height: 60px; }
	.row { display: flex; gap: 8px; }
	.m { color: var(--pu-muted); margin: 0; }
	.err { color: #c62828; }
	.pu-btn { padding: 8px 12px; border-radius: 8px; border: var(--pu-border-width) solid var(--pu-border); background: var(--pu-surface); color: var(--pu-text); font-weight: 600; cursor: pointer; }
	.pu-danger { background: #c62828; color: #fff; border-color: #c62828; }
	.pu-danger:disabled { opacity: 0.5; }
</style>
