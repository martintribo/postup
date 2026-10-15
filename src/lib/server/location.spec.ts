import { describe, expect, it, vi } from 'vitest';
vi.mock('$env/dynamic/public', () => ({ env: {} }));
import { guessLocation } from './location';

describe('guessLocation', () => {
	it('uses Vercel edge headers first', async () => {
		const h = new Headers({ 'x-vercel-ip-latitude': '34.1', 'x-vercel-ip-longitude': '-118.3', 'x-vercel-ip-city': 'Los%20Angeles' });
		const f = vi.fn();
		const r = await guessLocation(h, '1.2.3.4', f as never);
		expect(r).toMatchObject({ latitude: 34.1, longitude: -118.3, city: 'Los Angeles', source: 'edge' });
		expect(f).not.toHaveBeenCalled();
	});
	it('looks up the forwarded client IP, not the server IP', async () => {
		const f = vi.fn(async (_url: string) => new Response(JSON.stringify({ status: 'success', lat: 40, lon: -74, city: 'NYC' })));
		const r = await guessLocation(new Headers({ 'x-forwarded-for': '8.8.8.8, 10.0.0.1' }), '3.3.3.3', f as never);
		expect(f.mock.calls[0][0]).toContain('8.8.8.8');
		expect(r.source).toBe('ip');
	});
	it('falls back to the launch area for private IPs', async () => {
		const r = await guessLocation(new Headers(), '127.0.0.1');
		expect(r).toMatchObject({ source: 'default', latitude: 33.9765 });
	});
});
