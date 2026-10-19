<script lang="ts">
	/** Mockup bottom sheet (.dim + .bs). Phone: slides up from the bottom; desktop: same sheet, centred by ui.css. */
	import type { Snippet } from 'svelte';
	let { open = $bindable(false), title = '', sub = '', testid = 'sheet', children }: { open?: boolean; title?: string; sub?: string; testid?: string; children?: Snippet } = $props();
</script>

<svelte:window onkeydown={(e) => open && e.key === 'Escape' && (open = false)} />
{#if open}
	<div class="dim" onclick={() => (open = false)} role="presentation"></div>
	<div class="bs" role="dialog" aria-modal="true" aria-label={title || undefined} data-testid={testid}>
		<span class="grab"></span>
		{#if title}<h2>{title}</h2>{/if}
		{#if sub}<p class="mu">{sub}</p>{/if}
		{@render children?.()}
	</div>
{/if}
