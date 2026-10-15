// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		interface Locals {
			user: import('$lib/server/auth').SessionValidationResult['user'];
			session: import('$lib/server/auth').SessionValidationResult['session'];
			anonymousSessionId: string;
			agent: {
				userId: string;
				agentSessionId: string;
				tokenId: string;
				scope: import('$lib/server/auth').AgentScope;
			} | null;
		}
	} // interface Error {}
	// interface Locals {}
} // interface PageData {}
// interface PageState {}

// interface Platform {}

declare module 'svelte/elements' {
	export interface SvelteHTMLElements {
		'gmp-place-details-compact': import('svelte/elements').HTMLAttributes<HTMLElement> & {
			orientation?: 'horizontal' | 'vertical' | 'HORIZONTAL' | 'VERTICAL';
			'truncation-preferred'?: boolean;
		};
		'gmp-place-details-place-request': import('svelte/elements').HTMLAttributes<HTMLElement> & {
			place?: string;
		};
		'gmp-place-content-config': import('svelte/elements').HTMLAttributes<HTMLElement>;
		'gmp-place-media': import('svelte/elements').HTMLAttributes<HTMLElement> & {
			'lightbox-preferred'?: boolean;
			'preferred-size'?: 'SMALL' | 'MEDIUM' | 'LARGE';
		};
		'gmp-place-rating': import('svelte/elements').HTMLAttributes<HTMLElement>;
		'gmp-place-type': import('svelte/elements').HTMLAttributes<HTMLElement>;
		'gmp-place-price': import('svelte/elements').HTMLAttributes<HTMLElement>;
		'gmp-place-accessible-entrance-icon': import('svelte/elements').HTMLAttributes<HTMLElement>;
		'gmp-place-open-now-status': import('svelte/elements').HTMLAttributes<HTMLElement>;
		'gmp-place-attribution': import('svelte/elements').HTMLAttributes<HTMLElement> & {
			'light-scheme-color'?: string;
			'dark-scheme-color'?: string;
		};
	}
}

export {};
