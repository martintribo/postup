import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

/** Parking scan used Google reviews as AI source. Disabled on this branch (ToS). */
export const POST: RequestHandler = async () => {
	return json(
		{ error: 'Parking scan is disabled. Google review content is not used beside the Stadia map.' },
		{ status: 410 }
	);
};

export const GET: RequestHandler = async () => {
	return json(
		{ error: 'Parking scan is disabled.' },
		{ status: 410 }
	);
};
