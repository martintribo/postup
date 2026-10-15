<script lang="ts">
	/** "Continue with Apple / Google" sheet, shown at the moment someone acts (post, join, ask). */
	let {
		providers = [],
		next = '/',
		reason = 'Sign in to continue'
	}: { providers?: string[]; next?: string; reason?: string } = $props();
	const label: Record<string, string> = { apple: 'Continue with Apple', google: 'Continue with Google', mock: 'Continue (dev mock)' };
	const href = (p: string) => `/auth/${p}?next=${encodeURIComponent(next)}`;
</script>

{#if providers.length}
	<div class="pu-sheet" data-testid="signin-sheet">
		<p class="pu-sheet-reason">{reason}</p>
		{#each providers as p (p)}
			<a class="pu-btn pu-btn-{p}" href={href(p)} data-sveltekit-reload>{label[p] ?? p}</a>
		{/each}
		<p class="pu-sheet-fine">We only use your name and photo. Nothing is posted for you.</p>
	</div>
{/if}

<style>
	.pu-sheet {
		display: grid;
		gap: 10px;
		padding: 16px;
		background: var(--pu-surface);
		color: var(--pu-text);
		border: var(--pu-border-width) solid var(--pu-border);
		border-radius: var(--pu-radius);
		box-shadow: var(--pu-shadow);
		font-family: var(--pu-font);
	}
	.pu-sheet-reason { margin: 0 0 4px; font-weight: 600; }
	.pu-sheet-fine { margin: 4px 0 0; font-size: 12px; color: var(--pu-muted); }
	.pu-btn {
		display: block;
		text-align: center;
		padding: 12px;
		border-radius: calc(var(--pu-radius) - 4px);
		border: var(--pu-border-width) solid var(--pu-border);
		font-weight: 600;
		text-decoration: none;
		color: var(--pu-text);
		background: var(--pu-surface);
	}
	.pu-btn-apple { background: #000; color: #fff; border-color: #000; }
</style>
