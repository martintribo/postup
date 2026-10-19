<script lang="ts">
	/** Mockup #ov-share: the link with Copy, then Messages / WhatsApp / Email / More (native share). */
	import Sheet from './Sheet.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	let { open = $bindable(false), path, text }: { open?: boolean; path: string; text: string } = $props();
	let copied = $state(false);
	const url = $derived(typeof location === 'undefined' ? path : new URL(path, location.origin).toString());
	const shown = $derived(url.replace(/^https?:\/\//, ''));
	const msg = $derived(`${text} ${url}`);
	async function copy() {
		await navigator.clipboard?.writeText(url).catch(() => {});
		copied = true;
		setTimeout(() => (copied = false), 2000);
	}
	async function more() {
		if (navigator.share) {
			try {
				await navigator.share({ title: 'PostUp', text, url });
				open = false;
				return;
			} catch {
				/* cancelled */
			}
		} else await copy();
	}
</script>

<Sheet bind:open title="Share" testid="share-sheet">
	<div class="link"><span>{shown}</span><button class="pill" onclick={copy} data-testid="share-copy"><Icon name="copy" size={14} /> {copied ? 'Copied' : 'Copy'}</button></div>
	<div class="shr">
		<a href="sms:?&body={encodeURIComponent(msg)}" onclick={() => (open = false)}><span class="ixi"><Icon name="chat" size={20} /></span><span class="xs">Messages</span></a>
		<a href="https://wa.me/?text={encodeURIComponent(msg)}" target="_blank" rel="noopener" onclick={() => (open = false)}><span class="ixi"><Icon name="send" size={20} /></span><span class="xs">WhatsApp</span></a>
		<a href="mailto:?subject={encodeURIComponent('PostUp')}&body={encodeURIComponent(msg)}" onclick={() => (open = false)}><span class="ixi"><Icon name="mail" size={20} /></span><span class="xs">Email</span></a>
		<button onclick={more}><span class="ixi"><Icon name="more" size={20} /></span><span class="xs">More</span></button>
	</div>
	<button class="tx" onclick={() => (open = false)}>Cancel</button>
</Sheet>
