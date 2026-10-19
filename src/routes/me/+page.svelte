<script lang="ts">
	/** Mockup #me, signed out: an empty profile with the "Your profile" sign-in sheet over it. */
	import { onMount } from 'svelte';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import { gate } from '$lib/gate';
	onMount(() => gate('me', '/me'));
</script>

<div class="acctscr scr-me" data-testid="me-gate">
	<TopBar>{#snippet right()}<a class="ib" href="/settings" aria-label="Settings"><Icon name="settings" size={20} /></a>{/snippet}</TopBar>
	<div class="pad prof">
		<div class="phd">
			<span class="av" style="--c:var(--n300);width:88px;height:88px"><Icon name="user" size={36} /></span>
			<h1>You</h1>
			<p class="mu">Your postups, projects and regular cafes show up here.</p>
			<button class="btn" onclick={() => gate('me', '/me')}>Sign in</button>
		</div>
	</div>
</div>
