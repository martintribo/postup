# Floating mockup menu (every control in one place). exec'd by build.py after notes.py.
import re, html as H
def _items(chunk): return re.findall(r'<a class="ixr" href="#([\w-]+)">.*?<b>(.*?)</b><span class="mu sm">(.*?)</span>',chunk,re.S)
idx=S['index']; groups=[]; seen=set()
groups.append(('Home page (/)',[('home','Home page (/)','Live · Building modes'),('home-overlay-alt','Home overlay (alt)','Alternative, not chosen')])); seen.update(['home','home-overlay-alt'])
for title,chunk in re.findall(r'<h3 class="sh">([^<]+)</h3><div class="grp">(.*?)</div>(?=\s*<h3|\s*</div>\s*$)',idx,re.S):
    its=[(i,H.unescape(t),H.unescape(d)) for i,t,d in _items(chunk) if i in S and '--' not in i]
    its=[x for x in its if x[0] not in seen]
    if its: groups.append((H.unescape(title),its)); seen.update(i for i,_,_ in its)
for t,its in groups:
    if t=='First visit' and 'invite-project' in S: its.append(('invite-project','Project link','Follow Maya')); seen.add('invite-project')
other=[(k,NOTES[k]['title'],'') for k in S if '--' not in k and k not in seen and k!='index']
if other: groups.append(('More',other))
assert all(k in seen or k in [o[0] for o in other] or k=='index' for k in S if '--' not in k)
def li(i,t,d): return f'<button class="pmi" data-go="{i}" data-q="{H.escape((i+" "+t+" "+d).lower())}"><b>{H.escape(t)}</b><span>{H.escape(d) if d else "#"+i}</span></button>'
SCREENS=''.join(f'<div class="pmg"><h5>{H.escape(t)}</h5>'+''.join(li(*x) for x in its)+'</div>' for t,its in groups)
OVL=''.join(f'<button class="pmo" data-ov="{k[3:]}">{H.escape(NOTES[k]["title"].replace("Sheet · ",""))}</button>' for k in ORDER if k.startswith('ov-'))
def seg(attr,opts): return '<span class="pms">'+''.join(f'<button data-{attr}="{v}">{t}</button>' for v,t in opts)+'</span>'
MENU_HTML=f'''<div class="pmenu" id="pmenu"><button class="pmb" id="pmb" aria-label="Mockup menu" aria-expanded="false" onclick="pmToggle()"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg><span class="pmcur" id="pmcur"></span></button>
<div class="pmp" id="pmp" hidden><div class="pmh"><b>Mockup</b><span class="pmsp"></span><a href="#index" class="pml">Full index</a><button class="pmx" onclick="pmToggle(false)" aria-label="Close">×</button></div>
<div class="pmr"><label>Scenario</label>{seg("ma",[("out","Signed out"),("in","Signed in")])}{seg("ml",[("live","Live nearby"),("none","None live")])}</div>
<div class="pmr"><label>Home mode</label>{seg("mhm",[("live","Live"),("building","Building")])}</div>
<div class="pmr"><label>Style</label>{seg("mst",[("fresh","Fresh"),("cozy","Cozy"),("night","Night"),("bold","Bold")])}</div>
<div class="pmr"><label>Device</label>{seg("mdv",[("phone","Phone"),("desktop","Desktop")])}<label class="pmn"><input type="checkbox" id="pmnotes"> Notes</label></div>
<div class="pmr"><label>Sheets</label><div class="pmos">{OVL}</div></div>
<div class="pmr pmscr"><label>Screens</label><input class="pmq" id="pmq" placeholder="Search screens" autocomplete="off"><div class="pmlist" id="pmlist">{SCREENS}</div></div></div></div>'''
MENU_CSS=open('gen/menu.css').read(); MENU_JS=open('gen/menu.js').read()
