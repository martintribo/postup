<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import LocationAutocomplete from '$lib/components/LocationAutocomplete.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { zod4Client } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { z } from 'zod';
	import { invalidateAll } from '$app/navigation';
	import { enhance as enhanceForm } from '$app/forms';

	const postSchema = z.object({
		name: z.string().min(1, 'Name is required'),
		activity: z.string().min(1, 'Activity is required'),
		location: z.string().min(1, 'Location is required'),
		latitude: z.number(),
		longitude: z.number(),
		hours: z.number().int().min(1, 'Hours must be at least 1').max(24, 'Hours cannot exceed 24')
	});

	let { data } = $props();

	const formData = $derived.by(() => data.form);
	const { form, enhance, submitting, errors, message } = superForm(formData, {
		validators: zod4Client(postSchema),
		resetForm: true,
		dataType: 'json'
	});

	$effect(() => {
		if ($message) {
			invalidateAll();
			closeFormModal();
		}
	});

	let locationValue = $state('');
	let selectedLocation = $state<{ name: string; latitude: number; longitude: number } | null>(null);
	let showFormModal = $state(false);
	let showFaqModal = $state(false);

	// Initialize hours if not set
	if (!$form.hours) {
		$form.hours = 1;
	}

	function openFormModal() {
		showFormModal = true;
	}

	function closeFormModal() {
		showFormModal = false;
	}

	function openFaqModal() {
		showFaqModal = true;
	}

	function closeFaqModal() {
		showFaqModal = false;
	}

	function handleLocationSelect(location: { name: string; latitude: number; longitude: number }) {
		selectedLocation = location;
		locationValue = location.name;
		$form.location = location.name;
		$form.latitude = location.latitude;
		$form.longitude = location.longitude;
	}

	function incrementHours() {
		if ($form.hours < 24) {
			$form.hours++;
		}
	}

	function decrementHours() {
		if ($form.hours > 1) {
			$form.hours--;
		}
	}

	const projectTypeStyles: Record<string, { border: string; bg: string; text: string }> = {
		software: { border: 'border-l-blue-500 dark:border-l-blue-400', bg: 'bg-blue-100 dark:bg-blue-900/50', text: 'text-blue-600 dark:text-blue-400' },
		art: { border: 'border-l-purple-500 dark:border-l-purple-400', bg: 'bg-purple-100 dark:bg-purple-900/50', text: 'text-purple-600 dark:text-purple-400' },
		writing: { border: 'border-l-amber-500 dark:border-l-amber-400', bg: 'bg-amber-100 dark:bg-amber-900/50', text: 'text-amber-600 dark:text-amber-400' },
		business: { border: 'border-l-emerald-500 dark:border-l-emerald-400', bg: 'bg-emerald-100 dark:bg-emerald-900/50', text: 'text-emerald-600 dark:text-emerald-400' },
		activities: { border: 'border-l-rose-500 dark:border-l-rose-400', bg: 'bg-rose-100 dark:bg-rose-900/50', text: 'text-rose-600 dark:text-rose-400' },
	};
	const defaultTypeStyle = projectTypeStyles.software;
</script>

<div class="flex flex-col h-screen w-screen overflow-hidden bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
	<!-- Header Bar -->
	<header class="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900" style="display: flex; align-items: center; justify-content: space-between;">
		<!-- Left: Auth -->
		<div style="min-width: 10rem;">
			{#if data.user}
				<form method="POST" action="?/logout" use:enhanceForm style="display: flex; align-items: center; gap: 0.75rem;">
					<span class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{data.user.username}</span>
					<button
						type="submit"
						class="text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
					>
						Log out
					</button>
				</form>
			{:else}
				<a
					href="/login"
					class="px-3 py-1.5 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
					style="display: inline-block;"
				>
					Log in
				</a>
			{/if}
		</div>

		<!-- Center: Brand -->
		<h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100">postup.now</h1>

		<!-- Right: FAQ -->
		<div style="width: 8rem; display: flex; justify-content: flex-end;">
		<button
			type="button"
			onclick={openFaqModal}
			class="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
			aria-label="Open FAQ"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-5 w-5"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="2"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z"
				/>
			</svg>
		</button>
		</div>
	</header>

	<!-- Main Content Area -->
	<div class="flex flex-col lg:flex-row flex-1 min-h-0">
		<!-- Map Container - Full width on vertical, flexible on horizontal -->
		<div class="flex-1 min-h-0 lg:min-w-0 relative">
			{#if data.location}
				<Map
					latitude={data.location.latitude}
					longitude={data.location.longitude}
					city={data.location.city}
					country={data.location.country}
					posts={data.posts}
				/>
			{:else}
				<div class="h-full flex items-center justify-center">
					<p class="text-gray-500 dark:text-gray-400">Loading map...</p>
				</div>
			{/if}
			
			<!-- Floating slogan and button -->
			<div class="absolute bottom-4 left-1/2 -translate-x-1/2 z-[1000] flex items-center justify-between gap-2 sm:gap-4 px-3 sm:px-4 py-2 sm:py-3 bg-white dark:bg-gray-900 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 w-[calc(100%-2rem)] max-w-[450px]">
				<div class="flex-1 flex justify-center">
					<p class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 text-center min-w-0">Doing something and open to company?</p>
				</div>
				<button
					type="button"
					onclick={openFormModal}
					class="px-3 sm:px-4 py-1.5 sm:py-2 bg-blue-600 text-white text-sm sm:text-base font-bold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors whitespace-nowrap flex-shrink-0"
				>
					Post Up
				</button>
			</div>
		</div>

		<!-- Sidebar - Bottom half on vertical, right bar on horizontal -->
		<aside class="w-full lg:w-80 xl:w-96 h-1/2 lg:h-full border-t lg:border-t-0 lg:border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-y-auto">
			<div class="p-4">
				<!-- Posts List -->
				{#if data.posts && data.posts.length > 0}
					<div>
						<h3 class="text-lg font-medium mb-3 text-gray-800 dark:text-gray-200">Who's posting up?</h3>
						<div class="space-y-3">
							{#each data.posts as postItem}
								<div class="p-3 border border-gray-200 dark:border-gray-700 rounded-md bg-gray-50 dark:bg-gray-800">
									<div class="flex items-start justify-between gap-2">
										<div class="flex-1 min-w-0">
											<p class="font-medium text-gray-900 dark:text-gray-100 truncate">
												{postItem.name}
											</p>
											<p class="text-sm text-gray-700 dark:text-gray-300 mt-0.5">
												{postItem.activity}
											</p>
											<p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
												{postItem.location}
											</p>
											{#if postItem.neighborhood || postItem.locality || postItem.district}
												<div class="flex flex-wrap items-center gap-1.5 mt-1.5 text-xs text-gray-500 dark:text-gray-500">
													{#if postItem.neighborhood}
														<span class="px-2 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">
															{postItem.neighborhood}
														</span>
													{/if}
													{#if postItem.locality}
														<span class="px-2 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">
															{postItem.locality}
														</span>
													{/if}
													{#if postItem.district}
														<span class="px-2 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">
															{postItem.district}
														</span>
													{/if}
												</div>
											{/if}
											<div class="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-gray-500">
												<span>{postItem.hours} {postItem.hours === 1 ? 'hour' : 'hours'}</span>
												<span>•</span>
												<span>
													{new Date(postItem.startTime).toLocaleString(undefined, {
														month: 'short',
														day: 'numeric',
														hour: 'numeric',
														minute: '2-digit'
													})}
												</span>
												<span>–</span>
												<span>
													{new Date(new Date(postItem.startTime).getTime() + postItem.hours * 60 * 60 * 1000).toLocaleString(undefined, {
														month: 'short',
														day: 'numeric',
														hour: 'numeric',
														minute: '2-digit'
													})}
												</span>
											</div>
										</div>
										{#if data.anonymousSessionId && postItem.sessionId === data.anonymousSessionId}
											<form method="POST" action="?/delete" use:enhanceForm>
												<input type="hidden" name="postId" value={postItem.id} />
												<button
													type="submit"
													class="flex-shrink-0 p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors rounded hover:bg-gray-200 dark:hover:bg-gray-700"
													title="Delete post"
												>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														class="h-5 w-5"
														fill="none"
														viewBox="0 0 24 24"
														stroke="currentColor"
														stroke-width="2"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
														/>
													</svg>
												</button>
											</form>
										{/if}
									</div>
								</div>
							{/each}
						</div>
					</div>
				{:else}
					<div class="text-center text-gray-500 dark:text-gray-400 py-8">
						<p>No posts yet. Be the first to post up!</p>
					</div>
				{/if}

				<!-- Projects List -->
				<div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
					<div class="flex items-center justify-between mb-3">
						<h3 class="text-lg font-medium text-gray-800 dark:text-gray-200">Projects</h3>
						<a href="/projects" class="text-xs font-medium text-blue-600 dark:text-blue-400 hover:underline">View all</a>
					</div>
					{#if data.projects && data.projects.length > 0}
						<div class="space-y-3">
							{#each data.projects as proj (proj.id)}
								{@const style = projectTypeStyles[proj.type] ?? defaultTypeStyle}
								{@const lastPostUp = proj.lastPostUpAt ? new Date(proj.lastPostUpAt) : null}
								{@const updated = proj.updatedAt.getTime() !== proj.createdAt.getTime() ? new Date(proj.updatedAt) : null}
								{@const mostRecent = lastPostUp && updated ? (lastPostUp > updated ? 'postup' : 'updated') : lastPostUp ? 'postup' : updated ? 'updated' : 'created'}
								<div class="p-3 border border-gray-200 dark:border-gray-700 rounded-md bg-gray-50 dark:bg-gray-800 border-l-4 {style.border}">
									<div class="flex items-start gap-2.5">
										<div class="flex-shrink-0 mt-0.5 w-7 h-7 rounded-md {style.bg} flex items-center justify-center">
											{#if proj.type === 'software'}
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {style.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
													<path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
												</svg>
											{:else if proj.type === 'art'}
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {style.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
													<path stroke-linecap="round" stroke-linejoin="round" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42" />
												</svg>
											{:else if proj.type === 'writing'}
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {style.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
													<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
												</svg>
											{:else if proj.type === 'business'}
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {style.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
													<path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0" />
												</svg>
											{:else if proj.type === 'activities'}
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {style.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
													<path stroke-linecap="round" stroke-linejoin="round" d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" />
												</svg>
											{/if}
										</div>
										<div class="flex-1 min-w-0">
											<p class="font-medium text-gray-900 dark:text-gray-100 truncate">{proj.name}</p>
											<p class="text-sm text-gray-600 dark:text-gray-400 mt-0.5 line-clamp-2">{proj.shortDescription}</p>
											<p class="text-xs text-gray-400 dark:text-gray-500 mt-1.5">
												{#if mostRecent === 'postup'}
													Last post up {lastPostUp?.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
												{:else if mostRecent === 'updated'}
													Updated {updated?.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
												{:else}
													Created {new Date(proj.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
												{/if}
											</p>
										</div>
									</div>
								</div>
							{/each}
						</div>
					{:else}
						<div class="py-6 text-center">
							<div class="w-10 h-10 mx-auto mb-2 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
								</svg>
							</div>
							<p class="text-sm text-gray-500 dark:text-gray-400">No active projects yet.</p>
						</div>
					{/if}
				</div>
			</div>
		</aside>
	</div>

	<!-- Form Modal -->
	{#if showFormModal}
		<div
			class="fixed inset-0 bg-black bg-opacity-50 z-[9999] flex items-center justify-center p-4"
			onclick={closeFormModal}
			onkeydown={(e) => {
				if (e.key === 'Escape') {
					closeFormModal();
				}
			}}
			role="button"
			tabindex="0"
		>
			<div
				class="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto relative z-[10000]"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-modal="true"
				aria-labelledby="modal-title"
				tabindex="-1"
			>
				<div class="p-6">
					<div class="flex items-center justify-between mb-4">
						<h2 id="modal-title" class="text-xl font-semibold text-gray-900 dark:text-gray-100">Post up</h2>
						<button
							type="button"
							onclick={closeFormModal}
							class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
							aria-label="Close modal"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-6 w-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>

					<form method="POST" action="?/create" use:enhance class="space-y-4">
						<!-- Name Field -->
						<div>
							<label for="modal-name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
								Your Name
							</label>
							<input
								type="text"
								id="modal-name"
								name="name"
								bind:value={$form.name}
								class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
								placeholder="e.g., John, Sarah, etc."
							/>
							{#if $errors.name}
								<p class="mt-1 text-sm text-red-600 dark:text-red-400">{$errors.name}</p>
							{/if}
						</div>

						<!-- Activity Field -->
						<div>
							<label for="modal-activity" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
								What are you doing?
							</label>
							<input
								type="text"
								id="modal-activity"
								name="activity"
								bind:value={$form.activity}
								class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
								placeholder="e.g., Working on laptop, Reading, etc."
							/>
							{#if $errors.activity}
								<p class="mt-1 text-sm text-red-600 dark:text-red-400">{$errors.activity}</p>
							{/if}
						</div>

						<!-- Location Autocomplete -->
						<div>
							<label for="modal-location" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
								Location
							</label>
							<LocationAutocomplete
								name="location"
								value={locationValue}
								onSelect={handleLocationSelect}
								proximity={data.location ? { latitude: data.location.latitude, longitude: data.location.longitude } : undefined}
							/>
							<input type="hidden" name="location" bind:value={$form.location} />
							<input type="hidden" name="latitude" bind:value={$form.latitude} />
							<input type="hidden" name="longitude" bind:value={$form.longitude} />
							{#if $errors.location}
								<p class="mt-1 text-sm text-red-600 dark:text-red-400">{$errors.location}</p>
							{/if}
						</div>

						<!-- Hours Counter -->
						<div>
							<label for="modal-hours" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
								Hours
							</label>
							<div class="flex items-center gap-3">
								<button
									type="button"
									onclick={decrementHours}
									class="w-10 h-10 flex items-center justify-center border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
									disabled={$form.hours <= 1}
								>
									−
								</button>
								<input
									type="number"
									id="modal-hours"
									name="hours"
									bind:value={$form.hours}
									min="1"
									max="24"
									class="w-20 px-3 py-2 text-center border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
								/>
								<button
									type="button"
									onclick={incrementHours}
									class="w-10 h-10 flex items-center justify-center border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
									disabled={$form.hours >= 24}
								>
									+
								</button>
							</div>
							{#if $errors.hours}
								<p class="mt-1 text-sm text-red-600 dark:text-red-400">{$errors.hours[0]}</p>
							{/if}
						</div>

						<!-- Submit Button -->
						<button
							type="submit"
							class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
						>
							Post up
						</button>

						{#if $message}
							<p class="text-sm text-green-600 dark:text-green-400">{$message}</p>
						{/if}
					</form>
				</div>
			</div>
		</div>
	{/if}

	<!-- FAQ Modal -->
	{#if showFaqModal}
		<div
			class="fixed inset-0 bg-black bg-opacity-50 z-[9999] flex items-center justify-center p-4"
			onclick={closeFaqModal}
			onkeydown={(e) => {
				if (e.key === 'Escape') {
					closeFaqModal();
				}
			}}
			role="button"
			tabindex="0"
		>
			<div
				class="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto relative z-[10000]"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
				role="dialog"
				aria-modal="true"
				aria-labelledby="faq-modal-title"
				tabindex="-1"
			>
				<div class="p-6">
					<div class="flex items-center justify-between mb-6">
						<h2 id="faq-modal-title" class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Frequently Asked Questions</h2>
						<button
							type="button"
							onclick={closeFaqModal}
							class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
							aria-label="Close modal"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-6 w-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>

					<div class="space-y-6">
						<div>
							<p class="text-gray-600 dark:text-gray-400">
								Hello and welcome! Appologies in advance for the AI generated text, I'll come back soon to clean the FAQ up!
							</p>
						</div>
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">What is postup.now?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								postup.now is a platform designed to turn solo activities into social opportunities by letting you share what you're up to and invite like-minded people to join. Inspired by the idea of connecting creators and anyone pursuing personal projects during off-hours, it's open to all kinds of activities—whether you're coding at a cafe, sketching in a park, hitting the gym, or exploring a new hobby. Post your location and what you're doing, and others can request to join if it sparks their interest. If approved, you can share exact details to meet up and collaborate or just hang out.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Why was postup.now created?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								The site stems from a desire to build communities around shared drives and passions, like turning off-hours activities into enriching social experiences. Since there aren't many systems to easily support connections with others outside regular day job hours, postup.now offers a welcoming space to meet similar people—coders, writers, artists, or anyone pursuing side projects—while being flexible for casual meetups, fitness sessions, or group activities. It's about making solo time more vibrant through unexpected connections that could lead to friendships, collaborations, or just better motivation.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">How do I post up?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								Click the "Post Up" button, enter your name or handle, describe what you're doing (e.g., "Building a TypeScript app" or "Gym session focusing on strength training"), add your general location (with optional obfuscation for privacy), and specify how long you'll be there. Your post appears on the map as a public invite—others can see the basics and request to join for more details if you approve.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">How does joining work?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								If a post catches your eye, click "Request to Join" and add a quick note about why (e.g., "I'm also into app development and nearby!"). The poster gets notified and can approve or decline. If approved, you'll get the exact location or contact info to connect—perfect for turning a solo session into a spontaneous meetup with people who share your vibe.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">How long do posts stay active?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								Posts remain active for the time you set (from 1 hour up to a full day or more, depending on your activity). They auto-expire afterward to keep things fresh, but you can extend, edit, or delete them anytime via the manage icon on your post.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Is my information private?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								You control what you share—posts show only what you input, like a general area and activity description publicly. Exact locations are revealed only to approved joiners. No personal data is stored beyond what's needed for the post, and you can delete everything at any time. We prioritize safety and consent in connections.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">How do I find others who are posting up?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								Browse the interactive map for icons (like coffee cups for work spots or activity markers for gyms/parks). Filter by interests or location to spot posts that match your energy—click for details on what they're doing, how long they're there, and to send a join request if it aligns with your plans.
							</p>
						</div>
						
						<div>
							<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">Is it only for work or creative projects?</h3>
							<p class="text-gray-600 dark:text-gray-400">
								Not at all! While it's great for off-hours creators looking to meet similar minds, postup.now is versatile for any activity—gym buddies, park reads, group hikes, language exchanges, or casual hangs. Use it to make everyday outings more social and discover people with overlapping interests.
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
