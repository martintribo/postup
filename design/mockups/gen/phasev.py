# Per-phase screen versions in the HTML [M1035]. exec'd by build.py after home.py.
# One HTML chunk per screen carries both versions: elements with class p2only render only in phase 2+, p1only only in phase 1.
# The mockup sets html[data-vph] from ?ph= or the shared Phase toggle (localStorage pu-ph1); 'All' renders the latest phase.
# The drift check (sitegraph.py) parses each phase version separately against the model links valid in that phase.
import re
P2T=('project','projects','project-new','project-update','project-attach','invite-project','activity','postup-ask','ask','ask-signin','requested')  # + ask to join [M1036]
import sys as _s; _s.path.insert(0,'gen'); import model as _PM
_SKIP=set(P2T)|{'inbox','index'}|{k for k,v in _PM.load()[0].items() if (v.get('phase') or 0)>=2}  # phase-2 screens keep their links
_TGT=re.compile(r"""(?:go|act)\('(%s)'|href="#(%s)\"""" % ('|'.join(P2T),'|'.join(P2T)))
def _mark(tag):
    if 'p2only' in tag or 'p1only' in tag: return tag
    if re.search(r'\sclass="',tag): return re.sub(r'\sclass="',' class="p2only ',tag,count=1)
    return re.sub(r'^<(\w+)',r'<\1 class="p2only"',tag)
def p2links(h):
    """Phase 1 hides every element that links to a phase-2 screen (projects, Activity)."""
    return re.sub(r'<\w+\b[^>]*>',lambda m:_mark(m[0]) if _TGT.search(m[0]) else m[0],h)
for k in list(S):
    if k.split('--')[0] in _SKIP: continue
    S[k]=p2links(S[k])
DESK=p2links(DESK)
OVS=p2links(OVS)
# Home: no Live | Building switch in phase 1 (Building mode is phase 2)
for k in [k for k in S if k=='home' or k.startswith('home--')]:
    S[k]=S[k].replace('<span class="hsw ','<span class="p2only hsw ')

# Nearby feed: project-update cards are phase 2
for k in [k for k in S if k.split('--')[0] in ('quiet-feed','quiet-feed-b')]:
    S[k]=re.sub(r'<article class="fc">(?=(?:(?!</article>).)*<span class="mu sm">Update</span>)','<article class="p2only fc">',S[k],flags=re.S)
# Nearby with nobody live: phase 2 falls back to projects; phase 1 shows who posted up nearby lately
_RECENT=(f'<div class="p1only"><h3 class="sh">Recently nearby</h3><div class="grp">'
 f'<div class="lrow" onclick="go(\'profile\')">{av("MK",32)}<div class="lm"><b class="sm">Maya posted up at Bean Theory</b><span class="xs mu">Tue · 3 joined</span></div></div>'
 f'<div class="lrow" onclick="go(\'profile\')">{av("JR",32)}<div class="lm"><b class="sm">Jon posted up at Lot 1 Coffee</b><span class="xs mu">Mon · 2 joined</span></div></div></div></div>')
for k in ('quiet-feed--none','quiet-feed-b--none'):
    assert '<aside class="dside">' in S[k] and 'What people are building' in S[k], k
    S[k]=S[k].replace('<aside class="dside">',_RECENT+'<aside class="dside">',1).replace('What people are building','<span class="p2only">What people are building</span><span class="p1only">Who posted up nearby lately</span>',1)
# Postup: the "working on" card stays in phase 1, without the project tag or link
_c=re.search(r'<div class="p2only card" onclick="go\(\'project\'\)"><div class="ch"><span class="tag">(.*?)</span>(.*?)</div><p>(.*?)</p></div>',S['postup'],re.S)
assert _c, 'postup card'
_p1=f'<div class="p1only card"><p>{_c[3]}</p></div>'
for k in [k for k in S if k=='postup' or k.startswith('postup--') or k.startswith('join-signin')]:
    if _c[0] in S[k]: S[k]=S[k].replace(_c[0],_c[0]+_p1)

# mockup index: the same Phase choice as the flow views (All = latest version)
S['index']=S['index'].replace('<h3 class="sh">Style</h3>','<h3 class="sh">Phase</h3><div class="seg vps"><button data-vp="0" onclick="setVph(\'0\')">All (latest)</button><button data-vp="1" onclick="setVph(\'1\')">1 (pre-MVP)</button><button data-vp="2" onclick="setVph(\'2\')">≤2 (MVP)</button></div><h3 class="sh">Style</h3>',1)
assert 'data-vp="1"' in S['index']

# Ask to join is phase 2 [M1036]: phase 1 hides the "Who can join" choice and the host's Requests (approval) section
for k in [k for k in S if k.split('--')[0] in ('post','post-signin','post-edit','where','where-search','live')]:
    S[k]=re.sub(r'(<label( class="lab")?>Who can join</label><div class="seg[^"]*">.*?</div>)',r'<div class="p2only">\1</div>',S[k],count=1,flags=re.S)
for k in [k for k in S if k.split('--')[0]=='live']:
    S[k]=re.sub(r'(<div class="sp-h"><h2>Requests</h2>.*?)(?=<div class="sp-h"><h2>Joined</h2>)',r'<div class="p2only">\1</div>',S[k],count=1,flags=re.S)
assert 'Requests</h2>' in S['live'] and '<div class="p2only"><div class="sp-h"><h2>Requests' in S['live']
for k in [k for k in S if k=='home' or k.startswith('home--')]:
    S[k]=S[k].replace('<span class="mu sm">3 nearby</span>','<span class="mu sm p2only">3 nearby</span><span class="mu sm p1only">2 nearby</span>')  # Tess (ask to join) hidden in phase 1 [M1036]
