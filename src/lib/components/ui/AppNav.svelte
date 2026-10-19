<script lang="ts">
	/** Phone bottom tab bar (mockup nav.tab.t5) + desktop left rail (mockup aside.rail). CSS shows one per breakpoint. */
	import { page, navigating } from '$app/state';
	import { resolve } from '$app/paths';
	import Icon from './Icon.svelte';
	import Av from './Av.svelte';
	let { user = null, unread = 0, hideTabs = false }: { user?: { username: string; displayName?: string | null; avatarUrl?: string | null } | null; unread?: number; hideTabs?: boolean } = $props();
	// Highlight the tab being opened while it loads (mockup #loading keeps Nearby lit).
	const path = $derived(navigating.to?.url.pathname ?? page.url.pathname);
	const at = (p: string) => (p === '/' ? path === '/' : path === p || path.startsWith(p + '/'));
</script>

{#if !hideTabs}
	<nav class="tab t5" data-testid="tabbar" aria-label="Main">
		<a href={resolve('/')} class:on={at('/') || at('/places')}><Icon name="home" size={22} /><span>Home</span></a>
		<a href={resolve('/nearby')} class:on={at('/nearby')}><Icon name="list" size={22} /><span>Nearby</span></a>
		<a href={resolve('/post')} class="tp"><Icon name="plus" size={22} /><span>Post up</span></a>
		<a href={resolve('/projects')} class:on={at('/projects')}><Icon name="folder" size={22} /><span>Projects</span></a>
		<a href={resolve('/inbox')} class:on={at('/inbox')}>{#if unread}<i class="bdg"></i>{/if}<Icon name="chat" size={22} /><span>Inbox</span></a>
	</nav>
{/if}

<aside class="rail" data-testid="rail" aria-label="Main">
	<a class="rlogo" href={resolve('/')} aria-label="PostUp home"><Icon name="coffee" size={22} /></a>
	<a href={resolve('/')} class:on={at('/') || at('/places')}><Icon name="home" size={22} /><span>Home</span></a>
	<a href={resolve('/nearby')} class:on={at('/nearby')}><Icon name="list" size={22} /><span>Nearby</span></a>
	<a href={resolve('/projects')} class:on={at('/projects')}><Icon name="folder" size={22} /><span>Projects</span></a>
	<a href={resolve('/inbox')} class:on={at('/inbox')}><Icon name="chat" size={22} /><span>Inbox</span></a>
	<a class="rpost" href={resolve('/post')}><Icon name="plus" size={22} /><span>Post up</span></a>
	<span class="rsp"></span>
	<a href={user ? resolve('/u/[username]', { username: user.username }) : resolve('/login')} class="rme" aria-label="Profile">
		{#if user}<Av name={user.displayName || user.username} src={user.avatarUrl} size={36} />{:else}<Icon name="users" size={22} /><span>Sign in</span>{/if}
	</a>
</aside>
