import { error } from '@sveltejs/kit';
import { eq, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { user } from '$lib/server/db/schema';
import type { PageServerLoad } from './$types';

const TYPES = ['post', 'user', 'message', 'project'] as const;

/** Mockups #report → #reported. /report?type=post|user|message|project&id=…&uid=<person>&back=<path>. */
export const load: PageServerLoad = async ({ url, locals }) => {
	const type = url.searchParams.get('type') ?? '';
	const id = url.searchParams.get('id') ?? '';
	if (!(TYPES as readonly string[]).includes(type) || !id) error(404, 'Nothing to report');
	const uid = url.searchParams.get('uid');
	let name: string | null = null;
	if (uid) [{ name } = { name: null }] = await db.select({ name: sql<string>`coalesce(${user.displayName}, ${user.username})` }).from(user).where(eq(user.id, uid));
	const back = url.searchParams.get('back');
	return {
		title: 'Report',
		noTabs: true,
		signedIn: !!locals.user,
		target: { type, id, uid: uid && uid !== locals.user?.id ? uid : null, name },
		back: back && back.startsWith('/') && !back.startsWith('//') ? back : '/'
	};
};
