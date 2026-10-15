import { json } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

/** Android App Links. ANDROID_CERT_SHA256 = comma-separated signing cert fingerprints. */
export const GET = () => {
	const fps = (env.ANDROID_CERT_SHA256 || '').split(',').map((s) => s.trim()).filter(Boolean);
	return json(fps.length ? [{ relation: ['delegate_permission/common.handle_all_urls'], target: { namespace: 'android_app', package_name: env.CAP_APP_ID || 'now.postup.app', sha256_cert_fingerprints: fps } }] : []);
};
