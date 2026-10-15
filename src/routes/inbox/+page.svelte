<script lang="ts">
	/** Mockup #inbox. */
	let { data } = $props();
</script>

<main class="pu-page" data-testid="inbox">
	<a href="/" class="pu-back">← Back</a>
	<h1>Inbox</h1>
	{#if !data.chats.length}
		<p class="pu-muted">No chats yet. Join a postup or post your own and the group chat shows up here.</p>
	{:else}
		<ul>
			{#each data.chats as c (c.postId)}
				<li>
					<a href="/postups/{c.postId}/chat">
						<b>{c.title}</b>{#if c.unread}<span class="badge" data-testid="chat-unread">{c.unread}</span>{/if}
						<span class="pu-muted">{c.last ? c.last.body : 'No messages yet'}{c.state !== 'live' ? ' · ended' : ''}</span>
					</a>
				</li>
			{/each}
		</ul>
	{/if}
</main>

<style>
	.pu-page { max-width: 640px; margin: 0 auto; padding: 20px 16px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	h1 { font-family: var(--pu-font-display); }
	.pu-back { color: var(--pu-muted); text-decoration: none; }
	.pu-muted { color: var(--pu-muted); display: block; font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	ul { list-style: none; padding: 0; display: grid; gap: 8px; }
	li a { display: block; padding: 10px 12px; background: var(--pu-surface); border: var(--pu-border-width) solid var(--pu-border); border-radius: var(--pu-radius); color: inherit; text-decoration: none; }
	.badge { margin-left: 6px; padding: 0 6px; border-radius: 999px; background: #e53935; color: #fff; font-size: 11px; }
</style>
