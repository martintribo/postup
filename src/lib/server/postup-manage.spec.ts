import { describe, expect, it, vi } from 'vitest';
vi.mock('$lib/server/db', () => ({ db: {} }));
import { minutesLeft } from './postup-manage';
describe('minutesLeft', () => {
	it('never negative', () => {
		expect(minutesLeft(new Date(1000), 5000)).toBe(0);
		expect(minutesLeft(new Date(90 * 60000), 0)).toBe(90);
	});
});
