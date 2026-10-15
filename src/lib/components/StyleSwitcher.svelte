<script lang="ts">
	// Dev-only floating control to compare the four styles on real pages.
	import { THEMES, type Theme } from '$lib/config';
	import { saveTheme } from '$lib/theme';

	let { current }: { current: Theme } = $props();
	let open = $state(false);
</script>

<div class="pu-switcher" data-testid="style-switcher">
	{#if open}
		<div class="pu-switcher-menu" role="group" aria-label="Style">
			{#each THEMES as t (t)}
				<button type="button" class:on={t === current} aria-pressed={t === current} onclick={() => saveTheme(t)}>{t}</button>
			{/each}
			<button type="button" class="reset" onclick={() => saveTheme(null)}>reset</button>
		</div>
	{/if}
	<button type="button" class="pu-switcher-toggle" aria-expanded={open} onclick={() => (open = !open)} title="Style (dev only)">
		<span class="material-symbols-outlined" aria-hidden="true">palette</span>
		<span>{current}</span>
	</button>
</div>

<style>
	.pu-switcher {
		position: fixed;
		left: 12px;
		bottom: calc(12px + var(--pu-tabbar, 0px));
		z-index: 100000;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 6px;
		font: 600 12px/1 var(--pu-font);
	}
	.pu-switcher-toggle,
	.pu-switcher-menu {
		background: var(--pu-surface);
		color: var(--pu-text);
		border: var(--pu-border-width) solid var(--pu-border);
		border-radius: 999px;
		box-shadow: var(--pu-shadow);
	}
	.pu-switcher-toggle {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 6px 10px 6px 8px;
		text-transform: capitalize;
	}
	.pu-switcher-toggle .material-symbols-outlined {
		font-size: 18px;
	}
	.pu-switcher-menu {
		display: flex;
		gap: 2px;
		padding: 3px;
	}
	.pu-switcher-menu button {
		padding: 6px 10px;
		border-radius: 999px;
		text-transform: capitalize;
	}
	.pu-switcher-menu button.on {
		background: var(--pu-accent);
		color: var(--pu-accent-text);
	}
	.pu-switcher-menu .reset {
		color: var(--pu-muted);
	}
</style>
