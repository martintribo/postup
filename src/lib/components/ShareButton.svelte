<script lang="ts">
	/** Mockup #ov-share: native share sheet when available, else copy link. */
	let { path, text, label = 'Share' }: { path: string; text: string; label?: string } = $props();
	let copied = $state(false);
	async function share() {
		const url = new URL(path, location.origin).toString();
		if (navigator.share) {
			try {
				await navigator.share({ title: 'PostUp', text, url });
				return;
			} catch {
				/* cancelled: fall back to copy */
			}
		}
		await navigator.clipboard?.writeText(url).catch(() => {});
		copied = true;
		setTimeout(() => (copied = false), 2000);
	}
</script>

<button type="button" class="pu-btn" onclick={share} data-testid="share">{copied ? 'Link copied' : label}</button>

<style>
	.pu-btn { padding: 10px 14px; border-radius: calc(var(--pu-radius) - 4px); border: var(--pu-border-width) solid var(--pu-border); background: var(--pu-surface); color: var(--pu-text); font-weight: 600; cursor: pointer; }
</style>
