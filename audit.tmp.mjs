import { chromium } from '@playwright/test';
const H = 'https://dev-vm.burbot-fence.ts.net';
const sites = JSON.parse(process.argv[2]);
const out = [];
for (const [name, port, routes] of sites) {
  for (const r of routes) {
    const b = await chromium.launch({ args: ['--ignore-certificate-errors'] });
    const p = await b.newPage({ ignoreHTTPSErrors: true });
    const errs = [];
    p.on('console', (m) => m.type() === 'error' && errs.push('console: ' + m.text().slice(0, 220)));
    p.on('pageerror', (e) => errs.push('uncaught: ' + String(e.message).slice(0, 220)));
    p.on('requestfailed', (q) => errs.push('failed: ' + q.url().slice(0, 120) + ' ' + q.failure()?.errorText));
    p.on('response', (s) => s.status() >= 400 && errs.push(`http ${s.status()}: ${s.url().slice(0, 140)}`));
    let status = 0;
    try { const res = await p.goto(`${H}:${port}${r}`, { waitUntil: 'load', timeout: 30000 }); status = res?.status() ?? 0; await p.waitForTimeout(3500); } catch (e) { errs.push('goto: ' + e.message.slice(0, 150)); }
    const overlay = await p.evaluate(() => !!document.querySelector('vite-error-overlay')).catch(() => false);
    const body = (await p.evaluate(() => document.body?.innerText?.slice(0, 160)).catch(() => '')) || '';
    const shot = `/workspace/postup-pm/siteaudit/${name}${r.replace(/\W+/g, '_')}.png`;
    await p.screenshot({ path: shot }).catch(() => {});
    out.push({ name, port, r, status, overlay, errs: [...new Set(errs)].slice(0, 12), body: body.replace(/\s+/g, ' ') });
    await b.close();
  }
}
console.log(JSON.stringify(out, null, 1));
