#!/usr/bin/env node
/**
 * Import real dev data from the old worktrees (projects-agent, places-photos) into THIS
 * worktree's dev DB, whatever phase schema it has. Idempotent: re-running skips rows
 * already imported (tracked in table import_map). DEV ONLY: refuses prod-looking URLs.
 *
 *   DATABASE_URL=postgres://...worktree-db  \
 *   IMPORT_SOURCES="projects=postgres://.../postup_import_projects,photos=postgres://.../postup_import_photos" \
 *   [IMPORT_UPLOADS_DIR=/path/to/old/static/uploads]   # copied into static/uploads/import/<source>/
 *   [IMPORT_PHOTOS_DIR=/path/to/old/PHOTO_ARCHIVE_DIR] # copied into static/uploads/import/photos-archive/
 *   [IMPORT_KEEP_PASSWORDS=1]                          # keep password hashes (dev only); default: accounts get no password
 *   node scripts/import-dev-data.mjs [--dry-run]
 *
 * Mapping: for each table, only columns present in BOTH source and target are copied.
 * Required target columns the source lacks get sensible fills (timestamps from created_at/now,
 * post.ends_at = start_time + hours, post.status from ends_at, enums -> first label, etc.).
 * Serial ids are re-assigned and foreign keys remapped, so seeded test rows never collide.
 * Never copied: session, agent_token, oauth_account, device_token (secrets / per-device).
 */
import postgres from 'postgres';
import { cp, mkdir, stat } from 'node:fs/promises';
import path from 'node:path';

const DRY = process.argv.includes('--dry-run');
const target = process.env.DATABASE_URL;
const sources = Object.fromEntries(
	(process.env.IMPORT_SOURCES || '').split(',').filter(Boolean).map((s) => {
		const i = s.indexOf('=');
		return [s.slice(0, i), s.slice(i + 1)];
	})
);
if (!target || !Object.keys(sources).length) {
	console.error('Set DATABASE_URL and IMPORT_SOURCES (see header).');
	process.exit(2);
}
for (const u of [target, ...Object.values(sources)]) {
	if (/neon\.tech|vercel|amazonaws|supabase|prod/i.test(u)) {
		console.error('Refusing: this looks like a production database URL:', u.replace(/:[^:@/]*@/, ':***@'));
		process.exit(3);
	}
}

// Table order respects foreign keys. fk: column -> referenced table (serial ids get remapped).
const TABLES = [
	{ t: 'user', key: 'id', text: true },
	{ t: 'place', fk: {} },
	{ t: 'project', fk: {} },
	{ t: 'project_status', fk: { project_id: 'project' } },
	{ t: 'project_change', fk: { target_project_id: 'project' } },
	{ t: 'place_review', fk: { place_id: 'place' } },
	{ t: 'place_tag', fk: { place_id: 'place' } },
	{ t: 'post', fk: { place_id: 'place', project_id: 'project' } }
];
const USER_FK = ['user_id', 'created_by'];

const dst = postgres(target, { max: 1, onnotice: () => {} });

async function columns(sql, table) {
	return sql`
		select c.column_name, c.is_nullable, c.column_default, c.data_type, c.udt_name
		from information_schema.columns c
		where c.table_schema = 'public' and c.table_name = ${table}`;
}
async function enumLabels(udt) {
	const r = await dst`select e.enumlabel from pg_enum e join pg_type t on t.oid = e.enumtypid where t.typname = ${udt} order by e.enumsortorder`;
	return r.map((x) => x.enumlabel);
}

async function main() {
	if (!DRY) {
		await dst`create table if not exists import_map (
			source text not null, tbl text not null, src_id text not null, dst_id text not null,
			primary key (source, tbl, src_id))`;
	}
	const report = [];
	for (const [source, url] of Object.entries(sources)) {
		const src = postgres(url, { max: 1, onnotice: () => {} });
		const idMap = {}; // tbl -> Map(srcId -> dstId)
		const loadMap = async (tbl) => {
			if (idMap[tbl]) return idMap[tbl];
			const m = new Map();
			if (!DRY) for (const r of await dst`select src_id, dst_id from import_map where source = ${source} and tbl = ${tbl}`) m.set(r.src_id, r.dst_id);
			return (idMap[tbl] = m);
		};
		for (const spec of TABLES) {
			const sCols = await columns(src, spec.t);
			const dCols = await columns(dst, spec.t);
			if (!sCols.length || !dCols.length) {
				report.push(`${source}.${spec.t}: skipped (${!sCols.length ? 'not in source' : 'not in this phase'})`);
				continue;
			}
			const sNames = new Set(sCols.map((c) => c.column_name));
			const map = await loadMap(spec.t);
			const rows = await src`select * from ${src(spec.t)} order by 1`;
			let added = 0, skipped = 0;
			for (const row of rows) {
				const srcId = String(row.id);
				if (map.has(srcId)) { skipped++; continue; }
				const out = {};
				for (const c of dCols) {
					const n = c.column_name;
					if (n === 'id' && !spec.text) continue; // serial: let target assign
					if (sNames.has(n)) out[n] = row[n];
				}
				// remap foreign keys
				for (const [col, ref] of Object.entries(spec.fk || {})) {
					if (out[col] == null) continue;
					const m = await loadMap(ref);
					out[col] = m.has(String(out[col])) ? Number(m.get(String(out[col]))) : null;
				}
				for (const col of USER_FK) if (col in out && out[col] != null && !(await loadMap('user')).has(String(out[col]))) out[col] = null;
				// secrets
				if (spec.t === 'user' && 'password_hash' in out && process.env.IMPORT_KEEP_PASSWORDS !== '1') {
					const pw = dCols.find((c) => c.column_name === 'password_hash');
					out.password_hash = pw.is_nullable === 'YES' ? null : '!imported-no-password';
				}
				// fills for required target columns the source lacks
				for (const c of dCols) {
					const n = c.column_name;
					if (n in out || (n === 'id' && !spec.text) || c.is_nullable === 'YES' || c.column_default != null) continue;
					if (spec.t === 'post' && n === 'ends_at') out[n] = new Date(new Date(row.start_time).getTime() + (row.hours || 2) * 3600e3);
					else if (spec.t === 'post' && n === 'status') out[n] = 'ended';
					else if (c.data_type.startsWith('timestamp')) out[n] = row.created_at ?? new Date();
					else if (c.data_type === 'boolean') out[n] = false;
					else if (['integer', 'real', 'double precision', 'numeric'].includes(c.data_type)) out[n] = 0;
					else if (c.data_type === 'USER-DEFINED') out[n] = (await enumLabels(c.udt_name))[0];
					else if (c.data_type === 'jsonb' || c.data_type === 'json') out[n] = {};
					else out[n] = '';
				}
				if (spec.t === 'post' && dCols.some((c) => c.column_name === 'ends_at') && out.ends_at == null && row.start_time)
					out.ends_at = new Date(new Date(row.start_time).getTime() + (row.hours || 2) * 3600e3);
				if (spec.t === 'post' && dCols.some((c) => c.column_name === 'status') && out.ends_at && new Date(out.ends_at) < new Date()) out.status = 'ended';
				if (spec.t === 'post' && 'ends_at' in out && 'status' in out && out.status === 'live' && new Date(out.ends_at) < new Date()) out.status = 'ended';
				// image paths: /uploads/... -> /uploads/import/<source>/...
				for (const k of ['description', 'body', 'short_description', 'avatar_url']) {
					if (typeof out[k] === 'string') out[k] = out[k].replaceAll('/uploads/projects/', `/uploads/import/${source}/projects/`);
				}
				if (DRY) { added++; continue; }
				if (spec.t === 'user') {
					const clash = await dst`select id from "user" where id = ${out.id} or username = ${out.username} limit 1`;
					if (clash.length) {
						map.set(srcId, clash[0].id);
						await dst`insert into import_map ${dst({ source, tbl: 'user', src_id: srcId, dst_id: clash[0].id })} on conflict do nothing`;
						skipped++;
						continue;
					}
				}
				for (const k of Object.keys(out)) if (out[k] !== null && typeof out[k] === 'object' && !(out[k] instanceof Date)) out[k] = dst.json(out[k]);
				const [ins] = await dst`insert into ${dst(spec.t)} ${dst(out)} returning id`;
				map.set(srcId, String(ins.id));
				await dst`insert into import_map ${dst({ source, tbl: spec.t, src_id: srcId, dst_id: String(ins.id) })}`;
				added++;
			}
			report.push(`${source}.${spec.t}: ${added} ${DRY ? 'would be added' : 'added'}, ${skipped} already there`);
		}
		await src.end();
	}
	// files
	const copies = [
		[process.env.IMPORT_UPLOADS_DIR, 'static/uploads/import/' + (Object.keys(sources)[0] || 'projects')],
		[process.env.IMPORT_PHOTOS_DIR, 'static/uploads/import/photos-archive']
	];
	for (const [from, to] of copies) {
		if (!from) continue;
		await stat(from);
		if (!DRY) { await mkdir(path.dirname(to), { recursive: true }); await cp(from, to, { recursive: true, force: false, errorOnExist: false }); }
		report.push(`files: ${from} -> ${to}${DRY ? ' (dry run)' : ''}`);
	}
	console.log(report.join('\n'));
	await dst.end();
}
main().catch((e) => { console.error(e); process.exit(1); });
