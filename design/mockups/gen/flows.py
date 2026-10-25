# Critical flows (Martin, Oct 24 2026 [M1024]). exec'd by build.py after menu.py.
# Reads gen/flowdata.py; writes flows/<id>.md, flows/<id>.html (player), flows/index.html, flows/all.md;
# appends to notes/all.md and llms.txt; adds a Flows group to the index and the floating menu.
import json, re, os, html as H
exec(open('gen/flowdata.py').read())
OVHOST={o:NOTES['ov-'+o]['host'] for o in re.findall(r'id="ov-([\w-]+)"',OVS)}
ids=set()
for f in FLOWS:
    assert f['id'] not in ids, f['id']; ids.add(f['id'])
    assert f['pri'] in ('MVP must','nice') and f['status'] in ('martin','draft')
    texts=[f['goal']]+[s[4] for s in f['steps']]+f['branches']+f['success']+f['decide']
    for t in texts:
        if not tags(t): raise SystemExit(f'flows: untagged line in {f["id"]}: {t}')
        for g in tags(t):
            if re.match(r'F\d',g) and g not in FACTS: raise SystemExit(f'flows: unknown fact {g} in {f["id"]}')
    for sc,a,l,x,t in f['steps']:
        if sc not in S: raise SystemExit(f'flows: unknown screen {sc} in {f["id"]}')
        assert a in ('in','out') and l in ('live','none')
        if 'ov' in x and x['ov'] not in OVHOST: raise SystemExit(f'flows: unknown sheet {x["ov"]} in {f["id"]}')
def surl(f,st,rel='../'):
    sc,a,l,x,_=st; d=x.get('device',f['start']['device'])
    q=f'style=fresh&device={d}&auth={a}&live={l}'+(f'&mode={x["mode"]}' if 'mode' in x else '')+(f'&ov={x["ov"]}' if 'ov' in x else '')
    return f'{rel}index.html?{q}#{sc}'
def murl(f,st): return surl(f,st,'/mockups/').replace('/mockups/index.html','/mockups/')
STAT={'martin':"Martin's example (Oct 24)",'draft':'Draft, inferred from the notes; confirm with Martin'}
def flow_md(f,lvl='#'):
    s=f['start']; L=lvl+'#'
    o=f"{lvl} Flow: {f['name']} (`{f['id']}`)\nPriority: **{f['pri']}** · Status: {STAT[f['status']]} [M1024]\nPlayer: /mockups/flows/{f['id']}.html\n\n"
    o+=f"{L} Persona\n- {f['persona']}\n\n{L} Starting state\n- auth={s['auth']} · live={s['live']} · device={s['device']} · entry URL `{s['url']}`\n\n{L} Goal\n- {f['goal']}\n\n{L} Steps\n"
    o+=''.join(f"{i}. `#{st[0]}`{' + sheet `'+st[3]['ov']+'`' if 'ov' in st[3] else ''} · auth={st[1]} live={st[2]}{' mode='+st[3]['mode'] if 'mode' in st[3] else ''} — {st[4]} ({murl(f,st)})\n" for i,st in enumerate(f['steps'],1))
    for h,k in [('Branches and edge cases','branches'),('Success criteria','success'),('Needs Martin\'s decision','decide')]:
        if f[k]: o+=f"\n{L} {h}\n"+''.join(f'- {b}\n' for b in f[k])
    return o
os.makedirs('flows',exist_ok=True)
for fn in os.listdir('flows'):
    if os.path.isfile(os.path.join('flows',fn)): os.remove(os.path.join('flows',fn))
HEAD='Critical flows (Martin, Oct 24 2026 [M1024]): a type of user arrives in a certain situation and goes through a scenario step by step. Each step names the screen and the scenario params (auth, live, Home mode, sheet). Flows marked Draft were inferred from the screen notes; confirm with Martin.'
for f in FLOWS: open(f'flows/{f["id"]}.md','w').write(flow_md(f)+f'\n{LEGEND} M1024 = Martin, Oct 24 2026: track critical flows.\n')
FALL='# PostUp critical flows\n'+HEAD+'\n\n'+'\n'.join(f"- [{f['id']}]({f['id']}.md) · {f['pri']} · {f['name']}" for f in FLOWS)+'\n\n'+'\n---\n\n'.join(flow_md(f,'##') for f in FLOWS)
open('flows/all.md','w').write(FALL)
# all.md + llms.txt
with open('notes/all.md','a') as fh: fh.write('\n---\n\n# Critical flows\n'+HEAD+'\n\n'+'\n---\n\n'.join(flow_md(f,'##') for f in FLOWS))
with open('llms.txt','a') as fh: fh.write('\n## Critical flows\n'+HEAD+'\n- [All flows in one file](flows/all.md)\n'+''.join(f"- [{f['id']}](flows/{f['id']}.md): {f['name']} ({f['pri']}{', draft' if f['status']=='draft' else ''}) · player: flows/{f['id']}.html\n" for f in FLOWS))
# player pages
PCSS='''*{box-sizing:border-box}body{margin:0;font:14px/1.4 Inter,system-ui,sans-serif;color:#232322;background:#f4f3ef}a{color:#0f7a4f}
.fp{display:grid;grid-template-columns:360px 1fr;height:100vh}.side{overflow:auto;padding:16px;background:#fff;border-right:1px solid #e4e2dc}
.side h1{font-size:18px;margin:6px 0}.meta{font-size:12px;color:#6b6b67}.pill{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:99px;background:#e6f4ec;color:#0f7a4f;margin-right:4px}.pill.dr{background:#fff3d6;color:#8a5a00}.pill.nc{background:#eceae4;color:#55544f}
.nv{display:flex;gap:8px;align-items:center;margin:12px 0}.nv button{font:600 14px Inter,sans-serif;padding:9px 16px;border-radius:10px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}.nv button.pr{background:#10a364;border-color:#10a364;color:#fff}.nv button:disabled{opacity:.4}
.cur{background:#f7f6f2;border-radius:10px;padding:10px;margin:8px 0}.cur code{font-size:12px}
ol{padding-left:22px;margin:6px 0}ol li{padding:5px 6px;border-radius:8px;cursor:pointer;margin:2px 0}ol li.on{background:#e6f4ec;font-weight:600}ol li:hover{background:#f1f0eb}
h3{font-size:13px;margin:14px 0 4px;text-transform:uppercase;letter-spacing:.04em;color:#6b6b67}ul{padding-left:18px;margin:4px 0}.tg{font-size:10.5px;color:#8a8984}
.stage{display:flex;align-items:center;justify-content:center;overflow:hidden;padding:12px}iframe{border:0;background:#fff;border-radius:18px;box-shadow:0 8px 30px rgba(0,0,0,.15)}
iframe.phone{width:430px;height:min(900px,calc(100vh - 24px))}iframe.desktop{width:100%;height:calc(100vh - 24px)}
@media(max-width:820px){.fp{display:flex;flex-direction:column;height:auto}.side{display:contents}.top{order:0;padding:12px 14px 4px}.stage{order:1}.side>*:not(.top){order:2;padding:0 14px}.stage{padding:0 0 12px}iframe.phone,iframe.desktop{width:100%;height:72vh;border-radius:12px}}'''
def esc(t): return re.sub(r'(\[[^\]]+\])',r'<span class="tg">\1</span>',H.escape(t,quote=False))
def player(f):
    st=[{'u':surl(f,s),'sc':s[0],'ov':s[3].get('ov',''),'p':f"auth={s[1]} · live={s[2]}"+(f" · mode={s[3]['mode']}" if 'mode' in s[3] else '')+(f" · sheet={s[3]['ov']}" if 'ov' in s[3] else ''),'t':esc(s[4])} for s in f['steps']]
    s=f['start']; dev=s['device']
    li=''.join(f'<li data-i="{i}">#{x["sc"]}{" + "+x["ov"] if x["ov"] else ""} <span class="meta">{x["p"]}</span></li>' for i,x in enumerate(st))
    sec=lambda h,k:(f'<h3>{h}</h3><ul>'+''.join(f'<li>{esc(b)}</li>' for b in f[k])+'</ul>') if f[k] else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flow · {H.escape(f['name'])} · PostUp mockups</title><style>{PCSS}</style></head><body>
<div class="fp"><div class="side"><div class="top"><a href="index.html">← All flows</a> · <a href="../index.html#index">Mockups</a>
<h1>{H.escape(f['name'])}</h1><span class="pill{'' if f['pri']=='MVP must' else ' nc'}">{f['pri']}</span><span class="pill{' dr' if f['status']=='draft' else ''}">{'Draft' if f['status']=='draft' else "Martin's example"}</span> <span class="tg">[M1024]</span>
<div class="nv"><button id="bk" onclick="step(i-1)">Back</button><button id="nx" class="pr" onclick="step(i+1)">Next</button><span class="meta" id="pos"></span></div>
<div class="cur"><b id="ct"></b><div class="meta"><code id="cp"></code> · <a id="cu" target="_blank">open with notes</a></div></div></div>
<p class="meta"><b>Persona:</b> {H.escape(f['persona'])}<br><b>Start:</b> auth={s['auth']} · live={s['live']} · {dev} · entry <code>{H.escape(s['url'])}</code><br><b>Goal:</b> {esc(f['goal'])}</p>
<h3>Steps</h3><ol id="sl">{li}</ol>{sec('Branches and edge cases','branches')}{sec('Success','success')}{sec("Needs Martin's decision",'decide')}
<p class="meta"><a href="{f['id']}.md">{f['id']}.md</a></p></div>
<div class="stage"><iframe id="fr" class="{dev}" title="Mockup step"></iframe></div></div>
<script>var S={json.dumps(st)},i=0,fr=document.getElementById("fr"),y=0;fr.addEventListener("load",function(){{scrollTo(0,y);setTimeout(function(){{scrollTo(0,y)}},300)}});
function step(n){{if(n<0||n>=S.length)return;i=n;y=scrollY;var x=S[i];fr.className=x.u.indexOf("device=desktop")>0?"desktop":"phone";fr.src=x.u.replace("#","&notes=0&fs="+i+"#");
document.getElementById("ct").innerHTML=(i+1)+". "+x.t;document.getElementById("cp").textContent="#"+x.sc+" · "+x.p;document.getElementById("cu").href=x.u;
document.getElementById("pos").textContent="Step "+(i+1)+" of "+S.length;document.getElementById("bk").disabled=i==0;document.getElementById("nx").disabled=i==S.length-1;
document.querySelectorAll("#sl li").forEach(function(l){{l.classList.toggle("on",+l.dataset.i===i)}});history.replaceState(null,"","#"+(i+1))}}
document.getElementById("sl").addEventListener("click",function(e){{var l=e.target.closest("li");if(l)step(+l.dataset.i)}});
addEventListener("keydown",function(e){{if(e.key==="ArrowRight")step(i+1);if(e.key==="ArrowLeft")step(i-1)}});
step(Math.max(0,Math.min(S.length-1,(parseInt(location.hash.slice(1))||1)-1)));</script></body></html>'''
for f in FLOWS: open(f'flows/{f["id"]}.html','w').write(player(f))
rows=''.join(f'<li><a href="{f["id"]}.html"><b>{H.escape(f["name"])}</b></a> <span class="pill{"" if f["pri"]=="MVP must" else " nc"}">{f["pri"]}</span>{"<span class=\"pill dr\">Draft</span>" if f["status"]=="draft" else "<span class=\"pill\">Martin&#39;s example</span>"}<div class="meta">{H.escape(f["persona"])} · start auth={f["start"]["auth"]}, live={f["start"]["live"]}, {f["start"]["device"]}, <code>{H.escape(f["start"]["url"])}</code> · {len(f["steps"])} steps</div></li>' for f in FLOWS)
open('flows/index.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flows · PostUp mockups</title><style>{PCSS} .wrap{{max-width:760px;margin:0 auto;padding:20px}} .wrap li{{margin:10px 0;cursor:default}}</style></head><body><div class="wrap"><a href="../index.html#index">← Mockups</a> · <a href="grid.html">All flows grid</a><h1>Critical flows</h1><p class="meta">{esc(HEAD)} · <a href="all.md">all.md</a></p><ol>{rows}</ol></div></body></html>''')
# all flows on one page: one cell per step (thumbs from gen/flowthumbs.mjs)
TAPS=json.load(open('flows/thumbs/taps.json')) if os.path.exists('flows/thumbs/taps.json') else {}
GCSS=PCSS+""".gb{position:sticky;top:0;z-index:5;background:rgba(244,243,239,.95);backdrop-filter:blur(6px);border-bottom:1px solid #e4e2dc;padding:10px 16px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.gb input{flex:1;min-width:160px;font:14px Inter,sans-serif;padding:8px 12px;border:1px solid #d7d5cf;border-radius:10px}.gb button{font:600 13px Inter,sans-serif;padding:7px 12px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}.gb button.on{background:#10a364;color:#fff;border-color:#10a364}
.gb select{font:13px Inter,sans-serif;padding:7px;border-radius:10px;border:1px solid #d7d5cf;max-width:220px}.gw{max-width:1600px;margin:0 auto;padding:8px 16px 40px}
.gf{margin:22px 0 8px;scroll-margin-top:70px}.gf h2{font-size:18px;margin:0 0 2px}.gf h2 a{color:inherit;text-decoration:none}.gc{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}
.cell{width:240px;background:#fff;border:1px solid #e4e2dc;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:box-shadow .15s}.cell:hover{box-shadow:0 6px 20px rgba(0,0,0,.12)}.cell.dk{width:480px}
.cell img{width:100%;aspect-ratio:390/844;object-fit:cover;object-position:top;background:#eceae4;display:block}.cell.dk img{aspect-ratio:1280/800}
.cb{padding:8px 10px 10px}.cn{font:700 11px Inter,sans-serif;color:#0f7a4f;letter-spacing:.03em;text-transform:uppercase}.ct{font-size:12.5px;margin-top:2px}.ctap{font-size:11px;color:#6b6b67;margin-top:4px}
@media(max-width:560px){.gc{display:grid;grid-template-columns:1fr 1fr;gap:8px}.cell,.cell.dk{width:auto}.cell.dk{grid-column:1/-1}.gw{padding:4px 10px 30px}}"""
def cell(f,i,st):
    sc,a,l,x,t=st; tp=TAPS.get(f'{f["id"]}-{i}'); dk=(x.get('device',f['start']['device'])=='desktop')
    tap=(f'<div class="ctap">● taps {"Back" if tp["back"] else "“"+H.escape(tp["label"])+"”"}</div>' if tp else '')
    return f'<a class="cell{" dk" if dk else ""}" href="{f["id"]}.html#{i}"><img loading="lazy" src="thumbs/{f["id"]}-{i}.webp" alt="Step {i}: #{sc}" width="{480 if dk else 240}"><div class="cb"><div class="cn">{i} · {H.escape(NOTES[sc]["title"] if sc in NOTES else sc)}{" + "+x["ov"] if "ov" in x else ""}</div><div class="ct">{esc(t)}</div>{tap}<div class="meta" style="font-size:10.5px">auth={a} · live={l}{" · mode="+x["mode"] if "mode" in x else ""}</div></div></a>'
GSEC=''.join(f'<section class="gf" id="{f["id"]}" data-p="{"must" if f["pri"]=="MVP must" else "nice"}" data-q="{H.escape((f["name"]+" "+f["persona"]+" "+" ".join(s[0]+" "+s[4] for s in f["steps"])).lower())}"><h2><a href="{f["id"]}.html">{H.escape(f["name"])}</a></h2><div class="meta"><span class="pill{"" if f["pri"]=="MVP must" else " nc"}">{f["pri"]}</span>{"<span class=\"pill dr\">Draft</span>" if f["status"]=="draft" else "<span class=\"pill\">Martin&#39;s example</span>"} {H.escape(f["persona"])} · start auth={f["start"]["auth"]}, live={f["start"]["live"]}, {f["start"]["device"]}, <code>{H.escape(f["start"]["url"])}</code> · {len(f["steps"])} steps</div><div class="gc">'+''.join(cell(f,i,st) for i,st in enumerate(f['steps'],1))+'</div></section>' for f in FLOWS)
JUMP=''.join(f'<option value="{f["id"]}">{H.escape(f["name"])}</option>' for f in FLOWS)
open('flows/grid.html','w').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All flows · grid · PostUp mockups</title><style>{GCSS}</style></head><body>
<div class="gb"><a href="../index.html#index">← Mockups</a><b>All flows</b><button data-p="all" class="on">All</button><button data-p="must">MVP must</button><button data-p="nice">Nice</button><input id="q" placeholder="Search flows, screens, steps" autocomplete="off"><select id="j"><option value="">Jump to flow…</option>{JUMP}</select><span class="meta" id="cnt"></span></div>
<div class="gw"><p class="meta">{esc(HEAD)} Each cell is one step; the green ring marks what gets tapped next. Click a cell to open the player at that step.</p>{GSEC}</div>
<script>var P="all";function f(){{var q=document.getElementById("q").value.trim().toLowerCase(),n=0,c=0;document.querySelectorAll(".gf").forEach(function(s){{var m=(P=="all"||s.dataset.p==P)&&(!q||s.dataset.q.indexOf(q)>=0);s.hidden=!m;if(m){{n++;c+=s.querySelectorAll(".cell").length}}}});document.getElementById("cnt").textContent=n+" flows · "+c+" steps"}}
document.querySelectorAll(".gb button").forEach(function(b){{b.onclick=function(){{P=b.dataset.p;document.querySelectorAll(".gb button").forEach(function(x){{x.classList.toggle("on",x===b)}});f()}}}});
document.getElementById("q").oninput=f;document.getElementById("j").onchange=function(e){{var s=document.getElementById(e.target.value);if(s){{s.hidden=false;s.scrollIntoView()}}e.target.value=""}};f();</script></body></html>""")
# index + floating menu
FIX=''.join(ix(f'flows/{f["id"]}.html',f['name'],f"{f['pri']}{' · draft' if f['status']=='draft' else ''} · {len(f['steps'])} steps",'spark') for f in FLOWS)
S['index']=S['index'].replace('<h3 class="sh">Scenario</h3>',f'<h3 class="sh">Critical flows</h3><div class="grp"><a class="ixr" href="flows/index.html"><span class="ixi">{I("list",18)}</span><span class="lm"><b>All flows</b><span class="mu sm">Who arrives, in what situation, step by step</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/grid.html"><span class="ixi">{I("image",18)}</span><span class="lm"><b>All flows grid</b><span class="mu sm">Every step of every flow at once</span></span>{I("chev",18,"mu")}</a>{FIX}</div><h3 class="sh">Scenario</h3>',1)
assert 'Critical flows' in S['index']
FMENU='<div class="pmr pmfl"><label>Flows</label><div class="pmos">'+''.join(f'<a class="pmo pmf" href="flows/{f["id"]}.html" title="{H.escape(f["pri"])}">{H.escape(f["name"])}{"" if f["pri"]=="MVP must" else " (nice)"}</a>' for f in FLOWS)+'<a class="pmo pmf" href="flows/grid.html"><b>All flows grid →</b></a><a class="pmo pmf" href="flows/index.html"><b>Flow list →</b></a></div></div>'
MENU_HTML=MENU_HTML.replace('<div class="pmr"><label>Sheets</label>',FMENU+'<div class="pmr"><label>Sheets</label>',1)
assert 'pmfl' in MENU_HTML
MENU_CSS+='.pmf{text-decoration:none;color:inherit;display:inline-block}'
print('flows',len(FLOWS))
