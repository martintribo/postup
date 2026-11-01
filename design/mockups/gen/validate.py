# Validate the mockup model (model/*.toml) [M1030]; run by build.py before it writes anything [M1031-draft]. Exit 1 with file:line messages on any error. Also writes model/INDEX.md.
# Usage (from mockups/): python3 gen/validate.py [--no-index]
import os, sys, re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import model as M
sc,fl,ev,gl=M.load(); ERR=[]; WARN=[]
rel=lambda p:os.path.relpath(p,os.path.join(M.ROOT,'..'))
def err(p,needle,msg,nth=0,kind='error'): (ERR if kind=='error' else WARN).append(f'{rel(p)}:{M.lineof(p,needle,nth)}: {msg}')
def chk_when(p,w,ctx):
    for alt in M.parse_when(w):
        for k,v in alt.items():
            if k=='phase':
                if not re.fullmatch(r'(>=|<=)?\d+',v): err(p,ctx,f'invalid condition phase{"" if v[:1] in "<>" else "="}{v}')
            elif k not in M.DIMS or v not in M.DIMS[k]: err(p,ctx,f'invalid condition {k}={v}')
ALLC=[dict(auth=a,live=l,tab=t,phase=ph) for a in M.DIMS['auth'] for l in M.DIMS['live'] for t in M.DIMS['tab'] for ph in M.PHASES]
REPL=M.REPL
EVIDS={e['id'] for e in ev['events']}|{c['id'] for c in ev['conditions']}
# --- screens ---
for sid,s in sc.items():
    p=s['_file']
    if s.get('kind') not in M.SCREEN_KINDS: err(p,'kind =',f'invalid screen kind {s.get("kind")!r}')
    for sl in s.get('slots',[]):
        if sl.get('kind') not in M.SLOT_KINDS: err(p,'slots',f'invalid slot kind {sl.get("kind")!r}')
        if sl.get('device') and sl['device'] not in M.DEVICES: err(p,'slots',f'invalid slot device {sl["device"]!r}')
        for c in sl.get('accepts',[]):
            if c in sc and sl['kind'] in ('tab','panel') and sc[c]['kind']!=sl['kind']: err(p,f'"{c}"',f'{sl["kind"]} slot {sl["name"]} accepts {c!r} of kind {sc[c]["kind"]}')
        for c in sl.get('accepts',[]):
            if c not in sc: err(p,f'"{c}"',f'slot {sl["name"]} accepts unknown screen {c!r}')
            elif sc[c]['kind']=='page': err(p,f'"{c}"',f'slot {sl["name"]} accepts a page ({c}); only child screens go in slots')
    for l in s.get('links',[]):
        ctx=f'id = "{l["id"]}"'
        if l.get('action') not in M.ACTIONS: err(p,ctx,f'invalid action {l.get("action")!r}')
        t=l.get('to')
        if l['action'] in ('replace','open','swap') and t not in sc: err(p,ctx,f'link {l["id"]}: unknown screen {t!r}')
        if l['action']=='replace' and t in sc and sc[t]['kind']!='page': err(p,ctx,f'link {l["id"]}: replace to a child screen {t!r} (use open)')
        if l.get('then') and (l['action']!='open' or sc.get(l['then'],{}).get('kind')!='page'): err(p,ctx,f'link {l["id"]}: then= needs an open link and a page')
        if l.get('continue') and l['action']!='close': err(p,ctx,f'link {l["id"]}: continue= needs a close link')
        if l['action']=='open' and t in sc and not M.slot_accepts(sc,sid,l.get('slot','sheet'),t): err(p,ctx,f'link {l["id"]}: no slot {l.get("slot","sheet")!r} on {sid} accepts {t!r}')
        chk_when(p,l.get('when',''),ctx)
    for n in s.get('notes',[]):
        for i,b in enumerate(n['lines']):
            if not re.search(M.TAG,b): err(p,b[:40],f'note without source tag: {b[:60]}')
    if not s.get('notes'): err(p,'id =','screen has no notes')
    if s['kind']=='sheet' and s.get('host') not in sc: err(p,'id =','sheet needs host = <page> (where its notes URL shows it)')
    for w in (s.get('variants') or {}): chk_when(p,w,'variants')
    ids={}
    for l in s.get('links',[]): ids.setdefault(l['id'],[]).append(l)
    for i,ls in ids.items():
        for a in range(len(ls)):
            for b_ in range(a+1,len(ls)):
                if any(M.matches(ls[a].get('when',''),c) and M.matches(ls[b_].get('when',''),c) for c in ALLC): err(p,f'id = "{i}"',f'link id {i!r} is used twice with overlapping conditions')
# slot accepting at any depth: every child chain reachable by open/swap must be accepted by its host slot
def walk(host,child,slot,seen):
    if (host,child) in seen: return
    seen.add((host,child))
    for l in sc[child].get('links',[]):
        if l['action']=='swap' and l.get('to') in sc and l['to']!=child and not M.slot_accepts(sc,host,slot,l['to']):
            err(sc[child]['_file'],f'id = "{l["id"]}"',f'link {l["id"]}: swaps {l["to"]!r} into {host}.{slot}, which does not accept it (opened from {host})')
        if l['action']=='open' and l.get('to') in sc:
            if not M.slot_accepts(sc,child,l.get('slot','sheet'),l['to']): err(sc[child]['_file'],f'id = "{l["id"]}"',f'link {l["id"]}: {child} has no slot accepting {l["to"]!r}')
            else: walk(child,l['to'],l.get('slot','sheet'),seen)
_seen=set()
for sid,s in sc.items():
    for sl in s.get('slots',[]):
        for c in sl.get('accepts',[]):
            if c in sc: walk(sid,c,sl['name'],_seen)
# events / conditions
for e in ev['events']+ev['conditions']:
    p=ev['_file']; ctx=f'id = "{e["id"]}"'
    for o in e.get('on',[]):
        if o!='*' and o not in sc: err(p,ctx,f'event {e["id"]}: unknown screen {o!r}')
    for k in ('to','replaces','with'):
        if e.get(k) and e[k] not in sc: err(p,ctx,f'event {e["id"]}: unknown screen {e[k]!r}')
    if e.get('action') and e['action'] not in M.ACTIONS: err(p,ctx,f'invalid action {e["action"]!r}')
    chk_when(p,e.get('when',''),ctx)
# global notes tags
for sec in ('notes','index_notes'):
    for n in gl.get(sec,[]):
        for b in n['lines']:
            if not re.search(M.TAG,b): err(gl['_file'],b[:40],f'note without source tag: {b[:60]}')
# --- flows: re-derive each step's state ---
def ev_apply(e,st):
    on=e.get('on',['*'])
    if st['kids'] or not ('*' in on or st['root'] in on): return None
    return M.resolve(sc,st,e,owner=st['root'])
def parse_site(s):
    m=re.fullmatch(r'([\w-]+)(?:\+([\w-]+))?@(in|out)\.(live|none)(?:\.(live|building))?',s)
    if not m: return None
    p,o,a,l,t=m.groups(); return dict(root=p,kids=[('sheet',o)] if o else [],auth=a,live=l,tab=(t or M.dmode(l)) if p=='home' else None)
GAPS=[]; ENTERS=set()
for fid,f in fl.items():
    p=f['_file']
    if f.get('role') not in M.ROLES: err(p,'role =',f'invalid role {f.get("role")!r}')
    if f.get('status') not in M.STATUSES: err(p,'status =',f'invalid status {f.get("status")!r}')
    for k in ('goal',):
        if not re.search(M.TAG,f.get(k,'')): err(p,k+' =',f'{k} without source tag')
    s0=f['start']
    if s0['screen'] not in sc: err(p,'start =',f'unknown start screen {s0["screen"]!r}'); continue
    FPH=M.flow_phase(f)  # walk this flow's phase version of every screen [M1035]
    cur=dict(device=s0.get('device','phone'),root=s0['screen'],kids=[('sheet',s0['sheet'])] if s0.get('sheet') else [],auth=s0['auth'],live=s0['live'],tab=s0.get('tab') if s0['screen']=='home' else None,phase=FPH)
    if s0['screen']=='home' and not cur['tab']: cur['tab']=M.dmode(cur['live'],FPH)
    if s0['screen']=='home' and cur['tab']!=M.dmode('live',FPH) and FPH<2 and cur['tab']=='building': err(p,'start =',f'phase-{FPH} flow starts in Building mode, which is phase 2')
    ENTERS.add(s0['screen']); hist=[cur]
    for i,st in enumerate(f['steps']):
        ctx='[[steps]]'
        if not re.search(M.TAG,st.get('shows','')): err(p,ctx,f'step {i+1}: "shows" without source tag',nth=i)
        if st.get('device') and st['device'] not in M.DEVICES: err(p,ctx,f'step {i+1}: invalid device',nth=i)
        cur=dict(cur,device=st.get('device') or s0.get('device','phone'))
        if i and ('link' in st or 'event' in st) and not st.get('act'): err(p,ctx,f'step {i+1}: needs act = "<what the user does>"',nth=i)
        if i==0: pass
        elif 'gap' in st:
            GAPS.append(f'{rel(p)}:{M.lineof(p,ctx,i)}: step {i+1}: no single link or event from {M.key(cur)} to {st.get("expect")} ({st["gap"]})')
            n=parse_site(st.get('expect',''))
            if n: n['phase']=FPH 
            if n: cur=n; hist.append(n)
            continue
        elif 'event' in st:
            e=next((x for x in ev['events']+ev['conditions'] if x['id']==st['event']),None)
            if not e: err(p,ctx,f'step {i+1}: unknown event {st["event"]!r}',nth=i); continue
            n=ev_apply(e,cur)
            if not n: err(p,ctx,f'step {i+1}: event {e["id"]} cannot happen in {M.key(cur)}',nth=i); continue
            cur=n; hist.append(n)
        elif 'link' in st:
            own,ls=M.find_link(sc,cur,st['link'])
            if own not in sc: err(p,ctx,f'step {i+1}: unknown screen {own!r} in link',nth=i); continue
            if ls is None: err(p,ctx,f'step {i+1}: link {st["link"]} is on {own}, which is not on top or in chrome in {M.key(cur)}',nth=i); continue
            if not ls: err(p,ctx,f'step {i+1}: no link {st["link"]}',nth=i); continue
            if st.get('condition') and st['condition'] not in EVIDS: err(p,ctx,f'step {i+1}: unknown condition {st["condition"]!r}',nth=i)
            n=None
            if st.get('condition') and st['condition'] in REPL and not any(M.cond_link(cur,l,st['condition'])[1] is not l or M.cond_link(cur,l,st['condition'])[0] is not cur for l in ls): err(p,ctx,f'step {i+1}: condition {st["condition"]} swaps {REPL[st["condition"]][0]}, which link {st["link"]} does not lead to here',nth=i)
            for l in ls:
                _cur,l=M.cond_link(cur,l,st.get('condition'))  # [M1033] [M1040]
                n=M.resolve(sc,_cur,l,own)
                if n: break
            if n is None: err(p,ctx,f'step {i+1}: link {st["link"]} not available in {M.key(cur)}',nth=i); continue
            if n=='back':
                if len(hist)<2: err(p,ctx,f'step {i+1}: back with no history',nth=i); continue
                hist.pop(); cur=dict(hist[-1])
            else: cur=n; hist.append(n)
        else: err(p,ctx,f'step {i+1}: needs link, event or gap',nth=i); continue
        if st.get('expect') and M.key(cur)!=st['expect']: err(p,ctx,f'step {i+1}: derived {M.key(cur)} but expected {st["expect"]}',nth=i)
def _pint(v): return isinstance(v,int) and not isinstance(v,bool) and v in M.PHASES  # a known phase: 0, 1 or 2 [M1037]
# outcomes [M1040]: each outcome is a labelled, source-tagged alternative ending that branches off the main path at a real step
for fid,f in fl.items():
    if f.get('parent'): continue
    p=f['_file']; os_=f.get('outcomes',[])
    if not os_: continue
    if not re.search(M.TAG,f.get('outcome','')): err(p,'outcome =',f'flow {fid} has outcomes, so it needs outcome = "<label of the main path> [tag]"')
    if any(o.get('at')==0 for o in os_) and not re.search(M.TAG,f.get('entry','')): err(p,'outcome =',f'flow {fid} has start branches, so it needs entry = "<when the main path starts> [tag]"')
    seen=set()
    for k,o in enumerate(os_):
        ctx='[[outcomes]]'
        if not isinstance(o.get('id'),str) or not re.fullmatch(r'[a-z0-9-]+',o['id']): err(p,ctx,f'outcome {k+1}: id must be lowercase-dashed',nth=k); continue
        if o['id'] in seen: err(p,ctx,f'outcome {o["id"]}: duplicate id',nth=k)
        seen.add(o['id'])
        if not o.get('label') or re.search(M.TAG,o['label']): err(p,ctx,f'outcome {o["id"]}: needs a plain label (no tag)',nth=k)
        if not re.search(M.TAG,o.get('when','')): err(p,ctx,f'outcome {o["id"]}: when (what triggers it) needs a source tag',nth=k)
        at=o.get('at'); fr=o.get('from')
        if fr is not None and fr not in [x.get('id') for x in os_[:k]]: err(p,ctx,f'outcome {o["id"]}: from = {fr!r} must name an earlier outcome of this flow',nth=k); continue
        base=(fl.get(f"{fid}--{fr}") or {}).get('steps') if fr else f['steps']
        if base is None: err(p,ctx,f'outcome {o["id"]}: its from outcome {fr!r} is invalid',nth=k); continue
        if not isinstance(at,int) or isinstance(at,bool) or not 0<=at<len(base): err(p,ctx,f'outcome {o["id"]}: at must be 0 (a start branch) or a step number 1..{len(base)-1} of the path it branches from',nth=k); continue
        if at==0 and fr: err(p,ctx,f'outcome {o["id"]}: a start branch (at = 0) cannot also have from',nth=k)
        if not o.get('steps'): err(p,ctx,f'outcome {o["id"]}: needs [[outcomes.steps]]',nth=k); continue
        b=o['steps'][0]
        if at==0:  # start branch [M1041]: its own entry state, reached by arriving
            st_=o.get('start') or {}
            if not st_.get('screen') or st_.get('auth') not in M.DIMS['auth'] or st_.get('live') not in M.DIMS['live']: err(p,ctx,f'outcome {o["id"]}: a start branch needs start = {{ screen, auth, live, ... }}',nth=k)
            elif st_==f['start'] or any((y.get('start')==st_ and y.get('at')==0) for y in os_[:k]): err(p,ctx,f'outcome {o["id"]}: start branch has the same start state as another entry; it is not a different entry',nth=k)
            if 'arrive' not in b: err(p,ctx,f'outcome {o["id"]}: a start branch begins with an arrive step',nth=k)
        else:
            if 'start' in o: err(p,ctx,f'outcome {o["id"]}: only start branches (at = 0) have their own start',nth=k)
            m=base[at]
            if 'arrive' in b or not ('link' in b or 'event' in b): err(p,ctx,f'outcome {o["id"]}: its first step must be one link or event (one tap per step)',nth=k)
            elif all(b.get(x)==m.get(x) for x in ('link','event','condition','expect')): err(p,ctx,f'outcome {o["id"]}: its first step is the same as step {at+1} of the path it branches from, so it is not a different outcome',nth=k)
        if 'phase' in o and (not _pint(o['phase']) or (f.get('phase') is not None and o['phase']<f['phase'])): err(p,ctx,f'outcome {o["id"]}: phase must be a phase no lower than the flow\'s',nth=k)
        for a_ in o.get('aliases',[]):
            if a_ in fl: err(p,ctx,f'outcome {o["id"]}: alias {a_} is still a flow',nth=k)
# phases [M1031-draft]
for sid,s in sc.items():
    if 'phase' in s and not _pint(s['phase']): err(s['_file'],'phase =',f'phase must be one of the phases 0, 1, 2, got {s["phase"]!r}')
    for k,v in s.get('state_phases',{}).items():
        if not _pint(v): err(s['_file'],k,f'state phase must be one of the phases 0, 1, 2, got {v!r}')
for k,v in gl.get('state_phases',{}).items():
    if not _pint(v): err(gl['_file'],k,f'state phase must be one of the phases 0, 1, 2, got {v!r}')
for fid,f in fl.items():
    p=f['_file']
    if 'phase' in f and not _pint(f['phase']): err(p,'phase =',f'phase must be one of the phases 0, 1, 2, got {f["phase"]!r}')
    if f.get('user') not in M.USERS: err(p,'user =',f'user must be one of {sorted(M.USERS)}')
    elif (f['user']=='newcomer')!=(f['start']['auth']=='out'): err(p,'user =',f'user {f["user"]!r} does not match start auth {f["start"]["auth"]!r}')
if not ERR:
    _SO=dict(gl.get('state_phases',{}))
    for s in sc.values(): _SO.update(s.get('state_phases',{}))
    for fid,f in fl.items():
        ph=f.get('phase')
        if ph is None: continue
        for i,(k,scs) in enumerate(M.flow_states(sc,f)):
            for s in scs:
                if sc[s].get('phase') is not None and sc[s]['phase']>ph: err(f['_file'],'[[steps]]',f'phase-{ph} flow {fid} step {i+1} uses {s}, tagged phase {sc[s]["phase"]}',nth=i)
            if _SO.get(k) is not None and _SO[k]>ph: err(f['_file'],'[[steps]]',f'phase-{ph} flow {fid} step {i+1} passes state {k}, tagged phase {_SO[k]}',nth=i)
# situations [M1031-draft]
SIT,_sp=M.load_situations()
SGR=M.load_situations.groups
for gi,g in SGR.items():
    if not g.get('title') or not isinstance(g.get('order'),int): err(_sp,f'id = "{gi}"',f'group {gi}: needs title and integer order')
for i,x in SIT.items():
    if x.get('group') not in SGR: err(_sp,f'id = "{i}"',f'situation {i}: group {x.get("group")!r} is not in groups')
    if x.get('user') not in M.USERS: err(_sp,f'id = "{i}"',f'situation {i}: user must be one of {sorted(M.USERS)}')
    if not re.search(M.TAG,x.get('setting','')): err(_sp,f'id = "{i}"',f'situation {i}: setting without source tag')
    if 'phase' in x and not _pint(x['phase']): err(_sp,f'id = "{i}"',f'situation {i}: phase must be one of the phases 0, 1, 2')
for fid,f in fl.items():
    si=f.get('situation')
    if si not in SIT: err(f['_file'],'situation' if si else 'user =',f'flow {fid}: situation {si!r} is not in situations.toml')
    elif SIT[si]['user']!=f.get('user'): err(f['_file'],'situation',f'flow {fid}: situation {si} is for {SIT[si]["user"]}, flow user is {f.get("user")}')
# goals [M1042]: ordered milestone tracks; typed outcomes (goal reached / drop-off); first-visit-style flows must reach them
GS,GSH,_gp=M.load_goals()
MIDS={}
if GS:
    for k,m in GSH.items():
        if not re.search(M.TAG,m.get('note','')) or not m.get('label'): err(_gp,f'id = "{k}"',f'shared milestone {k}: needs label and a source-tagged note')
    for gid,g in GS.items():
        ctx=f'id = "{gid}"'
        if not re.fullmatch(r'#[0-9a-fA-F]{6}',g.get('color','')): err(_gp,ctx,f'goal {gid}: color must be #rrggbb')
        if not g.get('label'): err(_gp,ctx,f'goal {gid}: needs a label')
        if 'likely' in g and not re.search(M.TAG,g['likely']): err(_gp,ctx,f'goal {gid}: likely note needs a source tag')
        if 'phase' in g and not _pint(g['phase']): err(_gp,ctx,f'goal {gid}: phase must be 0, 1 or 2')
        ids=[m.get('id') for m in g['ms']]
        if len(ids)<2: err(_gp,ctx,f'goal {gid}: needs at least two milestones')
        if len(set(ids))!=len(ids): err(_gp,ctx,f'goal {gid}: milestone ids must be unique')
        for sid_ in GSH:
            if ids.count(sid_)!=1: err(_gp,ctx,f'goal {gid}: must list the shared milestone {sid_} exactly once')
        if ids and ids[-1] in GSH: err(_gp,ctx,f'goal {gid}: its final milestone must be its own, not shared')
        for m in g['ms']:
            if m.get('id') in GSH: continue
            if m.get('id') in MIDS: err(_gp,f'id = "{m.get("id")}"',f'milestone {m.get("id")}: used by goals {MIDS[m["id"]]} and {gid}; only shared milestones may repeat')
            MIDS[m.get('id')]=gid
            if not m.get('label') or not re.search(M.TAG,m.get('note','')): err(_gp,f'id = "{m.get("id")}"',f'milestone {m.get("id")}: needs label and a source-tagged note')
    for gid in list(GS):
        if gid in MIDS or gid in GSH: err(_gp,f'id = "{gid}"',f'goal id {gid} clashes with a milestone id')
    ALLM=set(MIDS)|set(GSH)
    HIT=set(); PROG={}
    if not ERR:
        for fid,f in fl.items():
            p=f['_file']; advs=[st.get('advances') for st in f['steps']]
            for i,a_ in enumerate(advs):
                if a_ and a_ not in ALLM: err(p,'advances',f'step {i+1}: advances {a_!r} is not a milestone in goals.toml',nth=0)
            keys=[k for k,_ in M.flow_states(sc,f)]
            pr,_=M.progress(GS,keys,advs); PROG[fid]=pr
            for k,a_ in zip(keys,advs): HIT|=M.step_hits(GS,k,a_)
        for mid in sorted(ALLM-HIT): err(_gp,f'id = "{mid}"',f'milestone {mid}: no step of any flow reaches it (match its states or add advances = "{mid}")')
        # typed outcomes
        for fid,f in fl.items():
            if f.get('parent'): continue
            fam=[fid]+[k for k,g in fl.items() if g.get('parent')==fid]
            res={k:fl[k].get('result') for k in fam}
            if not any(res.values()): 
                if f.get('goals'): err(f['_file'],'goals =',f'flow {fid} tracks goals, so every path needs result = "goal:<goal>" or "drop:<milestone>"')
                continue
            for k,r in res.items():
                ctx='result' if k==fid else f'id = "{k.split("--",1)[1]}"'
                if not r: err(f['_file'],ctx,f'{k}: some paths of {fid} are typed, so this one needs result = "goal:<goal>" or "drop:<milestone>"'); continue
                kind,_,x=r.partition(':'); last=PROG[k][-1] if PROG.get(k) else {}
                if kind=='goal':
                    if x not in GS: err(f['_file'],ctx,f'{k}: unknown goal {x!r}'); continue
                    if last.get(x,0)<len(GS[x]['ms']): err(f['_file'],ctx,f'{k}: says it reaches goal {x}, but it stops at milestone {last.get(x,0)}/{len(GS[x]["ms"])} ({GS[x]["ms"][last.get(x,0)]["id"]} not reached in order)')
                elif kind=='drop':
                    if x not in ALLM: err(f['_file'],ctx,f'{k}: drop-off must name a milestone, got {x!r}'); continue
                    lasts={g['ms'][last.get(gid,0)-1]['id'] for gid,g in GS.items() if last.get(gid,0)>0}
                    if x not in lasts: err(f['_file'],ctx,f'{k}: drops off at {x}, but the furthest milestones it reaches are {sorted(lasts) or "none"}')
                    if any(last.get(gid,0)>=len(g['ms']) for gid,g in GS.items()): err(f['_file'],ctx,f'{k}: typed as a drop-off but it reaches a goal')
                else: err(f['_file'],ctx,f'{k}: result must be goal:<goal> or drop:<milestone>')
            if f.get('goals'):
                fin={k:PROG[k][-1] for k in fam if PROG.get(k)}
                if not any(v.get(g_,0)>=[m['id'] for m in GS[g_]['ms']].index('signed-up')+1 for v in fin.values() for g_ in GS): err(f['_file'],'goals =',f'flow {fid}: no path reaches signed-up')
                for gid,g in GS.items():
                    if not any(v.get(gid,0)>=len(g['ms']) and (fl[k].get('phase') if fl[k].get('phase') is not None else M.MAXPH)<=M.MAXPH for k,v in fin.items()):
                        GAPS.append(f'{rel(f["_file"])}:1: flow {fid}: no path reaches goal {gid} ({g["label"]}) in phase {M.MAXPH} or lower [M1042]')
# orphans
IN={t for s in sc.values() for l in s.get('links',[]) for t in [l.get('to')] if t and t!=s['id']}
IN|={c for s in sc.values() for sl in s.get('slots',[]) for c in sl.get('accepts',[])}
IN|={e.get('to') for e in ev['events']+ev['conditions']}|{e.get('with') for e in ev['conditions']}|ENTERS
for sid,s in sc.items():
    if sid not in IN and not s.get('entry') and not s.get('alternative'): err(s['_file'],'id =',f'orphan screen {sid}: no link, slot, event or flow reaches it (mark entry = true if it is a landing)')
# INDEX.md
if '--no-index' not in sys.argv:
    _FP,_SP,_STP=M.phases(sc,fl,gl) if not ERR else ({},{},{})
    L=['# PostUp model index [M1030]','One line per screen and flow. Generated by gen/validate.py; edit the .toml files.','','## Screens']
    for sid,s in sorted(sc.items(),key=lambda x:(x[1]['kind']!='page',x[1].get('group',''),x[0])):
        sl=' · slots: '+', '.join(f'{x["name"]}({x["kind"]})→{len(x.get("accepts",[]))}' for x in s.get('slots',[])) if s.get('slots') else ''
        L.append(f'- `{sid}` ({s["kind"]}, {s.get("group","")}, {"phase "+str(_SP[sid]) if _SP.get(sid) else "unphased"}{"" if s.get("phase") else " derived" if _SP.get(sid) else ""}) {s["title"]} · {len(s.get("links",[]))} links{sl}{" · entry" if s.get("entry") else ""} → screens/{sid}.toml')
    L+=['','## Flows']
    for fid,f in fl.items(): L.append(f'- `{fid}` ({f["role"]}, {"phase "+str(f["phase"]) if f.get("phase") else "unphased"}, {f.get("user","?")}, {f["status"]}) {f["name"]} · {len(f["steps"])} steps · starts {f["start"]["screen"]} → flows/{fid}.toml')
    L+=['',f'## Phases [M1031-draft] [M1032]']+[f'- {nm}: {sum(1 for v in _FP.values() if v==n)} flows, {sum(1 for v in _SP.values() if v==n)} screens, {sum(1 for v in _STP.values() if v==n)} site states' for n,nm in ((1,'Phase 1 (pre-MVP)'),(2,'Phase 2 (MVP)'))]+['- Screens/states are derived from flows unless tagged; lowest phase wins. Untagged = unclassified, kept. The MVP is phases 1 and 2.']
    L+=['','## Events and conditions']+[f'- `{e["id"]}` {e["label"]}' for e in ev['events']+ev['conditions']]
    open(os.path.join(M.ROOT,'INDEX.md'),'w').write('\n'.join(L)+'\n')
print(f'model: {len(sc)} screens ({sum(1 for s in sc.values() if s["kind"]=="page")} pages), {sum(len(s.get("links",[])) for s in sc.values())} links, {len(fl)} flows, {sum(len(f["steps"]) for f in fl.values())} steps, {len(ev["events"])} events, {len(ev["conditions"])} conditions')
for g in GAPS: print('GAP',g)
for e in ERR: print(e)
print(f'{len(ERR)} errors, {len(GAPS)} design gaps')
sys.exit(1 if ERR or GAPS else 0)
