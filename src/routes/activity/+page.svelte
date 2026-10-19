<script lang="ts">
	/** Mockup #activity. Each row opens the related screen. */
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import TopBar from '$lib/components/ui/TopBar.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import Icon from '$lib/components/ui/Icon.svelte';
	import InboxTabs from '$lib/components/ui/InboxTabs.svelte';
	import { gate } from '$lib/gate';
	let { data } = $props();
	// Count shown on the tab is the one from before this visit marks them read.
	const unread = page.data.unreadInbox ?? 0;
	type Item = (typeof data.items)[number];
	const VERB: Record<string, [string, string]> = {
		join_request: ['asked to join your postup', 'users'],
		joined: ['joined your postup', 'check'],
		approved: ['said yes to your request', 'check'],
		declined: ["can't take more people this time", 'x'],
		removed: ['took you off their postup', 'x'],
		left: ["can't make it anymore", 'x'],
		followed: ['followed you', 'user'],
		message: ['', 'chat']
	};
	const href = (n: Item) => (n.type === 'followed' && n.actorUsername ? `/u/${n.actorUsername}` : n.type === 'message' && n.postId ? `/postups/${n.postId}/chat` : n.postId ? `/postups/${n.postId}` : '/activity');
	const ago = (iso: string) => {
		const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
		if (m < 1) return 'Just now';
		if (m < 60) return `${m} min ago`;
		if (m < 20 * 60) return `${Math.round(m / 60)}h ago`;
		if (m < 48 * 60) return 'Yesterday';
		return new Date(iso).toLocaleDateString('en-US', { weekday: 'short' });
	};
	onMount(() => {
		if (!data.signedIn) return gate('inbox', '/activity');
		fetch('/api/notifications/read', { method: 'POST' });
	});
</script>

<div class="acctscr scr-activity" data-testid="activity">
	<TopBar title="Inbox" back={false} />
	<div class="pad">
		<InboxTabs on="activity" {unread} />
		{#if data.items.length}
			<div class="grp">
				{#each data.items as n (n.id)}
					{@const v = VERB[n.type]}
					<a class="lrow" class:unread={!n.readAt} href={href(n)}>
						<Av name={n.actor || 'PostUp'} src={n.actorAvatar} size={40} />
						<div class="lm">
							<span class="sm">{#if v && n.actor && v[0]}<b>{n.actor.split(' ')[0]}</b> {v[0]}{:else}{n.body}{/if}</span>
							<span class="xs mu">{ago(n.createdAt)}</span>
						</div>
						<span class="ixi"><Icon name={v?.[1] ?? 'spark'} size={16} /></span>
					</a>
				{/each}
			</div>
		{:else if data.signedIn}
			<div class="estate"><h2>Alerts show up here</h2><p class="mu">When someone joins, asks to join or follows you, you'll see it here.</p><a class="btn" href="/post">Post up</a></div>
		{/if}
	</div>
</div>
