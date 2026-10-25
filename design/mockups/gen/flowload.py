# Loads gen/flowdata.py and adds the legacy tuple view used by renderers:
#   f['sx'] = step dicts (site, user, act, do[, device]);  f['steps'] = (page, auth, live, extra, do) tuples
import re as _re
exec(open('gen/flowdata.py').read())
def parse_site(sid):
    m=_re.fullmatch(r'([\w-]+)(?:\+([\w-]+))?@(in|out)\.(live|none)(?:\.(live|building))?',sid)
    if not m: raise SystemExit(f'bad site-state id {sid}')
    return dict(page=m[1],ov=m[2],auth=m[3],live=m[4],mode=m[5])
for _f in FLOWS:
    _f['sx']=_f['steps']; _t=[]
    for _d in _f['sx']:
        _p=parse_site(_d['site']); _x={}
        if _p['mode']: _x['mode']=_p['mode']
        if _p['ov']: _x['ov']=_p['ov']
        if _d.get('device'): _x['device']=_d['device']
        _t.append((_p['page'],_p['auth'],_p['live'],_x,_d['do']))
    _f['steps']=_t
