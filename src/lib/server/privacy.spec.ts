import { describe, expect, it, vi } from 'vitest';
vi.mock('$lib/server/db', () => ({ db: {} }));
vi.mock('$env/dynamic/public', () => ({ env: {} }));
import { fuzz, sanitizePosts } from './privacy';

const base = { id: 1, userId: 'owner', latitude: 33.97612, longitude: -118.41734, location: 'Bean Theory', placeId: 7, neighborhood: 'Playa Vista', locality: null } as any;

describe('privacy', () => {
	it('fuzz moves the point to a cell centre', () => {
		const f = fuzz(33.97612, -118.41734);
		expect(f.latitude).not.toBe(33.97612);
		expect(Math.abs(f.latitude - 33.97612)).toBeLessThan(0.015);
		expect(fuzz(33.9701, -118.41)).toEqual(fuzz(33.9749, -118.4049));
	});
	it('hides ask-mode cafes from strangers, not open ones or the owner', async () => {
		const [ask, open] = await sanitizePosts([{ ...base, joinMode: 'ask' }, { ...base, id: 2, joinMode: 'open' }], null);
		expect(ask.location).toBe('a cafe in Playa Vista');
		expect(ask.placeId).toBeNull();
		expect(ask.latitude).not.toBe(base.latitude);
		expect(open.location).toBe('Bean Theory');
		const [own] = await sanitizePosts([{ ...base, joinMode: 'ask' }], 'owner');
		expect(own.location).toBe('Bean Theory');
	});
});
