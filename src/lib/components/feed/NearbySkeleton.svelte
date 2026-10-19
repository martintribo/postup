<script lang="ts">
	/** Mockup #loading: skeleton of the Nearby hero and cards; the tab bar stays. */
	import TopBar from '$lib/components/ui/TopBar.svelte';
</script>

<div class="scr-loading" data-testid="nearby-loading" aria-busy="true">
	<TopBar title="Nearby" back={false} />
	<div class="pad fd">
		<div class="hero"><i class="sk w70 h28"></i><i class="sk w50"></i></div>
		{#each [0, 1, 2] as i (i)}
			<article class="fc skel"><div class="fm sh1"></div><div class="fbd"><i class="sk w40"></i><i class="sk w80"></i><i class="sk w60"></i></div></article>
		{/each}
	</div>
</div>
