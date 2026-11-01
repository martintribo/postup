# Builds FLOWS from model/flows/*.toml (the model is the single source [M1031-draft]) and adds the views renderers use:
#   f['sx'] = step dicts (site, user, act, do[, device], how);  f['steps'] = (page, auth, live, extra, do) tuples
# Step 'how' = the link/event label that reaches it (derived by replaying the model, same rules as gen/validate.py).
import re as _re, sys as _sys
_sys.path.insert(0,'gen'); import model as M
_SC,_FL,_EV,_GL=M.load()
def parse_site(sid):
    m=_re.fullmatch(r'([\w-]+)(?:\+([\w-]+))?@(in|out)\.(live|none)(?:\.(live|building))?',sid)
    if not m: raise SystemExit(f'bad site-state id {sid}')
    return dict(page=m[1],ov=m[2],auth=m[3],live=m[4],mode=m[5])
_EVS={e['id']:e for e in _EV['events']+_EV['conditions']}
FLOWS=[]
for _id in sorted(_FL,key=lambda k:({0:0,1:0}.get(_FL[k].get('phase'),1),_FL[k].get('order',99),k)):
    _f=_FL[_id]; s0=_f['start']
    f=dict(id=_id,name=_f['name'],pri={0:'Phase 0',1:'Phase 1',2:'Phase 2 (MVP)'}.get(_f.get('phase'),'Unphased'),phase=_f.get('phase'),user=_f['user'],situation=_f.get('situation'),aliases=_f.get('aliases',[]),status=_f['status'],persona=_f['persona'],goal=_f['goal'],
           start=dict(auth=s0['auth'],live=s0['live'],device=s0['device'],url=s0['url']),branches=_f.get('edge_cases',[]),success=_f.get('success',[]),decide=_f.get('decide',[]),role=_f['role'],parent=_f.get('parent'),outcome=_f.get('outcome'),outcome_when=_f.get('outcome_when',''),outcome_at=_f.get('outcome_at'))
    sx=[]
    for i,st in enumerate(_f['steps']):
        if 'link' in st:
            own,_,lid=st['link'].partition(':'); l=next(x for x in _SC[own]['links'] if x['id']==lid)
            how=('back' if l['action']=='back' else 'tap: '+(l['label'] or lid)+(f" ({_EVS[st['condition']]['label']})" if st.get('condition') in _EVS else ''))
        elif 'event' in st: how=('event: ' if 'action' in _EVS[st['event']] and _EVS[st['event']] in _EV['events'] else 'cond: ')+_EVS[st['event']]['label']
        else: how='entry'
        d=dict(site=st['expect'],user=st['thought'],act=st.get('act') or st.get('arrive',''),do=st['shows'],how=how,ref=st.get('link') or st.get('event') or '')
        if st.get('device'): d['device']=st['device']
        sx.append(d)
    f['sx']=sx; _t=[]
    for _d in sx:
        _p=parse_site(_d['site']); _x={}
        if _p['mode']: _x['mode']=_p['mode']
        if _p['ov']: _x['ov']=_p['ov']
        if _d.get('device'): _x['device']=_d['device']
        _t.append((_p['page'],_p['auth'],_p['live'],_x,_d['do']))
    f['steps']=_t; FLOWS.append(f)
# outcomes [M1040]: every flow lists its ways to end: the main path first, then each [[outcomes]] (a walkable flow '<id>--<outcome>')
_FBY={f['id']:f for f in FLOWS}
for f in FLOWS:
    top=f['parent'] or f['id']; p=_FBY[top]
    f['outs']=[dict(id=top,label=_FL[top].get('outcome') or 'Done',when='',at=None,phase=p['phase'],entry=_FL[top].get('entry',''))]+[dict(id=g['id'],label=g['outcome'],when=g['outcome_when'],at=g['outcome_at'],phase=g['phase'],entry=g['outcome_when'] if g['outcome_at']==0 else '') for g in sorted((g for g in FLOWS if g['parent']==top),key=lambda g:[o['id'] for o in _FL[top]['outcomes']].index(g['id'].split('--',1)[1]))]  # model order [M1040]
FLOWS_TOP=[f for f in FLOWS if not f['parent']]
# forks [M1041]: on each page, after step a (1-based), which ways on share this page's first a steps. {a: [out ids]}
def _key(g,n): return [(d['site'],d['ref']) for d in g['sx'][:n]]
for f in FLOWS:
    f['forks']={}
    for o in f['outs']:
        g=_FBY[o['id']]
        for a in range(1,min(len(f['sx']),len(g['sx']))):
            if _key(g,a)==_key(f,a) and (g['sx'][a]['site'],g['sx'][a]['ref'])!=(f['sx'][a]['site'],f['sx'][a]['ref']):
                f['forks'].setdefault(a,[f['id']]).append(o['id']); break
# goals [M1042]: per step milestone progress {goal: n reached in order}, and the path's typed result
GOALS,_GSH,_=M.load_goals()
USERS_D=M.load_users()  # user types: label, auth, main goal-tracked flow, milestones [M1044]
GOALS_U={u:M.load_goals(user=u)[0] for u in USERS_D}
for f in FLOWS:
    _st=_FL[f['id']]['steps']
    f['prog'],_=M.progress(GOALS_U.get(f['user'],GOALS),[d['site'] for d in f['sx']],[x.get('advances') for x in _st],_FL[f['id']]['start'].get('holds') or ())
    f['result']=_FL[f['id']].get('result')
