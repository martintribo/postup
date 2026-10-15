<script lang="ts">
	import { page } from '$app/state';
	const gone = $derived(page.status === 404 || page.status === 410);
</script>

<main class="pu-err" data-testid="error-page">
	<h1>{gone ? "This isn't here anymore" : 'Something went wrong'}</h1>
	<p>{page.error?.message || (gone ? 'It may have ended or been removed.' : 'Please try again in a moment.')}</p>
	<a href="/">See who's posted up nearby</a>
</main>

<style>
	.pu-err { max-width: 520px; margin: 0 auto; padding: 60px 20px; min-height: 100vh; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	h1 { font-family: var(--pu-font-display); }
	p { color: var(--pu-muted); }
	a { display: inline-block; padding: 12px 16px; border-radius: var(--pu-radius); background: var(--pu-accent); color: var(--pu-accent-text); font-weight: 700; text-decoration: none; }
</style>
