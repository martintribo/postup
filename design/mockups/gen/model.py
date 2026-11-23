# PostUp mockup model (Martin, Oct 27 2026 [M1030]): loader + state resolver shared by validate.py and the generator.
# Files: model/screens/<id>.toml, model/flows/<id>.toml, model/events.toml, model/global.toml, model/phases.toml. Plain TOML.
import tomllib, os, re, glob
ROOT=os.environ.get('MODEL_ROOT') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','model')
SLOT_KINDS={'sheet','modal','drawer','panel','tab'}
ACTIONS={'replace','open','swap','close','back'}
SCREEN_KINDS={'page','sheet','modal','drawer','panel','tab'}
DEVICES={'phone','desktop'}
ROLES={'joiner','host','account','visitor'}
STATUSES={'martin','draft'}
DIMS={'auth':('in','out'),'live':('live','none'),'tab':('live','building')}
# View phase [M1035] [M1047-draft]: a dimension like auth, but not part of the state id. Phase ids and order
# live in model/phases.toml. An item may set since= / until= (inclusive phase ids); untagged = every phase.
# A flow is walked in its `since` phase if set, otherwise the latest phase. The "All" UI view renders the latest phase.
TAG=r'\[(F\d{3}|FS|TK§\d|R\d+⚠?|drawn|unsourced|M1018[bc]?|M1024|M1025|M1030|M1031-draft|M1032|M1033|M1034|M1035|M1036|M1037|M1038|M1039|M1040|M1041|M1042|M1043|M1044|M1045|M1046|M1047-draft|M1047|M1048)\]'

# ---- phases.toml [M1047-draft] ----
PHASES=[]; PBY={}; PIDS=[]; LATEST=None; PEXCEPT=[]; PHASES_FILE=None; ALIAS={}
def load_phases(root=ROOT):
    """Ordered phases, exceptions, and the file path. Omitted deliverable/rules inherit the previous phase."""
    p=os.path.join(root,'phases.toml')
    d=tomllib.load(open(p,'rb')) if os.path.exists(p) else {'phases':[]}
    phases=list(d.get('phases') or [])
    prev=None
    for ph in phases:
        inh=dict(prev['deliverable']) if prev and prev.get('deliverable') else {}
        if 'deliverable' not in ph and inh: ph['deliverable']=inh
        elif 'deliverable' in ph and inh:
            ph['deliverable']=dict(inh, **{k:ph['deliverable'][k] for k in ph['deliverable']})
        prev=ph
    return phases, list(d.get('exceptions') or []), p
def init_phases(root=ROOT):
    """Load phase ids, aliases (including 0/ph0 and the badge), and latest = last in the file."""
    global PHASES,PBY,PIDS,LATEST,PEXCEPT,PHASES_FILE,ALIAS
    PHASES,PEXCEPT,PHASES_FILE=load_phases(root)
    PIDS=[x['id'] for x in PHASES]; PBY={x['id']:x for x in PHASES}
    LATEST=PIDS[-1] if PIDS else None
    ALIAS={}
    for i,x in enumerate(PHASES):
        ALIAS[x['id']]=x['id']
        for a in list(x.get('aliases') or [])+[str(i), x.get('badge'), f"ph{i}", f"p{x.get('badge',i)}"]:
            if a is not None and str(a) not in ALIAS: ALIAS[str(a)]=x['id']
    return PHASES
def pid(val, default=None):
    """Resolve a phase id or alias. None -> default (typically LATEST for a view, never for availability)."""
    if val is None: return default
    s=str(val)
    if s not in ALIAS: raise ValueError(f'unknown phase {val!r}')
    return ALIAS[s]
def pindex(val):
    return PIDS.index(pid(val, LATEST))
def phase_label(val):
    ph=PBY.get(pid(val, LATEST), {})
    return ph.get('label') or (pid(val, LATEST) or '')
def phase_badge(val):
    if val is None: return None
    return PBY[pid(val)].get('badge')
def in_phase(item, ph):
    """True if item (dict with optional since/until) is available in phase ph. Untagged = every phase."""
    try:
        ph=pid(ph)
    except ValueError:
        return False
    if ph not in PIDS: return False
    i=PIDS.index(ph)
    s,u=item.get('since'), item.get('until')
    try:
        if s is not None and PIDS.index(pid(s))>i: return False
        if u is not None and PIDS.index(pid(u))<i: return False
    except ValueError:
        return False
    return True


def walk_phase(item):
    """Phase version a flow/outcome is walked in: its since, or the latest phase if untagged [M1047-draft]."""
    return pid(item.get('since'), LATEST)
def phase_rules(ph):
    d=(PBY.get(pid(ph, LATEST)) or {}).get('deliverable') or {}
    return list(d.get('rules') or [])
def phase_goals(ph):
    d=(PBY.get(pid(ph, LATEST)) or {}).get('deliverable') or {}
    return list(d.get('goals') or [])
def has_rule(ph, rule):
    return rule in phase_rules(ph)
def vp(ph):
    """View phase: None or 'all' -> latest phase id (the All view renders latest)."""
    if ph is None or str(ph) in ('all','','latest'): return LATEST
    return pid(ph)
init_phases(ROOT)

def load(root=ROOT):
    init_phases(root)
    sc={}; fl={}
    for p in sorted(glob.glob(f'{root}/screens/*.toml')):
        d=tomllib.load(open(p,'rb')); d['_file']=p; sc[d['id']]=d
    for p in sorted(glob.glob(f'{root}/flows/*.toml')):
        d=tomllib.load(open(p,'rb')); d['_file']=p; fl[d['id']]=d
    US=load_users(root); WAYS=load_ways(root); SEGS=load_segments(root)
    for fid in list(fl): apply_ways(fl[fid],US,WAYS)
    for fid in list(fl): expand_segments(fl[fid],SEGS,US)
    for fid in list(fl): fl.update(expand_outcomes(fl[fid]))
    ev=tomllib.load(open(f'{root}/events.toml','rb')); ev['_file']=f'{root}/events.toml'
    gl=tomllib.load(open(f'{root}/global.toml','rb')); gl['_file']=f'{root}/global.toml'
    global _SC; _SC=sc
    return sc,fl,ev,gl
_SC=None
# Normalized model data [M1044] (Martin, Oct 31 2026): user types, ways in and segments are each defined once and reused.
def _tload(root,name,key):
    p=f'{root}/{name}'
    if not os.path.exists(p): return {},p
    d=tomllib.load(open(p,'rb')); return {x['id']:dict(x,_file=p) for x in d.get(key,[]) if isinstance(x.get('id'),str)},p
def load_users(root=ROOT):
    """model/users.toml: each user type (id, label, sub, auth, main_flow, milestones it can reach) [M1044]."""
    return _tload(root,'users.toml','users')[0]
def load_ways(root=ROOT):
    """model/ways.toml: ways in (id, label, when, start without auth, users, optional holds = goals already reached) [M1044]."""
    return _tload(root,'ways.toml','ways')[0]
def load_segments(root=ROOT):
    """model/segments.toml: reusable step runs shared by every flow [M1044]; a flow may still declare its own [[segments]]."""
    return _tload(root,'segments.toml','segments')[0]
def way_start(w,auth):
    s=dict(w.get('start',{})); s['auth']=auth; s.setdefault('device','phone')
    if w.get('holds'): s['holds']=list(w['holds'])
    return s
def apply_ways(f,US,WAYS):
    """way = "<id>" on a flow (its main entry) or on an at = 0 outcome sets start (auth from the flow's user type) and the
    entry text from model/ways.toml, so a way in is written once for every user type [M1044]."""
    auth=US.get(f.get('user'),{}).get('auth','out')
    if f.get('way') in WAYS:
        w=WAYS[f['way']]; f['start']=way_start(w,auth); f.setdefault('entry',w.get('when',''))
    for o in f.get('outcomes',[]):
        if o.get('at')==0 and o.get('way') in WAYS:
            w=WAYS[o['way']]; o['start']=way_start(w,auth); o.setdefault('when',w.get('when','')); o.setdefault('label',w.get('label',''))
def _fill(v,vars_):
    if isinstance(v,str):
        for k,x in vars_.items(): v=v.replace('{'+k+'}',str(x))
    return v
def expand_segments(f,gsegs=None,US=None):
    """Reusable step runs [M1043]. A flow may declare [[segments]] (id, note, steps); a step { use = "<segment>", live = "none" }
    is replaced by that segment's steps, with {name} placeholders in their strings filled from the use step's other keys.
    So one sub-path (e.g. the Post up form) is written once and reached from every entry, without copied steps."""
    segs=dict(gsegs or {}); segs.update({g.get('id'):g for g in f.get('segments',[])})
    base={'auth':(US or {}).get(f.get('user'),{}).get('auth','out')}  # {auth} defaults to the flow's user type [M1044]
    f['_raw']={'main':list(f.get('steps',[]))}; f['_raw'].update({o.get('id'):list(o.get('steps',[])) for o in f.get('outcomes',[])})
    def ex(steps,d=0):
        out=[]
        for st in steps:
            if 'use' in st and st['use'] in segs and d<5:  # segments may use segments [M1043]
                vars_=dict(base); vars_.update({k:v for k,v in st.items() if k!='use'})
                out+=[dict(x,_seg=x.get('_seg',st['use']),**({'device':st['device']} if 'device' in st else {})) for x in ex([{k:_fill(v,vars_) for k,v in s2.items()} for s2 in segs[st['use']].get('steps',[])],d+1)]
            else: out.append(st)
        return out
    f['steps']=ex(f.get('steps',[]))
    for o in f.get('outcomes',[]):
        if 'steps' in o: o['steps']=ex(o['steps'])
def reach(sc,seeds,phase,limit=4000):
    """Every site-state key reachable from the seed states by real links (top screen + tab bar/rail chrome) [M1043]."""
    seen={}; q=[]
    for k in seeds:
        st=dict(parse_key(k),device='phone',phase=phase,cont=None)
        if st['root']=='home': st['tab']=st['tab'] if not has_rule(phase,'no-building-mode') or st['tab']=='live' else 'live'
        q.append(st)
    while q and len(seen)<limit:
        cur=q.pop(); k=key(cur)
        if k in seen: continue
        seen[k]=cur
        for own,l in available(sc,cur):
            try: n=resolve(sc,cur,l,own)
            except Exception: n=None
            if n and n!='back' and key(n) not in seen: q.append(n)
    return set(seen)
def goal_target(g):
    """State patterns that show a goal is reachable: the last milestone of the goal that has screen states [M1043]."""
    for m in reversed(g['ms']):
        if m.get('states') and not m.get('_shared'): return m['states']
    return []
def goal_entries(fl,fid):
    """Entry -> path ids of a flow: 'main' (the flow's own start) and each start branch (at = 0); a from-branch belongs to the
    entry its chain starts at [M1043]."""
    ent={'main':[fid]}
    for k,g in fl.items():
        if g.get('parent')!=fid: continue
        o=g
        while o.get('outcome_from'): o=fl[f"{fid}--{o['outcome_from']}"]
        ent.setdefault(o['outcome'] and (o['id'].split('--',1)[1] if o.get('outcome_at')==0 else 'main'),[]).append(k)
    return ent
def goal_reachable(sc,fl,ks,g,phase):
    """First goal-target state reachable by real links from the signed-out states those paths pass through, or None [M1043]."""
    import fnmatch
    seeds={k for kk in ks if M_phase_ok(fl[kk],phase) for k,_ in flow_states(sc,fl[kk]) if f"@{fl[kk]['start']['auth']}." in k}  # states in the entry's own sign-in state (newcomer: before sign-up) [M1044]
    R=sorted(reach(sc,seeds,phase)); hit=None
    for m in g['ms']:  # every milestone with its own screens must be reachable (not just the last one) [M1043]
        if m.get('_shared') or not (m.get('states') or m.get('shows')): continue
        hit=next((r for r in R if any(fnmatch.fnmatchcase(r,p) for p in m.get('states',[])) or shows(r,m.get('shows'),phase)),None)
        if not hit: return None
    return hit
def entry_phase(fl,ks,goal,flow):
    """Phase id to check a goal for an entry: the goal's since (or the flow's walk phase), no earlier than the entry's own since [M1044] [M1047-draft]."""
    gp=pid(goal.get('since'), flow_phase(flow))
    ev=min((pindex(flow_phase(fl[k])) for k in ks), default=pindex(flow_phase(flow)))
    return PIDS[max(pindex(gp), ev)]
def M_phase_ok(f,phase):
    """True if this flow/outcome path is available in the check phase (since/until, or untagged = all)."""
    return in_phase(f, phase)
def expand_outcomes(f):
    """Flow outcomes [M1040]. A flow may end in more than one way: [[outcomes]] each have id, label, at (steps 1..at are shared
    with the path it branches from), when (what triggers it, source-tagged), optional phase, situation and aliases, and
    [[outcomes.steps]] that follow. Each outcome becomes a walkable flow '<flow>--<outcome>' (parent, outcome set).
    Start branches [M1041]: at = 0 with its own start = {...} and an arrive first step (a different entry state).
    Trees [M1041]: from = "<earlier outcome id>" branches off that outcome's path instead of the main path."""
    out={}; paths={None:(f['steps'],f.get('start'))}
    for o in f.get('outcomes',[]):
        if not isinstance(o.get('id'),str) or not isinstance(o.get('at'),int) or not o.get('steps'): continue  # validate.py reports it
        if o.get('from') not in paths: continue  # validate.py reports it
        bsteps,bstart=paths[o.get('from')]
        g={k:v for k,v in f.items() if k not in ('outcomes','aliases','outcome','entry')}
        g.update(id=f"{f['id']}--{o['id']}",name=f"{f['name']} → {o.get('label','')}",steps=bsteps[:o['at']]+o['steps'],parent=f['id'],
                 outcome=o.get('label',''),outcome_when=o.get('when',''),outcome_at=o['at'],outcome_from=o.get('from'),aliases=o.get('aliases',[]),edge_cases=[],decide=[],
                 success=o.get('success',[]),start=o['start'] if o['at']==0 and 'start' in o else bstart)
        g['result']=o.get('result')  # typed outcome [M1042]
        if 'since' in o: g['since']=o['since']
        if 'until' in o: g['until']=o['until']
        if 'situation' in o: g['situation']=o['situation']
        paths[o['id']]=(g['steps'],g['start'])
        out[g['id']]=g
    return out
def parse_when(w):
    """'auth=out,live=none; auth=in' -> list of dicts (alternatives). '' -> [{}] (always).
    Keys use = only. Phase bounds belong on since=/until=, not in when. [M1047-draft]"""
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
    """when= conditions (auth/live/tab). Phase availability is in_phase(), not when. [M1047-draft]"""
    return any(all(_ok(st.get(k),v) for k,v in alt.items()) for alt in parse_when(w))
# A site state: root screen + open child (slot, screen) chain + conditions. Kept flat for the current depth (page + one sheet)
# but resolve() walks children generically. dict(root=, kids=[(slot,screen),...], auth=, live=, tab=)
def key(st): return st['root']+''.join('+'+c for _,c in st['kids'])+f"@{st['auth']}.{st['live']}"+(f".{st['tab']}" if st['root']=='home' else '')
def top(st): return st['kids'][-1][1] if st['kids'] else st['root']
def dmode(l,ph=None): return 'live' if l=='live' or has_rule(ph, 'no-building-mode') else 'building'  # named rule [M1047-draft]
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
    ph=vp(st.get('phase'))
    cond=dict(auth=st['auth'],live=st['live'],tab=st.get('tab'),phase=ph)
    if not in_phase(link, ph): return None
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
    ph=vp(st.get('phase')); t=top(st)
    out=[(t,l) for l in sc[t].get('links',[]) if in_phase(l,ph)]+[(c,l) for c in chrome(sc,st) for l in sc[c].get('links',[]) if in_phase(l,ph)]
    return out
def find_link(sc,st,ref):
    """'screen:id' -> (owner, link alternatives with that id) if that screen is on top or in chrome now."""
    own,_,lid=ref.partition(':')
    if own!=top(st) and own not in chrome(sc,st): return own,None
    return own,[l for l in sc.get(own,{}).get('links',[]) if l['id']==lid]
def rendered_id(s,auth,live,tab,phase=None):
    """HTML element id that renders screen s in these conditions: first matching 'variants' entry, else the screen id.
    Variant keys may name the phase, e.g. "phase=1" or "phase=1,auth=out" [M1035]."""
    c=dict(auth=auth,live=live,tab=tab,phase=vp(phase))  # variants may still mention phase only if migrated; phase is the view id
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
USERS=set(load_users()) or {'newcomer','registered'}  # from model/users.toml [M1044]
import tomllib as _tl, os as _os
REPL={c['id']:(c['replaces'],c['with']) for c in _tl.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','model','events.toml'),'rb'))['conditions'] if 'replaces' in c}
def cond_link(cur,l,cond):
    """A data condition swaps the target screen [M1033]: the link's own 'to', or the page a sheet continues to (signin's
    continue=true goes to the page remembered by 'then') [M1040]."""
    _c=REPL.get(cond)
    if not _c: return cur,l
    if l.get('to')==_c[0]: return cur,dict(l,to=_c[1])
    if l.get('continue') and cur.get('cont')==_c[0]: return dict(cur,cont=_c[1]),l
    return cur,l
def flow_phase(f): return walk_phase(f)  # since, or latest if untagged [M1047-draft]
def flow_states(sc,f):
    """Replay a flow; return the list of (state-key, screens on it) per step (assumes it validates)."""
    s0=f['start']; cur=dict(device=s0.get('device','phone'),root=s0['screen'],kids=[('sheet',s0['sheet'])] if s0.get('sheet') else [],auth=s0['auth'],live=s0['live'],tab=s0.get('tab') if s0['screen']=='home' else None,phase=flow_phase(f))
    if cur['root']=='home' and not cur['tab']: cur['tab']=dmode(cur['live'],cur['phase'])
    out=[]; hist=[cur]
    for i,st in enumerate(f['steps']):
        if i and 'link' in st:
            own,ls=find_link(sc,dict(cur,device=st.get('device') or s0.get('device','phone')),st['link']); n=None
            for l in ls or []:
                _cur,l=cond_link(cur,l,st.get('condition'))
                n=resolve(sc,_cur,l,own)
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
    """since (or None = all phases) per flow and per screen. No derived-from-flows classification [M1047-draft]."""
    FP={k:f.get('since') for k,f in fl.items()}
    SP={k:s.get('since') for k,s in sc.items()}
    return FP,SP,{}
def load_situations(root=ROOT):
    p=f'{root}/situations.toml'
    d=tomllib.load(open(p,'rb')) if os.path.exists(p) else {'situations':[]}
    load_situations.groups={g['id']:g for g in sorted(d.get('groups',[]),key=lambda g:g.get('order',99))}
    return {x['id']:x for x in d['situations']},p
# Goals [M1042]: ordered milestone tracks (model/goals.toml). A step reaches a milestone when its site state matches one of
# the milestone's state patterns, or the step says advances = "<milestone>". Progress on a goal = how many of its milestones
# were reached in order so far.
import fnmatch as _fn
def load_goals(root=ROOT,user=None):
    """Goals with g['ms'] = the goal's milestones that user type can reach (model/users.toml milestones) [M1044]."""
    gs,sh,p=_load_goals(root)
    if user is None: return gs,sh,p
    allow=set(load_users(root).get(user,{}).get('milestones',[]))
    return {k:dict(g,ms=[m for m in g['ms'] if m.get('id') in allow]) for k,g in gs.items()},sh,p
def _load_goals(root=ROOT):
    p=f'{root}/goals.toml'
    if not os.path.exists(p): return {},{},p
    d=tomllib.load(open(p,'rb')); sh={m['id']:m for m in d.get('shared',[])}
    gs={}
    for g in d.get('goals',[]):
        g=dict(g); g['ms']=[dict(sh.get(m['id'],{}),_shared=True,**m) if m.get('id') in sh and len(m)==1 else m for m in g.get('milestones',[])]; gs[g['id']]=g
    return gs,sh,p
def shows(key,refs,phase=None):
    """True if the site state shows one of these links ('screen:id') on its top screen or chrome (tab bar) [M1044].
    Evaluated in `phase` (default: latest). [M1047-draft]"""
    if not _SC or not refs: return False
    try: st=dict(parse_key(key),device='phone',phase=vp(phase),cont=None)
    except Exception: return False
    return any(f'{o}:{l["id"]}' in refs for o,l in available(_SC,st))
def step_hits(gs,key,adv=None):
    """Milestone ids this step reaches: by state pattern, by a link the state shows (shows = [...]) [M1044], or advances."""
    out=set()
    for g in gs.values():
        for m in g['ms']:
            if any(_fn.fnmatchcase(key,pt) for pt in m.get('states',[])) or shows(key,m.get('shows')) or (adv and m.get('id')==adv): out.add(m['id'])
    return out
def progress(gs,keys,advs,held=()):
    """keys/advs: per step. Returns per step {goal: milestones reached in order} and the skipped-order notes. held: goals the
    way in already has (came back while hosting or joined) start complete [M1044]."""
    p={g:(len(gs[g]['ms']) if g in held else 0) for g in gs}; out=[]; skips=[]
    for i,(k,a) in enumerate(zip(keys,advs)):
        h=step_hits(gs,k,a)
        for gid,g in gs.items():
            ids=[m['id'] for m in g['ms']]
            while p[gid]<len(ids) and ids[p[gid]] in h: p[gid]+=1
            for j,mid in enumerate(ids):
                if mid in h and j>p[gid] and mid!='signed-up': skips.append((i,gid,mid,ids[p[gid]]))
        out.append(dict(p))
    return out,skips


def ph_attr(item):
    """data-ph value: space-separated ids the item is available in, or 'all' if untagged."""
    if item.get('since') is None and item.get('until') is None:
        return 'all'
    return ' '.join(p for p in PIDS if in_phase(item, p))

def drop_classes(ph):
    """HTML class names not rendered in this view phase."""
    ph=pid(ph, LATEST); i=pindex(ph); d=[]
    for x in PIDS:
        if pindex(x)>i: d.append(f'since-{x}')
        if pindex(x)<i: d.append(f'until-{x}')
        if x!=ph: d.append(f'only-{x}')
    return tuple(d)

def visibility_css():
    """CSS so html[data-vph=<id>] hides since-/until-/only- classes not in that phase [M1047-draft]."""
    lines=['/* generated from phases.toml [M1047-draft] */']
    for ph in PIDS:
        for cls in drop_classes(ph):
            lines.append(f'html[data-vph="{ph}"] .{cls}{{display:none!important}}')
    return '\n'.join(lines)

def tabbar_cols_css(sc):
    """Tab bar column count per phase, from how many tabbar links are available."""
    tb=sc.get('tabbar') or {}
    lines=[]
    for ph in PIDS:
        n=sum(1 for l in tb.get('links') or [] if in_phase(l, ph))
        if n:
            lines.append(f'html[data-vph="{ph}"] .tab.t5{{grid-template-columns:repeat({n},1fr)}}')
    return '\n'.join(lines)

def js_phase_config():
    return dict(ids=list(PIDS), latest=LATEST, labels={x['id']:x.get('label') or x['id'] for x in PHASES},
                badges={x['id']:x.get('badge') for x in PHASES}, aliases=dict(ALIAS))
