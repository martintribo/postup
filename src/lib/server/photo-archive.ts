import { env } from '$env/dynamic/private';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { AwsClient } from 'aws4fetch';

export function archiveConfigured(): boolean {
	return Boolean(env.R2_ACCOUNT_ID && env.R2_ACCESS_KEY_ID && env.R2_SECRET_ACCESS_KEY && env.R2_BUCKET) ||
		Boolean(env.PHOTO_ARCHIVE_DIR);
}

function r2Client(): { client: AwsClient; base: string } | null {
	const account = env.R2_ACCOUNT_ID;
	const accessKeyId = env.R2_ACCESS_KEY_ID;
	const secretAccessKey = env.R2_SECRET_ACCESS_KEY;
	const bucket = env.R2_BUCKET;
	if (!account || !accessKeyId || !secretAccessKey || !bucket) return null;
	const endpoint = env.R2_ENDPOINT || `https://${account}.r2.cloudflarestorage.com`;
	const client = new AwsClient({
		accessKeyId,
		secretAccessKey,
		service: 's3',
		region: 'auto'
	});
	return { client, base: `${endpoint.replace(/\/$/, '')}/${bucket}` };
}

export async function putArchiveObject(key: string, body: Uint8Array, contentType: string, etag?: string | null) {
	const r2 = r2Client();
	if (r2) {
		const headers: Record<string, string> = { 'content-type': contentType };
		if (etag) headers['x-amz-meta-source-etag'] = etag;
		const res = await r2.client.fetch(`${r2.base}/${key}`, {
			method: 'PUT',
			headers,
			body: body as unknown as BodyInit
		});
		if (!res.ok) {
			const text = await res.text().catch(() => '');
			throw new Error(`R2 PUT ${res.status} ${text.slice(0, 200)}`);
		}
		return;
	}
	const dir = env.PHOTO_ARCHIVE_DIR;
	if (!dir) return;
	const full = path.join(dir, key);
	await mkdir(path.dirname(full), { recursive: true });
	await writeFile(full, body);
}
