import { sql } from 'drizzle-orm';
import { db } from '$lib/server/db';

/** First markdown image URL in a text (project covers and update photos live in markdown). */
export function firstImage(md: string | null | undefined): string | null {
	const m = /!\[[^\]]*\]\(([^)\s]+)\)/.exec(md ?? '');
	return m && m[1] !== 'placeholder' ? m[1] : null;
}
export function stripImages(md: string | null | undefined): string {
	return (md ?? '').replace(/!\[[^\]]*\]\([^)]*\)/g, '').trim();
}

export type ProjectCard = {
	id: number; name: string; type: string | null; short: string; cover: string | null;
	owner: string | null; ownerAvatar: string | null; lastUpdate: string | null; lastAt: string | null;
	cafe: string | null; week: number;
};

/** Projects grid (mockup #projects). filter: all | following | mine. */
export async function listProjectCards(filter: 'all' | 'following' | 'mine', viewerId?: string | null): Promise<ProjectCard[]> {
	const where =
		filter === 'mine' && viewerId ? sql`and p.user_id = ${viewerId}`
		: filter === 'following' && viewerId ? sql`and exists (select 1 from follow f where f.follower_id = ${viewerId} and f.target_type = 'project' and f.target_id = p.id::text)`
		: filter === 'all' ? sql`` : sql`and false`;
	const rows = (await db.execute(sql`
		select p.id, p.name, p.type, p.short_description as short, p.description,
			coalesce(u.display_name, u.username) as owner, u.avatar_url as "ownerAvatar",
			s.title as "lastTitle", s.body as "lastBody", s.occurred_at as "lastAt",
			(select pl.name from post po left join place pl on pl.id = po.place_id where po.project_id = p.id order by po.start_time desc limit 1) as cafe,
			(select po.location from post po where po.project_id = p.id order by po.start_time desc limit 1) as "cafeText",
			(select count(*)::int from post po where po.project_id = p.id and po.start_time > now() - interval '7 days') as week,
			greatest(p.updated_at, coalesce(s.occurred_at, p.updated_at), coalesce(p.last_post_up_at, p.updated_at)) as touched
		from project p left join "user" u on u.id = p.user_id
		left join lateral (select title, body, occurred_at from project_status where project_id = p.id order by occurred_at desc limit 1) s on true
		where p.hidden = false and p.active = true ${where}
		order by touched desc limit 60`)) as unknown as Record<string, any>[];
	return [...rows].map((r) => ({
		id: r.id, name: r.name, type: r.type, short: r.short,
		cover: firstImage(r.description) ?? firstImage(r.lastBody),
		owner: r.owner, ownerAvatar: r.ownerAvatar,
		lastUpdate: r.lastTitle || stripImages(r.lastBody) || null,
		lastAt: r.lastAt ? new Date(r.lastAt).toISOString() : null,
		cafe: r.cafe ?? r.cafeText ?? null, week: r.week ?? 0
	}));
}

/** "Yesterday", "Tue", "Oct 9". */
export function dayLabel(iso: string | null, now = new Date()): string {
	if (!iso) return '';
	const d = new Date(iso);
	const days = Math.floor((new Date(now.toDateString()).getTime() - new Date(d.toDateString()).getTime()) / 864e5);
	if (days <= 0) return 'Today';
	if (days === 1) return 'Yesterday';
	if (days < 7) return d.toLocaleDateString('en-US', { weekday: 'short' });
	return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}
