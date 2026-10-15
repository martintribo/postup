import { error, redirect } from '@sveltejs/kit';
import { flag } from '$lib/flags';
import { inbox } from '$lib/server/chat';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!flag('chat')) error(404);
	if (!locals.user) redirect(302, `/login?next=${encodeURIComponent(url.pathname)}`);
	return { title: 'Inbox', chats: await inbox(locals.user.id) };
};
