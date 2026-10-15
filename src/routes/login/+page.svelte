<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

	let { form }: { form: ActionData } = $props();
	let mode = $state<'login' | 'register'>('login');
</script>

<div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;" class="bg-surface px-4">
	<div class="w-full" style="max-width: 24rem;">
		<!-- Brand -->
		<div class="text-center mb-8">
			<a href="/" class="text-2xl font-semibold text-ink hover:opacity-80 transition-opacity">
				postup.now
			</a>
			<p class="mt-2 text-sm text-muted">
				{mode === 'login' ? 'Welcome back' : 'Create your account'}
			</p>
		</div>

		<!-- Card -->
		<div class="border border-line rounded-lg p-6 bg-surface">
			<!-- Mode Toggle -->
			<div class="flex mb-6 border-b border-line">
				<button
					type="button"
					onclick={() => mode = 'login'}
					class="flex-1 pb-3 text-sm font-medium border-b-2 transition-colors {mode === 'login'
						? 'border-brand text-brand '
						: 'border-transparent text-muted hover:text-ink '}"
				>
					Log in
				</button>
				<button
					type="button"
					onclick={() => mode = 'register'}
					class="flex-1 pb-3 text-sm font-medium border-b-2 transition-colors {mode === 'register'
						? 'border-brand text-brand '
						: 'border-transparent text-muted hover:text-ink '}"
				>
					Sign up
				</button>
			</div>

			<!-- Form -->
			<form method="POST" action={mode === 'login' ? '?/login' : '?/register'} use:enhance class="space-y-4">
				<div>
					<label for="username" class="block text-sm font-medium text-ink mb-1">
						Username
					</label>
					<input
						type="text"
						id="username"
						name="username"
						autocomplete="username"
						required
						minlength={3}
						maxlength={31}
						pattern="[a-z0-9_\-]+"
						class="w-full px-3 py-2 border border-line rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand bg-surface text-ink"
						placeholder="lowercase letters, numbers, _ -"
					/>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium text-ink mb-1">
						Password
					</label>
					<input
						type="password"
						id="password"
						name="password"
						autocomplete={mode === 'login' ? 'current-password' : 'new-password'}
						required
						minlength={6}
						maxlength={255}
						class="w-full px-3 py-2 border border-line rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-brand focus:border-brand bg-surface text-ink"
						placeholder={mode === 'login' ? 'Your password' : 'At least 6 characters'}
					/>
				</div>

				{#if form?.message}
					<p class="text-sm text-danger">{form.message}</p>
				{/if}

				<button
					type="submit"
					class="w-full px-4 py-2 bg-brand text-on-brand font-medium rounded-md hover:bg-brand-hover focus:outline-none focus:ring-2 focus:ring-brand focus:ring-offset-2 transition-colors"
				>
					{mode === 'login' ? 'Log in' : 'Create account'}
				</button>
			</form>
		</div>

		<!-- Footer link -->
		<p class="mt-4 text-center text-sm text-muted">
			{#if mode === 'login'}
				Don't have an account?
				<button type="button" onclick={() => mode = 'register'} class="text-brand hover:underline font-medium">Sign up</button>
			{:else}
				Already have an account?
				<button type="button" onclick={() => mode = 'login'} class="text-brand hover:underline font-medium">Log in</button>
			{/if}
		</p>
	</div>
</div>
