<script lang="ts">
	import { enhance } from '$app/forms';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import PhotoPick from '$lib/components/ui/PhotoPick.svelte';
	let { data, form } = $props();
	let busy = $state(false);
</script>

<form class="formscr scr-project-update" method="POST" enctype="multipart/form-data" use:enhance={() => { busy = true; return async ({ update }) => { await update(); busy = false; }; }} data-testid="project-update">
	<TopBar title="Update" href="/projects/{data.project.id}" />
	<div class="pad form">
		<label for="ut">Title</label>
		<input id="ut" class="in" name="title" maxlength="120" placeholder="Corneria II playable" value={form?.title ?? ''} />
		<label for="un">Notes</label>
		<textarea id="un" class="in" name="notes" rows="4" placeholder="What changed? What's next?">{form?.notes ?? ''}</textarea>
		<PhotoPick name="image" label="Add image" />
		{#if form?.message}<p class="err" role="alert">{form.message}</p>{/if}
	</div>
	<div class="cta"><button class="btn" disabled={busy}>{busy ? 'Posting…' : 'Post update'}</button></div>
</form>
