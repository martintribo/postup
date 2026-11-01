import { describe, expect, it, vi } from 'vitest';

vi.mock('$env/dynamic/public', () => ({ env: {} }));

import { distanceVerdict, milesBetween } from './post-distance';

const cafe = { latitude: 33.9765, longitude: -118.4176 };

describe('distanceVerdict', () => {
	it('allows a cafe at the same spot', () => {
		const v = distanceVerdict(cafe, cafe, { maxMiles: 0.5 });
		expect(v.ok).toBe(true);
	});

	it('blocks a cafe a couple of miles away', () => {
		const far = { latitude: 34.01, longitude: -118.4176 };
		expect(milesBetween(cafe, far)).toBeGreaterThan(0.5);
		const v = distanceVerdict(cafe, far, { maxMiles: 0.5 });
		expect(v).toMatchObject({ ok: false, reason: 'far' });
	});

	it('blocks when location is denied, even if a guess was passed', () => {
		expect(distanceVerdict(cafe, cafe, { denied: true, maxMiles: 0.5 })).toEqual({ ok: false, reason: 'denied', miles: null });
	});

	it('blocks when there is no location at all', () => {
		const v = distanceVerdict(null, cafe, { maxMiles: 0.5 });
		expect(v.ok).toBe(false);
		if (!v.ok) expect(v.reason).toBe('denied');
	});
});
