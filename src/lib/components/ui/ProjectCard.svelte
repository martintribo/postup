<script lang="ts">
	import { resolve } from '$app/paths';
	import Icon from './Icon.svelte';
	import Av from './Av.svelte';
	type Card = { id: number; name: string; cover: string | null; owner: string | null; ownerAvatar: string | null; lastUpdate: string | null; short: string; when: string; cafe: string | null; week: number };
	let { c }: { c: Card } = $props();
	let coverOk = $state(true);
</script>

<a class="fc pc" href={resolve('/projects/[id]', { id: String(c.id) })} data-testid="project-card">
	{#if c.cover && coverOk}
		<div class="fm"><img src={c.cover} alt="" loading="lazy" onerror={() => (coverOk = false)} /></div>
	{:else}
		<div class="fm fb" style="--c:var(--brand)"><span><Icon name="folder" size={28} /></span></div>
	{/if}
	<div class="fbd">
		<b class="fw">{c.name}</b>
		{#if c.owner}<div class="fh"><Av name={c.owner} src={c.ownerAvatar} size={24} /><span class="sm">{c.owner}</span>{#if c.when}<span class="mu sm">· {c.when}</span>{/if}</div>{/if}
		<p class="sm">{c.lastUpdate || c.short}</p>
		<div class="fa">
			{#if c.cafe}<span class="mu sm"><Icon name="pin" size={13} /> {c.cafe}</span>{:else}<span></span>{/if}
			{#if c.week}<span class="pill">{c.week} this week</span>{/if}
		</div>
	</div>
</a>
