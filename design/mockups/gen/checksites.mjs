// Render check: every site state in flows/sitegraph.json shows the right screen and sheet in the mockup.
// Usage (from mockups/, after the build): node gen/checksites.mjs
import { createRequire } from 'module'; import http from 'http'; import fs from 'fs'; import path from 'path';
const require = createRequire('/workspace/postup-pm/videos/tools/'); const { chromium } = require('playwright-core');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const G = JSON.parse(fs.readFileSync(`${ROOT}/flows/sitegraph.json`, 'utf8'));
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': p.endsWith('.html') ? 'text/html' : 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome' }); const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
const bad = []; let n = 0;
for (const [id, s] of Object.entries(G.states)) {
  await pg.goto(`http://127.0.0.1:${srv.address().port}/${s.url.replace('#', `&ck=${n++}#`)}`); await pg.waitForTimeout(60);
  const r = await pg.evaluate(() => [document.querySelector('.scr.on')?.id, [...document.querySelectorAll('.ov.on')].map(e => e.id.slice(3)).join(), document.documentElement.dataset.auth, document.documentElement.dataset.live, document.documentElement.dataset.hmode || '']);
  if (r[0] !== s.page || r[1] !== (s.ov || '') || r[2] !== s.auth || r[3] !== s.live || (s.mode && r[4] !== s.mode)) bad.push([id, r]);
}
await b.close(); srv.close(); console.log(JSON.stringify({ checked: n, bad: bad.slice(0, 20), nbad: bad.length }));
