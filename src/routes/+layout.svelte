<script lang="ts">
	import './layout.css';
	import '$lib/styles/tokens.css';
	import '$lib/styles/themes/cozy.css';
	import '$lib/styles/themes/night.css';
	import '$lib/styles/themes/bold.css';
	import { page, navigating } from '$app/state';
	import NearbySkeleton from '$lib/components/feed/NearbySkeleton.svelte';
	import { dev } from '$app/environment';
	import { config } from '$lib/config';
	import { resolveTheme } from '$lib/theme';
	import StyleSwitcher from '$lib/components/StyleSwitcher.svelte';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { isNative, registerPush, listenDeepLinks } from '$lib/native';
	import OfflineBanner from '$lib/components/OfflineBanner.svelte';
	import AppNav from '$lib/components/ui/AppNav.svelte';
	import SignInSheet from '$lib/components/ui/SignInSheet.svelte';
	import { askSignIn } from '$lib/signin.svelte';
	import '$lib/styles/ui.css';
	import '$lib/styles/app.css';

	let { children } = $props();

	const SITE = 'PostUp';
	const DESC = 'Post up at a cafe and see who is working nearby. Join someone, or share what you are building.';
	// ?theme=bold previews another style; the dev switcher saves one per browser.
	let bump = $state(0);
	const theme = $derived.by(() => {
		bump;
		return resolveTheme(page.url.searchParams.get('theme'));
	});
	$effect(() => {
		document.documentElement.dataset.theme = theme;
	});
	// Display fonts load only for the active style.
	const FONTS: Record<string, string> = {
		cozy: 'https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,700;1,500&display=swap',
		bold: 'https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500;700&display=swap'
	};
	const showSwitcher = dev || config.styleSwitcher;
	const title = $derived(page.data?.title ? `${page.data.title} · ${SITE}` : `${SITE} · Work from a cafe, together`);

	// Full-screen routes keep their own chrome; form screens hide the phone tab bar (mockup: no nav on forms).
	const BARE = ['/login', '/admin', '/style', '/agent'];
	const NO_TABS = [/^\/post$/, /^\/projects\/new$/, /^\/projects\/[^/]+\/(update|edit|attach)$/, /^\/settings/];
	const bare = $derived(BARE.some((b) => page.url.pathname === b || page.url.pathname.startsWith(b + '/')));
	const hideTabs = $derived(NO_TABS.some((r) => r.test(page.url.pathname)));
	// Any link to /login opens the sign-in sheet over the current screen instead.
	function interceptLogin(e: MouseEvent) {
		if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
		const a = (e.target as HTMLElement)?.closest?.('a');
		if (!a || a.hasAttribute('data-signin-skip') || page.url.pathname === '/login') return;
		const u = new URL(a.href, location.href);
		if (u.origin !== location.origin || u.pathname !== '/login') return;
		e.preventDefault();
		const next = u.searchParams.get('next') || location.pathname + location.search;
		askSignIn({ next, sub: u.searchParams.get('why') || 'Sign in to keep going.' });
	}

	onMount(() => {
		if (isNative()) {
			listenDeepLinks();
			if (page.data?.user) registerPush();
		}
		document.addEventListener('click', interceptLogin, true);
		const onTheme = () => bump++;
		window.addEventListener('pu-theme', onTheme);
		window.addEventListener('storage', onTheme);
		return () => {
			document.removeEventListener('click', interceptLogin, true);
			window.removeEventListener('pu-theme', onTheme);
			window.removeEventListener('storage', onTheme);
		};
	});
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={page.data?.description || DESC} />
	<meta property="og:site_name" content={SITE} />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={page.data?.description || DESC} />
	<meta property="og:type" content="website" />
	<meta property="og:url" content={page.url.origin + page.url.pathname} />
	<meta name="twitter:card" content="summary" />
	<meta name="theme-color" content="#0f9d63" />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />
	{#if FONTS[theme]}<link rel="stylesheet" href={FONTS[theme]} />{/if}
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</svelte:head>

<OfflineBanner />
{#if bare}
	{@render children()}
{:else}
	<div class="app" class:notabs={hideTabs} class:homepage={page.url.pathname === '/'}>
		<AppNav user={page.data?.user} unread={page.data?.unreadInbox ?? 0} {hideTabs} />
		<main class="app-main">{#if navigating.to?.url.pathname === '/nearby' && page.url.pathname !== '/nearby'}<NearbySkeleton />{:else}{@render children()}{/if}</main>
	</div>
{/if}
<SignInSheet providers={page.data?.providers ?? []} />

{#if showSwitcher}
	<StyleSwitcher current={theme} />
{/if}
