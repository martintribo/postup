# Site graph (Martin, Oct 25 2026 [M1025]; from the model since Oct 31 [M1031-draft]). exec'd by flows.py (needs S, OVS, NOTES, FLOWS).
# A SITE STATE = page [+ sheet in its slot] + auth (out|in) + live (someone live nearby: live|none) [+ Home tab].
# States and edges come from model/ (screens, slots, links, events, conditions) via gen/model.py. The mockup HTML is still
# hand-written, so the build checks DRIFT both ways: every link the HTML renders must be in the model, and every model link
# must be rendered (same rendered variant the browser picks). Writes flows/sitegraph.json, flows/sitegraph.md, flows/site.html.
import sys as _sys
_sys.path.insert(0,'gen'); import model as M, htmllinks as HL
SC,_MFL,MEV,_MGL=M.load()
PH_F,PH_S,PH_ST=M.phases(SC,_MFL,_MGL)  # phase per flow / screen / site state (derived) [M1031-draft]
def ph1(x,kind='s'): return 1 if (PH_S if kind=='s' else PH_ST).get(x)==1 else 0
PAGES=[k for k in S if '--' not in k and k!='index']
OVCH={m[1]:m[2] for m in re.finditer(r'<div class="ov" id="ov-([\w-]+)">(.*?)</div></div>(?=<div class="ov"|$)',OVS,re.S)}
assert set(OVCH)==set(OVHOST), (set(OVCH)^set(OVHOST))
_mp=[k for k,v in SC.items() if v['kind']=='page']; _ms=[k for k,v in SC.items() if v['kind']=='sheet']
if set(_mp)!=set(PAGES) or set(_ms)!=set(OVCH): raise SystemExit(f'model/HTML screen drift: pages {set(_mp)^set(PAGES)} sheets {set(_ms)^set(OVCH)}')
PGROUPS=[]
for p in PAGES:
    g=SC[p]['group']
    if g not in [x for x,_ in PGROUPS]: PGROUPS.append((g,[]))
    dict(PGROUPS)[g].append(p)
def rendered(page,a,l,mode): return S[M.rendered_id(SC[page],a,l,mode)]
def sid(p,ov,a,l,m=None): return f'{p}{"+"+ov if ov else ""}@{a}.{l}{"."+m if m else ""}'
def dmode(l): return 'live' if l=='live' else 'building'
def _mst(k):
    s=SST[k]; return dict(root=s['page'],kids=[('sheet',s['ov'])] if s['ov'] else [],auth=s['auth'],live=s['live'],tab=s['mode'],device='phone')
def _sk(n): return sid(n['root'],n['kids'][-1][1] if n['kids'] else None,n['auth'],n['live'],n['tab'] if n['root']=='home' else None)
SST={}
for p in PAGES:
    for a in ('out','in'):
        for l in ('live','none'):
            for m in (('live','building') if p=='home' else (None,)):
                SST[sid(p,None,a,l,m)]=dict(page=p,ov=None,auth=a,live=l,mode=m)
                for x in SC[p].get('slots',[]):
                    if x['kind']!='sheet': continue
                    for o in x['accepts']:
                        if o=='signin' and a=='in': continue
                        SST[sid(p,o,a,l,m)]=dict(page=p,ov=o,auth=a,live=l,mode=m)
SHEETON={o:{OVHOST[o]}|{s['page'] for s in SST.values() if s['ov']==o} for o in OVHOST}
EDGES={}
def add(f,t,lab,kind):
    if t is not None and t not in SST: return
    EDGES.setdefault(f,[])
    if not any(e[0]==t and e[2]==kind and e[1]==lab for e in EDGES[f]): EDGES[f].append((t,lab,kind))
def _kind(l,st,n):
    if l['action']=='back': return 'back'
    if 'auth=in' in (l.get('sets') or ''): return 'sign-in'
    if l['action']=='close': return 'close'
    if l['action'] in ('open',) or (l['action']=='swap' and n['kids']): return 'sheet'
    if 'tab=' in (l.get('sets') or ''): return 'mode'
    return 'tap'
CONT={}  # page -> continuation targets of links that open signin there
for p in PAGES:
    CONT[p]={l['then'] for l in SC[p].get('links',[]) if l.get('then')}
for k,st in SST.items():
    ms=_mst(k)
    for dev in ('phone','desktop'):
        for own,l in M.available(SC,dict(ms,device=dev)):
            n=M.resolve(SC,dict(ms,device=dev),l,own)
            if n is None: continue
            if n=='back': add(k,None,'Back','back'); continue
            add(k,_sk(n),l.get('label') or l['id'],_kind(l,ms,n))
            if l.get('continue') and st['ov']:
                for t in sorted(CONT.get(st['page'],())):
                    n2=M.resolve(SC,dict(ms,cont=t),l,own); add(k,_sk(n2),'signs in → continues','sign-in')
POSTUPISH=[e for e in MEV['events'] if e['id']=='postup-ends'][0]['on']
def _ev_ok(e,ms):
    on=e.get('on',['*']); return not ms['kids'] and ('*' in on or ms['root'] in on)
for k,st in SST.items():
    ms=_mst(k)
    for e in MEV['events']+[c for c in MEV['conditions'] if 'action' in c]:
        if _ev_ok(e,ms):
            n=M.resolve(SC,ms,e,ms['root'])
            if n: add(k,_sk(n),e['label'],'event' if e in MEV['events'] else 'cond')
    for c in [c for c in MEV['conditions'] if 'replaces' in c]:
        for t,lab,kind in list(EDGES.get(k,[])):
            if t and SST[t]['page']==c['replaces'] and not SST[t]['ov']: add(k,sid(c['with'],None,SST[t]['auth'],SST[t]['live']),lab+f' ({c["label"]})','cond')
NE=sum(len(v) for v in EDGES.values())
# ---- drift check: HTML links vs model links, per page x condition (and per sheet x auth) ----
_DRIFT=[]
def _norm(t): return (t[0],t[1] if t[0]!='swap' or t[1] else '',t[3] if t[0]=='open' else '')
def _mlinks(sc_id,cond,in_sheet):
    out=set()
    for l in SC[sc_id].get('links',[]):
        if not M.matches(l.get('when',''),cond): continue
        out.add((l['action'],l.get('to',''),l.get('then','') if l['action']=='open' else ''))
    return out
_IDS=set(S)
for p in PAGES:
    for a in ('out','in'):
        for l in ('live','none'):
            for m in (('live','building') if p=='home' else (None,)):
                ch=rendered(p,a,l,m); cond=dict(auth=a,live=l,tab=m)
                html={(x[0],x[1],x[3] if x[0]=='open' else '') for tg,lab in HL.links(HL.TABNAV.sub('',ch),_IDS) for x in HL.acts(tg,lab,a,p,False) if x[1]!='index'}
                mod=_mlinks(p,cond,False)
                if html!=mod: _DRIFT.append(f'{p} {a}.{l}{"."+m if m else ""}: HTML only {sorted(html-mod)} · model only {sorted(mod-html)}')
                has=bool(HL.TABNAV.search(ch)); dec=any(x['kind']=='tab' for x in SC[p].get('slots',[]))
                if has!=dec: _DRIFT.append(f'{p} {a}.{l}: tab bar drawn={has} but model tab slot={dec}')
for o in OVCH:
    for a in (('out',) if o=='signin' else ('out','in')):
        html={(x[0],x[1],'') for tg,lab in HL.links(OVCH[o],_IDS) for x in HL.acts(tg,lab,a,o,True)}
        mod={(x,y,'') for x,y,_ in _mlinks(o,dict(auth=a,live='live',tab=None),True)}
        if html!=mod: _DRIFT.append(f'sheet {o} {a}: HTML only {sorted(html-mod)} · model only {sorted(mod-html)}')
_tb={(x[0],x[1]) for tg,lab in HL.links(HL.TABNAV.search(S['home'])[0],_IDS) for x in HL.acts(tg,lab,'in','',False)}
if _tb!={(l['action'],l['to']) for l in SC['tabbar']['links']}: _DRIFT.append(f'tabbar: HTML {sorted(_tb)} vs model')
_rl={(x[0],x[1]) for tg,lab in HL.links(DESK.split('</aside>')[0],_IDS) for x in HL.acts(tg,lab,'in','',False) if x[1]!='index'}
if _rl!={(l['action'],l['to']) for l in SC['rail']['links']}: _DRIFT.append(f'rail: HTML {sorted(_rl)} vs model')
if _DRIFT: raise SystemExit('model/HTML link drift (the model is the source; fix the HTML or the model):\n  '+'\n  '.join(_DRIFT))
# ---- flow steps: how each is reached (from the model replay in flowload.py; validate.py already proved them) ----
SG_GAPS=[]; SG_HOW={}
for f in FLOWS:
    for i,d in enumerate(f['sx']):
        if d['site'] not in SST: raise SystemExit(f'sitegraph: {f["id"]} step {i+1}: site state {d["site"]} is not in the site graph')
        SG_HOW[(f['id'],i)]=d['how']
# ---- derive next states and enterable flows ----
def live_inv(p,ov,a):
    if ov: return True
    if p=='home': return False
    return rendered(p,a,'live',None)==rendered(p,a,'none',None)
def compat(x,y):
    X,Y=SST[x],SST[y]
    if (X['page'],X['ov'],X['auth'],X['mode'])!=(Y['page'],Y['ov'],Y['auth'],Y['mode']): return False
    return X['live']==Y['live'] or live_inv(X['page'],X['ov'],X['auth'])
SG_NEXT={}; SG_ENTER={}
for f in FLOWS:
    xs=f['sx']
    for i,d in enumerate(xs):
        nx=xs[i+1]['site'] if i+1<len(xs) else None
        seen=[]
        for t,lab,kind in EDGES.get(d['site'],[]):
            if kind in('event',): continue
            key=t or 'back'
            if key==d['site']: continue
            if key not in [s[0] for s in seen]: seen.append((key,lab,kind,key==nx))
        SG_NEXT[(f['id'],i)]=seen
        en=[]
        for g in FLOWS:
            if g['id']==f['id']: continue
            for j,e in enumerate(g['sx'][:-1]):
                if compat(d['site'],e['site']):
                    en.append(dict(f=g['id'],j=j,user=e['user'],next=g['sx'][j+1]['site'],same=(g['sx'][j+1]['site']==nx))); break
        SG_ENTER[(f['id'],i)]=en
SG_CONN={}
for f in FLOWS:
    xs=f['sx']; out=[]; inn=[]
    for i,d in enumerate(xs):
        for e in SG_ENTER[(f['id'],i)]:
            g=[h for h in FLOWS if h['id']==e['f']][0]
            if not e['same']: out.append((i,e['f'],e['j']))
            gp=g['sx'][e['j']-1]['site'] if e['j']>0 else None; mp=xs[i-1]['site'] if i>0 else None
            if e['j']>0 and gp!=mp: inn.append((i,e['f'],e['j']))
    SG_CONN[f['id']]=dict(out=out,inn=inn)
NCONN=sum(len(v) for v in SG_ENTER.values())
# ---- outputs ----
def surl_s(k,dev='phone'):
    s=SST[k]; q=f'style=fresh&device={dev}&auth={s["auth"]}&live={s["live"]}'+(f'&mode={s["mode"]}' if s['mode'] else '')+(f'&ov={s["ov"]}' if s['ov'] else '')
    return f'../index.html?{q}#{s["page"]}'
print('sitegraph',len(PAGES),'pages',len(OVHOST),'sheets',len(SST),'states',NE,'edges',NCONN,'connections',len(SG_GAPS),'gaps')

def sg_write():
    global SGHEAD,EVN
    json.dump(dict(states={k:dict(v,url=surl_s(k)[3:]) for k,v in SST.items()},edges={k:[list(e) for e in v] for k,v in EDGES.items()}),open('flows/sitegraph.json','w'))
    def ptitle(p): return NOTES[p]['title'] if p in NOTES else p
    def stname(k):
        s=SST[k]; return f'{s["auth"]}·{s["live"]}'+(f'·{s["mode"]}' if s['mode'] else '')
    def pedges(p,ov=None):
        agg={}
        for k,st in SST.items():
            if st['page']!=p or st['ov']!=ov: continue
            for t,lab,kind in EDGES.get(k,[]):
                if kind=='event': continue
                tp=('Back' if t is None else (SST[t]['page']+('+'+SST[t]['ov'] if SST[t]['ov'] else '')+(' (signs in)' if SST[t]['auth']!=st['auth'] and SST[t]['auth']=='in' else ' (signed out)' if SST[t]['auth']!=st['auth'] else '')))
                agg.setdefault((lab,tp,kind),set()).add(stname(k))
        allst={stname(k) for k,st in SST.items() if st['page']==p and st['ov']==ov}
        return [(lab,tp,kind,'' if v==allst else ', '.join(sorted(v))) for (lab,tp,kind),v in sorted(agg.items(),key=lambda x:(x[0][2]!='tap',x[0][1]))]
    EVN='Site events: '+'; '.join(e['label']+(' (on '+', '.join(e['on'])+')' if e.get('on')!=['*'] else '') for e in MEV['events'])+'. live = someone live nearby; a postup ending changes only its own page.'
    SGHEAD=f'Site graph (Martin, Oct 25 2026 [M1025]): {len(PAGES)} pages + {len(OVHOST)} sheets, {len(SST)} site states (page [+ child in a slot] × auth out|in × live (nearby) live|none, Home × tab), {NE} edges from the model (model/: screen links, tab bar and rail chrome slots, events, conditions). A flow is a path of steps, each a link (screen:id) or event that reaches the expected site state. Site-state id: page[+child]@auth.live[.tab]. See model/CONCEPTS.md. [M1031-draft]'
    md=f'# PostUp site graph\n{SGHEAD}\n\n{EVN}\n\nDimensions: auth = out | in; live = live (someone live nearby) | none; mode = live | building (Home only); data conditions are pages: postup-ask (host approves), postup-full, postup-cancelled, postup-ended, live (you are hosting), joined, requested (pending ask), empty-area, offline, cafe-gfail.\n'
    for gname,ps in PGROUPS:
        md+=f'\n## {gname}\n'
        for p in ps:
            md+=f'\n### {ptitle(p)} (`{p}`)\nStates: '+', '.join(f'`{k}`' for k,s in SST.items() if s['page']==p and not s['ov'])+'\n'
            md+=''.join(f'- {lab or "(tap)"} → `{tp}` [{kind}]{" — only "+c if c else ""}\n' for lab,tp,kind,c in pedges(p))
            for o in sorted({s['ov'] for s in SST.values() if s['page']==p and s['ov']}):
                md+=f'- sheet `{o}` over this page: '+'; '.join(f'{lab or "(tap)"} → `{tp}`' for lab,tp,kind,c in pedges(p,o))+'\n'
    md+='\n## Missing edges found by the flows (design gaps)\n'+(''.join(f'- `{fi}` step {n}: `{a}` → `{b}` ("{act}") [M1025]\n' for fi,n,a,b,act in SG_GAPS) or '- none\n')
    open('flows/sitegraph.md','w').write(md)
    # site.html
    def chip(k): s=SST[k]; return f'<a class="sc" data-ph="{ph1(k,"st")}" href="{surl_s(k)}" target="_blank">{stname(k)}</a>'
    cards=''
    for gname,ps in PGROUPS:
        cards+=f'<section class="pg"><h2>{H.escape(gname)}</h2><div class="pgs">'
        for p in ps:
            sts=''.join(chip(k) for k,s in SST.items() if s['page']==p and not s['ov'])
            ed=''.join(f'<li class="k-{kind}"><span class="el">{H.escape(lab or "(tap)")}</span> → <b>{H.escape(tp)}</b>{"<span class=cnd>"+H.escape(c)+"</span>" if c else ""}</li>' for lab,tp,kind,c in pedges(p))
            sh=''.join(f'<li class="k-sheet">sheet <b>{o}</b>: '+H.escape('; '.join(f'{lab or "(tap)"} → {tp}' for lab,tp,kind,c in pedges(p,o)))+'</li>' for o in sorted({s['ov'] for s in SST.values() if s['page']==p and s['ov']}))
            used=sorted({f['id'] for f in FLOWS for d in f['sx'] if SST[d['site']]['page']==p})
            cards+=f'<article class="pc" data-ph="{ph1(p)}" id="p-{p}"><h3>{H.escape(ptitle(p))}{p1b(ph1(p))} <code>{p}</code> <a class="sc" href="states.html#screen={p}">all states</a></h3><div class="sts">{sts}</div><ul>{ed}{sh}</ul>'+(f'<p class="fl">In flows: '+' '.join(f'<a href="{x}.html">{x}</a>' for x in used)+'</p>' if used else '')+'</article>'
        cards+='</div></section>'
    gaps=''.join(f'<li><a href="{fi}.html#{n}">{fi} step {n}</a>: <code>{H.escape(a)}</code> → <code>{H.escape(b)}</code> <span class="meta">({H.escape(act)})</span></li>' for fi,n,a,b,act in SG_GAPS) or '<li>none</li>'
    SITECSS=""".sgw{max-width:1500px;margin:0 auto;padding:10px 20px 40px}.pg h2{font-size:16px;margin:22px 0 8px;text-transform:uppercase;letter-spacing:.04em;color:#33332f}.pgs{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}
    .pc{background:#fff;border:1px solid #e4e2dc;border-radius:14px;padding:12px 14px}.pc h3{font-size:14.5px;margin:0 0 6px;text-transform:none;letter-spacing:0;color:#232322}.pc h3 code{font-size:11px;color:#6b6b67}
    .sts{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}.sc{font:600 10.5px ui-monospace,monospace;padding:2px 6px;border-radius:6px;background:#eef6f1;color:#0f7a4f;text-decoration:none}
    .pc ul{list-style:none;padding:0;margin:0;font-size:12.5px}.pc li{padding:2px 0;border-top:1px dashed #eceae4}.el{color:#55544f}.cnd{margin-left:6px;font-size:10.5px;color:#8a5a00;background:#fff3d6;border-radius:5px;padding:0 5px}
    .k-sign-in b{color:#0f7a4f}.k-back{color:#8a8984}.k-sheet{color:#4a3d8f}.fl{font-size:11.5px;color:#6b6b67;margin:6px 0 0}.fl a{margin-right:4px}.gp2{background:#fff8e6;border:1px solid #f1d9a6;border-radius:12px;padding:10px 14px;margin-top:10px}"""
    open('flows/site.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site graph · PostUp mockups</title><style>{PCSS}{SITECSS}{PHCSS}</style></head><body>
    <div class="sgw"><p><a href="../index.html#index">← Mockups</a> · <a href="sitemap.html">Site map (visual)</a> · <a href="states.html">States by screen</a> · {PHBTN} · <a href="map.html">Flow map</a> · <a href="grid.html">All flows grid</a> · <a href="index.html">Flow list</a> · <a href="sitegraph.md">sitegraph.md</a></p>
    <h1>Site graph</h1><p class="meta">{esc(SGHEAD)}<br>{H.escape(EVN)}<br>Chips are site states (auth·live[·mode]); each opens that state in the mockup. Arrows list taps; an amber note says the edge exists only in those states.</p>
    <div class="gp2"><b>Missing edges found by the flows (design gaps)</b><ul>{gaps}</ul></div>{cards}</div>{PHJS}</body></html>''')
    with open('llms.txt','a') as fh: fh.write(f'\n## Site graph\n{SGHEAD}\n- [Site graph: pages, site states, edges, design gaps](flows/sitegraph.md) · page: flows/site.html · data: flows/sitegraph.json\n')
