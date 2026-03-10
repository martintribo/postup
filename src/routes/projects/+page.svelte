<script lang="ts">
	let { data } = $props();

	const typeLabels: Record<string, string> = {
		software: 'Software',
		art: 'Art',
		writing: 'Writing',
		business: 'Business',
		activities: 'Activities'
	};

	const typeColors: Record<string, { badge: string; border: string }> = {
		software: { badge: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300', border: 'border-l-blue-500 dark:border-l-blue-400' },
		art: { badge: 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300', border: 'border-l-purple-500 dark:border-l-purple-400' },
		writing: { badge: 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300', border: 'border-l-amber-500 dark:border-l-amber-400' },
		business: { badge: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-300', border: 'border-l-emerald-500 dark:border-l-emerald-400' },
		activities: { badge: 'bg-rose-100 text-rose-700 dark:bg-rose-900 dark:text-rose-300', border: 'border-l-rose-500 dark:border-l-rose-400' },
	};

	let selectedTypes = $state<Set<string>>(new Set());
	let showActiveOnly = $state(true);

	const filteredProjects = $derived(
		data.projects.filter((p) => {
			if (showActiveOnly && !p.active) return false;
			if (selectedTypes.size > 0 && !selectedTypes.has(p.type)) return false;
			return true;
		})
	);

	function toggleType(type: string) {
		const next = new Set(selectedTypes);
		if (next.has(type)) {
			next.delete(type);
		} else {
			next.add(type);
		}
		selectedTypes = next;
	}
</script>

<div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
	<!-- Header -->
	<header class="border-b border-gray-200 dark:border-gray-700 px-4 py-3">
		<div class="max-w-6xl mx-auto flex items-center justify-between">
			<div class="flex items-center gap-3">
				<a href="/" class="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
					</svg>
				</a>
				<h1 class="text-xl font-semibold">Projects</h1>
			</div>
			<!-- TODO: "Create Project" button -->
			<button
				type="button"
				disabled
				class="px-3 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-md opacity-50 cursor-not-allowed"
			>
				New Project
			</button>
		</div>
	</header>

	<div class="max-w-6xl mx-auto flex gap-6 p-4" style="flex-direction: row;">
		<!-- Filters Sidebar -->
		<aside style="width: 16rem; flex-shrink: 0;">
			<div class="lg:sticky lg:top-4 space-y-6">
				<!-- Active Toggle -->
				<div>
					<h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</h3>
					<label class="flex items-center gap-2 text-sm cursor-pointer">
						<input
							type="checkbox"
							bind:checked={showActiveOnly}
							class="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
						/>
						<span class="text-gray-600 dark:text-gray-400">Active only</span>
					</label>
				</div>

				<!-- Type Filters -->
				<div>
					<h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Type</h3>
					<div class="flex flex-wrap lg:flex-col gap-2">
						{#each Object.entries(typeLabels) as [type, label]}
							<button
								type="button"
								onclick={() => toggleType(type)}
								class="px-2.5 py-1 text-sm rounded-md border transition-colors {selectedTypes.has(type)
									? typeColors[type].badge + ' border-transparent font-medium'
									: 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'}"
							>
								{label}
							</button>
						{/each}
					</div>
					{#if selectedTypes.size > 0}
						<button
							type="button"
							onclick={() => selectedTypes = new Set()}
							class="mt-2 text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
						>
							Clear filters
						</button>
					{/if}
				</div>

				<!-- TODO: Additional filters -->
				<div class="text-xs text-gray-400 dark:text-gray-600 border border-dashed border-gray-300 dark:border-gray-700 rounded-md p-3">
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
						<div class="border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 border-l-4 {colors.border} overflow-hidden">
							<div class="p-4">
								<div class="flex items-start justify-between gap-4">
									<div class="flex-1 min-w-0">
										<div class="flex items-center gap-2 mb-1">
											<h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 truncate">{proj.name}</h2>
											<span class="flex-shrink-0 text-xs px-2 py-0.5 rounded-full {colors.badge}">{typeLabels[proj.type] ?? proj.type}</span>
											{#if !proj.active}
												<span class="flex-shrink-0 text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400">Inactive</span>
											{/if}
										</div>
										<p class="text-sm text-gray-600 dark:text-gray-400">{proj.shortDescription}</p>
									</div>
								</div>

								<!-- Full Description -->
								<div class="mt-3 text-sm text-gray-700 dark:text-gray-300">
									<p>{proj.description}</p>
								</div>

								<!-- TODO: Project owner / creator -->
								<div class="mt-4 border border-dashed border-gray-300 dark:border-gray-700 rounded-md p-3 text-xs text-gray-400 dark:text-gray-600">
									<p class="font-medium mb-1">Placeholder: Project owner</p>
									<p>Display user avatar, name, and link to profile. Requires user-project relationship.</p>
								</div>

								<!-- TODO: Recent post-ups for this project -->
								<div class="mt-3 border border-dashed border-gray-300 dark:border-gray-700 rounded-md p-3 text-xs text-gray-400 dark:text-gray-600">
									<p class="font-medium mb-1">Placeholder: Recent post-ups</p>
									<p>Show the last few post-ups associated with this project — who posted up, where, and when. Requires post-project foreign key.</p>
								</div>

								<!-- Metadata Footer -->
								<div class="mt-4 text-xs text-gray-400 dark:text-gray-500" style="display: flex; align-items: center; gap: 1rem;">
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
					<p class="text-gray-500 dark:text-gray-400">No projects match your filters.</p>
				</div>
			{/if}
		</main>
	</div>
</div>
