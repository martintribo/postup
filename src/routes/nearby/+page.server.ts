import { sql } from 'drizzle-orm';
import { db } from '$lib/server/db';
import { getNearbyFeed } from '$lib/server/feed';
import { listProjectCards, dayLabel } from '$lib/server/projects-view';
import { config } from '$lib/config';
import { getUserLocation } from '$lib/server/location';
import type { PageServerLoad } from './$types';

const miles = (lat: number, lng: number) =>
	sql`(3959 * acos(least(1, cos(radians(${lat})) * cos(radians(pl.latitude)) * cos(radians(pl.longitude) - radians(${lng})) + sin(radians(${lat})) * sin(radians(pl.latitude)))))`;

export const load: PageServerLoad = async (event) => {
	const { location } = await getUserLocation(event);
	const { latitude: lat, longitude: lng } = location;
	const feed = await getNearbyFeed(lat, lng, 30, event.locals.user?.id);
	// Mockup #quiet-feed: the photo feed runs while someone nearby is live. Nobody live (or nothing
	// this week): fall back to projects in general, closest first, never an empty screen.
	const anyLive = feed.items.some((i) => i.kind === 'postup' && i.live);
	const projects = anyLive ? [] : (await listProjectCards('all', event.locals.user?.id, { lat, lng })).slice(0, 12).map((c) => ({ ...c, when: dayLabel(c.lastAt) }));
	// Sidebar (desktop): cafes with postups this week.
	const week = (await db.execute(sql`
		select pl.id, pl.name, count(*)::int as n,
			(array_agg(coalesce(u.display_name, u.username, p.name) order by p.start_time desc))[1:3] as who
		from post p join place pl on pl.id = p.place_id left join "user" u on u.id = p.user_id
		where p.start_time > now() - interval '7 days' and p.join_mode <> 'ask' and p.status <> 'cancelled' and ${miles(lat, lng)} <= 25
		group by pl.id, pl.name order by n desc limit 3`)) as unknown as { id: number; name: string; n: number; who: string[] }[];
	// Empty area (mockup #empty-area): the two closest cafes to start at.
	const cafes = !anyLive && !projects.length
		? ((await db.execute(sql`select pl.id, pl.name, ${miles(lat, lng)} as mi from place pl order by mi asc limit 2`)) as unknown as { id: number; name: string; mi: number }[])
		: [];
	const who = [...new Set(feed.items.flatMap((i) => (i.kind === 'postup' ? [i.who] : [])))].slice(0, 4);
	const items = feed.items.map((i) => ({ ...i, when: i.kind === 'postup' && i.live ? 'Now' : dayLabel(i.at) }));
	return { title: 'Nearby', items, weekCount: feed.weekCount, anyLive, projects, week: [...week], cafes: [...cafes], who, area: location.city || config.launchArea.name };
};
