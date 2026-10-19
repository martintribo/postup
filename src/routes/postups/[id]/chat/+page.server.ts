import { error } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { listMessages, ChatError } from '$lib/server/chat';
import type { PageServerLoad } from './$types';

/** Mockup #chat. Signed out keeps the screen and the page opens the sign-in sheet ("Join the chat"). */
export const load: PageServerLoad = async ({ params, locals }) => {
	if (!flag('chat')) error(404);
	if (!locals.user) return { title: 'Chat', signedIn: false as const, postId: Number(params.id) };
	try {
		const d = await listMessages(Number(params.id), locals.user.id);
		return { title: 'Chat', signedIn: true as const, postId: Number(params.id), ...d, me: locals.user.id, noTabs: true };
	} catch (e) {
		if (e instanceof ChatError) error(e.status, e.message);
		throw e;
	}
};
