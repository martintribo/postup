<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';

	let { children } = $props();

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
	<link rel="icon" href={favicon} />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
</svelte:head>

{@render children()}
