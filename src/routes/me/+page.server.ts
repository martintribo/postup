import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

/** Mockup #me. Signed in: your profile page. Signed out: the screen stays and the sign-in sheet opens over it. */
export const load: PageServerLoad = ({ locals }) => {
	if (locals.user) redirect(302, `/u/${locals.user.username}`);
	return { title: 'Your profile' };
};
