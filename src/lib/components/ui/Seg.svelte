<script lang="ts">
	/** Mockup segmented control, backed by a hidden input so it posts with the form. */
	let { name, value = $bindable(), options, testid, onchange }: { name: string; value: string; options: { v: string; label: string }[]; testid?: string; onchange?: (v: string) => void } = $props();
</script>

<div class="seg" role="radiogroup" data-testid={testid}>
	{#each options as o (o.v)}
		<button type="button" class:on={value === o.v} role="radio" aria-checked={value === o.v} onclick={() => { value = o.v; onchange?.(o.v); }}>{o.label}</button>
	{/each}
</div>
<input type="hidden" {name} {value} />
