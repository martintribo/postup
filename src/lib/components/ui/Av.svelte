<script lang="ts">
	/** Round avatar: photo if there is one, else a coloured initial (colour stable per name). */
	let { name = '?', src = null, size = 36 }: { name?: string | null; src?: string | null; size?: number } = $props();
	const COLORS = ['#7c3aed', '#e11d48', '#0891b2', '#d97706', '#2563eb', '#10a364', '#db2777', '#4f46e5'];
	const n = $derived(name || '?');
	const c = $derived(COLORS[[...n].reduce((a, ch) => (a * 31 + ch.charCodeAt(0)) >>> 0, 7) % COLORS.length]);
</script>

{#if src}
	<img class="av" src={src} alt="" style="width:{size}px;height:{size}px;object-fit:cover" />
{:else}
	<span class="av" style="--c:{c};width:{size}px;height:{size}px;font-size:{Math.round(size * 0.4)}px" aria-hidden="true">{n[0].toUpperCase()}</span>
{/if}
