<script lang="ts">
	/** Dismissable first-visit line (mockup .welcome). Remembered per key in localStorage. */
	import { onMount } from 'svelte';
	import Icon from './Icon.svelte';
	let { id, icon = 'coffee', text, cls = '' }: { id: string; icon?: string; text: string; cls?: string } = $props();
	let show = $state(false);
	onMount(() => (show = localStorage.getItem(`pu.welcome.${id}`) !== '1'));
	function dismiss() {
		localStorage.setItem(`pu.welcome.${id}`, '1');
		show = false;
	}
</script>

{#if show}
	<div class="welcome {cls}"><span class="ci sm {icon === 'folder' ? 'pj' : ''}"><Icon name={icon} size={16} /></span><p>{text}</p><button class="ib" onclick={dismiss} aria-label="Dismiss"><Icon name="x" size={18} /></button></div>
{/if}
