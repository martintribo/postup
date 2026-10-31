# Situations map (Martin, Oct 27 2026 [M1031-draft]): one flow map per user type. Situations (model/situations.toml) are
# blocks with a setting line and buttons for their flows (from model/flows, situation = ...). exec'd by flows.py after
# flowmap.py. Both user types on one page, stacked as two rows: Newcomer, then Registered [M1038]. Writes flows/map.html (the old user-state machine is now flows/map-states.html). Respects the Phase toggle.
import model as _MOD
SITS,_=_MOD.load_situations()
UT=[('newcomer','Newcomer','Signed out, never used PostUp'),('registered','Registered','Signed in, has used PostUp')]
_TINT=['#e8f5ee','#e9f0fb','#fdf1e4','#f3ecfb','#fbeef1','#eaf6f6','#eef1f4','#f4f1e8']
def _fbtn(f): return f'<a class="fb" data-ph="{"n" if f["phase"] is None else f["phase"]}" href="{f["id"]}.html" title="{H.escape(f["persona"])}">{H.escape(f["name"])}{p1b(f["phase"])}<i>{len(f["steps"])} steps</i></a>'
_lanes=''
for u,ut,usub in UT:
    cards=''; n=0
    for gid,g in _MOD.load_situations.groups.items():
        inner=''; gph=None
        for sid,x in [(k,v) for k,v in SITS.items() if v['user']==u and v['group']==gid]:
            fs=[f for f in FLOWS if f['situation']==sid]
            _ps=[p for p in [x.get('phase')]+[f['phase'] for f in fs] if p is not None]; ph=min(_ps) if _ps else None; gph=min([p for p in (gph,ph) if p is not None] or [None]) if (gph is not None or ph is not None) else None  # 0 is phase 0, None = unphased [M1037]
            btns=''.join(_fbtn(f) for f in fs) or '<span class="nof">No flow yet</span>'
            inner+=f'<section class="sit" data-ph="{"n" if ph is None else ph}" id="s-{sid}" style="--t:{_TINT[n%len(_TINT)]}"><h3>{H.escape(x["title"])}{p1b(ph)}</h3><p>{esc(x["setting"])}</p><div class="fbs">{btns}</div></section>'; n+=1
        if inner: cards+=f'<div class="grp" data-ph="{"n" if gph is None else gph}" id="g-{u}-{gid}"><h2>{H.escape(g["title"])}</h2>{inner}</div>'
    nf=sum(1 for f in FLOWS if f['user']==u)
    _lanes+=f'<div class="lane" id="{u}"><div class="root"><b>{ut}</b><span>{usub}</span><span class="cnt">{sum(1 for v in SITS.values() if v["user"]==u)} situations · {nf} flows</span></div><div class="sits">{cards}</div></div>'
SMCSS='''.lane[hidden]{display:none!important}.mb{position:sticky;top:0;z-index:5;background:rgba(244,243,239,.96);border-bottom:1px solid #e4e2dc;padding:9px 16px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}.mb b{font-size:16px}
.ut{display:inline-flex;border:1px solid #d7d5cf;border-radius:99px;overflow:hidden}.ut a{padding:5px 14px;font:600 13px Inter,sans-serif;color:#33332f;text-decoration:none}.ut a.on{background:#232322;color:#fff}
.lane{display:flex;gap:14px;align-items:flex-start;padding:14px 16px 18px;margin:0 auto;border-bottom:1px solid #e4e2dc;scroll-margin-top:56px;transition:background .6s}.lane.hl{background:#e3f4ea}#registered .root{background:#2f4f8a}.root{flex:none;width:170px;background:#0f7a4f;color:#fff;border-radius:16px;padding:14px;position:sticky;top:64px}
.root b{display:block;font-size:17px}.root span{display:block;font-size:12px;opacity:.9;margin-top:3px}.root .cnt{margin-top:10px;opacity:.75}
.sits{flex:1;min-width:0;display:flex;gap:12px;align-items:flex-start;overflow-x:auto;padding-bottom:6px}.grp{flex:0 0 300px;background:#fff;border:1px solid #e4e2dc;border-radius:16px;padding:8px;margin:0 0 12px;display:flex;flex-direction:column;gap:8px}.grp h2{margin:2px 4px 0;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#6b6b67}
.sit{background:var(--t);border:1px solid rgba(0,0,0,.07);border-radius:14px;padding:10px 12px;position:relative}
.sit h3{margin:0;font-size:14px;color:#232322}.sit p{margin:3px 0 8px;font-size:12px;color:#55544f}.fbs{display:flex;flex-wrap:wrap;gap:5px}
.fb{display:inline-flex;align-items:center;gap:4px;background:#fff;border:1px solid #d7d5cf;border-radius:10px;padding:5px 9px;font:600 12.5px Inter,sans-serif;color:#232322;text-decoration:none}.fb:hover{border-color:#10a364;color:#0f7a4f}.fb i{font-style:normal;font-weight:400;font-size:10.5px;color:#8a8984}
.nof{font-size:12px;color:#8a5a00;background:#fff3d6;border-radius:8px;padding:3px 8px}
@media(max-width:700px){.lane{flex-direction:column;padding:10px}.root{position:static;width:auto}.sits{width:100%}.grp{flex-basis:82vw}.sit:before{display:none}}'''
SMJS='''function sh(){var u=location.hash.slice(1);document.querySelectorAll(".ut a").forEach(function(a){a.classList.toggle("on",a.getAttribute("href")==="#"+u)});var l=document.getElementById(u);if(!l||!l.classList.contains("lane"))return;l.scrollIntoView({block:"start"});l.classList.add("hl");setTimeout(function(){l.classList.remove("hl")},1500)}addEventListener("hashchange",sh);addEventListener("load",sh);/* both rows always shown; #newcomer / #registered scroll to and highlight a row [M1038] */'''
open('flows/map.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flow map by situation · PostUp mockups</title><style>{PCSS}{PHCSS}{SMCSS}</style></head><body>
<div class="mb"><a href="../index.html#index">← Mockups</a><b>Flow map</b><span class="ut"><a href="#newcomer">Newcomer</a><a href="#registered">Registered</a></span>{PHBTN}<span class="meta">Row 1 Newcomer, row 2 Registered; each row scrolls sideways. Each button opens the flow player. [M1038]</span><span style="flex:1"></span><a href="index.html">Flow list</a><a href="grid.html">Grid</a><a href="map-states.html">User-state map (old)</a><a href="explore.html">Map + states</a></div>
{_lanes}{PHJS}<script>{SMJS}</script></body></html>''')
with open('llms.txt','a') as fh: fh.write('- [Flow map by situation](flows/map.html): per user type (#newcomer, #registered), situations with their flows; data model/situations.toml\n')
print('situations map',len(SITS),'situations')
