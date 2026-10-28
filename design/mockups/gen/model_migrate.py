# One-off migration (Oct 27 2026 [M1030]): old sources (HTML links, notes.md, flowdata.py, sitegraph.py) -> model/*.toml.
# Runs the old pipeline in a temp copy (old generator untouched), dumps its in-memory data, writes model files.
import os, re, json, shutil, subprocess, pickle, itertools, sys
HERE=os.path.dirname(os.path.abspath(__file__)); MOCK=os.path.dirname(HERE); OUT=os.path.join(MOCK,'model')
TMP='/tmp/mm_migrate'
shutil.rmtree(TMP,ignore_errors=True); shutil.copytree(MOCK,TMP,ignore=shutil.ignore_patterns('model','flows','shots','img','node_modules'))
os.makedirs(TMP+'/img',exist_ok=True); shutil.copytree(MOCK+'/flows/thumbs',TMP+'/flows/thumbs',dirs_exist_ok=True)
with open(TMP+'/gen/flows.py','a') as fh: fh.write('''
import pickle as _pk
_LK={f'{p}|{a}|{l}|{m}':links(rendered(p,a,l,m)) for p in PAGES for a in ('out','in') for l in ('live','none') for m in (('live','building') if p=='home' else (None,))}
_OL={o:links(OVCH[o]) for o in OVCH}
_pk.dump(dict(LK=_LK,OL=_OL,S=list(S),OVHOST=OVHOST,NOTES=NOTES,ORDER=ORDER,G=G,PGROUPS=PGROUPS,SHEETON={k:sorted(v) for k,v in SHEETON.items()},SDEST=SDEST,FLOWS=FLOWS,PAGES=PAGES,POSTUPISH=POSTUPISH,ROLE=ROLE),open('/tmp/mm_dump.pkl','wb'))
''')
subprocess.run(['python3','gen/build.py'],cwd=TMP,check=True,stdout=subprocess.DEVNULL)
D=pickle.load(open('/tmp/mm_dump.pkl','rb'))
PAGES=D['PAGES']; SHEETS=sorted(D['OVHOST']); NOTES=D['NOTES']
def q(s): return json.dumps(s,ensure_ascii=False)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:28] or 'x'
SIGNOUT=re.compile(r'sign out|delete',re.I)
def acts(tg,lab,a,owner,in_sheet):
    """old link -> list of (action,to,sets,slot) for one rendered combo"""
    kinds=[k for k,_ in tg]; out=[]
    for kind,t in tg:
        if kind=='ovx' and len(tg)>1: continue
        so='auth=out' if SIGNOUT.search(lab or '') else ''
        if kind=='go': out.append(('replace',t.split('--')[0],so,''))
        elif kind=='sheet': out.append(('replace',t if a=='out' else D['SDEST'].get(t,t),'',''))
        elif kind=='ov': out.append(('swap' if in_sheet else 'open',t,'','sheet'))
        elif kind=='ovx': out.append(('close','',so,''))
        elif kind=='act': out.append(('open','signin','','sheet') if a=='out' else ('replace',t,'',''))
        elif kind=='follow': out.append(('open','signin','','sheet') if a=='out' else ('swap',owner,'following=toggle',''))
        elif kind=='signIn': out.append(('close','','auth=in','') if (in_sheet and not t) else ('replace',t or owner,'auth=in',''))
        elif kind=='setHome': out.append(('swap','home','tab='+t,''))
        elif kind=='back': out.append(('back','','',''))
    return out
def combos(p):
    return [(a,l,m) for a in ('out','in') for l in ('live','none') for m in (('live','building') if p=='home' else (None,))]
def condense(p,cs):
    al=set(combos(p))
    if set(cs)==al: return ''
    dims=['auth','live']+(['tab'] if p=='home' else [])
    def val(c,d): return {'auth':c[0],'live':c[1],'tab':c[2]}[d]
    for r in (1,2,3):
        for ds in itertools.combinations(dims,r):
            vals={tuple(val(c,d) for d in ds) for c in cs}
            # alternatives over these dims that exactly cover cs
            cover={c for c in al if tuple(val(c,d) for d in ds) in vals}
            if cover==set(cs): return ';'.join(','.join(f'{d}={v}' for d,v in zip(ds,vs)) for vs in sorted(vals))
    return ';'.join(','.join(f'{d}={val(c,d)}' for d in dims) for c in sorted(cs,key=str))
def links_for(p):
    acc={}  # (lab,action,to,sets,slot)->[combos]
    for c in combos(p):
        a,l,m=c
        for tg,lab in D['LK'][f'{p}|{a}|{l}|{m}']:
            for x in acts(tg,lab,a,p,False):
                acc.setdefault((lab.strip(),)+x,[]).append(c)
    return [(k,condense(p,v)) for k,v in acc.items()]
def sheet_links(o):
    acc={}
    for tg,lab in D['OL'][o]:
        for a in (('out',) if o=='signin' else ('out','in')):
            for x in acts(tg,lab,a,o,True): acc.setdefault((lab.strip(),)+x,[]).append(a)
    res=[]
    for k,v in acc.items():
        v=set(v); w='' if (o=='signin' or v=={'out','in'}) else 'auth='+v.pop()
        res.append((k,w))
    return res
def link_lines(ls):
    ids=set(); out=[]
    for (lab,act,to,sets,slot),w in ls:
        base=slug((lab or act)+('-'+to if to and act!='back' else ''))
        i=base; n=2
        while i in ids: i=f'{base}-{n}'; n+=1
        ids.add(i)
        f=[f'id = {q(i)}',f'label = {q(lab)}',f'action = {q(act)}']
        if to: f.append(f'to = {q(to)}')
        if slot: f.append(f'slot = {q(slot)}')
        if sets: f.append(f'sets = {q(sets)}')
        if w: f.append(f'when = {q(w)}')
        out.append('  { '+', '.join(f)+' },')
    return out
def notes_toml(n):
    o=[]
    for s,bs in n['secs']:
        o.append(f'[[notes]]\nsection = {q(s)}\nlines = [')
        o+= [f'  {q(b)},' for b in bs]; o.append(']\n')
    return '\n'.join(o)
GROUP={p:g for g,ps in D['PGROUPS'] for p in ps}
ENTRY={'home','invite','invite-ended','invite-project'}
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'/screens'); os.makedirs(OUT+'/flows')
# signin sheet hosts: wherever a link opens it
SIGNHOST={p for p in PAGES for c in combos(p) for tg,lab in D['LK'][f'{p}|{c[0]}|{c[1]}|{c[2]}'] for k,_ in tg if k in('act','follow') and c[0]=='out'}
ACCEPT={p:set() for p in PAGES}
for o,ps in D['SHEETON'].items():
    for p in ps: ACCEPT[p].add(o)
for p in SIGNHOST: ACCEPT[p].add('signin')
# closure: a sheet can swap in another sheet (More -> Block/Share), so the host slot must accept it too (as the mockup does)
_sw={o:{t for tg,_ in D['OL'][o] for k,t in tg if k=='ov'} for o in D['OL']}
for p in PAGES:
    ch=True
    while ch:
        ch=False
        for o in list(ACCEPT[p]):
            for t in _sw.get(o,()):
                if t not in ACCEPT[p]: ACCEPT[p].add(t); ch=True
VARIANTS={p:[k for k in D['S'] if k.split('--')[0]==p and '--' in k] for p in PAGES}
for p in PAGES:
    n=NOTES[p]; L=[f'# Screen: {n["title"]}. Model [M1030]; migrated from gen/notes.md, gen/build.py/more.py HTML links, sitegraph.py.',
      f'id = {q(p)}',f'title = {q(n["title"])}','kind = "page"',f'group = {q(GROUP.get(p,"More"))}']
    if p in ENTRY: L.append('entry = true')
    if p in ('home-overlay-alt','quiet-feed-b'): L.append('alternative = true  # design alternative, not linked from the site')
    if VARIANTS[p]: L.append(f'variants = {q(VARIANTS[p])}  # old HTML variants, by condition')
    if p=='home': L.append('states = { tab = ["live", "building"] }')
    if ACCEPT[p]: L.append(f'slots = [ {{ name = "sheet", kind = "sheet", accepts = {q(sorted(ACCEPT[p]))} }} ]')
    L.append('links = ['); L+=link_lines(links_for(p)); L.append(']\n')
    L.append(notes_toml(n))
    open(f'{OUT}/screens/{p}.toml','w').write('\n'.join(L))
for o in SHEETS:
    n=NOTES['ov-'+o]; L=[f'# Sheet: {n["title"]}. Model [M1030]; migrated (old id ov-{o}, notes host {n["host"]}).',
      f'id = {q(o)}',f'title = {q(n["title"])}','kind = "sheet"','group = "Sheets"']
    L.append('links = ['); L+=link_lines(sheet_links(o)); L.append(']\n'); L.append(notes_toml(n))
    open(f'{OUT}/screens/{o}.toml','w').write('\n'.join(L))
# global + index notes
G=D['G']; I=NOTES['index']
open(f'{OUT}/global.toml','w').write('# Global rules + mockup-index notes (not product screens). [M1030]\n'+notes_toml(G)+'\n# ---- mockup index (site chrome) ----\n'+notes_toml(I).replace('[[notes]]','[[index_notes]]'))
# events + data conditions (from sitegraph.py)
EV=f'''# Site events (not taps) and data conditions, from gen/sitegraph.py. [M1030]
# on = screens it can happen on ("*" = any page, no sheet open). action/to/sets as for links.
events = [
  {{ id = "postups-end", label = "postups end", on = ["*"], when = "live=live", action = "swap", sets = "live=none" }},
  {{ id = "someone-goes-live", label = "someone goes live", on = ["*"], when = "live=none", action = "swap", sets = "live=live" }},
  {{ id = "alert-arrives", label = "alert arrives", on = ["*"], when = "auth=in", action = "replace", to = "activity" }},
  {{ id = "comes-back-later", label = "comes back later", on = ["*"], action = "replace", to = "home" }},
  {{ id = "postup-fills", label = "postup fills", on = {q(D['POSTUPISH'])}, action = "replace", to = "postup-full" }},
  {{ id = "postup-cancelled", label = "postup is cancelled", on = {q(D['POSTUPISH'])}, action = "replace", to = "postup-cancelled" }},
  {{ id = "postup-ends", label = "postup ends", on = {q(D['POSTUPISH'])}, action = "replace", to = "postup-ended", sets = "live=none" }},
  {{ id = "network-drops", label = "network drops", on = ["quiet-feed", "loading", "home"], action = "replace", to = "offline" }},
]
conditions = [
  {{ id = "google-card-fails", label = "Google card fails", replaces = "cafe", with = "cafe-gfail" }},
  {{ id = "empty-area", label = "area has no postups", on = ["home"], when = "live=none", action = "replace", to = "empty-area" }},
]
'''
open(f'{OUT}/events.toml','w').write(EV)
# flows
sys.path.insert(0,HERE); import model as M
sc,_,ev,_=M.load(OUT)
def parse_site(s):
    m=re.fullmatch(r'([\w-]+)(?:\+([\w-]+))?@(in|out)\.(live|none)(?:\.(live|building))?',s)
    p,o,a,l,t=m.groups(); return dict(root=p,kids=[('sheet',o)] if o else [],auth=a,live=l,tab=(t or M.dmode(l)) if p=='home' else None)
def same(x,y): return M.key(x)==M.key(y)
def ev_apply(e,st):
    on=e.get('on',['*'])
    if st['kids'] or not ('*' in on or st['root'] in on): return None
    return M.resolve(sc,st,dict(e),owner=st['root'])
REPORT=[]
for f in D['FLOWS']:
    L=[f'# Flow: {f["name"]}. Model [M1030]; migrated from gen/flowdata.py.',f'id = {q(f["id"])}',f'name = {q(f["name"])}',
       f'role = {q(D["ROLE"].get(f["id"],"joiner"))}',f'mvp = {"true" if f["pri"]=="MVP must" else "false"}',f'status = {q(f["status"])}',
       f'persona = {q(f["persona"])}',f'goal = {q(f["goal"])}',f'intent = {q(f["sx"][0]["user"])}']
    st0=parse_site(f['sx'][0]['site']); s=f['start']
    L.append(f'start = {{ screen = {q(st0["root"])}'+(f', sheet = {q(st0["kids"][0][1])}' if st0['kids'] else '')+f', auth = {q(st0["auth"])}, live = {q(st0["live"])}'+(f', tab = {q(st0["tab"])}' if st0['tab'] else '')+f', device = {q(s["device"])}, url = {q(s["url"])} }}')
    for k,h in (('edge_cases','branches'),('success','success'),('decide','decide')):
        L.append(f'{k} = [\n'+''.join(f'  {q(b)},\n' for b in f[h])+']')
    hist=[st0]; cur=st0
    for i,d in enumerate(f['sx']):
        L.append('\n[[steps]]')
        if i==0: L.append(f'arrive = {q(d["act"])}')
        else:
            nxt=parse_site(d['site']); got=None
            if not d['act'].startswith('later:'):
                for own,l in M.available(sc,cur):
                    r=M.resolve(sc,cur,l,own)
                    if r and r!='back' and same(r,nxt): got=('link',f'{own}:{l["id"]}',None); break
                if not got and len(hist)>1 and any(l['action']=='back' for _,l in M.available(sc,cur)) and same(hist[-2],nxt): got=('link',f'{M.top(cur)}:back',None)
                if not got:
                    for own,l in M.available(sc,cur):
                        if l.get('to')=='cafe':
                            r=M.resolve(sc,cur,dict(l,to='cafe-gfail'),own)
                            if r and r!='back' and same(r,nxt): got=('link',f'{own}:{l["id"]}','google-card-fails'); break
            if not got:
                for e in ev['events']+[c for c in ev['conditions'] if 'action' in c]:
                    r=ev_apply(e,cur)
                    if r and same(r,nxt): got=('event',e['id'],None); break
            if not got:
                got=('gap',d['act'],None); REPORT.append((f['id'],i+1,M.key(cur),d['site'],d['act']))
            if got[0]=='link': L.append(f'link = {q(got[1])}  # {d["act"]}')
            elif got[0]=='event': L.append(f'event = {q(got[1])}  # {d["act"]}')
            else: L.append(f'gap = {q(got[1])}  # no single link/event from {M.key(cur)} to {d["site"]}')
            if got[2]: L.append(f'condition = {q(got[2])}')
            if got[1].endswith(':back') and got[0]=='link': hist.pop(); cur=hist[-1]
            else: cur=nxt; hist.append(nxt)
        L.append(f'expect = {q(d["site"])}')
        L.append(f'thought = {q(d["user"])}'); L.append(f'shows = {q(d["do"])}')
        if d.get('device'): L.append(f'device = {q(d["device"])}')
    open(f'{OUT}/flows/{f["id"]}.toml','w').write('\n'.join(L)+'\n')
print('screens',len(PAGES),'sheets',len(SHEETS),'flows',len(D['FLOWS']),'unmatched steps',len(REPORT))
for r in REPORT: print('  UNMATCHED',r)
