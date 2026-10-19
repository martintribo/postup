<script lang="ts">
	/** Mockup #ov-block. */
	import Sheet from './Sheet.svelte';
	let { open = $bindable(false), userId, name, onBlocked }: { open?: boolean; userId: string | null; name: string; onBlocked?: () => void } = $props();
	const first = $derived(name.split(' ')[0]);
	let busy = $state(false);
	async function block() {
		if (!userId) return;
		busy = true;
		await fetch('/api/blocks', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ userId }) });
		busy = false;
		open = false;
		if (onBlocked) onBlocked();
		else location.href = '/';
	}
</script>

<Sheet bind:open title="Block {first}?" sub="You won't see each other's postups or messages. {first} won't be told." testid="block-sheet">
	<button class="btn danger" disabled={busy} onclick={block}>Block</button>
	<button class="tx" onclick={() => (open = false)}>Cancel</button>
</Sheet>
