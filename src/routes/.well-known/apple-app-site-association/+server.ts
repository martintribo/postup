import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

/** iOS Universal Links: /p/*, /projects/*, /postups/* open the app. Needs APPLE_TEAM_ID + APPLE_BUNDLE_ID. */
export const GET = () => {
	const appID = env.APPLE_TEAM_ID && env.APPLE_BUNDLE_ID ? `${env.APPLE_TEAM_ID}.${env.APPLE_BUNDLE_ID}` : null;
	return json({ applinks: { details: appID ? [{ appIDs: [appID], components: [{ '/': '/p/*' }, { '/': '/projects/*' }, { '/': '/postups/*' }] }] : [] } });
};
