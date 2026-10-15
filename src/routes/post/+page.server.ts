import { fail, redirect } from '@sveltejs/kit';
import { and, desc, eq, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { post, project } from '$lib/server/db/schema';
import { getUserLocation, reverseGeocode } from '$lib/server/location';
import { computeEndsAt, upsertGooglePlace } from '$lib/server/postups';
import { config } from '$lib/config';
import type { Actions, PageServerLoad } from './$types';

/** Post-up form (mockups #post, #where, #post-signin, #project-attach). Signed-out visitors can fill it; the sign-in sheet opens on submit. */
export const load: PageServerLoad = async (event) => {
	const { location } = await getUserLocation(event);
	const lat = location.latitude, lng = location.longitude;
	const dist = sql<number>`(3959 * acos(least(1, cos(radians(${lat})) * cos(radians(pl.latitude)) * cos(radians(pl.longitude) - radians(${lng})) + sin(radians(${lat})) * sin(radians(pl.latitude)))))`;
	const places = [...((await db.execute(sql`
		select pl.id, pl.name, pl.latitude, pl.longitude, ${dist} as mi,
			(select count(*)::int from post p where p.place_id = pl.id and p.status = 'live' and coalesce(p.ends_at, p.start_time + (p.hours || ' hours')::interval) > now()) as live
		from place pl order by mi asc limit 12`)) as unknown as { id: number; name: string; latitude: number; longitude: number; mi: number; live: number }[])];
	const user = event.locals.user;
	const mine = user
		? await db.select({ id: project.id, name: project.name }).from(project).where(and(eq(project.userId, user.id), eq(project.active, true))).orderBy(desc(project.updatedAt))
		: [];
	const pid = Number(event.url.searchParams.get('project'));
	let attach: { id: number; name: string } | null = null;
	if (pid) {
		const [p] = await db.select({ id: project.id, name: project.name }).from(project).where(eq(project.id, pid));
		attach = p ?? null;
	}
	return { title: 'Post up', places, mine, attach, location, signedIn: !!user, defaultJoin: config.defaultJoinMode, placeId: Number(event.url.searchParams.get('place')) || null };
};

export const actions: Actions = {
	default: async (event) => {
		const user = event.locals.user;
		if (!user) return fail(401, { message: 'Sign in to post up' });
		const f = await event.request.formData();
		const activity = String(f.get('activity') ?? '').trim();
		const until = String(f.get('until') ?? '2h');
		const when = String(f.get('when') ?? 'now');
		const joinMode = f.get('join') === 'ask' ? 'ask' : 'open';
		const projectId = Number(f.get('projectId')) || null;
		let placeId = Number(f.get('placeId')) || null;
		const name = String(f.get('placeName') ?? '').trim();
		const latitude = Number(f.get('latitude')), longitude = Number(f.get('longitude'));
		const googlePlaceId = String(f.get('googlePlaceId') ?? '') || null;
		if (!name || !Number.isFinite(latitude) || !Number.isFinite(longitude)) return fail(400, { message: 'Pick where you are' });
		if (!activity && !projectId) return fail(400, { message: 'Say what you are working on' });
		if (!placeId && googlePlaceId) placeId = await upsertGooglePlace({ googlePlaceId, name, latitude, longitude }, user.id);

		const now = new Date();
		let hours = Number(/^(\d)h$/.exec(until)?.[1] ?? 0);
		let endsAt: Date;
		if (hours) endsAt = computeEndsAt(now, hours);
		else {
			// "until 4pm" style: the next round hour at least 30 min out, sent as an ISO time from the client.
			const t = new Date(String(f.get('untilAt') ?? ''));
			endsAt = Number.isFinite(t.getTime()) && t > now ? t : computeEndsAt(now, 2);
			hours = Math.max(1, Math.ceil((endsAt.getTime() - now.getTime()) / 3600e3));
		}
		const earlier = when === 'earlier';
		const start = earlier ? new Date(now.getTime() - hours * 3600e3) : now;
		if (earlier) endsAt = now;
		let projName: string | null = null;
		if (projectId) [{ name: projName } = { name: null }] = await db.select({ name: project.name }).from(project).where(eq(project.id, projectId));
		const geo = await reverseGeocode(latitude, longitude).catch(() => ({ neighborhood: null, locality: null, district: null }));
		const [row] = await db
			.insert(post)
			.values({
				userId: user.id, name: user.username, activity: activity || `Working on ${projName ?? 'a project'}`,
				location: name, latitude, longitude, hours, placeId, projectId, joinMode,
				startTime: start, endsAt, status: earlier ? 'ended' : 'live',
				neighborhood: geo.neighborhood, locality: geo.locality, district: geo.district, sessionId: event.locals.session?.id
			})
			.returning();
		if (projectId) await db.update(project).set({ lastPostUpAt: now }).where(eq(project.id, projectId));
		redirect(303, earlier ? `/projects/${projectId}` : `/postups/${row.id}?posted=1`);
	}
};
