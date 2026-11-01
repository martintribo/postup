import { describe, expect, it, vi } from 'vitest';

const env: Record<string, string | undefined> = {};
vi.mock('$env/dynamic/public', () => ({ env }));

describe('phase', () => {
	it('defaults to phase 0 and only accepts 1 or 2', async () => {
		vi.resetModules();
		env.PUBLIC_PHASE = undefined;
		const { phase } = await import('./phase');
		expect(phase()).toBe(0);
		env.PUBLIC_PHASE = '2';
		expect(phase()).toBe(2);
		env.PUBLIC_PHASE = '9';
		expect(phase()).toBe(0);
		env.PUBLIC_PHASE = '1';
		expect(phase()).toBe(1);
	});
});
