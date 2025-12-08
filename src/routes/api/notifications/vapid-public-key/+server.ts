import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

export const GET: RequestHandler = async () => {
	const publicKey = env.VAPID_PUBLIC_KEY;
	
	if (!publicKey) {
		return json({ error: 'VAPID public key not configured' }, { status: 500 });
	}
	
	return json({ publicKey });
};

