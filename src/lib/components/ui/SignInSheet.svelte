<script lang="ts">
	/** Global sign-in sheet (mockup #signin): opens over the current screen. */
	import { signin } from '$lib/signin.svelte';
	import { verifiedOnly } from '$lib/features';
	let { providers = [] }: { providers?: string[] } = $props();
	const href = (p: string) => `/auth/${p}?next=${encodeURIComponent(signin.next)}`;
	const close = () => (signin.open = false);
	const sso = $derived(providers.filter((p) => p !== 'mock'));
	const show = (id: string) => sso.includes(id) || (verifiedOnly() && ['apple', 'google', 'x', 'github'].includes(id));
</script>

<svelte:window onkeydown={(e) => e.key === 'Escape' && close()} />
{#if signin.open}
	<div class="dim" onclick={close} role="presentation"></div>
	<div class="bs" role="dialog" aria-modal="true" aria-labelledby="signin-title" data-testid="signin-sheet">
		<span class="grab"></span>
		<h2 id="signin-title">{signin.title}</h2>
		<p class="mu">{signin.sub}</p>
		{#if show('apple')}
			<a class="sso ap" href={href('apple')} data-sveltekit-reload>
				<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.6c0-2.4 2-3.5 2-3.6-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9-.7 0-1.8-.8-3-.8-1.5 0-3 .9-3.8 2.3-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.3 0 2-1.1 2.8-2.3.9-1.3 1.2-2.5 1.3-2.6-.1 0-2.5-.9-2.5-3.7zM14.1 5.5c.6-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1 .1 2.1-.6 2.8-1.4z" /></svg>
				Continue with Apple
			</a>
		{/if}
		{#if show('google')}
			<a class="sso" href={href('google')} data-sveltekit-reload>
				<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.6a4.8 4.8 0 0 1-2.1 3.1v2.6h3.4c2-1.8 3.1-4.5 3.1-7.5z" /><path fill="#34A853" d="M12 22c2.8 0 5.2-.9 6.9-2.5l-3.4-2.6c-.9.6-2.1 1-3.5 1-2.7 0-5-1.8-5.8-4.3H2.7v2.7A10 10 0 0 0 12 22z" /><path fill="#FBBC05" d="M6.2 13.6a6 6 0 0 1 0-3.8V7.1H2.7a10 10 0 0 0 0 9z" /><path fill="#EA4335" d="M12 5.9c1.5 0 2.9.5 4 1.5l3-3A10 10 0 0 0 2.7 7.1l3.5 2.7C7 7.7 9.3 5.9 12 5.9z" /></svg>
				Continue with Google
			</a>
		{/if}
		{#if show('x')}
			<a class="sso" href={href('x')} data-sveltekit-reload>Continue with X</a>
		{/if}
		{#if show('github')}
			<a class="sso" href={href('github')} data-sveltekit-reload>Continue with GitHub</a>
		{/if}
		{#if providers.includes('mock')}
			<a class="sso" href={href('mock')} data-sveltekit-reload data-testid="signin-mock">Continue (dev sign-in)</a>
		{/if}
		{#if !verifiedOnly()}
			<a class="tx ctr sm" href="/login?next={encodeURIComponent(signin.next)}" data-sveltekit-reload data-signin-skip>Use a PostUp username</a>
		{/if}
		<button class="tx" onclick={close}>Not now</button>
	</div>
{/if}
