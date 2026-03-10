<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

	let { form }: { form: ActionData } = $props();
	let mode = $state<'login' | 'register'>('login');
</script>

<div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;" class="bg-white dark:bg-gray-900 px-4">
	<div class="w-full" style="max-width: 24rem;">
		<!-- Brand -->
		<div class="text-center mb-8">
			<a href="/" class="text-2xl font-semibold text-gray-900 dark:text-gray-100 hover:opacity-80 transition-opacity">
				postup.now
			</a>
			<p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
				{mode === 'login' ? 'Welcome back' : 'Create your account'}
			</p>
		</div>

		<!-- Card -->
		<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
			<!-- Mode Toggle -->
			<div class="flex mb-6 border-b border-gray-200 dark:border-gray-700">
				<button
					type="button"
					onclick={() => mode = 'login'}
					class="flex-1 pb-3 text-sm font-medium border-b-2 transition-colors {mode === 'login'
						? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
						: 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
				>
					Log in
				</button>
				<button
					type="button"
					onclick={() => mode = 'register'}
					class="flex-1 pb-3 text-sm font-medium border-b-2 transition-colors {mode === 'register'
						? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400'
						: 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
				>
					Sign up
				</button>
			</div>

			<!-- Form -->
			<form method="POST" action={mode === 'login' ? '?/login' : '?/register'} use:enhance class="space-y-4">
				<div>
					<label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
						placeholder="lowercase letters, numbers, _ -"
					/>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
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
						class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
						placeholder={mode === 'login' ? 'Your password' : 'At least 6 characters'}
					/>
				</div>

				{#if form?.message}
					<p class="text-sm text-red-600 dark:text-red-400">{form.message}</p>
				{/if}

				<button
					type="submit"
					class="w-full px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
				>
					{mode === 'login' ? 'Log in' : 'Create account'}
				</button>
			</form>
		</div>

		<!-- Footer link -->
		<p class="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
			{#if mode === 'login'}
				Don't have an account?
				<button type="button" onclick={() => mode = 'register'} class="text-blue-600 dark:text-blue-400 hover:underline font-medium">Sign up</button>
			{:else}
				Already have an account?
				<button type="button" onclick={() => mode = 'login'} class="text-blue-600 dark:text-blue-400 hover:underline font-medium">Log in</button>
			{/if}
		</p>
	</div>
</div>
