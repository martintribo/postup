// Render one critical flow as an MP4 on a 390x844 phone frame.
// Usage: node gen/flowvideo.mjs <flow-id> [out.mp4]   (run from anywhere; needs a built mockups dir, ffmpeg, Chrome)
// Playwright comes from /workspace/postup-pm/videos/tools/node_modules (playwright-core).
import { createRequire } from 'module'; import http from 'http'; import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
const require = createRequire('/workspace/postup-pm/videos/tools/');
const { chromium } = require('playwright-core');
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const id = process.argv[2] || 'cautious-joiner';
const OUT = process.argv[3] || `/workspace/postup-pm/videos/${id}.mp4`;
const W = 390, H = 844, HOLD = 2.3, TAP = 0.7, FADE = 0.4, CARD = 3.2;
const flows = JSON.parse(execFileSync('python3', ['-c', `import json;import os;os.chdir('${ROOT}');exec(open('gen/flowload.py').read());print(json.dumps(FLOWS))`]));
const f = flows.find(x => x.id === id); if (!f) throw new Error('no flow ' + id);
const clean = t => t.replace(/\s*\[[^\]]+\]/g, '').trim();
const title = sc => { try { return fs.readFileSync(`${ROOT}/notes/${sc}.md`, 'utf8').split('\n')[0].replace(/^# /, ''); } catch { return '#' + sc; } };
const url = st => { const [sc, a, l, x] = st; const q = new URLSearchParams({ style: 'fresh', device: 'phone', auth: a, live: l, notes: '0' }); if (x.mode) q.set('mode', x.mode); if (x.ov) q.set('ov', x.ov); return `/index.html?${q}#${sc}`; };
// static server over the build
const srv = http.createServer((req, res) => { let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp)) { res.writeHead(404); return res.end(); }
  const ty = { '.html': 'text/html', '.svg': 'image/svg+xml', '.png': 'image/png', '.css': 'text/css', '.js': 'text/javascript' }[path.extname(fp)] || 'application/octet-stream';
  res.writeHead(200, { 'content-type': ty }); fs.createReadStream(fp).pipe(res); }).listen(0);
const base = `http://127.0.0.1:${srv.address().port}`;
const tmp = fs.mkdtempSync('/tmp/flowvid-'); const shots = [];
const CSS = `#fvcap{position:fixed;left:10px;right:10px;top:10px;z-index:9999;background:rgba(20,20,19,.88);color:#fff;border-radius:14px;padding:10px 14px;font:500 14px/1.35 Inter,system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.25)}
#fvcap b{display:block;font-size:12px;color:#7ee2b0;letter-spacing:.03em;margin-bottom:2px}
#fvring{position:fixed;z-index:9998;border:3px solid #10a364;border-radius:14px;box-shadow:0 0 0 6px rgba(16,163,100,.25);pointer-events:none}
#fvdot{position:fixed;z-index:9999;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;background:rgba(16,163,100,.45);border:2px solid #fff;pointer-events:none}
.mock,.pmenu{display:none!important}`;
const cardHTML = (h, rows, kicker) => `<html><body style="margin:0;width:${W}px;height:${H}px;display:flex;flex-direction:column;justify-content:center;padding:32px;box-sizing:border-box;background:linear-gradient(160deg,#0f7a4f,#10a364);color:#fff;font:16px/1.45 Inter,system-ui,sans-serif">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet"><div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;opacity:.8">${kicker}</div>
<h1 style="font-size:28px;line-height:1.15;margin:10px 0 18px;font-weight:800">${h}</h1>${rows.map(r => `<p style="margin:0 0 12px;opacity:.95">${r}</p>`).join('')}</body></html>`;
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome' });
const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
let n = 0; const snap = async dur => { const p = `${tmp}/${String(n++).padStart(3, '0')}.png`; await pg.screenshot({ path: p }); shots.push([p, dur]); };
const s0 = f.start;
await pg.setContent(cardHTML(esc(f.name), [`<b>Who:</b> ${esc(f.persona)}`, `<b>Starts:</b> ${s0.auth === 'in' ? 'signed in' : 'signed out'} · ${s0.live === 'live' ? 'people live nearby' : 'nobody live'} · ${s0.device} · opens <code>${esc(s0.url)}</code>`, `<b>Goal:</b> ${esc(clean(f.goal))}`], 'PostUp flow · ' + f.pri));
await pg.waitForTimeout(600); await snap(CARD);
const missed = [];
for (let i = 0; i < f.steps.length; i++) {
  const st = f.steps[i], nx = f.steps[i + 1];
  await pg.goto(base + url(st).replace('#', `&fvs=${i}#`)); await pg.waitForTimeout(700);
  await pg.evaluate(() => { const p = document.querySelector('.ph'); if (p) p.scrollTop = 0; scrollTo(0, 0); });
  const cap = `<b>STEP ${i + 1} OF ${f.steps.length} · ${esc(title(st[0]).toUpperCase())}</b>${esc(clean(st[4]))}`;
  await pg.evaluate(([css, cap]) => { const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); const d = document.createElement('div'); d.id = 'fvcap'; d.innerHTML = cap; document.body.appendChild(d); }, [CSS, cap]);
  await pg.waitForTimeout(250); await snap(HOLD);
  // find what gets tapped to reach the next step
  let box = null;
  if (nx) box = await pg.evaluate(([cur, nsc, nov]) => {
    const vis = e => { const r = e.getBoundingClientRect(); return r.width > 4 && r.height > 4 && r.bottom > 0 && r.top < innerHeight && getComputedStyle(e).visibility !== 'hidden' && e.closest('.scr.on,.ov.on'); };
    const root = [...document.querySelectorAll('.ov.on')].pop() || document.querySelector('.scr.on');
    const all = [...root.querySelectorAll('[onclick],a[href]')].filter(vis);
    const hit = e => { const o = (e.getAttribute('onclick') || '') + ' ' + (e.getAttribute('href') || '');
      if (nov && nsc === cur) return o.includes(`ov('${nov}')`);
      return o.includes(`'${nsc}'`) || o.includes(`#${nsc}"`) || o.endsWith(`#${nsc}`) || (nsc === 'joined' && /sheet\('join-signin'\)|signIn\('joined'\)/.test(o)) || (nsc === 'posted' && /sheet\('(post|attach)-signin'\)/.test(o)); };
    let e = all.find(hit);
    if (!e && nsc !== cur) e = all.find(x => /bk\(\)/.test(x.getAttribute('onclick') || ''));
    if (!e) return null; e.scrollIntoView({ block: 'center' }); const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height };
  }, [st[0], nx[0], nx[3].ov || '']);
  if (box) { await pg.evaluate(bx => { const r = document.createElement('div'); r.id = 'fvring'; Object.assign(r.style, { left: bx.x - 4 + 'px', top: bx.y - 4 + 'px', width: bx.w + 2 + 'px', height: bx.h + 2 + 'px' }); document.body.appendChild(r);
      const d = document.createElement('div'); d.id = 'fvdot'; Object.assign(d.style, { left: bx.x + bx.w / 2 + 'px', top: bx.y + bx.h / 2 + 'px' }); document.body.appendChild(d); }, box); await pg.waitForTimeout(150); await snap(TAP); }
  else { if (nx) missed.push(`${i + 1}:${st[0]}→${nx[0]}`); shots[shots.length - 1][1] += TAP; }
}
await pg.setContent(cardHTML('Success looks like', f.success.map(s => '✓ ' + esc(clean(s))), f.name)); await pg.waitForTimeout(600); await snap(CARD + 0.5);
await b.close(); srv.close();
// ffmpeg: still images chained with crossfades
const args = ['-y']; shots.forEach(([p, d]) => args.push('-loop', '1', '-t', String(d + FADE), '-i', p));
let fc = shots.map((_, i) => `[${i}:v]scale=${W * 2}:${H * 2},setsar=1,fps=30,format=yuv420p[v${i}]`).join(';'), last = 'v0', off = 0;
for (let i = 1; i < shots.length; i++) { off += shots[i - 1][1]; const isTap = shots[i][1] === TAP; const t = isTap ? 0.15 : FADE;
  fc += `;[${last}][v${i}]xfade=transition=fade:duration=${t}:offset=${(off).toFixed(2)}[x${i}]`; last = `x${i}`; }
fs.mkdirSync(path.dirname(OUT), { recursive: true });
execFileSync('ffmpeg', [...args, '-filter_complex', fc, '-map', `[${last}]`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], { stdio: 'ignore' });
if (process.env.KEEP) console.log('shots in', tmp); else fs.rmSync(tmp, { recursive: true });
console.log(JSON.stringify({ out: OUT, shots: shots.length, noTapTarget: missed }));
