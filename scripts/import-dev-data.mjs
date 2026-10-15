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
 *   node scripts/import-dev-data.mjs [--dry-run] [--cleanup]
 *
 * Dedupe: a row whose natural key (NK below) already exists in the target is not inserted again;
 * it is mapped to the existing row and its empty columns are filled from the source (e.g. place photos).
 * --cleanup: first merges duplicates left by earlier runs (imported rows only, via import_map):
 * child rows are repointed to the kept row (lowest id), then the duplicate is deleted.
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
const CLEANUP = process.argv.includes('--cleanup');
// Natural keys (target-side values, after FK remap). First key whose columns are all non-null wins.
const NK = {
	user: [['username']],
	place: [['google_place_id'], ['name', 'address']],
	project: [['name', 'created_at']],
	project_status: [['project_id', 'body', 'occurred_at']],
	project_change: [['agent_session_id', 'action', 'created_at']],
	place_review: [['place_id', 'user_id', 'created_at'], ['place_id', 'created_at']],
	place_tag: [['place_id', 'tag']],
	post: [['name', 'activity', 'start_time']]
};
function pickKey(t, row, cols) {
	for (const k of NK[t] || []) if (k.every((c) => cols.has(c) && row[c] != null)) return k;
	return null;
}
async function findByKey(t, key, row) {
	const conds = key.map((c) => dst`${dst(c)} = ${row[c]}`);
	let where = conds[0];
	for (const c of conds.slice(1)) where = dst`${where} and ${c}`;
	const r = await dst`select id from ${dst(t)} where ${where} order by id limit 1`;
	return r[0]?.id ?? null;
}
async function fillNulls(t, id, row, dCols) {
	const set = {};
	for (const c of dCols) if (c.column_name !== 'id' && c.is_nullable === 'YES' && row[c.column_name] != null) set[c.column_name] = row[c.column_name];
	const keys = Object.keys(set);
	if (!keys.length) return;
	for (const k of keys) {
		const v = set[k] !== null && typeof set[k] === 'object' && !(set[k] instanceof Date) ? dst.json(set[k]) : set[k];
		await dst`update ${dst(t)} set ${dst(k)} = ${v} where id = ${id} and ${dst(k)} is null`;
	}
}
async function referencing(t) {
	return dst`select cl.relname as tbl, a.attname as col from pg_constraint c
		join pg_class cl on cl.oid = c.conrelid join pg_attribute a on a.attrelid = c.conrelid and a.attnum = any(c.conkey)
		where c.contype = 'f' and c.confrelid = ${'public.' + (t === 'user' ? '"user"' : t)}::regclass`;
}
async function cleanup(report) {
	const has = await dst`select 1 from information_schema.tables where table_name = 'import_map'`;
	if (!has.length) return report.push('cleanup: nothing imported yet');
	for (const spec of TABLES) {
		const dCols = await columns(dst, spec.t);
		if (!dCols.length || spec.t === 'user') continue;
		const cols = new Set(dCols.map((c) => c.column_name));
		const imported = new Set((await dst`select distinct dst_id from import_map where tbl = ${spec.t}`).map((r) => String(r.dst_id)));
		if (!imported.size) continue;
		const rows = await dst`select * from ${dst(spec.t)} order by id`;
		const keeper = new Map(); let removed = 0;
		const refs = await referencing(spec.t);
		for (const row of rows) {
			const key = pickKey(spec.t, row, cols);
			if (!key) continue;
			const sig = key.map((c) => (row[c] instanceof Date ? row[c].toISOString() : String(row[c]))).join('\u0001') + '|' + key.join(',');
			if (!keeper.has(sig)) { keeper.set(sig, row); continue; }
			if (!imported.has(String(row.id))) continue; // never delete rows the import didn't create
			const keep = keeper.get(sig);
			if (DRY) { removed++; continue; }
			await fillNulls(spec.t, keep.id, row, dCols);
			for (const r of refs) await dst`update ${dst(r.tbl)} set ${dst(r.col)} = ${keep.id} where ${dst(r.col)} = ${row.id}`;
			await dst`update import_map set dst_id = ${String(keep.id)} where tbl = ${spec.t} and dst_id = ${String(row.id)}`;
			await dst`delete from ${dst(spec.t)} where id = ${row.id}`;
			removed++;
		}
		report.push(`cleanup ${spec.t}: ${removed} duplicate${removed === 1 ? '' : 's'} ${DRY ? 'would be ' : ''}merged`);
	}
}

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
	if (CLEANUP) await cleanup(report);
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
			let added = 0, skipped = 0, merged = 0;
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
				if (Object.keys(spec.fk || {}).some((col) => out[col] == null && dCols.find((c) => c.column_name === col)?.is_nullable === 'NO')) { skipped++; continue; } // parent missing
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
				if (spec.t !== 'user') {
					const key = pickKey(spec.t, out, new Set(dCols.map((c) => c.column_name)));
					const existing = key ? await findByKey(spec.t, key, out) : null;
					if (existing != null) {
						await fillNulls(spec.t, existing, out, dCols);
						map.set(srcId, String(existing));
						await dst`insert into import_map ${dst({ source, tbl: spec.t, src_id: srcId, dst_id: String(existing) })} on conflict do nothing`;
						merged++;
						continue;
					}
				}
				for (const k of Object.keys(out)) if (out[k] !== null && typeof out[k] === 'object' && !(out[k] instanceof Date)) out[k] = dst.json(out[k]);
				const [ins] = await dst`insert into ${dst(spec.t)} ${dst(out)} returning id`;
				map.set(srcId, String(ins.id));
				await dst`insert into import_map ${dst({ source, tbl: spec.t, src_id: srcId, dst_id: String(ins.id) })}`;
				added++;
			}
			report.push(`${source}.${spec.t}: ${added} ${DRY ? 'would be added' : 'added'}, ${merged} merged into existing, ${skipped} already there`);
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
