import { error } from '@sveltejs/kit';
import { and, desc, eq, sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { project, projectStatus, user, post, place } from '$lib/server/db/schema';
import { liveCondition } from '$lib/server/postups';
import { firstImage, stripImages, dayLabel } from '$lib/server/projects-view';
import type { PageServerLoad } from './$types';
import { isFollowing } from '$lib/server/profile';

/** Project page + shared-project landing (mockups #project, #invite-project). */
export const load: PageServerLoad = async ({ params, locals, url }) => {
	const id = Number(params.id);
	if (!Number.isInteger(id)) error(404, 'Project not found');
	const [p] = await db
		.select({ id: project.id, name: project.name, type: project.type, short: project.shortDescription, description: project.description, hidden: project.hidden, userId: project.userId, owner: sql<string | null>`coalesce(${user.displayName}, ${user.username})`, ownerUsername: user.username, ownerAvatar: user.avatarUrl })
		.from(project)
		.leftJoin(user, eq(project.userId, user.id))
		.where(eq(project.id, id));
	if (!p || p.hidden) error(404, 'Project not found');
	const updates = await db
		.select({ id: projectStatus.id, title: projectStatus.title, body: projectStatus.body, at: projectStatus.occurredAt, placeId: sql<number | null>`(select po.place_id from post po where po.project_id = ${id} and po.start_time <= ${projectStatus.occurredAt} + interval '6 hours' and coalesce(po.ends_at, po.start_time + (po.hours || ' hours')::interval) >= ${projectStatus.occurredAt} - interval '1 hour' order by po.start_time desc limit 1)`, placeName: sql<string | null>`(select coalesce(pl.name, po.location) from post po left join place pl on pl.id = po.place_id where po.project_id = ${id} and po.start_time <= ${projectStatus.occurredAt} + interval '6 hours' and coalesce(po.ends_at, po.start_time + (po.hours || ' hours')::interval) >= ${projectStatus.occurredAt} - interval '1 hour' order by po.start_time desc limit 1)` })
		.from(projectStatus)
		.where(eq(projectStatus.projectId, id))
		.orderBy(desc(projectStatus.occurredAt))
		.limit(30);
	const live = await db
		.select({ id: post.id, who: sql<string>`coalesce(${user.displayName}, ${user.username}, ${post.name})`, avatarUrl: user.avatarUrl, cafe: sql<string>`coalesce(${place.name}, ${post.location})`, placeId: post.placeId, endsAt: post.endsAt, startTime: post.startTime, hours: post.hours })
		.from(post)
		.leftJoin(user, eq(post.userId, user.id))
		.leftJoin(place, eq(post.placeId, place.id))
		.where(and(eq(post.projectId, id), liveCondition))
		.orderBy(desc(post.startTime));
	const [counts] = (await db.execute(sql`
		select count(*)::int as total,
			count(*) filter (where start_time > now() - interval '7 days')::int as week,
			(array_agg(distinct coalesce(u.display_name, u.username, po.name)) filter (where po.start_time > now() - interval '7 days'))[1:3] as who,
			(select coalesce(pl.name, p2.location) from post p2 left join place pl on pl.id = p2.place_id where p2.project_id = ${id} and p2.start_time > now() - interval '7 days' group by 1 order by count(*) desc limit 1) as "weekCafe"
		from post po left join "user" u on u.id = po.user_id where po.project_id = ${id}`)) as unknown as { total: number; week: number; who: string[] | null; weekCafe: string | null }[];
	const owner = !!locals.user && locals.user.id === p.userId;
	const end = (r: (typeof live)[number]) => r.endsAt ?? new Date(r.startTime.getTime() + r.hours * 3600e3);
	return {
		title: p.owner ? `${p.owner} is building ${p.name}` : p.name,
		description: p.short || `${p.name} on PostUp`,
		project: { id: p.id, name: p.name, type: p.type, short: p.short, about: stripImages(p.description) || p.short, cover: firstImage(p.description) ?? updates.map((u) => firstImage(u.body)).find(Boolean) ?? null, owner: p.owner, ownerUsername: p.ownerUsername, ownerAvatar: p.ownerAvatar },
		isOwner: owner,
		landing: !locals.user && url.searchParams.has('s'),
		// Mockup #invite-project is a landing: no tab bar.
		noTabs: !locals.user && url.searchParams.has('s'),
		signedIn: !!locals.user,
		following: locals.user ? await isFollowing(locals.user.id, 'project', String(id)) : false,
		stats: { total: counts?.total ?? 0, week: counts?.week ?? 0, who: counts?.who ?? [], weekCafe: counts?.weekCafe ?? null },
		live: live.map((r) => ({ id: r.id, who: r.who, avatarUrl: r.avatarUrl, cafe: r.cafe, placeId: r.placeId, endsAt: end(r).toISOString() })),
		liveId: live[0]?.id ?? null,
		updates: updates.map((u) => ({ id: u.id, title: u.title, body: stripImages(u.body), image: firstImage(u.body), at: u.at.toISOString(), when: dayLabel(u.at.toISOString()), placeName: u.placeName, placeId: u.placeId }))
	};
};
