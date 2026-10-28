# Parse the links a mockup HTML chunk renders (onclick handlers + #hrefs). Used by the build-time drift check (sitegraph.py):
# the model (model/screens) is the source for links; the hand-written HTML must render exactly those. [M1031-draft]
import re
from html.parser import HTMLParser
VOID=('br','img','input','meta','link','path','circle','rect')
class LP(HTMLParser):
    def __init__(s,ids,drop=None): super().__init__(); s.ids=ids; s.st=[]; s.out=[]; s.drop=drop; s.skip=0  # drop: class of elements not rendered in this phase [M1035]
    def handle_starttag(s,t,a):
        a=dict(a)
        if s.skip:
            if t not in VOID: s.skip+=1
            return
        if s.drop and s.drop in (a.get('class') or '').split():
            if t not in VOID: s.skip=1
            return
        js=(a.get('onclick') or ''); hr=a.get('href') or ''
        tg=[]
        for m in re.finditer(r"\b(go|ov|signIn|setHome|act)\('([\w-]*)'",js): tg.append((m[1],m[2]))
        if re.search(r'\bsignIn\(\)',js): tg.append(('signIn',''))
        if re.search(r'\bpostAt\(',js): tg.append(('go','post'))
        if re.search(r'\bfollow\(',js): tg.append(('follow',''))
        if re.search(r'\bbk\(\)',js): tg.append(('back',''))
        if re.search(r'\bovx\(\)',js) and not tg: tg.append(('ovx',''))
        if re.search(r'\bpick\(',js): tg.append(('back',''))
        m=re.fullmatch(r'#([\w-]+)',hr)
        if m and m[1] in s.ids: tg.append(('go',m[1]))
        if t in VOID:
            if tg: s.out.append([tg,a.get('aria-label','') or a.get('alt','') or a.get('placeholder','')])
            return
        s.st.append([tg,a.get('aria-label',''),''])
    def handle_endtag(s,t):
        if t in VOID: return
        if s.skip: s.skip-=1; return
        if s.st:
            tg,al,tx=s.st.pop()
            if s.st: s.st[-1][2]+=' '+tx
            if tg: s.out.append([tg,(re.sub(r'\s+',' ',tx).strip() or al)[:34]])
    def handle_data(s,d):
        if s.skip: return
        if s.st: s.st[-1][2]+=d
TABNAV=re.compile(r'<nav class="tab[^"]*">.*?</nav>',re.S)
def links(chunk,ids,phase=None):
    """phase=1 drops .p2only elements, phase>=2 drops .p1only (the per-phase HTML versions [M1035])."""
    p=LP(ids,None if phase is None else ('p2only' if phase<2 else 'p1only')); p.feed(chunk); return p.out
SIGNOUT=re.compile(r'sign out|delete',re.I)
def acts(tg,lab,auth,owner,in_sheet):
    """one rendered link -> model-shaped (action,to,sets,then) tuples for this auth"""
    out=[]
    for kind,t in tg:
        if kind=='ovx' and len(tg)>1: continue
        so='auth=out' if SIGNOUT.search(lab or '') else ''
        if kind=='go': out.append(('replace',t.split('--')[0],so,''))
        elif kind=='ov': out.append(('swap' if in_sheet else 'open',t,'',''))
        elif kind=='ovx': out.append(('close','',so,''))
        elif kind=='act': out.append(('open','signin','',t) if auth=='out' else ('replace',t,'',''))
        elif kind=='follow': out.append(('open','signin','','') if auth=='out' else ('swap',owner,'',''))
        elif kind=='signIn': out.append(('close','','auth=in','') if (in_sheet and not t) else ('replace',t or owner,'auth=in',''))
        elif kind=='setHome': out.append(('swap','home','tab='+t,''))
        elif kind=='back': out.append(('back','','',''))
    return out
