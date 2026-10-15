<script lang="ts">
	/** Share-link landing for a postup (mockups #invite, #invite-ended). */
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	let { data } = $props();
	const i = $derived(data.invite);
	const first = $derived(i.who.split(' ')[0]);
</script>

<div class="scr-invite" data-testid="invite">
	<header class="nb"><span class="ib"></span><b class="brand2"><Icon name="coffee" size={16} /> postup</b><span class="nr"></span></header>
	<div class="pad done inv">
		<div class="pair" class:dimmed={!i.live}><Av name={i.who} src={i.avatarUrl} size={72} /></div>
		{#if i.live}
			<h1>{i.who} is working at {i.where} till {i.until}. Join {first}?</h1>
			<p>{#if i.projectName}<a class="tag" href="/projects/{i.projectId}?s=1">{i.projectName}</a>{:else}<span class="mu">“{i.activity}”</span>{/if}</p>
			<a class="btn" href="/postups/{i.id}" data-testid="invite-join">{i.ask ? `Ask to join ${first}` : `Join ${first}`}</a>
			<a class="btn sec" href="/postups/{i.id}"><Icon name="pin" size={16} /> {i.where}</a>
		{:else}
			<h1 data-testid="invite-ended">This postup ended</h1>
			<p class="mu">{first} was at {i.where}{#if i.projectName}, working on {i.projectName}{/if}.</p>
			<a class="btn" href="/nearby">See what's nearby</a>
		{/if}
		<p class="mu sm">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p>
	</div>
</div>
