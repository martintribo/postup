<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import LocationAutocomplete from '$lib/components/LocationAutocomplete.svelte';
	import NotificationButton from '$lib/components/NotificationButton.svelte';
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
</script>

<div class="flex flex-col h-screen w-screen overflow-hidden bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
	<!-- Header Bar -->
	<header class="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 flex items-center justify-between relative">
		<h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100 absolute left-1/2 -translate-x-1/2">postup.now</h1>
		<div class="flex items-center gap-2 ml-auto">
			<NotificationButton />
			<button
				type="button"
				onclick={openFaqModal}
				class="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
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
