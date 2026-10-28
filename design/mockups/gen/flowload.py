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
for _id in sorted(_FL,key=lambda k:(0 if _FL[k].get('phase')==1 else 1,_FL[k].get('order',99),k)):
    _f=_FL[_id]; s0=_f['start']
    f=dict(id=_id,name=_f['name'],pri={1:'Phase 1',2:'Phase 2 (MVP)'}.get(_f.get('phase'),'Unphased'),phase=_f.get('phase'),user=_f['user'],situation=_f.get('situation'),aliases=_f.get('aliases',[]),status=_f['status'],persona=_f['persona'],goal=_f['goal'],
           start=dict(auth=s0['auth'],live=s0['live'],device=s0['device'],url=s0['url']),branches=_f.get('edge_cases',[]),success=_f.get('success',[]),decide=_f.get('decide',[]),role=_f['role'])
    sx=[]
    for i,st in enumerate(_f['steps']):
        if 'link' in st:
            own,_,lid=st['link'].partition(':'); l=next(x for x in _SC[own]['links'] if x['id']==lid)
            how=('back' if l['action']=='back' else 'tap: '+(l['label'] or lid)+(' (Google card fails)' if st.get('condition') else ''))
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
