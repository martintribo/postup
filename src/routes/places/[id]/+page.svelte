<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { zod4Client } from 'sveltekit-superforms/adapters';
	import { z } from 'zod';
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import type { PageData } from './$types';

	const reviewSchema = z.object({
		rating: z.number().int().min(1).max(5),
		text: z.string().optional(),
		wifiRating: z.number().int().min(1).max(5).optional(),
		noiseLevel: z.enum(['quiet', 'moderate', 'noisy']).optional(),
		hasOutlets: z.boolean().optional()
	});

	let { data }: { data: PageData } = $props();

	const { form, enhance: formEnhance, errors } = superForm(data.reviewForm, {
		validators: zod4Client(reviewSchema),
		resetForm: true,
		dataType: 'json',
		onResult: () => {
			showReviewForm = false;
			invalidateAll();
		}
	});

	let showReviewForm = $state(false);
	let newTag = $state('');
	let selectedRating = $state(0);
	let selectedWifi = $state(0);

	// Sync star selections to form
	$effect(() => {
		if (selectedRating > 0) $form.rating = selectedRating;
	});
	$effect(() => {
		if (selectedWifi > 0) $form.wifiRating = selectedWifi;
	});

	const p = $derived(data.place);
	const stats = $derived(data.stats);
	const dominantNoise = $derived.by(() => {
		const { quiet, moderate, noisy } = stats.noiseCounts;
		if (quiet + moderate + noisy === 0) return null;
		if (quiet >= moderate && quiet >= noisy) return 'quiet';
		if (moderate >= quiet && moderate >= noisy) return 'moderate';
		return 'noisy';
	});

	function renderStars(rating: number): string {
		const full = Math.round(rating);
		return '\u2605'.repeat(full) + '\u2606'.repeat(5 - full);
	}

	function timeAgo(date: Date): string {
		const now = new Date();
		const diff = now.getTime() - new Date(date).getTime();
		const minutes = Math.floor(diff / 60000);
		if (minutes < 60) return `${minutes}m ago`;
		const hours = Math.floor(minutes / 60);
		if (hours < 24) return `${hours}h ago`;
		const days = Math.floor(hours / 24);
		if (days < 30) return `${days}d ago`;
		return new Date(date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
	}
</script>

<div class="min-h-screen bg-surface text-ink">
	<!-- Header -->
	<header class="border-b border-line px-4 py-3" style="display: flex; align-items: center; gap: 1rem;">
		<a href="/places" class="text-muted hover:text-ink transition-colors">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
		</a>
		<h1 class="text-xl font-semibold truncate">{p.name}</h1>
		{#if p.category}
			<span class="px-2 py-0.5 text-xs rounded-full bg-surface-2 text-muted flex-shrink-0">{p.category}</span>
		{/if}
	</header>

	<div class="max-w-4xl mx-auto px-4 py-6 space-y-8">
		<!-- Place info + stats -->
		<section>
			<p class="text-muted">{p.address}</p>

			<div class="mt-4 grid gap-4" style="grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));">
				<!-- Overall rating -->
				<div class="p-4 rounded-lg bg-bg border border-line text-center">
					{#if stats.reviewCount > 0}
						<div class="text-3xl font-bold text-ink">{stats.avgRating.toFixed(1)}</div>
						<div class="text-ink text-lg">{renderStars(stats.avgRating)}</div>
						<div class="text-xs text-muted mt-1">{stats.reviewCount} {stats.reviewCount === 1 ? 'review' : 'reviews'}</div>
					{:else}
						<div class="text-lg text-subtle">No ratings</div>
						<div class="text-xs text-subtle mt-1">Leave a review</div>
					{/if}
				</div>

				<!-- WiFi -->
				<div class="p-4 rounded-lg bg-bg border border-line text-center">
					<div class="text-sm font-medium text-ink mb-1">WiFi</div>
					{#if stats.wifiCount > 0}
						<div class="text-2xl font-bold text-ink">{stats.avgWifi.toFixed(1)}<span class="text-sm text-subtle">/5</span></div>
						<div class="text-xs text-muted mt-1">{stats.wifiCount} {stats.wifiCount === 1 ? 'rating' : 'ratings'}</div>
					{:else}
						<div class="text-subtle">Unknown</div>
					{/if}
				</div>

				<!-- Noise -->
				<div class="p-4 rounded-lg bg-bg border border-line text-center">
					<div class="text-sm font-medium text-ink mb-1">Noise</div>
					{#if dominantNoise}
						<div class="text-2xl font-bold capitalize text-ink">{dominantNoise}</div>
						<div class="text-xs text-muted mt-1">
							{stats.noiseCounts.quiet}q / {stats.noiseCounts.moderate}m / {stats.noiseCounts.noisy}n
						</div>
					{:else}
						<div class="text-subtle">Unknown</div>
					{/if}
				</div>

				<!-- Outlets -->
				<div class="p-4 rounded-lg bg-bg border border-line text-center">
					<div class="text-sm font-medium text-ink mb-1">Outlets</div>
					{#if stats.outletTotal > 0}
						<div class="text-2xl font-bold text-ink">{Math.round((stats.outletYes / stats.outletTotal) * 100)}%</div>
						<div class="text-xs text-muted mt-1">say yes ({stats.outletYes}/{stats.outletTotal})</div>
					{:else}
						<div class="text-subtle">Unknown</div>
					{/if}
				</div>
			</div>
		</section>

		<!-- Tags -->
		<section>
			<h2 class="text-lg font-semibold mb-3">Tags</h2>
			<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;">
				{#each data.tags as tag (tag.id)}
					<form method="POST" action="?/voteTag" use:enhance>
						<input type="hidden" name="tagId" value={tag.id} />
						<button
							type="submit"
							class="px-3 py-1 text-sm rounded-full border border-line text-ink hover:border-brand hover:bg-brand-soft transition-colors"
							title="Vote for this tag"
						>
							{tag.tag} <span class="text-xs text-subtle ml-1">{tag.votes}</span>
						</button>
					</form>
				{/each}
				<!-- Add tag inline -->
				<form method="POST" action="?/addTag" use:enhance style="display: flex; gap: 0.25rem;">
					<input
						type="text"
						name="tag"
						bind:value={newTag}
						placeholder="Add tag..."
						class="px-2 py-1 text-sm border border-line rounded-full bg-surface text-ink focus:ring-1 focus:ring-brand"
						style="width: 7rem;"
					/>
					<button
						type="submit"
						disabled={!newTag.trim()}
						class="px-2 py-1 text-sm text-brand hover:text-brand disabled:text-subtle disabled:cursor-not-allowed"
					>+</button>
				</form>
			</div>
		</section>

		<!-- Active post-ups -->
		<section>
			<h2 class="text-lg font-semibold mb-3">
				Posting up now
				{#if data.activePosts.length > 0}
					<span class="text-sm font-normal text-muted ml-1">({data.activePosts.length})</span>
				{/if}
			</h2>
			{#if data.activePosts.length > 0}
				<div class="space-y-2">
					{#each data.activePosts as postItem (postItem.id)}
						<div class="p-3 border border-line rounded-md bg-bg">
							<p class="font-medium text-ink">{postItem.name}</p>
							<p class="text-sm text-muted mt-0.5">{postItem.activity}</p>
							<p class="text-xs text-muted mt-1">
								{postItem.hours} {postItem.hours === 1 ? 'hour' : 'hours'} &middot;
								started {timeAgo(postItem.startTime)}
							</p>
						</div>
					{/each}
				</div>
			{:else}
				<p class="text-sm text-muted italic">No one is posting up here right now.</p>
			{/if}
		</section>

		<!-- Reviews -->
		<section>
			<div style="display: flex; align-items: center; justify-content: space-between;" class="mb-3">
				<h2 class="text-lg font-semibold">Reviews</h2>
				<button
					type="button"
					onclick={() => showReviewForm = !showReviewForm}
					class="px-3 py-1.5 text-sm font-medium bg-brand text-on-brand rounded-md hover:bg-brand-hover transition-colors"
				>
					{showReviewForm ? 'Cancel' : 'Write a review'}
				</button>
			</div>

			<!-- Review form -->
			{#if showReviewForm}
				<div class="p-4 mb-4 border border-brand rounded-lg bg-brand-soft/50">
					<form method="POST" action="?/createReview" use:formEnhance class="space-y-4">
						<!-- Star rating -->
						<div>
							<label class="block text-sm font-medium text-ink mb-1">Rating *</label>
							<div style="display: flex; gap: 0.25rem;">
								{#each [1, 2, 3, 4, 5] as star}
									<button
										type="button"
										onclick={() => selectedRating = star}
										class="text-2xl transition-colors {selectedRating >= star ? 'text-ink' : 'text-subtle hover:text-ink'}"
									>&#9733;</button>
								{/each}
							</div>
							<input type="hidden" name="rating" value={$form.rating} />
							{#if $errors.rating}
								<p class="text-sm text-danger mt-1">{$errors.rating}</p>
							{/if}
						</div>

						<!-- Review text -->
						<div>
							<label for="review-text" class="block text-sm font-medium text-ink mb-1">Review</label>
							<textarea
								id="review-text"
								name="text"
								bind:value={$form.text}
								rows="3"
								placeholder="What was your experience like?"
								class="w-full px-3 py-2 border border-line rounded-md bg-surface text-ink focus:ring-2 focus:ring-brand"
							></textarea>
						</div>

						<!-- WiFi rating -->
						<div>
							<label class="block text-sm font-medium text-ink mb-1">WiFi quality</label>
							<div style="display: flex; gap: 0.25rem;">
								{#each [1, 2, 3, 4, 5] as star}
									<button
										type="button"
										onclick={() => selectedWifi = star}
										class="text-xl transition-colors {selectedWifi >= star ? 'text-brand' : 'text-subtle hover:text-brand'}"
									>&#9733;</button>
								{/each}
								{#if selectedWifi > 0}
									<button type="button" onclick={() => { selectedWifi = 0; $form.wifiRating = undefined; }} class="text-xs text-subtle ml-2 hover:text-muted">clear</button>
								{/if}
							</div>
							<input type="hidden" name="wifiRating" value={$form.wifiRating ?? ''} />
						</div>

						<!-- Noise level -->
						<div>
							<label class="block text-sm font-medium text-ink mb-1">Noise level</label>
							<div style="display: flex; gap: 0.5rem;">
								{#each ['quiet', 'moderate', 'noisy'] as level}
									<button
										type="button"
										onclick={() => $form.noiseLevel = $form.noiseLevel === level ? undefined : level as 'quiet' | 'moderate' | 'noisy'}
										class="px-3 py-1.5 text-sm rounded-md border transition-colors {$form.noiseLevel === level ? 'bg-brand-soft border-brand text-brand ' : 'border-line text-muted hover:border-line'}"
									>
										{level}
									</button>
								{/each}
							</div>
							<input type="hidden" name="noiseLevel" value={$form.noiseLevel ?? ''} />
						</div>

						<!-- Outlets -->
						<div>
							<label class="block text-sm font-medium text-ink mb-1">Power outlets?</label>
							<div style="display: flex; gap: 0.5rem;">
								<button
									type="button"
									onclick={() => $form.hasOutlets = $form.hasOutlets === true ? undefined : true}
									class="px-3 py-1.5 text-sm rounded-md border transition-colors {$form.hasOutlets === true ? 'bg-brand-soft border-live text-live ' : 'border-line text-muted hover:border-line'}"
								>Yes</button>
								<button
									type="button"
									onclick={() => $form.hasOutlets = $form.hasOutlets === false ? undefined : false}
									class="px-3 py-1.5 text-sm rounded-md border transition-colors {$form.hasOutlets === false ? 'bg-danger-soft border-danger text-danger ' : 'border-line text-muted hover:border-line'}"
								>No</button>
							</div>
							<input type="hidden" name="hasOutlets" value={$form.hasOutlets ?? ''} />
						</div>

						<button
							type="submit"
							disabled={selectedRating === 0}
							class="px-4 py-2 bg-brand text-on-brand rounded-md hover:bg-brand-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
						>
							Submit review
						</button>
					</form>
				</div>
			{/if}

			<!-- Reviews list -->
			{#if data.reviews.length > 0}
				<div class="space-y-3">
					{#each data.reviews as review (review.id)}
						<div class="p-4 border border-line rounded-lg bg-surface">
							<div style="display: flex; align-items: center; justify-content: space-between;">
								<div>
									<span class="text-ink">{renderStars(review.rating)}</span>
									<span class="text-xs text-muted ml-2">{timeAgo(review.createdAt)}</span>
								</div>
								{#if review.sessionId === data.anonymousSessionId}
									<form method="POST" action="?/deleteReview" use:enhance>
										<input type="hidden" name="reviewId" value={review.id} />
										<button type="submit" class="text-xs text-subtle hover:text-danger transition-colors" title="Delete review">
											<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
											</svg>
										</button>
									</form>
								{/if}
							</div>
							{#if review.text}
								<p class="text-ink mt-2">{review.text}</p>
							{/if}
							<div style="display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.5rem;" class="text-xs text-muted">
								{#if review.wifiRating != null}
									<span>WiFi: {review.wifiRating}/5</span>
								{/if}
								{#if review.noiseLevel}
									<span class="capitalize">Noise: {review.noiseLevel}</span>
								{/if}
								{#if review.hasOutlets != null}
									<span>Outlets: {review.hasOutlets ? 'Yes' : 'No'}</span>
								{/if}
							</div>
						</div>
					{/each}
				</div>
			{:else if !showReviewForm}
				<p class="text-sm text-muted italic">Leave a review: how is the wifi, noise and seating?</p>
			{/if}
		</section>
	</div>
</div>
