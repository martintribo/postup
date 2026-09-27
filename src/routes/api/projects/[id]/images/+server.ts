import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { project } from '$lib/server/db/schema';
import { and, eq } from 'drizzle-orm';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { randomBytes } from 'node:crypto';

const ALLOWED_MIME: Record<string, string> = {
	'image/png': 'png',
	'image/jpeg': 'jpg',
	'image/webp': 'webp',
	'image/gif': 'gif',
	'image/avif': 'avif'
};

const MAX_BYTES = 8 * 1024 * 1024; // 8 MB

const UPLOAD_DIR = 'static/uploads/projects';
const PUBLIC_BASE = '/uploads/projects';

function replaceNthPlaceholder(description: string, index: number, url: string): string | null {
	const regex = /!\[([^\]]*)\]\(placeholder\)/g;
	let match: RegExpExecArray | null;
	let i = 0;
	while ((match = regex.exec(description)) !== null) {
		if (i === index) {
			const before = description.slice(0, match.index);
			const after = description.slice(match.index + match[0].length);
			return `${before}![${match[1]}](${url})${after}`;
		}
		i++;
	}
	return null;
}

export const POST: RequestHandler = async ({ locals, params, request }) => {
	if (!locals.user) {
		return json({ error: 'Must be logged in' }, { status: 401 });
	}

	const id = Number(params.id);
	if (!Number.isInteger(id) || id <= 0) {
		return json({ error: 'Invalid project id' }, { status: 400 });
	}

	const [target] = await db
		.select()
		.from(project)
		.where(and(eq(project.id, id), eq(project.userId, locals.user.id)));
	if (!target) {
		return json({ error: 'Project not found or not owned by you' }, { status: 404 });
	}

	const form = await request.formData();
	const file = form.get('file');
	const placeholderIndexRaw = form.get('placeholderIndex');

	if (!(file instanceof File)) {
		return json({ error: 'file (multipart) is required' }, { status: 400 });
	}
	if (file.size === 0) {
		return json({ error: 'file is empty' }, { status: 400 });
	}
	if (file.size > MAX_BYTES) {
		return json({ error: `file exceeds ${MAX_BYTES} bytes` }, { status: 413 });
	}
	const ext = ALLOWED_MIME[file.type];
	if (!ext) {
		return json(
			{ error: `unsupported mime ${file.type}; allowed: ${Object.keys(ALLOWED_MIME).join(', ')}` },
			{ status: 415 }
		);
	}

	const index = Number(placeholderIndexRaw);
	if (!Number.isInteger(index) || index < 0) {
		return json({ error: 'placeholderIndex (int >= 0) is required' }, { status: 400 });
	}

	const projectDir = join(UPLOAD_DIR, String(id));
	await mkdir(projectDir, { recursive: true });
	const name = `${randomBytes(8).toString('hex')}.${ext}`;
	const filePath = join(projectDir, name);
	const buf = Buffer.from(await file.arrayBuffer());
	await writeFile(filePath, buf);

	const url = `${PUBLIC_BASE}/${id}/${name}`;
	const updatedDescription = replaceNthPlaceholder(target.description, index, url);
	if (updatedDescription === null) {
		return json(
			{ error: `No placeholder at index ${index} found in description` },
			{ status: 409 }
		);
	}

	const [updated] = await db
		.update(project)
		.set({ description: updatedDescription, updatedAt: new Date() })
		.where(eq(project.id, id))
		.returning();

	return json({ url, project: updated });
};
