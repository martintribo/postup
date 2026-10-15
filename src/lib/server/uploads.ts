import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { randomBytes } from 'node:crypto';

const MIME: Record<string, string> = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/gif': 'gif', 'image/avif': 'avif' };
const MAX = 8 * 1024 * 1024;

/** Save an uploaded image under static/uploads/<kind>/ and return its public URL (null if none). Throws on bad type/size. */
export async function saveImage(file: FormDataEntryValue | null, kind: 'projects' | 'updates' | 'postups'): Promise<string | null> {
	if (!file || typeof file === 'string' || file.size === 0) return null;
	const ext = MIME[file.type];
	if (!ext) throw new Error('Use a PNG, JPEG, WebP, GIF or AVIF image');
	if (file.size > MAX) throw new Error('Images can be up to 8 MB');
	const dir = join('static/uploads', kind);
	await mkdir(dir, { recursive: true });
	const name = `${Date.now()}-${randomBytes(6).toString('hex')}.${ext}`;
	await writeFile(join(dir, name), Buffer.from(await file.arrayBuffer()));
	return `/uploads/${kind}/${name}`;
}
