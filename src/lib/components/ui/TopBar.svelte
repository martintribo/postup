<script lang="ts">
	import type { Snippet } from 'svelte';
	import Icon from './Icon.svelte';
	/** Mockup .nb header: back, centred title, right slot. clear = over a hero image. */
	let { title = '', back = true, clear = false, href = null, right }: { title?: string; back?: boolean; clear?: boolean; href?: string | null; right?: Snippet } = $props();
	function goBack(e: MouseEvent) {
		if (href) return;
		e.preventDefault();
		if (history.length > 1) history.back();
		else location.href = '/';
	}
</script>

<header class="nb" class:clr={clear}>
	{#if back}
		<a class="ib" href={href ?? '/'} onclick={goBack} aria-label="Back"><Icon name="back" size={22} /></a>
	{:else}<span class="ib"></span>{/if}
	<b>{title}</b>
	<span class="nr">{@render right?.()}</span>
</header>
