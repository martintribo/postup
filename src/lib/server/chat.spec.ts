import { describe, expect, it, vi } from 'vitest';
vi.mock('$lib/server/db', () => ({ db: {} }));
vi.mock('$env/dynamic/public', () => ({ env: {} }));
import { chatWindow } from './chat';
describe('chatWindow (default 24h)', () => {
	const end = new Date('2026-10-15T20:00:00Z');
	it('writable only while live', () => {
		expect(chatWindow(end, 'live', end.getTime() - 1).canWrite).toBe(true);
		expect(chatWindow(end, 'ended', end.getTime() + 1).canWrite).toBe(false);
	});
	it('readable for 24h after end', () => {
		expect(chatWindow(end, 'ended', end.getTime() + 23 * 3600_000).canRead).toBe(true);
		expect(chatWindow(end, 'ended', end.getTime() + 25 * 3600_000).canRead).toBe(false);
	});
});
