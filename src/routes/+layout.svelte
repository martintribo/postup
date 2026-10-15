<script lang="ts">
	import './layout.css';
	import '$lib/styles/tokens.css';
	import '$lib/styles/themes/cozy.css';
	import '$lib/styles/themes/night.css';
	import '$lib/styles/themes/bold.css';
	import { page } from '$app/state';
	import { dev } from '$app/environment';
	import { config } from '$lib/config';
	import { resolveTheme } from '$lib/theme';
	import StyleSwitcher from '$lib/components/StyleSwitcher.svelte';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';

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
	const showSwitcher = dev || config.styleSwitcher;
	const title = $derived(page.data?.title ? `${page.data.title} · ${SITE}` : `${SITE} · Work from a cafe, together`);

	onMount(() => {
		const onTheme = () => bump++;
		window.addEventListener('pu-theme', onTheme);
		window.addEventListener('storage', onTheme);
		return () => {
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
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:ital,wght@0,500;0,700;1,500&family=Space+Grotesk:wght@400;500;700&family=Archivo+Black&display=swap" />
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</svelte:head>

{@render children()}

{#if showSwitcher}
	<StyleSwitcher current={theme} />
{/if}
