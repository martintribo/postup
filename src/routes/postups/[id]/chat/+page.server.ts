import { error, redirect } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { listMessages, ChatError } from '$lib/server/chat';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals, url }) => {
	if (!flag('chat')) error(404);
	if (!locals.user) redirect(302, `/login?next=${encodeURIComponent(url.pathname)}`);
	try {
		const d = await listMessages(Number(params.id), locals.user.id);
		return { title: 'Chat', ...d, me: locals.user.id };
	} catch (e) {
		if (e instanceof ChatError) error(e.status, e.message);
		throw e;
	}
};
