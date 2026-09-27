import devtoolsJson from 'vite-plugin-devtools-json';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vitest/config';
import { playwright } from '@vitest/browser-playwright';
import { sveltekit } from '@sveltejs/kit/vite';
import fs from 'node:fs';

function getHttpsConfig() {
	try {
		return {
			cert: fs.readFileSync('certs/dev.crt'),
			key: fs.readFileSync('certs/dev.key')
		};
	} catch {
		return undefined;
	}
}

const hubPort = Number(process.env.PORT || process.env.VITE_PORT || 5173);
const hubHost = process.env.HOST || '0.0.0.0';

export default defineConfig({
	server: {
		port: hubPort,
		host: hubHost,
		strictPort: !!process.env.PORT,
		allowedHosts: true,
		https: process.env.HUB_VITE_HTTP === '1' ? undefined : getHttpsConfig()
	},
	plugins: [tailwindcss(), sveltekit(), devtoolsJson()],
	test: {
		expect: { requireAssertions: true },
		projects: [
			{
				extends: './vite.config.ts',
				test: {
					name: 'client',
					browser: {
						enabled: true,
						provider: playwright(),
						instances: [{ browser: 'chromium', headless: true }]
					},
					include: ['src/**/*.svelte.{test,spec}.{js,ts}'],
					exclude: ['src/lib/server/**']
				}
			},
			{
				extends: './vite.config.ts',
				test: {
					name: 'server',
					environment: 'node',
					include: ['src/**/*.{test,spec}.{js,ts}'],
					exclude: ['src/**/*.svelte.{test,spec}.{js,ts}']
				}
			}
		]
	}
});
