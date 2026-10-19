<script lang="ts">
	/** Mockup #settings: Notifications toggles; Account: Blocked people, Sign out, Delete account (#ov-delacct). */
	import { onMount } from 'svelte';
	import { enhance } from '$app/forms';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Sheet from '$lib/components/sheets/Sheet.svelte';
	import { gate } from '$lib/gate';
	let { data } = $props();
	const TOGGLES: [keyof typeof data.prefs, string][] = [['requests', 'Join requests'], ['joins', 'Someone joins your postup'], ['messages', 'Messages'], ['follows', 'People you follow post up']];
	let delOpen = $state(false);
	let blockedOpen = $state(false);
	let prefsForm = $state<HTMLFormElement>();
	onMount(() => { if (!data.signedIn) gate('settings', '/settings'); });
</script>

<div class="acctscr scr-settings" data-testid="settings">
	<TopBar title="Settings" href={data.signedIn ? '/me' : '/'} />
	<div class="pad">
		<h3 class="sh">Notifications</h3>
		<form method="POST" action="?/prefs" bind:this={prefsForm} use:enhance={() => async ({ update }) => update({ reset: false })} class="grp" data-testid="prefs">
			{#each TOGGLES as [k, label] (k)}
				<label class="lrow tgr"><span class="lm sm">{label}</span><input type="checkbox" class="tg" name={k} checked={data.prefs[k]} disabled={!data.signedIn} onchange={() => prefsForm?.requestSubmit()} /></label>
			{/each}
		</form>
		<h3 class="sh">Account</h3>
		<div class="grp">
			<button class="lrow wr" onclick={() => data.signedIn && (blockedOpen = true)} data-testid="blocked"><span class="lm sm">Blocked people</span><span class="mu sm">{data.blocked.length}</span></button>
			{#if data.signedIn}
				<form method="POST" action="?/signout"><button class="lrow wr"><span class="lm sm">Sign out</span></button></form>
				<button class="lrow wr dg" onclick={() => (delOpen = true)}><span class="lm sm">Delete account</span></button>
			{/if}
		</div>
	</div>
</div>

<Sheet bind:open={blockedOpen} title="Blocked people" sub={data.blocked.length ? "They can't see your postups or ask to join, and you won't see theirs." : 'Block anyone from the ⋯ menu on their postup or profile.'} testid="blocked-sheet">
	{#each data.blocked as b (b.id)}
		<form method="POST" action="?/unblock" use:enhance class="lrow wr"><span class="lm sm">{b.name || b.username}</span><input type="hidden" name="userId" value={b.id} /><button class="pill">Unblock</button></form>
	{/each}
	<button class="tx" onclick={() => (blockedOpen = false)}>Done</button>
</Sheet>
<Sheet bind:open={delOpen} title="Delete your account?" sub="Your profile, postups and projects will be removed. This can't be undone." testid="delete-sheet">
	<form method="POST" action="?/delete" data-testid="delete-form"><input type="hidden" name="confirm" value="DELETE" /><button class="btn danger" style="width:100%">Delete account</button></form>
	<button class="tx" onclick={() => (delOpen = false)}>Cancel</button>
</Sheet>
