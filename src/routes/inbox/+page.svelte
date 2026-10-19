<script lang="ts">
	/** Mockup #inbox: Chats tab. Ended chats are dimmed. Root tab, so no Back. */
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import InboxTabs from '$lib/components/ui/InboxTabs.svelte';
	import { gate } from '$lib/gate';
	import { clock } from '$lib/time';
	let { data } = $props();
	const when = (iso: string) => {
		const d = new Date(iso);
		return Date.now() - d.getTime() < 20 * 3600e3 ? clock(d) : d.toLocaleDateString('en-US', { weekday: 'short' });
	};
	onMount(() => { if (!data.signedIn) gate('inbox', '/inbox'); });
</script>

<div class="acctscr scr-inbox" data-testid="inbox">
	<TopBar title="Inbox" back={false} />
	<div class="pad">
		<InboxTabs on="chats" unread={page.data.unreadInbox ?? 0} />
		{#if data.chats.length}
			<div class="grp">
				{#each data.chats as c (c.postId)}
					{@const ended = c.state !== 'live'}
					<a class="lrow" class:dimmed={ended} href={ended ? `/postups/${c.postId}` : `/postups/${c.postId}/chat`}>
						<Av name={c.who} src={c.avatarUrl} size={44} />
						<div class="lm"><b>{c.mine ? 'Your postup' : `${c.who.split(' ')[0]}'s postup`}</b><div class="l2">{#if ended}Ended · {when(c.endedAt)}{:else if c.last}{c.last.name}: {c.last.body}{:else}Say hi and share where you're sitting{/if}</div></div>
						{#if c.unread}<i class="bdg2" data-testid="chat-unread">{c.unread}</i>{:else}<span class="xs mu">{when(c.last?.at ?? c.endedAt)}</span>{/if}
					</a>
				{/each}
			</div>
		{:else if data.signedIn}
			<div class="estate"><h2>Your chats live here</h2><p class="mu">Join a postup or post up yourself, and its group chat shows up here.</p><a class="btn" href="/nearby">See who's nearby</a></div>
		{/if}
	</div>
</div>
