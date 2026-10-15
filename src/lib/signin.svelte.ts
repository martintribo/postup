/** Global "Almost there" sign-in sheet, opened over the current screen. */
export const signin = $state({ open: false, title: 'Almost there', sub: 'Sign in to keep going.', next: '/' });

export function askSignIn(opts: { title?: string; sub?: string; next?: string } = {}) {
	signin.title = opts.title ?? 'Almost there';
	signin.sub = opts.sub ?? 'Sign in to keep going.';
	signin.next = opts.next ?? (typeof location !== 'undefined' ? location.pathname + location.search : '/');
	signin.open = true;
}
