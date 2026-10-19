<script lang="ts">
	import { enhance } from '$app/forms';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import Seg from '$lib/components/ui/Seg.svelte';
	import PhotoPick from '$lib/components/ui/PhotoPick.svelte';
	import { askSignIn } from '$lib/signin.svelte';
	let { data, form } = $props();
	let type = $state(form?.type ?? 'game');
	let busy = $state(false);
</script>

<form class="formscr scr-project-new" method="POST" enctype="multipart/form-data" use:enhance={({ cancel }) => { if (!data.signedIn) { cancel(); askSignIn({ title: 'Almost there', sub: 'Sign in to create your project.' }); return; } busy = true; return async ({ update }) => { await update(); busy = false; }; }} data-testid="project-new">
	<TopBar title="New project" href="/projects" />
	<div class="pad form">
		<PhotoPick name="cover" variant="cover" label="Add cover" />
		<label for="pn">Name</label>
		<input id="pn" class="in" name="name" required maxlength="80" placeholder="Pixel Garden" value={form?.name ?? ''} />
		<label for="pk">Kind</label>
		<Seg name="type" bind:value={type} options={[{ v: 'software', label: 'Code' }, { v: 'game', label: 'Game' }, { v: 'art', label: 'Art' }, { v: 'other', label: 'Other' }]} />
		<label for="ps">One line</label>
		<input id="ps" class="in" name="short" maxlength="140" placeholder="A tiny pixel-art farming game" value={form?.short ?? ''} />
		{#if form?.message}<p class="err" role="alert">{form.message}</p>{/if}
	</div>
	<div class="cta"><button class="btn" disabled={busy}>{busy ? 'Creating…' : 'Create'} {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</button></div>
</form>
