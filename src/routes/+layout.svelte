<script lang="ts">
	import './layout.css';
	import '$lib/styles/tokens.css';
	import '$lib/styles/themes/bold.css';
	import { page } from '$app/state';
	import { config, isTheme } from '$lib/config';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';

	let { children } = $props();

	const SITE = 'PostUp';
	const DESC = 'Post up at a cafe and see who is working nearby. Join someone, or share what you are building.';
	// ?theme=bold previews another style (design tokens); default comes from config.
	const theme = $derived.by(() => {
		const q = page.url.searchParams.get('theme');
		return isTheme(q) ? q : config.theme;
	});
	$effect(() => {
		document.documentElement.dataset.theme = theme;
	});
	const title = $derived(page.data?.title ? `${page.data.title} · ${SITE}` : `${SITE} · Work from a cafe, together`);

	onMount(() => {
		// Detect system dark mode preference
		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		
		const updateTheme = (e?: MediaQueryListEvent) => {
			const isDark = e ? e.matches : mediaQuery.matches;
			if (isDark) {
				document.documentElement.classList.add('dark');
			} else {
				document.documentElement.classList.remove('dark');
			}
		};

		// Set initial theme
		updateTheme();

		// Listen for changes
		if (mediaQuery.addEventListener) {
			mediaQuery.addEventListener('change', updateTheme);
		} else {
			// Fallback for older browsers
			mediaQuery.addListener(updateTheme);
		}

		return () => {
			if (mediaQuery.removeEventListener) {
				mediaQuery.removeEventListener('change', updateTheme);
			} else {
				mediaQuery.removeListener(updateTheme);
			}
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
	<meta name="theme-color" content="#1f7a4d" />
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</svelte:head>

{@render children()}
