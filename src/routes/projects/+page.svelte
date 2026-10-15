<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import { SvelteSet } from 'svelte/reactivity';

	let { data } = $props();

	const typeLabels: Record<string, string> = {
		software: 'Software',
		art: 'Art',
		writing: 'Writing',
		business: 'Business',
		activities: 'Activities'
	};

	const typeColors: Record<string, { badge: string; border: string }> = {
		software: { badge: 'bg-brand-soft text-brand ', border: 'border-l-brand ' },
		art: { badge: 'bg-brand-soft text-ink ', border: 'border-l-line ' },
		writing: { badge: 'bg-brand-soft text-ink ', border: 'border-l-line ' },
		business: { badge: 'bg-brand-soft text-live ', border: 'border-l-live ' },
		activities: { badge: 'bg-brand-soft text-ink ', border: 'border-l-danger ' },
	};

	let selectedTypes = new SvelteSet<string>();
	let showActiveOnly = $state(true);

	const isLoggedIn = $derived(!!page.data.user);
	const currentUserId = $derived(page.data.user?.id ?? null);

	type AgentScope = 'projects' | 'status';
	type Handoff = { handoffUrl: string; token: string; expiresAt: string; scope: AgentScope };
	let handoff = $state<Handoff | null>(null);
	let handoffLoading = $state<AgentScope | null>(null);
	let handoffError = $state('');
	let handoffCopied = $state(false);

	type DescSegment =
		| { type: 'text'; value: string }
		| { type: 'image'; alt: string; url: string }
		| { type: 'placeholder'; alt: string; index: number };

	function parseDescription(desc: string): DescSegment[] {
		const segments: DescSegment[] = [];
		const regex = /!\[([^\]]*)\]\(([^)]+)\)/g;
		let last = 0;
		let placeholderIndex = 0;
		let match: RegExpExecArray | null;
		while ((match = regex.exec(desc)) !== null) {
			if (match.index > last) {
				segments.push({ type: 'text', value: desc.slice(last, match.index) });
			}
			const [, alt, url] = match;
			if (url === 'placeholder') {
				segments.push({ type: 'placeholder', alt, index: placeholderIndex++ });
			} else {
				segments.push({ type: 'image', alt, url });
			}
			last = match.index + match[0].length;
		}
		if (last < desc.length) {
			segments.push({ type: 'text', value: desc.slice(last) });
		}
		return segments;
	}

	let uploadingKey = $state<string | null>(null);

	async function uploadPlaceholder(
		projectId: number,
		placeholderIndex: number,
		file: File
	) {
		const key = `${projectId}:${placeholderIndex}`;
		uploadingKey = key;
		try {
			const form = new FormData();
			form.append('file', file);
			form.append('placeholderIndex', String(placeholderIndex));
			const res = await fetch(`/api/projects/${projectId}/images`, {
				method: 'POST',
				body: form
			});
			if (!res.ok) {
				const body = await res.json().catch(() => ({}));
				handoffError = body.error ?? `Upload failed (${res.status})`;
				return;
			}
			await invalidateAll();
		} finally {
			uploadingKey = null;
		}
	}

	function handlePlaceholderFile(
		event: Event,
		projectId: number,
		placeholderIndex: number
	) {
		const input = event.currentTarget as HTMLInputElement;
		const file = input.files?.[0];
		if (file) uploadPlaceholder(projectId, placeholderIndex, file);
		input.value = '';
	}

	const projectsById = $derived(
		new Map(data.projects.map((p) => [p.id, p]))
	);

	let reviewingId = $state<number | null>(null);

	const filteredProjects = $derived(
		data.projects.filter((p) => {
			if (showActiveOnly && !p.active) return false;
			if (selectedTypes.size > 0 && !selectedTypes.has(p.type)) return false;
			return true;
		})
	);

	function toggleType(type: string) {
		if (selectedTypes.has(type)) {
			selectedTypes.delete(type);
		} else {
			selectedTypes.add(type);
		}
	}

	async function mintHandoff(scope: AgentScope) {
		handoffLoading = scope;
		handoffError = '';
		handoffCopied = false;
		try {
			const res = await fetch('/api/agent/tokens', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({ scope })
			});
			if (!res.ok) {
				const body = await res.json().catch(() => ({}));
				handoffError = body.error ?? `Request failed (${res.status})`;
				return;
			}
			handoff = await res.json();
		} catch (err) {
			handoffError = err instanceof Error ? err.message : 'Failed to mint token';
		} finally {
			handoffLoading = null;
		}
	}

	async function copyHandoff() {
		if (!handoff) return;
		try {
			await navigator.clipboard.writeText(handoff.handoffUrl);
			handoffCopied = true;
			setTimeout(() => (handoffCopied = false), 2000);
		} catch {
			handoffError = 'Could not copy to clipboard';
		}
	}

	async function revokeHandoff() {
		await fetch('/api/agent/tokens', { method: 'DELETE' });
		handoff = null;
	}

	async function reviewChange(id: number, action: 'accept' | 'reject') {
		reviewingId = id;
		try {
			const res = await fetch(`/api/projects/changes/${id}`, {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({ action })
			});
			if (!res.ok) {
				const body = await res.json().catch(() => ({}));
				handoffError = body.error ?? `Review failed (${res.status})`;
				return;
			}
			await invalidateAll();
		} finally {
			reviewingId = null;
		}
	}

	function changeTitle(change: typeof data.pendingChanges[number]): string {
		const payload = (change.payload ?? {}) as Record<string, unknown>;
		if (change.action === 'create') {
			const name = typeof payload.name === 'string' ? payload.name : '(unnamed)';
			return `New project: "${name}"`;
		}
		const target =
			change.targetProjectId != null ? projectsById.get(change.targetProjectId) : null;
		const targetName = target?.name ?? `#${change.targetProjectId}`;
		if (change.action === 'status_update') return `Status update on "${targetName}"`;
		return `Update "${targetName}"`;
	}

	function fmtScalar(value: unknown): string {
		if (value === null || value === undefined) return '—';
		if (typeof value === 'boolean') return value ? 'true' : 'false';
		return String(value);
	}

	const SCALAR_FIELDS = new Set(['name', 'type', 'active']);
	const MULTILINE_FIELDS = new Set(['shortDescription', 'description']);
</script>

{#snippet renderDescription(segments: DescSegment[], ownerProjectId: number | null)}
	<div class="text-sm text-ink space-y-2">
		{#each segments as seg, i (i)}
			{#if seg.type === 'text'}
				<p class="whitespace-pre-line">{seg.value}</p>
			{:else if seg.type === 'image'}
				<img
					src={seg.url}
					alt={seg.alt}
					class="rounded-lg max-w-full max-h-96 object-cover"
				/>
			{:else if ownerProjectId !== null}
				{@const uploading = uploadingKey === `${ownerProjectId}:${seg.index}`}
				<label
					class="block border-2 border-dashed border-line rounded-lg p-6 text-center cursor-pointer hover:border-brand transition-colors {uploading ? 'opacity-50 pointer-events-none' : ''}"
				>
					<input
						type="file"
						accept="image/png,image/jpeg,image/webp,image/gif,image/avif"
						class="hidden"
						disabled={uploading}
						onchange={(e) => handlePlaceholderFile(e, ownerProjectId, seg.index)}
					/>
					<p class="text-sm font-medium text-muted">
						{uploading ? 'Uploading…' : `Click to upload: ${seg.alt}`}
					</p>
					<p class="text-xs text-subtle mt-1">
						PNG, JPEG, WEBP, GIF or AVIF · up to 8 MB
					</p>
				</label>
			{:else}
				<div class="border-2 border-dashed border-line rounded-lg p-4 text-center text-xs text-subtle">
					Image placeholder: {seg.alt}
				</div>
			{/if}
		{/each}
	</div>
{/snippet}

<div class="min-h-screen bg-surface text-ink">
	<!-- Header -->
	<header class="border-b border-line px-4 py-3">
		<div class="max-w-6xl mx-auto flex items-center justify-between">
			<div class="flex items-center gap-3">
				<a href="/" aria-label="Back to home" class="text-muted hover:text-ink transition-colors">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
					</svg>
				</a>
				<h1 class="text-xl font-semibold">Projects</h1>
			</div>
			<div class="flex items-center gap-2 flex-wrap justify-end">
				{#if isLoggedIn}
					<button
						type="button"
						onclick={() => mintHandoff('projects')}
						disabled={handoffLoading !== null}
						class="px-3 py-1.5 border border-line text-ink text-sm font-medium rounded-md hover:bg-bg disabled:opacity-50"
					>
						{handoffLoading === 'projects' ? 'Minting…' : 'Agent: edit projects'}
					</button>
					<button
						type="button"
						onclick={() => mintHandoff('status')}
						disabled={handoffLoading !== null}
						class="px-3 py-1.5 border border-line text-ink text-sm font-medium rounded-md hover:bg-bg disabled:opacity-50"
					>
						{handoffLoading === 'status' ? 'Minting…' : 'Agent: post status'}
					</button>
				{/if}
				<!-- TODO: "Create Project" button -->
				<button
					type="button"
					disabled
					class="px-3 py-1.5 bg-brand text-on-brand text-sm font-medium rounded-md opacity-50 cursor-not-allowed"
				>
					New Project
				</button>
			</div>
		</div>
	</header>

	{#if handoff || handoffError}
		<div class="max-w-6xl mx-auto px-4 pt-4">
			{#if handoff}
				<div class="border border-brand bg-brand-soft rounded-lg p-4 text-sm">
					<div class="flex items-start justify-between gap-3 mb-2">
						<div>
							<p class="font-medium text-brand">
								Give this URL to your agent ({handoff.scope === 'status' ? 'status updates' : 'edit projects'})
							</p>
							<p class="text-xs text-brand mt-0.5">
								The agent can fetch it to learn how to use the API. Expires {new Date(handoff.expiresAt).toLocaleString()}.
							</p>
						</div>
						<button
							type="button"
							onclick={revokeHandoff}
							class="text-xs text-brand hover:underline"
						>
							Revoke
						</button>
					</div>
					<div class="flex gap-2">
						<input
							type="text"
							readonly
							value={handoff.handoffUrl}
							class="flex-1 min-w-0 px-2 py-1 text-xs font-mono bg-surface border border-brand rounded"
						/>
						<button
							type="button"
							onclick={copyHandoff}
							class="px-3 py-1 text-xs bg-brand text-on-brand rounded hover:bg-brand-hover"
						>
							{handoffCopied ? 'Copied' : 'Copy'}
						</button>
					</div>
				</div>
			{/if}
			{#if handoffError}
				<div class="mt-2 border border-danger bg-danger-soft rounded-md p-2 text-xs text-danger">
					{handoffError}
				</div>
			{/if}
		</div>
	{/if}

	{#if data.pendingChanges.length > 0}
		<div class="max-w-6xl mx-auto px-4 pt-4">
			<div class="border border-line bg-brand-soft rounded-lg p-4">
				<h2 class="text-sm font-medium text-ink mb-3">
					Pending agent changes ({data.pendingChanges.length})
				</h2>
				<ul class="space-y-3">
					{#each data.pendingChanges as change (change.id)}
						{@const payload = (change.payload ?? {}) as Record<string, unknown>}
						{@const target = change.targetProjectId != null ? projectsById.get(change.targetProjectId) : null}
						<li class="bg-surface border border-line rounded-lg p-3 space-y-3">
							<div class="flex items-start justify-between gap-3">
								<p class="text-sm font-medium text-ink">{changeTitle(change)}</p>
								<div class="flex flex-shrink-0 gap-2">
									<button
										type="button"
										onclick={() => reviewChange(change.id, 'reject')}
										disabled={reviewingId === change.id}
										class="px-2 py-1 text-xs border border-line text-ink rounded hover:bg-brand-soft disabled:opacity-50"
									>
										Reject
									</button>
									<button
										type="button"
										onclick={() => reviewChange(change.id, 'accept')}
										disabled={reviewingId === change.id}
										class="px-2 py-1 text-xs bg-live text-on-brand rounded hover:bg-live disabled:opacity-50"
									>
										Accept
									</button>
								</div>
							</div>

							{#if change.action === 'create'}
								{@const newType = typeof payload.type === 'string' ? payload.type : 'software'}
								{@const newColors = typeColors[newType] ?? typeColors.software}
								<div class="border border-line rounded-md bg-bg border-l-4 {newColors.border} p-3">
									<div class="flex items-center gap-2 mb-1">
										<h3 class="font-medium text-ink">{fmtScalar(payload.name)}</h3>
										<span class="text-xs px-2 py-0.5 rounded-full {newColors.badge}">{typeLabels[newType] ?? newType}</span>
									</div>
									{#if typeof payload.shortDescription === 'string' && payload.shortDescription}
										<p class="text-sm text-muted mb-2">{payload.shortDescription}</p>
									{/if}
									{#if typeof payload.description === 'string' && payload.description}
										{@render renderDescription(parseDescription(payload.description), null)}
									{/if}
								</div>
							{:else if change.action === 'status_update'}
								{@const occurredAtRaw = typeof payload.occurredAt === 'string' ? payload.occurredAt : null}
								{@const occurredAt = occurredAtRaw ? new Date(occurredAtRaw) : null}
								{@const previewTitle = typeof payload.title === 'string' ? payload.title : ''}
								{@const previewBody = typeof payload.body === 'string' ? payload.body : ''}
								<article class="border-l-2 border-line pl-4">
									{#if occurredAt && !Number.isNaN(occurredAt.getTime())}
										<div class="text-xs text-subtle font-mono mb-1">
											{occurredAt.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
										</div>
									{/if}
									{#if previewTitle}
										<h3 class="text-base font-semibold text-ink mb-1">{previewTitle}</h3>
									{/if}
									<div class="text-sm text-ink space-y-2">
										{#each previewBody.split(/\n\n+/) as para, pi (pi)}
											<p class="whitespace-pre-line">{para}</p>
										{/each}
									</div>
								</article>
							{:else if change.action === 'update'}
								<dl class="space-y-2 text-sm">
									{#each Object.keys(payload) as field (field)}
										<div class="grid grid-cols-[6rem_1fr] gap-2 items-start">
											<dt class="text-xs font-mono text-muted pt-0.5">{field}</dt>
											<dd class="min-w-0">
												{#if SCALAR_FIELDS.has(field)}
													<div class="flex items-center gap-2 flex-wrap">
														<span class="text-xs text-muted line-through">{fmtScalar(target?.[field as keyof typeof target])}</span>
														<span class="text-xs text-subtle">→</span>
														<span class="text-sm text-ink font-medium">{fmtScalar(payload[field])}</span>
													</div>
												{:else if MULTILINE_FIELDS.has(field)}
													<div class="space-y-1">
														<details class="text-xs">
															<summary class="cursor-pointer text-muted">Before</summary>
															<div class="mt-1 p-2 bg-bg rounded border border-line whitespace-pre-line text-muted">{fmtScalar(target?.[field as keyof typeof target])}</div>
														</details>
														<div>
															<p class="text-xs text-muted">After</p>
															{#if field === 'description' && typeof payload[field] === 'string'}
																<div class="mt-1 p-2 bg-brand-soft rounded border border-live">
																	{@render renderDescription(parseDescription(payload[field] as string), null)}
																</div>
															{:else}
																<div class="mt-1 p-2 bg-brand-soft rounded border border-live whitespace-pre-line text-ink">{fmtScalar(payload[field])}</div>
															{/if}
														</div>
													</div>
												{:else}
													<span class="text-sm text-ink">{fmtScalar(payload[field])}</span>
												{/if}
											</dd>
										</div>
									{/each}
								</dl>
							{/if}

							<details class="text-xs">
								<summary class="cursor-pointer text-subtle">Raw JSON</summary>
								<pre class="mt-1 bg-bg border border-line rounded p-2 overflow-x-auto">{JSON.stringify(change.payload, null, 2)}</pre>
							</details>
						</li>
					{/each}
				</ul>
			</div>
		</div>
	{/if}

	<div class="max-w-6xl mx-auto flex flex-col lg:flex-row gap-6 p-4">
		<!-- Filters Sidebar -->
		<aside class="w-full lg:w-64 lg:flex-shrink-0">
			<div class="lg:sticky lg:top-4 space-y-6">
				<!-- Active Toggle -->
				<div>
					<h3 class="text-sm font-medium text-ink mb-2">Status</h3>
					<label class="flex items-center gap-2 text-sm cursor-pointer">
						<input
							type="checkbox"
							bind:checked={showActiveOnly}
							class="rounded border-line text-brand focus:ring-brand"
						/>
						<span class="text-muted">Active only</span>
					</label>
				</div>

				<!-- Type Filters -->
				<div>
					<h3 class="text-sm font-medium text-ink mb-2">Type</h3>
					<div class="flex flex-wrap lg:flex-col gap-2">
						{#each Object.entries(typeLabels) as [type, label] (type)}
							<button
								type="button"
								onclick={() => toggleType(type)}
								class="px-2.5 py-1 text-sm rounded-md border transition-colors {selectedTypes.has(type)
									? typeColors[type].badge + ' border-transparent font-medium'
									: 'border-line text-muted hover:bg-bg '}"
							>
								{label}
							</button>
						{/each}
					</div>
					{#if selectedTypes.size > 0}
						<button
							type="button"
							onclick={() => selectedTypes.clear()}
							class="mt-2 text-xs text-muted hover:text-ink"
						>
							Clear filters
						</button>
					{/if}
				</div>

				<!-- TODO: Additional filters -->
				<div class="text-xs text-subtle border border-dashed border-line rounded-md p-3">
					<p class="font-medium mb-1">Placeholder: More filters</p>
					<ul class="space-y-1">
						<li>- Sort by (newest, most active, most post-ups)</li>
						<li>- Search by name</li>
						<li>- Filter by creator</li>
					</ul>
				</div>
			</div>
		</aside>

		<!-- Project List -->
		<main class="flex-1 min-w-0">
			{#if filteredProjects.length > 0}
				<div class="space-y-4">
					{#each filteredProjects as proj (proj.id)}
						{@const colors = typeColors[proj.type] ?? typeColors.software}
						{@const segments = parseDescription(proj.description)}
						{@const isOwner = currentUserId !== null && currentUserId === proj.userId}
						<div class="border border-line rounded-lg bg-surface border-l-4 {colors.border} overflow-hidden">
							<div class="p-4">
								<div class="flex items-start justify-between gap-4">
									<div class="flex-1 min-w-0">
										<div class="flex items-center gap-2 mb-1">
											<h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 truncate"><a href="/projects/{proj.id}" id="p{proj.id}">{proj.name}</a></h2>
											<span class="flex-shrink-0 text-xs px-2 py-0.5 rounded-full {colors.badge}">{typeLabels[proj.type] ?? proj.type}</span>
											{#if !proj.active}
												<span class="flex-shrink-0 text-xs px-2 py-0.5 rounded-full bg-surface-2 text-muted">Inactive</span>
											{/if}
										</div>
										<p class="text-sm text-muted">{proj.shortDescription}</p>
									</div>
								</div>

								<!-- Full Description (segments) -->
								<div class="mt-3">
									{@render renderDescription(segments, isOwner ? proj.id : null)}
								</div>

								<!-- Status feed -->
								{#if proj.statuses.length > 0}
									<div class="mt-4 space-y-4">
										<p class="text-xs font-medium text-muted uppercase tracking-wide">Updates</p>
										{#each proj.statuses as status (status.id)}
											<article class="border-l-2 border-line pl-4">
												<div class="text-xs text-subtle font-mono mb-1">
													{new Date(status.occurredAt).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
												</div>
												{#if status.title}
													<h3 class="text-base font-semibold text-ink mb-1">{status.title}</h3>
												{/if}
												<div class="text-sm text-ink space-y-2">
													{#each status.body.split(/\n\n+/) as para, pi (pi)}
														<p class="whitespace-pre-line">{para}</p>
													{/each}
												</div>
											</article>
										{/each}
									</div>
								{/if}

								<!-- Metadata Footer -->
								<div class="mt-4 text-xs text-subtle" style="display: flex; align-items: center; gap: 1rem;">
									<span>Created {new Date(proj.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}</span>
									{#if proj.updatedAt.getTime() !== proj.createdAt.getTime()}
										<span>·</span>
										<span>Updated {new Date(proj.updatedAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
									{/if}
									{#if proj.lastPostUpAt}
										<span>·</span>
										<span>Last post-up {new Date(proj.lastPostUpAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
									{/if}
								</div>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<div class="text-center py-12">
					<p class="text-muted">No projects match your filters.</p>
				</div>
			{/if}
		</main>
	</div>
</div>
