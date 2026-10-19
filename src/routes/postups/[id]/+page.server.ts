import { error } from '@sveltejs/kit';
import { getPostup } from '$lib/server/postup-manage';
import { myRequest, listRequests, approvedCount } from '$lib/server/join';
import { config } from '$lib/config';
import { isBlockedBetween } from '$lib/server/safety';
import { flag } from '$lib/flags';
import { getUserLocation } from '$lib/server/location';
import { isFollowing } from '$lib/server/profile';
import { db } from '$lib/server/db';
import { project } from '$lib/server/db/schema';
import { and, desc, eq } from 'drizzle-orm';
import { post } from '$lib/server/db/schema';
import { saveImage } from '$lib/server/uploads';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
	const { params, locals } = event;
	const p = await getPostup(Number(params.id));
	if (!p) error(404, 'This postup does not exist');
	const isOwner = !!locals.user && locals.user.id === p.userId;
	if (locals.user && p.userId && !isOwner && (await isBlockedBetween(locals.user.id, p.userId))) error(404, 'This postup does not exist');
	const mine = locals.user && !isOwner ? await myRequest(p.id, locals.user.id) : null;
	const approved = mine?.status === 'approved';
	// D2: in ask mode, non-approved viewers see the neighborhood, not the cafe.
	const hideCafe = config.askHidesCafe && p.joinMode === 'ask' && !isOwner && !approved;
	const area = p.neighborhood || p.locality || 'nearby';
	const view = {
		...p,
		placeName: hideCafe ? null : p.placeName,
		placeId: hideCafe ? null : p.placeId,
		location: hideCafe ? `a cafe in ${area}` : p.location,
		latitude: hideCafe ? null : p.latitude,
		longitude: hideCafe ? null : p.longitude,
		startTime: p.startTime.toISOString(),
		endsAt: p.endsAt.toISOString()
	};
	const joined = await approvedCount(p.id);
	const all = await listRequests(p.id);
	// Mockup "Jon is joining" stack and the owner's Joined list (approved only).
	const joiners = all.filter((r) => r.status === 'approved').map((r) => ({ id: r.id, name: r.name, avatarUrl: r.avatarUrl, at: r.createdAt.toISOString() }));
	const { location } = await getUserLocation(event);
	let miles: number | null = null;
	if (view.latitude != null && view.longitude != null) {
		const R = Math.PI / 180;
		miles = 3959 * Math.acos(Math.min(1, Math.cos(location.latitude * R) * Math.cos(view.latitude * R) * Math.cos((view.longitude - location.longitude) * R) + Math.sin(location.latitude * R) * Math.sin(view.latitude * R)));
	}
	return {
		title: `${p.displayName || p.name} at ${view.placeName || view.location}`,
		postup: view,
		hideCafe,
		isOwner,
		joinEnabled: flag('join'),
		chatEnabled: flag('chat'),
		shareEnabled: flag('share_links'),
		signedIn: !!locals.user,
		myRequest: mine ? { id: mine.id, status: mine.status } : null,
		requests: isOwner ? all.filter((r) => r.status === 'pending').map((r) => ({ ...r, createdAt: r.createdAt.toISOString() })) : [],
		joiners,
		// Mockup #postup / #postup-ask / #ask have no tab bar (the Join CTA sits at the bottom).
		noTabs: !isOwner && p.state === 'live' && (event.url.searchParams.get('view') === '1' || !(mine && (mine.status === 'approved' || mine.status === 'pending'))) && !(!!p.capacity && joined >= p.capacity && !mine),
		miles,
		center: view.latitude != null && view.longitude != null ? { latitude: view.latitude, longitude: view.longitude } : { latitude: config.launchArea.latitude, longitude: config.launchArea.longitude },
		following: locals.user && p.userId && !isOwner ? await isFollowing(locals.user.id, 'user', p.userId) : false,
		mine: isOwner ? await db.select({ id: project.id, name: project.name }).from(project).where(and(eq(project.userId, locals.user!.id), eq(project.active, true))).orderBy(desc(project.updatedAt)) : [],
		joinedCount: joined,
		full: !!p.capacity && joined >= p.capacity
	};
};

export const actions: Actions = {
	/** Mockup #posted "Add a photo of your spot": owner only, optional, after posting. */
	photo: async ({ params, locals, request }) => {
		const id = Number(params.id);
		const p = await getPostup(id);
		if (!p || !locals.user || p.userId !== locals.user.id) return fail(403, { message: 'Only the person who posted can add a photo' });
		try {
			const url = await saveImage((await request.formData()).get('photo'), 'postups');
			if (url) await db.update(post).set({ photoUrl: url }).where(eq(post.id, id));
		} catch (e) {
			return fail(400, { message: (e as Error).message });
		}
		return { photoSaved: true };
	}
};
