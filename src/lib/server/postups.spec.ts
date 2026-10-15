import { describe, expect, it, vi } from 'vitest';
vi.mock('$lib/server/db', () => ({ db: {} }));
import { computeEndsAt } from './postups';
describe('computeEndsAt', () => {
	it('adds hours', () => {
		expect(computeEndsAt(new Date('2026-10-15T15:00:00Z'), 3).toISOString()).toBe('2026-10-15T18:00:00.000Z');
	});
});
