# Per-phase screen versions in the HTML [M1035] [M1047-draft]. exec'd by build.py after home.py.
# Classes: since-<id> (from that phase onward), until-<id> (through that phase), only-<id>.
# Generated CSS (model.visibility_css) hides them per html[data-vph]. Auto-mark elements that
# navigate to a screen with since= set; leftover visual-only tweaks stay here, keyed by phase id.
import re, json
import sys as _s; _s.path.insert(0,'gen'); import model as _PM
_SC,_FL,_EV,_GL=_PM.load()
_FIRST=_PM.PIDS[0]
_MVP='mvp' if 'mvp' in _PM.PBY else _PM.LATEST
_PRE='pre-mvp' if 'pre-mvp' in _PM.PBY else (_PM.PIDS[1] if len(_PM.PIDS)>1 else _PM.LATEST)

def _cls_for_target(toid):
    s=_SC.get(toid)
    if s and s.get('since') and s['since']!=_FIRST:
        return 'since-'+s['since']
    return None

# Auto-mark any element that goes/acts/hrefs/ovs to a later-since screen.
_TGT=re.compile(r"""(?:go|act|ov)\('([\w-]+)'|href="#([\w-]+)\"""")
def _mark(tag, cls):
    if not cls: return tag
    if cls in tag or 'since-' in tag or 'until-' in tag or 'only-' in tag: return tag
    if re.search(r'\sclass="', tag): return re.sub(r'\sclass="', f' class="{cls} ', tag, count=1)
    return re.sub(r'^<(\w+)', rf'<\1 class="{cls}"', tag)

def _autolinks(h):
    def one(m):
        tag=m.group(0)
        ids=_TGT.findall(tag)
        cls=None
        for a,b in ids:
            to=a or b
            c=_cls_for_target(to)
            # leave overlay
            if "ov('leave')" in tag or 'ov("leave")' in tag:
                c=_cls_for_target('leave') or c
            if c:
                # if several, keep the latest since
                if cls is None or (_PM.pindex(c.split('-',1)[1])>_PM.pindex(cls.split('-',1)[1])):
                    cls=c
        return _mark(tag, cls)
    return re.sub(r'<\w+\b[^>]*>', one, h)

_SKIP={'index'}
for k in list(S):
    if k.split('--')[0] in _SKIP: continue
    S[k]=_autolinks(S[k])
DESK=_autolinks(DESK)
OVS=_autolinks(OVS)

# Home: Live | Building switch is mvp (Building mode)
for k in [k for k in S if k=='home' or k.startswith('home--')]:
    S[k]=S[k].replace('<span class="hsw ','<span class="since-%s hsw '%_MVP)

# Nearby feed: project-update cards are mvp
for k in [k for k in S if k.split('--')[0] in ('quiet-feed','quiet-feed-b')]:
    S[k]=re.sub(r'<article class="fc">(?=(?:(?!</article>).)*<span class="mu sm">Update</span>)', f'<article class="since-{_MVP} fc">', S[k], flags=re.S)

# Nobody live: until pre-mvp shows who posted recently; mvp shows projects
_RECENT=(f'<div class="until-{_PRE}"><h3 class="sh">Recently nearby</h3><div class="grp">'
 f'<div class="lrow" onclick="go(\'profile\')">{av("MK",32)}<div class="lm"><b class="sm">Maya posted up at Bean Theory</b><span class="xs mu">Tue · 3 joined</span></div></div>'
 f'<div class="lrow" onclick="go(\'profile\')">{av("JR",32)}<div class="lm"><b class="sm">Jon posted up at Lot 1 Coffee</b><span class="xs mu">Mon · 2 joined</span></div></div></div></div>')
for k in ('quiet-feed--none','quiet-feed-b--none'):
    assert '<aside class="dside">' in S[k] and 'What people are building' in S[k], k
    S[k]=S[k].replace('<aside class="dside">',_RECENT+'<aside class="dside">',1).replace(
        'What people are building',
        f'<span class="since-{_MVP}">What people are building</span><span class="until-{_PRE}">Who posted up nearby lately</span>',1)

# Postup: "working on" card stays through pre-mvp without the project tag
_c=re.search(r'<div class="since-%s card" onclick="go\(\'project\'\)"><div class="ch"><span class="tag">(.*?)</span>(.*?)</div><p>(.*?)</p></div>'%re.escape(_MVP), S['postup'], re.S)
# After auto-mark the project card should already be since-mvp; fall back to old p2only / unclassed card
if not _c:
    _c=re.search(r'<div class="(?:since-[\w-]+ )?card" onclick="go\(\'project\'\)"><div class="ch"><span class="tag">(.*?)</span>(.*?)</div><p>(.*?)</p></div>', S['postup'], re.S)
assert _c, 'postup card'
_p1=f'<div class="until-{_PRE} card"><p>{_c[3]}</p></div>'
for k in [k for k in S if k=='postup' or k.startswith('postup--') or k.startswith('join-signin')]:
    if _c[0] in S[k] and _p1 not in S[k]: S[k]=S[k].replace(_c[0],_c[0]+_p1)

# Phase toggle on the mockup index: All + one button per phase (generated)
_btns='<button data-vp="all" onclick="setVph(\'all\')">All (latest)</button>'+''.join(
    f'<button data-vp="{ph["id"]}" onclick="setVph(\'{ph["id"]}\')">{ph.get("badge") or ph["id"]} ({(ph.get("label") or ph["id"]).split("(")[-1].rstrip(")") if "(" in (ph.get("label") or "") else ph["id"]})</button>'
    for ph in _PM.PHASES)
# Simpler labels: "0 (smallest)", "≤1 (pre-MVP)", "≤2 (MVP)" matching today's wording for the three current phases
def _btn_label(ph, i):
    lab=ph.get('label') or ph['id']
    # "Phase 0 (smallest)" -> "0 (smallest)" [M1047-draft]
    return lab.replace('Phase ', '', 1)
_btns='<button data-vp="all" onclick="setVph(\'all\')">All (latest)</button>'+''.join(
    f'<button data-vp="{ph["id"]}" onclick="setVph(\'{ph["id"]}\')">{_btn_label(ph,i)}</button>'
    for i,ph in enumerate(_PM.PHASES))
S['index']=S['index'].replace('<h3 class="sh">Style</h3>', '<h3 class="sh">Phase</h3><div class="seg vps">'+_btns+'</div><h3 class="sh">Style</h3>', 1)
assert f'data-vp="{_FIRST}"' in S['index']

# Ask to join is mvp: hide Who can join / Requests in earlier phases (visual controls; links already have since=)
for k in [k for k in S if k.split('--')[0] in ('post','post-signin','post-edit','where','where-search','live')]:
    S[k]=re.sub(r'(<label( class="lab")?>Who can join</label><div class="seg[^"]*">.*?</div>)', rf'<div class="since-{_MVP}">\1</div>', S[k], count=1, flags=re.S)
for k in [k for k in S if k.split('--')[0]=='live']:
    S[k]=re.sub(r'(<div class="sp-h"><h2>Requests</h2>.*?)(?=<div class="sp-h"><h2>Joined</h2>)', rf'<div class="since-{_MVP}">\1</div>', S[k], count=1, flags=re.S)
assert 'Requests</h2>' in S['live'] and f'<div class="since-{_MVP}"><div class="sp-h"><h2>Requests' in S['live']
for k in [k for k in S if k=='home' or k.startswith('home--')]:
    S[k]=S[k].replace('<span class="mu sm">3 nearby</span>', f'<span class="mu sm since-{_MVP}">3 nearby</span><span class="mu sm until-{_PRE}">2 nearby</span>')

# extend while hosting is pre-mvp+
_n=0
for k in [k for k in S if k=='live' or k.startswith('live--')]:
    S[k],c=re.subn(r'<button class="btn sec" onclick="this.innerHTML=\'Till 4:15pm ✓\'">', f'<button class="since-{_PRE} btn sec" onclick="this.innerHTML=\'Till 4:15pm ✓\'">', S[k]); _n+=c
assert _n, 'extend button'
