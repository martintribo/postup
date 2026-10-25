# Site graph (Martin, Oct 25 2026 [M1025]). exec'd by flows.py after the flow checks (needs S, OVS, NOTES, FLOWS).
# Pages = screens + sheets. A SITE STATE = page [+ sheet] + auth (out|in) + live (live|none) [+ Home mode].
# Edges are DERIVED from the mockup's own links (go/href/sheet/act/follow/ov/ovx/signIn/bk/setHome/postAt/pick)
# in whichever variant renders that state (same rule as gen/scen.js), plus a few site EVENTS (alerts, postup changes,
# network, someone goes live). Data conditions (full, ended, host, joined, pending ask...) are carried by the page.
# Writes flows/sitegraph.json, flows/sitegraph.md, flows/site.html; defines SG_* for flows.py.
from html.parser import HTMLParser
SDEST={"post-signin":"posted","join-signin":"joined","ask-signin":"ask","attach-signin":"posted"}
PAGES=[k for k in S if '--' not in k and k!='index']
OVCH={m[1]:m[2] for m in re.finditer(r'<div class="ov" id="ov-([\w-]+)">(.*?)</div></div>(?=<div class="ov"|$)',OVS,re.S)}
assert set(OVCH)==set(OVHOST), (set(OVCH)^set(OVHOST))
PGROUPS=[('Home & discover',['home','quiet-feed','quiet-feed-b','quiet','empty-area','loading','offline','home-overlay-alt']),
 ('Cafes & picking a place',['cafe','cafe-gfail','where','where-search']),
 ('Postups & joining',['postup','postup-ask','join-signin','ask-signin','ask','requested','joined','postup-full','postup-cancelled','postup-ended']),
 ('Posting & hosting',['post','post-signin','posted','live','post-edit']),
 ('Projects',['projects','project','project-new','project-update','project-attach','attach-signin']),
 ('Share-link landings',['invite','invite-ended','invite-project']),
 ('Inbox & people',['inbox','activity','chat','profile','me']),
 ('Account & safety',['settings','report','reported'])]
_g=[p for _,ps in PGROUPS for p in ps]; PGROUPS.append(('More',[p for p in PAGES if p not in _g])); PGROUPS=[g for g in PGROUPS if g[1]]
assert all(p in PAGES for p in _g), [p for p in _g if p not in PAGES]
class _LP(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.out=[]
    def handle_starttag(s,t,a):
        a=dict(a); js=(a.get('onclick') or ''); hr=a.get('href') or ''
        tg=[]
        for m in re.finditer(r"\b(go|sheet|ov|signIn|setHome|act)\('([\w-]*)'",js): tg.append((m[1],m[2]))
        if re.search(r'\bsignIn\(\)',js): tg.append(('signIn',''))
        if re.search(r'\bpostAt\(',js): tg.append(('go','post'))
        if re.search(r'\bfollow\(',js): tg.append(('follow',''))
        if re.search(r'\bbk\(\)',js): tg.append(('back',''))
        if re.search(r'\bovx\(\)',js) and not tg: tg.append(('ovx',''))
        if re.search(r'\bpick\(',js): tg.append(('back',''))
        m=re.fullmatch(r'#([\w-]+)',hr)
        if m and m[1] in S: tg.append(('go',m[1]))
        if t in ('br','img','input','meta','link','path','circle','rect'): 
            if tg: s.out.append([tg,a.get('aria-label','') or a.get('alt','') or a.get('placeholder','')])
            return
        s.st.append([tg,a.get('aria-label',''),''])
    def handle_endtag(s,t):
        if t in ('br','img','input','meta','link','path','circle','rect'): return
        if s.st:
            tg,al,tx=s.st.pop()
            if s.st: s.st[-1][2]+=' '+tx
            if tg: s.out.append([tg,(re.sub(r'\s+',' ',tx).strip() or al)[:34]])
    def handle_data(s,d):
        if s.st: s.st[-1][2]+=d
_LC={}
def links(chunk):
    if chunk not in _LC:
        p=_LP(); p.feed(chunk); _LC[chunk]=p.out
    return _LC[chunk]
def rendered(page,a,l,mode):
    if page=='home':
        k='home' if mode=='live' and l=='live' else 'home--map-none' if mode=='live' else 'home--bld-live' if l=='live' else 'home--bld'
        return S[k]
    for c in (f'{page}--{a}-{l}',f'{page}--{l}',f'{page}--{a}'):
        if c in S: return S[c]
    return S[page]
def sid(p,ov,a,l,m=None): return f'{p}{"+"+ov if ov else ""}@{a}.{l}{"."+m if m else ""}'
def dmode(l): return 'live' if l=='live' else 'building'
# site states: every page x auth x live (Home x mode); sheets on every page that opens them (+ their notes host)
SST={}
for p in PAGES:
    for a in ('out','in'):
        for l in ('live','none'):
            for m in (('live','building') if p=='home' else (None,)): SST[sid(p,None,a,l,m)]=dict(page=p,ov=None,auth=a,live=l,mode=m)
SHEETON={o:{OVHOST[o]} for o in OVHOST}
for k,st in list(SST.items()):
    for tg,_ in links(rendered(st['page'],st['auth'],st['live'],st['mode'])):
        for kind,t in tg:
            if kind=='ov' and t in OVHOST: SHEETON[t].add(st['page'])
            if kind in('act','follow') and st['auth']=='out': SHEETON['signin'].add(st['page'])
for o,ps in SHEETON.items():
    for p in ps:
        for a in (('out',) if o=='signin' else ('out','in')):
            for l in ('live','none'):
                for m in (('live','building') if p=='home' else (None,)): SST[sid(p,o,a,l,m)]=dict(page=p,ov=o,auth=a,live=l,mode=m)
# edges from links
EDGES={}  # from-id -> list of (to-id or None for back, label, kind)
def add(f,t,lab,kind):
    if t is not None and t not in SST: return
    EDGES.setdefault(f,[])
    if not any(e[0]==t and e[2]==kind and e[1]==lab for e in EDGES[f]): EDGES[f].append((t,lab,kind))
for k,st in SST.items():
    p,ov,a,l,m=st['page'],st['ov'],st['auth'],st['live'],st['mode']
    ch=OVCH[ov] if ov else rendered(p,a,l,m)
    for tg,lab in links(ch):
        out_=bool(re.search(r'sign out|delete',lab,re.I))
        for kind,t in tg:
            A='out' if out_ else a
            if kind=='go' and t in S: tp=t.split('--')[0]; add(k,sid(tp,None,A,l,(m if p=='home' else dmode(l)) if tp=='home' else None),lab,'tap')
            elif kind=='sheet': d=SDEST.get(t,t) if a=='in' else t; add(k,sid(d,None,a,l,None),lab,'tap')
            elif kind=='ov' and t in OVHOST: add(k,sid(p,t,a,l,m),lab,'sheet')
            elif kind=='ovx': add(k,sid(p,None,a,l,m),lab or 'close','close')
            elif kind=='act': add(k,sid(p,'signin',a,l,m) if a=='out' else sid(t,None,a,l,None),lab,'tap')
            elif kind=='follow' and a=='out': add(k,sid(p,'signin',a,l,m),lab,'sheet')
            elif kind=='signIn': d=t or p; add(k,sid(d,None,'in',l,(m or dmode(l)) if d=='home' else None),'signs in','sign-in')
            elif kind=='setHome' and p=='home': add(k,sid('home',None,a,l,t),lab or t,'mode')
            elif kind=='back': add(k,None,'Back','back')
# events (site changes the user doesn't tap)
POSTUPISH=['postup','postup-ask','joined','requested','invite','postup-full']
for k,st in SST.items():
    p,ov,a,l,m=st['page'],st['ov'],st['auth'],st['live'],st['mode']
    if ov: continue
    add(k,sid(p,None,a,'none' if l=='live' else 'live',m),'postups end' if l=='live' else 'someone goes live','event')
    if a=='in': add(k,sid('activity',None,a,l,None),'alert arrives','event')
    add(k,sid('home',None,a,l,dmode(l)),'comes back later','event')
    if p in POSTUPISH:
        for t in ('postup-full','postup-cancelled','postup-ended'): add(k,sid(t,None,a,l if t!='postup-ended' else 'none',None),'postup fills / is cancelled / ends','event')
    if p in ('quiet-feed','loading','home'): add(k,sid('offline',None,a,l,None),'network drops','event')
# data conditions (site data, not a tap): a cafe whose Google card fails, an area with no postups
for k,st in SST.items():
    for t,lab,kind in list(EDGES.get(k,[])):
        if t and SST[t]['page']=='cafe' and not SST[t]['ov']: add(k,sid('cafe-gfail',None,SST[t]['auth'],SST[t]['live']),lab+' (Google card fails)','cond')
    if st['page']=='home' and not st['ov'] and st['live']=='none': add(k,sid('empty-area',None,st['auth'],'none'),'area has no postups','cond')
NE=sum(len(v) for v in EDGES.values())
# ---- validate flows against the graph ----
SG_GAPS=[]; SG_HOW={}
for f in FLOWS:
    xs=f['sx']
    for i,d in enumerate(xs):
        if d['site'] not in SST: raise SystemExit(f'sitegraph: {f["id"]} step {i+1}: site state {d["site"]} is not in the site graph')
        if i==0: SG_HOW[(f['id'],0)]='entry'; continue
        pv=xs[i-1]['site']; cur=d['site']; es=EDGES.get(pv,[]); act=d['act']
        how=None
        if act.startswith('gap:'): how='gap'
        tap=[e for e in es if e[0]==cur and e[2]!='event']
        if not how and tap: how=tap[0][2]+': '+tap[0][1]
        if not how and any(e[2]=='back' for e in es) and cur in [x['site'] for x in xs[:i]]: how='back'
        c_=SST[cur]; flip=sid(c_['page'],c_['ov'],c_['auth'],'none' if c_['live']=='live' else 'live',c_['mode'])
        if not how and act.startswith('later:'):
            ev=[e for e in es if e[0] in (cur,flip) and e[2]=='event']
            if ev: how='event: '+ev[0][1]
        if not how:  # tap + the live state changing meanwhile
            c=SST[cur]; alt=sid(c['page'],c['ov'],c['auth'],'none' if c['live']=='live' else 'live',c['mode'] if c['page']!='home' else dmode('none' if c['live']=='live' else 'live') if c['mode']==dmode(c['live']) and False else c['mode'])
            t2=[e for e in es if e[0]==alt and e[2]!='event']
            if t2: how=t2[0][2]+': '+t2[0][1]+' (then live changes)'
        if not how:  # Back to an earlier step, then one tap
            for pr in [x['site'] for x in xs[:i-1]]:
                t3=[e for e in EDGES.get(pr,[]) if e[0]==cur and e[2]!='event']
                if t3 and any(e[2]=='back' for e in es): how=f'back, then {t3[0][2]}: {t3[0][1]}'; break
        if not how:  # two taps (e.g. close a sheet, then tap)
            for t1,l1,k1 in es:
                if t1 and k1 not in('event',):
                    t4=[e for e in EDGES.get(t1,[]) if e[0] in(cur,flip) and e[2]!='event']
                    if t4: how=f'2 taps: {l1 or k1}, then {t4[0][1] or t4[0][2]}'; break
        if not how or how=='gap': how='gap'; SG_GAPS.append((f['id'],i+1,pv,cur,act))
        SG_HOW[(f['id'],i)]=how
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
    EVN='Site events on every page: someone goes live / postups end (live ↔ none), alert arrives → Activity (signed in), comes back later → Home, network drops → Offline (Home, Nearby, Loading), postup fills / is cancelled / ends (postup pages).'
    SGHEAD=f'Site graph (Martin, Oct 25 2026 [M1025]): {len(PAGES)} pages + {len(OVHOST)} sheets, {len(SST)} site states (page [+ sheet] × auth out|in × live|none, Home × mode), {NE} edges derived from the mockup links plus site events. A flow is a path of steps, each = (site state, user state, action). Site-state id: page[+sheet]@auth.live[.mode].'
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
    def chip(k): s=SST[k]; return f'<a class="sc" href="{surl_s(k)}" target="_blank">{stname(k)}</a>'
    cards=''
    for gname,ps in PGROUPS:
        cards+=f'<section class="pg"><h2>{H.escape(gname)}</h2><div class="pgs">'
        for p in ps:
            sts=''.join(chip(k) for k,s in SST.items() if s['page']==p and not s['ov'])
            ed=''.join(f'<li class="k-{kind}"><span class="el">{H.escape(lab or "(tap)")}</span> → <b>{H.escape(tp)}</b>{"<span class=cnd>"+H.escape(c)+"</span>" if c else ""}</li>' for lab,tp,kind,c in pedges(p))
            sh=''.join(f'<li class="k-sheet">sheet <b>{o}</b>: '+H.escape('; '.join(f'{lab or "(tap)"} → {tp}' for lab,tp,kind,c in pedges(p,o)))+'</li>' for o in sorted({s['ov'] for s in SST.values() if s['page']==p and s['ov']}))
            used=sorted({f['id'] for f in FLOWS for d in f['sx'] if SST[d['site']]['page']==p})
            cards+=f'<article class="pc" id="p-{p}"><h3>{H.escape(ptitle(p))} <code>{p}</code></h3><div class="sts">{sts}</div><ul>{ed}{sh}</ul>'+(f'<p class="fl">In flows: '+' '.join(f'<a href="{x}.html">{x}</a>' for x in used)+'</p>' if used else '')+'</article>'
        cards+='</div></section>'
    gaps=''.join(f'<li><a href="{fi}.html#{n}">{fi} step {n}</a>: <code>{H.escape(a)}</code> → <code>{H.escape(b)}</code> <span class="meta">({H.escape(act)})</span></li>' for fi,n,a,b,act in SG_GAPS) or '<li>none</li>'
    SITECSS=""".sgw{max-width:1500px;margin:0 auto;padding:10px 20px 40px}.pg h2{font-size:16px;margin:22px 0 8px;text-transform:uppercase;letter-spacing:.04em;color:#33332f}.pgs{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}
    .pc{background:#fff;border:1px solid #e4e2dc;border-radius:14px;padding:12px 14px}.pc h3{font-size:14.5px;margin:0 0 6px;text-transform:none;letter-spacing:0;color:#232322}.pc h3 code{font-size:11px;color:#6b6b67}
    .sts{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}.sc{font:600 10.5px ui-monospace,monospace;padding:2px 6px;border-radius:6px;background:#eef6f1;color:#0f7a4f;text-decoration:none}
    .pc ul{list-style:none;padding:0;margin:0;font-size:12.5px}.pc li{padding:2px 0;border-top:1px dashed #eceae4}.el{color:#55544f}.cnd{margin-left:6px;font-size:10.5px;color:#8a5a00;background:#fff3d6;border-radius:5px;padding:0 5px}
    .k-sign-in b{color:#0f7a4f}.k-back{color:#8a8984}.k-sheet{color:#4a3d8f}.fl{font-size:11.5px;color:#6b6b67;margin:6px 0 0}.fl a{margin-right:4px}.gp2{background:#fff8e6;border:1px solid #f1d9a6;border-radius:12px;padding:10px 14px;margin-top:10px}"""
    open('flows/site.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site graph · PostUp mockups</title><style>{PCSS}{SITECSS}</style></head><body>
    <div class="sgw"><p><a href="../index.html#index">← Mockups</a> · <a href="map.html">Flow map</a> · <a href="grid.html">All flows grid</a> · <a href="index.html">Flow list</a> · <a href="sitegraph.md">sitegraph.md</a></p>
    <h1>Site graph</h1><p class="meta">{esc(SGHEAD)}<br>{H.escape(EVN)}<br>Chips are site states (auth·live[·mode]); each opens that state in the mockup. Arrows list taps; an amber note says the edge exists only in those states.</p>
    <div class="gp2"><b>Missing edges found by the flows (design gaps)</b><ul>{gaps}</ul></div>{cards}</div></body></html>''')
    with open('llms.txt','a') as fh: fh.write(f'\n## Site graph\n{SGHEAD}\n- [Site graph: pages, site states, edges, design gaps](flows/sitegraph.md) · page: flows/site.html · data: flows/sitegraph.json\n')
