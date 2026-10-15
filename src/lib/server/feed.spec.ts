import { describe, expect, it, vi } from 'vitest';
vi.mock('$lib/server/db', () => ({ db: {} }));
import { relTime } from './feed';
describe('relTime', () => {
	const now = Date.parse('2026-10-15T20:00:00Z');
	it('formats', () => {
		expect(relTime('2026-10-15T19:30:00Z', now)).toBe('30m ago');
		expect(relTime('2026-10-15T17:00:00Z', now)).toBe('3h ago');
		expect(relTime('2026-10-15T08:00:00Z', now)).toBe('earlier today');
		expect(relTime('2026-10-14T18:00:00Z', now)).toBe('yesterday');
		expect(relTime('2026-10-11T18:00:00Z', now)).toBe('4 days ago');
	});
});
