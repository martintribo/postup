<script lang="ts">
	/** Image picker shown as the mockup .addph / .cover tile, with a preview once chosen. */
	import Icon from './Icon.svelte';
	let { name, label = 'Add a photo', hint = '', variant = 'addph' }: { name: string; label?: string; hint?: string; variant?: 'addph' | 'cover' } = $props();
	let preview = $state<string | null>(null);
	function pick(e: Event) {
		const f = (e.currentTarget as HTMLInputElement).files?.[0];
		preview = f ? URL.createObjectURL(f) : null;
	}
</script>

<label class="{variant} photo-pick" class:has={!!preview}>
	{#if preview}
		<img src={preview} alt="" />
	{:else}
		<Icon name={variant === 'cover' ? 'image' : 'camera'} size={variant === 'cover' ? 22 : 18} />
		<span class={variant === 'cover' ? 'sm' : ''}>{label}</span>
		{#if hint}<span class="mu xs">{hint}</span>{/if}
	{/if}
	<input type="file" {name} accept="image/*" hidden onchange={pick} />
</label>
