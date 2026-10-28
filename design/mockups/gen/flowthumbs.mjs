// Pre-render one thumbnail per flow step for flows/grid.html (same rendering as gen/flowvideo.mjs:
// screen + sheet, fresh-load per step, green ring on the element tapped to reach the next step).
// Usage (from mockups/): python3 gen/build.py && node gen/flowthumbs.mjs   -> flows/thumbs/<flow>-<n>.webp + flows/thumbs/taps.json
import { createRequire } from 'module'; import http from 'http'; import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
const require = createRequire('/workspace/postup-pm/videos/tools/');
const { chromium } = require('playwright-core');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const OUT = `${ROOT}/flows/thumbs`; fs.mkdirSync(OUT, { recursive: true });
const flows = JSON.parse(execFileSync('python3', ['-c', `import json;import os;os.chdir('${ROOT}');exec(open('gen/flowload.py').read());print(json.dumps(FLOWS))`]));
const url = (f, st, i) => { const [sc, a, l, x] = st; const q = new URLSearchParams({ style: 'fresh', device: x.device || f.start.device, auth: a, live: l, notes: '0', fvs: i }); if (x.mode) q.set('mode', x.mode); if (x.ov) q.set('ov', x.ov); return `/index.html?${q}#${sc}`; };
const srv = http.createServer((req, res) => { let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp)) { res.writeHead(404); return res.end(); }
  const ty = { '.html': 'text/html', '.svg': 'image/svg+xml', '.png': 'image/png' }[path.extname(fp)] || 'application/octet-stream';
  res.writeHead(200, { 'content-type': ty }); fs.createReadStream(fp).pipe(res); }).listen(0);
const base = `http://127.0.0.1:${srv.address().port}`;
const CSS = `#fvring{position:fixed;z-index:9998;border:4px solid #10a364;border-radius:14px;box-shadow:0 0 0 7px rgba(16,163,100,.3);pointer-events:none}
#fvdot{position:fixed;z-index:9999;width:38px;height:38px;margin:-19px 0 0 -19px;border-radius:50%;background:rgba(16,163,100,.5);border:3px solid #fff;pointer-events:none}.mock,.pmenu{display:none!important}`;
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
const pages = { phone: await b.newPage({ viewport: { width: 390, height: 844 } }), desktop: await b.newPage({ viewport: { width: 1280, height: 800 } }) };
const taps = {}; let n = 0;
for (const f of flows) for (let i = 0; i < f.steps.length; i++) {
  const st = f.steps[i], nx = f.steps[i + 1], dev = st[3].device || f.start.device, pg = pages[dev];
  await pg.goto(base + url(f, st, i)); await pg.waitForTimeout(450);
  await pg.evaluate(css => { const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); const p = document.querySelector('.ph'); if (p) p.scrollTop = 0; scrollTo(0, 0); }, CSS);
  let hit = null;
  if (nx) hit = await pg.evaluate(([cur, nsc, nov]) => {
    const vis = e => { const r = e.getBoundingClientRect(); return r.width > 4 && r.height > 4 && r.bottom > 0 && r.top < innerHeight && getComputedStyle(e).visibility !== 'hidden'; };
    const root = [...document.querySelectorAll('.ov.on')].pop() || document.querySelector('.scr.on');
    const all = [...root.querySelectorAll('[onclick],a[href]')].filter(vis);
    const ok = e => { const o = (e.getAttribute('onclick') || '') + ' ' + (e.getAttribute('href') || '');
      if (nov && nsc === cur) return o.includes(`ov('${nov}')`);
      return o.includes(`'${nsc}'`) || o.includes(`#${nsc}"`) || o.endsWith(`#${nsc}`) || (nsc === 'posted' && /sheet\('(post|attach)-signin'\)|signIn\('posted'\)/.test(o)); };
    let e = all.find(ok), back = false;
    if (!e && nsc !== cur) { e = all.find(x => /bk\(\)/.test(x.getAttribute('onclick') || '')); back = !!e; }
    if (!e) return null; e.scrollIntoView({ block: 'center' }); const r = e.getBoundingClientRect();
    const d = document.createElement('div'); d.id = 'fvring'; Object.assign(d.style, { left: r.x - 4 + 'px', top: r.y - 4 + 'px', width: r.width + 2 + 'px', height: r.height + 2 + 'px' }); document.body.appendChild(d);
    const t = document.createElement('div'); t.id = 'fvdot'; Object.assign(t.style, { left: r.x + r.width / 2 + 'px', top: r.y + r.height / 2 + 'px' }); document.body.appendChild(t);
    return { label: (e.innerText || e.getAttribute('aria-label') || '').trim().split('\n')[0].slice(0, 40) || 'tap', back };
  }, [st[0], nx[0], nx[3].ov || '']);
  await pg.waitForTimeout(120);
  const png = `/tmp/fthumb.png`, out = `${OUT}/${f.id}-${i + 1}.webp`;
  await pg.screenshot({ path: png });
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', png, '-vf', `scale=${dev === 'desktop' ? 480 : 240}:-1:flags=lanczos`, '-quality', '72', out]);
  taps[`${f.id}-${i + 1}`] = hit; n++;
}
fs.writeFileSync(`${OUT}/taps.json`, JSON.stringify(taps, null, 1));
await b.close(); srv.close(); console.log('thumbs', n);
