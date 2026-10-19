import { fail, redirect } from '@sveltejs/kit';
import { eq } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { user, block } from '$lib/server/db/schema';
import * as auth from '$lib/server/auth';
import { updateSettings, deleteAccount } from '$lib/server/profile';
import { unblockUser } from '$lib/server/safety';
import { prefsOf, NOTIFY_DEFAULTS, type NotifyPrefs } from '$lib/server/notify';
import type { Actions, PageServerLoad } from './$types';

/** Mockups #settings, #ov-delacct. Signed out keeps the screen; the sign-in sheet opens over it. */
export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user) return { title: 'Settings', signedIn: false as const, prefs: { ...NOTIFY_DEFAULTS } as NotifyPrefs, blocked: [] };
	const [u] = await db.select().from(user).where(eq(user.id, locals.user.id));
	const blocked = await db.select({ id: user.id, name: user.displayName, username: user.username }).from(block).innerJoin(user, eq(block.blockedId, user.id)).where(eq(block.blockerId, locals.user.id));
	return { title: 'Settings', signedIn: true as const, prefs: prefsOf(u.notifyPrefs), blocked };
};

export const actions: Actions = {
	save: async ({ locals, request }) => {
		if (!locals.user) return fail(401);
		const f = await request.formData();
		try {
			await updateSettings(locals.user.id, { displayName: String(f.get('displayName') ?? ''), bio: String(f.get('bio') ?? '') });
		} catch (e) {
			return fail(400, { message: (e as Error).message });
		}
		return { saved: true };
	},
	prefs: async ({ locals, request }) => {
		if (!locals.user) return fail(401);
		const f = await request.formData();
		const prefs = Object.fromEntries(Object.keys(NOTIFY_DEFAULTS).map((k) => [k, f.get(k) === 'on'])) as NotifyPrefs;
		await db.update(user).set({ notifyPrefs: prefs }).where(eq(user.id, locals.user.id));
		return { prefsSaved: true };
	},
	unblock: async ({ locals, request }) => {
		if (!locals.user) return fail(401);
		await unblockUser(locals.user.id, String((await request.formData()).get('userId')));
		return { unblocked: true };
	},
	signout: async (event) => {
		if (event.locals.session) await auth.invalidateSession(event.locals.session.id);
		auth.deleteSessionTokenCookie(event);
		redirect(302, '/');
	},
	delete: async (event) => {
		if (!event.locals.user) return fail(401);
		const f = await event.request.formData();
		if (f.get('confirm') !== 'DELETE') return fail(400, { message: 'Confirm to delete your account' });
		await deleteAccount(event.locals.user.id);
		auth.deleteSessionTokenCookie(event);
		redirect(302, '/?deleted=1');
	}
};
