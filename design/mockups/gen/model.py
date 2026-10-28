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
DIMS={'auth':('in','out'),'live':('live','none'),'tab':('live','building')}
TAG=r'\[(F\d{3}|FS|TK§\d|R\d+⚠?|drawn|unsourced|M1018[bc]?|M1024|M1025|M1030|M1031-draft)\]'
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
    """'auth=out,live=none; auth=in' -> list of dicts (alternatives). '' -> [{}] (always)."""
    if not w: return [{}]
    return [dict(kv.split('=',1) for kv in alt.split(',')) for alt in w.split(';')]
def matches(w,st):
    return any(all(st.get(k)==v for k,v in alt.items()) for alt in parse_when(w))
# A site state: root screen + open child (slot, screen) chain + conditions. Kept flat for the current depth (page + one sheet)
# but resolve() walks children generically. dict(root=, kids=[(slot,screen),...], auth=, live=, tab=)
def key(st): return st['root']+''.join('+'+c for _,c in st['kids'])+f"@{st['auth']}.{st['live']}"+(f".{st['tab']}" if st['root']=='home' else '')
def top(st): return st['kids'][-1][1] if st['kids'] else st['root']
def dmode(l): return 'live' if l=='live' else 'building'
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
    cond=dict(auth=st['auth'],live=st['live'],tab=st.get('tab'))
    if not matches(link.get('when',''),cond): return None
    n=dict(st,kids=list(st['kids'])); n['cont']=None; a=link['action']; to=link.get('to')
    if a=='close' and link.get('continue') and st.get('cont'): a='replace'; to=st['cont']
    if a=='replace':
        n['root']=to; n['kids']=[]
        apply_sets(n,link.get('sets'))
        if to=='home' and st['root']!='home' and 'tab=' not in (link.get('sets') or ''): n['tab']=dmode(n['live'])
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
    elif not n.get('tab'): n['tab']=dmode(n['live'])
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
def rendered_id(s,auth,live,tab):
    """HTML element id that renders screen s in these conditions: first matching 'variants' entry, else the screen id."""
    c=dict(auth=auth,live=live,tab=tab)
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
