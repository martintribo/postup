import { describe, expect, it } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

// Every page must style through design tokens so all four themes work.
// Fix offenders with: python3 scripts/tokenize-styles.py
const PALETTE =
	/(?<![\w-])(?:[a-z-]+:)*(?:bg|text|border|ring|divide|placeholder|fill|stroke)-(?:white|(?:gray|slate|zinc|neutral|stone|blue|indigo|sky|red|rose|green|emerald|purple|violet|amber|yellow|orange|teal|lime|pink|cyan|fuchsia)-\d{2,3})(?![\w-])/g;

function walk(dir: string, out: string[] = []) {
	for (const f of readdirSync(dir)) {
		const p = join(dir, f);
		if (statSync(p).isDirectory()) {
			if (f !== 'stories') walk(p, out);
		} else if (p.endsWith('.svelte')) out.push(p);
	}
	return out;
}

describe('design tokens', () => {
	it('no raw Tailwind palette or dark: classes in components', () => {
		const bad: string[] = [];
		for (const f of walk('src')) {
			const s = readFileSync(f, 'utf8');
			for (const m of s.match(PALETTE) ?? []) bad.push(`${f}: ${m}`);
			for (const m of s.match(/(?<![\w-])dark:[\w-]+/g) ?? []) bad.push(`${f}: ${m}`);
		}
		expect(bad).toEqual([]);
	});
});
