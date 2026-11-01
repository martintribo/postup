# Walkthrough mode [M1045] (Martin, Nov 1 2026: "walkthrough mode ... a good one that a ux designer would find good").
# flows/walk.html: pick a user type (users.toml), a way in (ways.toml) and a phase; step through the real mockup screens one
# tap at a time. Everything comes from the model: the state machine is model/screens links resolved by gen/model.py (same
# rules as the validator and site graph), goals/milestones from goals.toml filtered per user type, drop-offs and outcome
# labels from each user type's main flow [[outcomes]], notes from the screens' [[notes]]. Nothing here names a user type,
# way, goal or screen. exec'd by flows.py after graphview.py (needs FLOWS, FBY, _FL, SC, M, USERS_D, GOALS_U, NOTES, OVCH, S).
import fnmatch as _wfn, model as MW
_WAYS=MW.load_ways(); _EVC={c['id']:c for c in MEV['conditions'] if 'replaces' in c}
def _wnk(st): return MW.key(st)+('>'+st['cont'] if st.get('cont') else '')
def _wtitle(st):
    t=SC[st['root']]['title']
    return t+(' + '+SC[st['kids'][-1][1]]['title'] if st['kids'] else '')
WALK={}; WALK_WARN=[]
for _u,_ud in USERS_D.items():
    _gs=GOALS_U[_u]; _mf=_ud.get('main_flow'); _top=FBY.get(_mf)
    # goal completion = the last tap of each main-flow outcome typed goal:<id>, plus arriving at the goal's own end state
    _gedge={}; _adv={}; _oute={}; _outs=[]
    for _f in [f for f in FLOWS if f['user']==_u]:
        for _i,_st in enumerate(_FL[_f['id']]['steps']):
            if _st.get('advances') and _i: _adv.setdefault((_f['sx'][_i-1]['site'],_f['sx'][_i]['ref']+('!'+_st['condition'] if _st.get('condition') else '')),set()).add(_st['advances'])
    if _top:
        for _o in _top['outs']:
            _g=FBY[_o['id']]; _r=_g['result'] or ''; _sx=_g['sx']
            _outs.append(dict(id=_g['id'],l=olab(_o),w=_o['when'] or _o['entry'] or '',r=_r,ph=MW.vp(_o['phase']),end=_sx[-1]['site']))
            for _i in range(1,len(_sx)):
                _c=_FL[_g['id']]['steps'][_i].get('condition')
                _k=(_sx[_i-1]['site'],_sx[_i]['ref']+('!'+_c if _c else ''))
                _oute.setdefault(_k,[]).append(_g['id'])
            if _r.startswith('goal:'):  # the tap where the path's goal track completes (prog), else its last tap
                _gg=_r[5:]; _n=len(_gs[_gg]['ms']) if _gg in _gs else 0; _pr=_g['prog']
                _ci=next((i for i in range(1,len(_sx)) if _pr[i].get(_gg,0)>=_n>0 and _pr[0].get(_gg,0)<_n),len(_sx)-1)
                _c=_FL[_g['id']]['steps'][_ci].get('condition')
                _gedge.setdefault(_gg,set()).add((_sx[_ci-1]['site'],_sx[_ci]['ref']+('!'+_c if _c else '')))
    _gend={g:MW.goal_target(gd) if gd['ms'] and not gd['ms'][-1].get('_shared') and gd['ms'][-1].get('states') else [] for g,gd in _gs.items()}
    for _ph in MW.PHASES:
        nodes=[]; idx={}; q=[]
        def node(st):
            k=_wnk(st)
            if k in idx: return idx[k]
            idx[k]=len(nodes); key=MW.key(st)
            nodes.append(dict(k=key,c=st.get('cont') or '',p=st['root'],o=st['kids'][-1][1] if st['kids'] else '',a=st['auth'],lv=st['live'],m=st.get('tab') or '',t=_wtitle(st),
                h={g:sorted(MW.step_hits({g:gd},key)) for g,gd in _gs.items()},
                gs=sorted(g for g,pt in _gend.items() if any(_wfn.fnmatchcase(key,p) for p in pt)),e=[],bk=0))
            q.append((idx[k],st)); return idx[k]
        ways=[]
        for _wid,_w in _WAYS.items():
            if _u not in _w.get('users',[]): continue
            s=MW.way_start(_w,_ud['auth']); sp=PH_S.get(s['screen'])
            st=dict(root=s['screen'],kids=[],auth=s['auth'],live=s['live'],tab=None,device='phone',phase=_ph,cont=None)
            if st['root']=='home': st['tab']=s.get('tab') if (_ph>=2 or s.get('tab')=='live') else 'live'
            ok=sp is None or sp<=_ph
            ways.append(dict(id=_wid,l=_w.get('label',_wid),w=_w.get('when',''),hold=_w.get('holds',[]),n=node(st) if ok else -1,ok=ok))
        while q:
            i,st=q.pop(0); N=nodes[i]
            for own,l in MW.available(SC,st):
                alts=[(None,l,st)]+[(cid,) + tuple(reversed(MW.cond_link(st,l,cid))) for cid in _EVC]
                seen_alt=set()
                for cid,l2,cur in alts:
                    if cid and (l2 is l and cur is st): continue
                    try: n=MW.resolve(SC,cur,l2,own)
                    except Exception: n=None
                    if n is None: continue
                    ref=f"{own}:{l['id']}"+('!'+cid if cid else '')
                    if n=='back': N['bk']=1; N['e'].append(dict(r=ref,l=l.get('label') or l['id'],t=-1,a='back',to='',ch=own!=MW.top(st))); continue
                    n['phase']=_ph; t=node(n); sk=(N['k'],ref)
                    e=dict(r=ref,l=l.get('label') or l['id'],t=t,a=l['action'],to=l.get('to') or '',ch=own!=MW.top(st),
                        cond=_EVC[cid]['label'] if cid else '',si=1 if 'auth=in' in (l2.get('sets') or '') else 0,oc=_oute.get(sk,[]),g=sorted(g for g,ks in _gedge.items() if sk in ks),adv=sorted(_adv.get(sk,())))
                    N['e'].append(e)
            if not any(e['t']>=0 for e in N['e']): WALK_WARN.append(f'{_u} phase {_ph}: dead end at {N["k"]} ({N["t"]}): no link leads on')
        # build-time checks: every node renders, every choice is a model link on a screen that is on top or in chrome
        for N in nodes:
            MW.rendered_id(SC[N['p']],N['a'],N['lv'],N['m'] or None,_ph)
            if N['o'] and N['o'] not in OVCH: raise SystemExit(f'walk: sheet {N["o"]} has no drawn overlay')
            for e in N['e']:
                o,_,lid=e['r'].split('!')[0].partition(':')
                if not any(x['id']==lid for x in SC[o].get('links',[])): raise SystemExit(f'walk: choice {e["r"]} on {N["k"]} is not a model link')
        drops=[dict(o=o['id'],m=o['r'][5:]) for o in _outs if o['r'].startswith('drop:') and o['ph']<=_ph]
        WALK[f'{_u}/{_ph}']=dict(n=nodes,w=ways,dr=drops)
    WALK[_u]=dict(l=_ud.get('label',_u),sub=_ud.get('sub',''),mf=_mf,mfn=_top['name'] if _top else '',outs=_outs,
        goals=[dict(id=g,l=gd['label'],c=gd['color'],ph=MW.vp(gd.get('phase')) if gd.get('phase') is not None else 0,lk=gd.get('likely',''),ms=[dict(id=m['id'],l=m.get('label',m['id'])) for m in gd['ms']]) for g,gd in _gs.items()])
_wscr={}
for _k,_d in SC.items():
    nk=('ov-'+_k) if _d['kind']=='sheet' else _k
    if nk in NOTES: _wscr[_k]=dict(t=_d['title'],s=NOTES[nk]['secs'])
WALK['_scr']=_wscr; WALK['_users']=list(USERS_D); WALK['_phases']=list(MW.PHASES)
def _wtip(t):
    try: return tip(t)
    except Exception: return t
_wj=json.dumps(WALK,ensure_ascii=False); WALK['_src']={t:_wtip(t) for t in sorted(set(re.findall(MW.TAG,_wj)))}  # hover text for each source tag
for _w in sorted(set(WALK_WARN)): print('walk WARN',_w)
def _wstrip(x):
    if isinstance(x,dict): return {k:_wstrip(v) for k,v in x.items() if v not in ('',[],{},None,0,False) or k in ('t','n','ph')}
    if isinstance(x,list): return [_wstrip(v) for v in x]
    return x
os.makedirs('flows/walk',exist_ok=True)
_wmeta={k:v for k,v in WALK.items() if '/' not in k}
for k,v in WALK.items():
    if '/' in k:
        for N in v['n']: N['h']={g:m for g,m in N['h'].items() if m}
        open(f'flows/walk/{k.replace("/","-")}.json','w').write(json.dumps(_wstrip(v),ensure_ascii=False,separators=(',',':')))
print('walk',{k:len(v['n']) for k,v in WALK.items() if '/' in k},'states;',len(set(WALK_WARN)),'dead ends')
exec(open('gen/walkpage.py').read())
