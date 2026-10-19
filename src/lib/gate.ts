import { askSignIn } from '$lib/signin.svelte';

/** Signed-out account screens keep their screen and put the sign-in sheet over it (mockup scenarios "gate"). */
export const GATES = {
	inbox: { title: 'Your inbox', sub: 'Sign in to see your chats and activity.' },
	chat: { title: 'Join the chat', sub: "Sign in to see this postup's chat." },
	me: { title: 'Your profile', sub: 'Sign in to see your profile.' },
	settings: { title: 'Settings', sub: 'Sign in to change your settings.' },
	report: { title: 'Report', sub: 'Sign in to send a report.' }
} as const;

export function gate(kind: keyof typeof GATES, next: string) {
	askSignIn({ ...GATES[kind], next });
}
