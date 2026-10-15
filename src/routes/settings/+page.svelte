<script lang="ts">
	/** Mockups #settings / #ov-delacct. */
	import { enhance } from '$app/forms';
	let { data, form } = $props();
	let showDelete = $state(false);
</script>

<main class="pu-page" data-testid="settings">
	<a href="/me" class="m">← Profile</a>
	<h1>Settings</h1>
	<form method="POST" action="?/save" use:enhance class="card">
		<label>Name <input name="displayName" value={data.me.displayName} maxlength="50" /></label>
		<label>Bio <textarea name="bio" maxlength="300">{data.me.bio}</textarea></label>
		<button class="btn primary">Save</button>
		{#if form?.saved}<span class="m" data-testid="saved">Saved</span>{/if}
		{#if form?.message}<span class="err" role="alert">{form.message}</span>{/if}
	</form>

	<h2>Blocked</h2>
	{#if data.blocked.length}
		{#each data.blocked as b (b.id)}
			<form method="POST" action="?/unblock" use:enhance class="row"><span>{b.name || b.username}</span><input type="hidden" name="userId" value={b.id} /><button class="btn">Unblock</button></form>
		{/each}
	{:else}<p class="m">Nobody.</p>{/if}

	<h2>Account</h2>
	<form method="POST" action="?/signout"><button class="btn">Sign out</button></form>
	{#if showDelete}
		<form method="POST" action="?/delete" class="card danger" data-testid="delete-form">
			<b>Delete your account?</b>
			<p class="m">This ends any live postup, removes your sign-ins, chats and profile, and can't be undone.</p>
			<label>Type DELETE to confirm <input name="confirm" autocomplete="off" /></label>
			<button class="btn del">Delete account</button>
		</form>
	{:else}
		<button class="btn link" onclick={() => (showDelete = true)}>Delete account…</button>
	{/if}
</main>

<style>
	.pu-page { max-width: 640px; margin: 0 auto; padding: 20px 16px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); display: grid; gap: 10px; align-content: start; }
	h1 { font-family: var(--pu-font-display); margin: 0; }
	h2 { margin: 10px 0 0; font-size: 16px; }
	.card { display: grid; gap: 8px; padding: 12px; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); }
	.danger { border-color: #c62828; }
	.row { display: flex; justify-content: space-between; align-items: center; }
	input, textarea { width: 100%; }
	.m { color: var(--pu-muted); text-decoration: none; margin: 0; }
	.err { color: #c62828; }
	.btn { padding: 8px 14px; border-radius: 10px; border: var(--pu-border-width) solid var(--pu-border); background: var(--pu-surface); color: var(--pu-text); font-weight: 600; cursor: pointer; justify-self: start; }
	.primary { background: var(--pu-accent); color: var(--pu-accent-text); }
	.del { background: #c62828; color: #fff; border-color: #c62828; }
	.link { border: 0; background: none; color: #c62828; padding: 0; }
</style>
