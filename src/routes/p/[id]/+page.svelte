<script lang="ts">
	/** Share-link landing for a postup (mockups #invite, #invite-ended). */
	import Icon from '$lib/components/ui/Icon.svelte';
	import Av from '$lib/components/ui/Av.svelte';
	import { askSignIn } from '$lib/signin.svelte';
	let { data } = $props();
	const i = $derived(data.invite);
	const first = $derived(i.who.split(' ')[0]);
</script>

<div class="scr-invite" data-testid="invite">
	<header class="nb"><span class="ib"></span><b class="brand2"><Icon name="coffee" size={16} /> postup</b><span class="nr"></span></header>
	<div class="pad done inv">
		<div class="pair" class:dimmed={!i.live}><Av name={i.who} src={i.avatarUrl} size={72} /></div>
		{#if i.live}
			<h1>{first} is working at {i.where} till {i.until}. Join {first}?</h1>
			<p>{#if i.projectName}<a class="tag" href="/projects/{i.projectId}?s=1">{i.projectName}</a>{:else}<span class="mu">“{i.activity}”</span>{/if}</p>
			<a class="btn" href="/postups/{i.id}?{i.ask ? 'ask' : 'join'}=1" data-testid="invite-join" onclick={(e) => {
				// Mockup #invite: signed out, Join opens the sign-in sheet over the invite; afterwards it carries on.
				if (data.signedIn) return;
				e.preventDefault();
				askSignIn({ title: i.ask ? `Ask ${first}` : `Join ${first}`, sub: i.ask ? `Sign in so ${first} knows who's asking.` : `Sign in so ${first} knows who's coming.`, next: `/postups/${i.id}?${i.ask ? 'ask' : 'join'}=1` });
			}}>{i.ask ? `Ask to join ${first}` : `Join ${first}`} {#if !data.signedIn}<Icon name="lock" size={14} class="lk" />{/if}</a>
			<a class="btn sec" href="/postups/{i.id}"><Icon name="pin" size={16} /> {i.where}</a>
		{:else}
			<h1 data-testid="invite-ended">This postup ended</h1>
			<p class="mu">{first} was at {i.where} {i.when}.</p>
			<a class="btn" href="/nearby">See what's nearby</a>
		{/if}
		<p class="mu sm">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p>
	</div>
</div>
