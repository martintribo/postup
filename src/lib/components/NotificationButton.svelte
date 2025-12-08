<script lang="ts">
	import { onMount } from 'svelte';
	
	let isSubscribed = $state(false);
	let isSupported = $state(false);
	let isLoading = $state(false);
	let registration: ServiceWorkerRegistration | null = $state(null);
	let subscription: PushSubscription | null = $state(null);
	
	onMount(async () => {
		// Check if browser supports notifications
		if (!('Notification' in window) || !('serviceWorker' in navigator) || !('PushManager' in window)) {
			isSupported = false;
			return;
		}
		
		isSupported = true;
		
		try {
			// Register service worker
			const reg = await navigator.serviceWorker.register('/sw.js');
			registration = reg;
			
			// Check current subscription status
			const sub = await reg.pushManager.getSubscription();
			subscription = sub;
			isSubscribed = !!sub;
		} catch (error) {
			console.error('Error registering service worker:', error);
		}
	});
	
	async function toggleSubscription() {
		if (!registration || !isSupported) return;
		
		isLoading = true;
		
		try {
			if (isSubscribed && subscription) {
				// Unsubscribe
				await subscription.unsubscribe();
				await fetch('/api/notifications/unsubscribe', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ endpoint: subscription.endpoint })
				});
				subscription = null;
				isSubscribed = false;
			} else {
				// Request notification permission first
				const permission = await Notification.requestPermission();
				if (permission !== 'granted') {
					throw new Error('Notification permission denied');
				}
				
				// Subscribe
				const response = await fetch('/api/notifications/vapid-public-key');
				const { publicKey } = await response.json();
				
				if (!publicKey) {
					throw new Error('VAPID public key not available');
				}
				
				const sub = await registration.pushManager.subscribe({
					userVisibleOnly: true,
					applicationServerKey: urlBase64ToUint8Array(publicKey)
				});
				
				subscription = sub;
				
				// Send subscription to server
				const subscriptionData = {
					endpoint: sub.endpoint,
					keys: {
						p256dh: arrayBufferToBase64(sub.getKey('p256dh')!),
						auth: arrayBufferToBase64(sub.getKey('auth')!)
					}
				};
				
				await fetch('/api/notifications/subscribe', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify(subscriptionData)
				});
				
				isSubscribed = true;
			}
		} catch (error) {
			console.error('Error toggling subscription:', error);
			alert('Failed to toggle notifications. Please try again.');
		} finally {
			isLoading = false;
		}
	}
	
	function urlBase64ToUint8Array(base64String: string): Uint8Array {
		const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
		const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
		const rawData = window.atob(base64);
		const outputArray = new Uint8Array(rawData.length);
		
		for (let i = 0; i < rawData.length; ++i) {
			outputArray[i] = rawData.charCodeAt(i);
		}
		return outputArray;
	}
	
	function arrayBufferToBase64(buffer: ArrayBuffer): string {
		const bytes = new Uint8Array(buffer);
		let binary = '';
		for (let i = 0; i < bytes.byteLength; i++) {
			binary += String.fromCharCode(bytes[i]);
		}
		return window.btoa(binary);
	}
</script>

{#if isSupported}
	<button
		onclick={toggleSubscription}
		disabled={isLoading}
		class="relative p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
		title={isSubscribed ? 'Disable notifications' : 'Enable notifications'}
	>
		{#if isLoading}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-6 w-6 animate-spin"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
				/>
			</svg>
		{:else if isSubscribed}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-6 w-6"
				fill="currentColor"
				viewBox="0 0 24 24"
			>
				<path
					d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"
				/>
			</svg>
		{:else}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-6 w-6"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="2"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
				/>
			</svg>
		{/if}
	</button>
{/if}

