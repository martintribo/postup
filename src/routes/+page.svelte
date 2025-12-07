<script lang="ts">
	import Map from '$lib/components/Map.svelte';
	import LocationAutocomplete from '$lib/components/LocationAutocomplete.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { zod4Client } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { z } from 'zod';
	import { invalidateAll } from '$app/navigation';

	const postSchema = z.object({
		name: z.string().min(1, 'Name is required'),
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
		}
	});

	let locationValue = $state('');
	let selectedLocation = $state<{ name: string; latitude: number; longitude: number } | null>(null);

	// Initialize hours if not set
	if (!$form.hours) {
		$form.hours = 1;
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

<div class="flex flex-col lg:flex-row h-screen w-screen overflow-hidden bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
	<!-- Map Container - Full width on vertical, flexible on horizontal -->
	<div class="flex-1 min-h-0 lg:min-w-0">
		{#if data.location}
			<Map
				latitude={data.location.latitude}
				longitude={data.location.longitude}
				city={data.location.city}
				country={data.location.country}
			/>
		{:else}
			<div class="h-full flex items-center justify-center">
				<p class="text-gray-500 dark:text-gray-400">Loading map...</p>
			</div>
		{/if}
	</div>

	<!-- Sidebar - Bottom half on vertical, right bar on horizontal -->
	<aside class="w-full lg:w-80 xl:w-96 h-1/2 lg:h-full border-t lg:border-t-0 lg:border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 overflow-y-auto">
		<div class="p-4">
			<h2 class="text-2xl font-semibold mb-4">Post Up</h2>
			
			<!-- Posts List -->
			{#if data.posts && data.posts.length > 0}
				<div class="mb-6">
					<h3 class="text-lg font-medium mb-3 text-gray-800 dark:text-gray-200">Recent Posts</h3>
					<div class="space-y-3">
						{#each data.posts as postItem}
							<div class="p-3 border border-gray-200 dark:border-gray-700 rounded-md bg-gray-50 dark:bg-gray-800">
								<div class="flex items-start justify-between gap-2">
									<div class="flex-1 min-w-0">
										<p class="font-medium text-gray-900 dark:text-gray-100 truncate">
											{postItem.name}
										</p>
										<p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
											{postItem.location}
										</p>
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
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			{/if}
			
			<form method="POST" use:enhance class="space-y-4">
				<!-- Name Field -->
				<div>
					<label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
						What are you doing?
					</label>
					<input
						type="text"
						id="name"
						name="name"
						bind:value={$form.name}
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
						placeholder="e.g., Working on laptop, Reading, etc."
					/>
					{#if $errors.name}
						<p class="mt-1 text-sm text-red-600 dark:text-red-400">{$errors.name}</p>
					{/if}
				</div>

				<!-- Location Autocomplete -->
				<div>
					<label for="location" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
					<label for="hours" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
	</aside>
</div>
