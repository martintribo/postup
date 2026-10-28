# PostUp mockup model (Martin, Oct 27 2026 [M1030]): loader + state resolver shared by validate.py (and, in phase 2, the generator).
# Files: model/screens/<id>.toml, model/flows/<id>.toml, model/events.toml, model/global.toml. Plain TOML (stdlib tomllib).
import tomllib, os, re, glob
ROOT=os.environ.get('MODEL_ROOT') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','model')
SLOT_KINDS={'sheet','modal','drawer','panel','tab'}
ACTIONS={'replace','open','swap','close','back'}
SCREEN_KINDS={'page','sheet','modal','drawer','panel','tab'}
DEVICES={'phone','desktop'}
ROLES={'joiner','host','account','visitor'}
STATUSES={'martin','draft'}
DIMS={'auth':('in','out'),'live':('live','none'),'tab':('live','building'),'phase':('1','2')}
# View phase [M1035]: a site-state dimension like auth, but not part of the state id. A phase-N flow walks phase-N screen
# versions; untagged flows and the 'All' view use the latest phase (MAXPH). Conditions: phase=1, phase>=2, phase<=1.
PHASES=(1,2); MAXPH=max(PHASES)
TAG=r'\[(F\d{3}|FS|TK§\d|R\d+⚠?|drawn|unsourced|M1018[bc]?|M1024|M1025|M1030|M1031-draft|M1032|M1033|M1034|M1035|M1036)\]'
def load(root=ROOT):
    sc={}; fl={}
    for p in sorted(glob.glob(f'{root}/screens/*.toml')):
        d=tomllib.load(open(p,'rb')); d['_file']=p; sc[d['id']]=d
    for p in sorted(glob.glob(f'{root}/flows/*.toml')):
        d=tomllib.load(open(p,'rb')); d['_file']=p; fl[d['id']]=d
    ev=tomllib.load(open(f'{root}/events.toml','rb')); ev['_file']=f'{root}/events.toml'
    gl=tomllib.load(open(f'{root}/global.toml','rb')); gl['_file']=f'{root}/global.toml'
    return sc,fl,ev,gl
def parse_when(w):
    """'auth=out,live=none; auth=in' -> list of dicts (alternatives). '' -> [{}] (always).
    Phase may use >= or <= ('phase>=2' -> {'phase': '>=2'}); other keys use = only. [M1035]"""
    if not w: return [{}]
    out=[]
    for alt in w.split(';'):
        d={}
        for kv in alt.split(','):
            m=re.fullmatch(r'\s*(\w+)\s*(>=|<=|=)\s*(\S+)\s*',kv)
            if not m: d[kv.strip()]='?'; continue
            d[m[1]]=(m[3] if m[2]=='=' else m[2]+m[3])
        out.append(d)
    return out
def _ok(cur,v):
    if v[:2] in ('>=','<='):
        try: c=int(cur); n=int(v[2:])
        except (TypeError,ValueError): return False
        return c>=n if v[:2]=='>=' else c<=n
    return cur is not None and str(cur)==v
def matches(w,st):
    st=dict(st); st.setdefault('phase',MAXPH)
    return any(all(_ok(st.get(k),v) for k,v in alt.items()) for alt in parse_when(w))
# A site state: root screen + open child (slot, screen) chain + conditions. Kept flat for the current depth (page + one sheet)
# but resolve() walks children generically. dict(root=, kids=[(slot,screen),...], auth=, live=, tab=)
def key(st): return st['root']+''.join('+'+c for _,c in st['kids'])+f"@{st['auth']}.{st['live']}"+(f".{st['tab']}" if st['root']=='home' else '')
def top(st): return st['kids'][-1][1] if st['kids'] else st['root']
def dmode(l,ph=None): return 'live' if l=='live' or (ph or MAXPH)<2 else 'building'  # phase 1 has no Building mode [M1035]
def apply_sets(st,sets):
    for kv in (sets or '').split(','):
        if '=' in kv:
            k,v=kv.split('=',1)
            if k in DIMS: st[k]=v
def resolve(sc,st,link,owner=None):
    """Return the new state after taking link from st (link belongs to owner: the top screen or a chrome screen), or None.
    'open' may carry then=<page>: the opened child remembers it (st['cont']); a child link with continue=true then
    replaces the root with that page instead of just closing (the signin sheet's continuation, [M1031-draft])."""
    owner=owner or top(st)
    cond=dict(auth=st['auth'],live=st['live'],tab=st.get('tab'),phase=st.get('phase') or MAXPH)
    if not matches(link.get('when',''),cond): return None
    n=dict(st,kids=list(st['kids'])); n['cont']=None; a=link['action']; to=link.get('to')
    if a=='close' and link.get('continue') and st.get('cont'): a='replace'; to=st['cont']
    if a=='replace':
        n['root']=to; n['kids']=[]
        apply_sets(n,link.get('sets'))
        if to=='home' and st['root']!='home' and 'tab=' not in (link.get('sets') or ''): n['tab']=dmode(n['live'],n.get('phase'))
    elif a=='open':
        slot=link.get('slot','sheet'); host=owner
        if not slot_accepts(sc,host,slot,to): return None
        n['kids'].append((slot,to)); apply_sets(n,link.get('sets')); n['cont']=link.get('then')
    elif a=='swap':
        if to==owner or (to==st['root'] and not st['kids']): apply_sets(n,link.get('sets'))
        else:
            if not n['kids']: return None
            slot=n['kids'][-1][0]; host=n['kids'][-2][1] if len(n['kids'])>1 else n['root']
            if not slot_accepts(sc,host,slot,to): return None
            n['kids'][-1]=(slot,to); apply_sets(n,link.get('sets'))
    elif a=='close':
        if not n['kids']: return None
        n['kids'].pop(); apply_sets(n,link.get('sets'))
    elif a=='back': return 'back'
    if n['root']!='home': n['tab']=None
    elif not n.get('tab'): n['tab']=dmode(n['live'],n.get('phase'))
    return n
def slot_accepts(sc,host,slot,child):
    s=sc.get(host)
    if not s: return False
    return any(x['name']==slot and child in x.get('accepts',[]) for x in s.get('slots',[]))
def chrome(sc,st):
    """Chrome screens showing in the root's tab/panel slots for this device (only when no child slot is open)."""
    if st['kids']: return []
    dev=st.get('device') or 'phone'
    return [c for x in sc[st['root']].get('slots',[]) if x['kind'] in ('tab','panel') and x.get('device',dev)==dev for c in x.get('accepts',[])]
def available(sc,st):
    """(owner, link) pairs the user can take: the top screen's links, then chrome links (tab bar, desktop rail)."""
    t=top(st); return [(t,l) for l in sc[t].get('links',[])]+[(c,l) for c in chrome(sc,st) for l in sc[c].get('links',[])]
def find_link(sc,st,ref):
    """'screen:id' -> (owner, link alternatives with that id) if that screen is on top or in chrome now."""
    own,_,lid=ref.partition(':')
    if own!=top(st) and own not in chrome(sc,st): return own,None
    return own,[l for l in sc.get(own,{}).get('links',[]) if l['id']==lid]
def rendered_id(s,auth,live,tab,phase=None):
    """HTML element id that renders screen s in these conditions: first matching 'variants' entry, else the screen id.
    Variant keys may name the phase, e.g. "phase=1" or "phase=1,auth=out" [M1035]."""
    c=dict(auth=auth,live=live,tab=tab,phase=phase or MAXPH)
    for w,hid in (s.get('variants') or {}).items():
        if matches(w,c): return hid
    return s['id']
def lineof(path,needle,nth=0):
    n=-1
    for i,l in enumerate(open(path),1):
        if needle in l:
            n+=1
            if n==nth: return i
    return 1
USERS={'newcomer','registered'}
import tomllib as _tl, os as _os
REPL={c['id']:(c['replaces'],c['with']) for c in _tl.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','model','events.toml'),'rb'))['conditions'] if 'replaces' in c}
def flow_phase(f): return f.get('phase') or MAXPH  # the phase version a flow walks [M1035]
def flow_states(sc,f):
    """Replay a flow; return the list of (state-key, screens on it) per step (assumes it validates)."""
    s0=f['start']; cur=dict(device=s0.get('device','phone'),root=s0['screen'],kids=[('sheet',s0['sheet'])] if s0.get('sheet') else [],auth=s0['auth'],live=s0['live'],tab=s0.get('tab') if s0['screen']=='home' else None,phase=flow_phase(f))
    if cur['root']=='home' and not cur['tab']: cur['tab']=dmode(cur['live'],cur['phase'])
    out=[]; hist=[cur]
    for i,st in enumerate(f['steps']):
        if i and 'link' in st:
            own,ls=find_link(sc,dict(cur,device=st.get('device') or s0.get('device','phone')),st['link']); n=None
            for l in ls or []:
                _c=REPL.get(st.get('condition'))
                if _c and l.get('to')==_c[0]: l=dict(l,to=_c[1])  # data condition swaps the target screen [M1033]
                n=resolve(sc,cur,l,own)
                if n: break
            if n=='back': hist.pop(); cur=dict(hist[-1])
            elif n: cur=n; hist.append(n)
        elif i and st.get('expect'):
            cur=dict(parse_key(st['expect']),phase=cur['phase']); hist.append(cur)
        out.append((key(cur),[cur['root']]+[c for _,c in cur['kids']]))
    return out
def parse_key(k):
    m=re.fullmatch(r'([\w-]+)(?:\+([\w-]+))?@(in|out)\.(live|none)(?:\.(live|building))?',k)
    p,o,a,l,t=m.groups(); return dict(root=p,kids=[('sheet',o)] if o else [],auth=a,live=l,tab=(t or dmode(l)) if p=='home' else None)
def phases(sc,fl,gl):
    """Phase classification [M1031-draft]. Explicit: flow 'phase', screen 'phase', state overrides (global.toml [state_phases],
    screen [state_phases]). Derived: a screen/state on a phased flow gets the lowest such flow phase unless tagged. Untagged = None."""
    FP={k:f.get('phase') for k,f in fl.items()}
    SO=dict(gl.get('state_phases',{}))
    for s in sc.values(): SO.update(s.get('state_phases',{}))
    SP={k:s.get('phase') for k,s in sc.items()}; STP={}; SRC={}
    for fid,f in fl.items():
        ph=FP[fid]
        if not ph: continue
        for k,scs in flow_states(sc,f):
            STP[k]=min(STP.get(k) or ph,ph)
            for s in scs:
                if sc[s].get('phase') is None: SP[s]=min(SP.get(s) or ph,ph)
    STP.update(SO)
    return FP,SP,STP
def load_situations(root=ROOT):
    p=f'{root}/situations.toml'
    d=tomllib.load(open(p,'rb')) if os.path.exists(p) else {'situations':[]}
    load_situations.groups={g['id']:g for g in sorted(d.get('groups',[]),key=lambda g:g.get('order',99))}
    return {x['id']:x for x in d['situations']},p
