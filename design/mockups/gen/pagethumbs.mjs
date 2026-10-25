// One thumbnail per page for flows/sitemap.html: signed-in, live state (fallback: any state of the page). [M1026]
// Usage (from mockups/): python3 gen/build.py && node gen/pagethumbs.mjs -> flows/pages/<page>.webp
import { createRequire } from 'module'; import http from 'http'; import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
const require = createRequire('/workspace/postup-pm/videos/tools/'); const { chromium } = require('playwright-core');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const OUT = `${ROOT}/flows/pages`; fs.mkdirSync(OUT, { recursive: true });
const { states } = JSON.parse(fs.readFileSync(`${ROOT}/flows/sitegraph.json`));
const pick = {}; const rank = k => (k.includes('@in.live') ? 0 : k.includes('@in.') ? 1 : 2) + (k.includes('+') ? 5 : 0) + (k.endsWith('.building') ? 1 : 0);
for (const [k, s] of Object.entries(states)) if (!pick[s.page] || rank(k) < rank(pick[s.page])) pick[s.page] = k;
const srv = http.createServer((req, res) => { let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': { '.html': 'text/html', '.svg': 'image/svg+xml', '.png': 'image/png' }[path.extname(fp)] || 'application/octet-stream' }); fs.createReadStream(fp).pipe(res); }).listen(0);
const base = `http://127.0.0.1:${srv.address().port}/`;
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome' }); const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
for (const [p, k] of Object.entries(pick)) {
  await pg.goto(base + states[k].url.replace('#', '&notes=0&embed=1#')); await pg.waitForTimeout(350);
  await pg.screenshot({ path: '/tmp/pthumb.png' });
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', '/tmp/pthumb.png', '-vf', 'scale=180:-1:flags=lanczos', '-quality', '75', `${OUT}/${p}.webp`]);
}
fs.writeFileSync(`${OUT}/states.json`, JSON.stringify(pick, null, 1));
await b.close(); srv.close(); console.log('pagethumbs', Object.keys(pick).length);
