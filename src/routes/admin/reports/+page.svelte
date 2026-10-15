<script lang="ts">
	let { data } = $props();
</script>

<main style="max-width: 900px; margin: 0 auto; padding: 20px; font-family: var(--pu-font)" data-testid="admin-reports">
	<h1>Open reports ({data.reports.length})</h1>
	<table style="width: 100%; border-collapse: collapse">
		<thead><tr><th align="left">When</th><th align="left">What</th><th align="left">Reason</th><th></th></tr></thead>
		<tbody>
			{#each data.reports as r (r.id)}
				<tr style="border-top: 1px solid var(--pu-border)">
					<td>{new Date(r.createdAt).toLocaleString()}</td>
					<td>{r.targetType} #{r.targetId}{#if r.targetType === 'post'} · <a href="/postups/{r.targetId}">open</a>{/if}</td>
					<td>{r.reason}{#if r.details}<div style="color: var(--pu-muted)">{r.details}</div>{/if}</td>
					<td>
						<form method="POST" style="display: flex; gap: 6px">
							<input type="hidden" name="id" value={r.id} />
							<button name="action" value="hide">Hide it</button>
							<button name="action" value="dismiss">Dismiss</button>
						</form>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</main>
