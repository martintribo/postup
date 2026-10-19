<script lang="ts">
	/** Mockup #inbox / #activity: Chats | Activity, one Inbox screen with two tabs (two URLs). */
	let { on, unread = 0 }: { on: 'chats' | 'activity'; unread?: number } = $props();
</script>

<div class="seg lnkseg" role="tablist">
	<a href="/inbox" class:on={on === 'chats'} role="tab" aria-selected={on === 'chats'}>Chats</a>
	<a href="/activity" class:on={on === 'activity'} role="tab" aria-selected={on === 'activity'}>Activity {#if unread}<i class="bdg2" data-testid="activity-unread">{unread}</i>{/if}</a>
</div>
