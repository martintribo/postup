import { describe, expect, it, vi } from 'vitest';

vi.mock('$lib/server/db', () => ({ db: {} }));
vi.mock('$env/dynamic/private', () => ({ env: {} }));

import { hidesPost, reportHideThreshold } from './safety';

describe('report hide threshold', () => {
	it('hides once several different people have reported', () => {
		expect(reportHideThreshold()).toBe(3);
		expect(hidesPost(2, 3)).toBe(false);
		expect(hidesPost(3, 3)).toBe(true);
		expect(hidesPost(4, 3)).toBe(true);
	});
});
