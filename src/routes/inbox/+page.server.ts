import { error } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { inbox } from '$lib/server/chat';
import type { PageServerLoad } from './$types';

/** Mockup #inbox. Signed out keeps the screen; the page opens the sign-in sheet over it. */
export const load: PageServerLoad = async ({ locals }) => {
	if (!flag('chat')) error(404);
	return { title: 'Inbox', signedIn: !!locals.user, chats: locals.user ? await inbox(locals.user.id) : [] };
};
