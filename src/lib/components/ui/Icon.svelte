<script lang="ts">
	import { ICONS } from './icons';
	let { name, size = 18, class: c = '' }: { name: string; size?: number; class?: string } = $props();
</script>

<svg class="ic {c}" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{@html ICONS[name] ?? ''}</svg>
