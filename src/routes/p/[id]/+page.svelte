<script lang="ts">
	let { data } = $props();
	const i = $derived(data.invite);
</script>

<main class="pu-invite" data-testid="invite">
	<div class="brand">PostUp</div>
	{#if i.live}
		<h1>{i.who} is working at {i.where} till {i.until}. Join {i.ask ? 'them' : 'in'}?</h1>
		<p class="act">“{i.activity}”{#if i.projectName} · for <a href="/projects/{i.projectId}">{i.projectName}</a>{/if}</p>
		<a class="cta" href="/postups/{i.id}" data-testid="invite-join">{i.ask ? 'Ask to join' : 'Join'}</a>
	{:else}
		<h1 data-testid="invite-ended">{i.who}'s postup has ended</h1>
		<p class="act">They were working on “{i.activity}”.</p>
		<a class="cta" href="/">See who's posted up nearby</a>
	{/if}
	<p class="what">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p>
</main>

<style>
	.pu-invite { max-width: 560px; margin: 0 auto; padding: 40px 20px; min-height: 100vh; display: grid; gap: 14px; align-content: start; background: var(--pu-bg); color: var(--pu-text); font-family: var(--pu-font); }
	.brand { font-weight: 800; color: var(--pu-accent); }
	h1 { font-family: var(--pu-font-display); font-size: 28px; line-height: 1.2; margin: 0; }
	.act { font-size: 18px; margin: 0; }
	.cta { display: block; text-align: center; padding: 14px; border-radius: var(--pu-radius); background: var(--pu-accent); color: var(--pu-accent-text); font-weight: 700; text-decoration: none; border: var(--pu-border-width) solid var(--pu-border); box-shadow: var(--pu-shadow); }
	.what { color: var(--pu-muted); font-size: 14px; }
	a { color: inherit; }
</style>
