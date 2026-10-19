# Home page (/) with two modes on one URL (Martin, Oct 18: [M1018b]). exec'd after scenarios.py.
# Sections: home (Live mode, someone live), home--map-none (Live mode, none live),
# home--bld (Building mode, none live), home--bld-live (Building mode while someone is live: banner),
# home-overlay-alt (comparison only: alternative, not chosen). scen.js picks the section.
import re
IC['home']='<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>'
# nav tab and rail say Home
for k in list(S): S[k]=S[k].replace(f'{I("map",22)}<span>Map</span>',f'{I("home",22)}<span>Home</span>')
DESK=DESK.replace(f'{I("map",22)}<span>Map</span>',f'{I("home",22)}<span>Home</span>')
assert '<span>Map</span>' not in DESK and not any('<span>Map</span></a>' in v for v in S.values())
def hsw(on,cls=''):
    return (f'<span class="hsw {cls}" role="tablist"><button class="{"on" if on=="live" else ""}" onclick="setHome(\'live\')">Live</button>'
            f'<button class="{"on" if on=="building" else ""}" onclick="setHome(\'building\')">Building</button></span>')
PC3=pcard("Star Fox 64 mod","MK","sf64","Corneria II playable","Yesterday","Bean Theory",2)+pcard("Pixel Garden","TS","pixel","New crop sprites","Tue","Grindhouse",1)+pcard("Bus Stop Zine","JR","sketch","Page 12 inked","Mon","Bean Theory",2)
THISWEEK=f'<div class="lrow" onclick="go(\'cafe\')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Lantern Tea</b><div class="l2">{stack(["AL","DN","MK"],20)} 3 postups</div></div>{I("chev",18,"mu")}</div>'
HWEL=f'<div class="welcome hwel"><span class="ci sm">{I("coffee",16)}</span><p>Post up at a cafe. See who\'s working nearby.</p><button class="ib" onclick="this.parentNode.remove()" aria-label="Dismiss">{I("x",18)}</button></div>'
# Live mode, someone live: the drawing + switch (phone: over the map; desktop: top of the panel)
h=S['home']
h=h.replace('<span class="brand">','<span class="brand hbr">',1)
h=re.sub(r'(<div class="mtop"><span class="brand hbr">.*?</span>)',lambda m:m[1]+hsw('live','hsw-ph'),h,count=1,flags=re.S)
h=h.replace('<section class="sheet-p"><span class="grab"></span>','<section class="sheet-p"><span class="grab"></span>'+hsw('live','hsw-dk'),1)
assert h.count('class="hsw')==2
S['home']=h
# Live mode, none live: map with cafes only + a positive invite
ml=re.sub(r'<button class="mk live".*?</button>','',h,flags=re.S)
ml=re.sub(r'<div class="sp-h"><h2>Live now</h2>.*?(?=<div class="sp-h" style="margin-top:12px">)',
 f'<div class="hinv"><h2>Working somewhere today?</h2><p class="mu sm">Post up and people nearby will see you on the map.</p><button class="btn" onclick="go(\'post\')">{I("plus",18)} Post up</button></div>',ml,count=1,flags=re.S)
assert 'Live now' not in ml and 'hinv' in ml
S['home--map-none']=ml.replace('hsw-ph','hsw-ph').replace('class="on" onclick="setHome(\'live\')"','class="on" onclick="setHome(\'live\')"')
# Building mode
def bld(banner):
    bn=(f'<div class="hban"><span class="dot"></span><span>{av("MK",22)} <b>Maya</b> just posted up nearby</span><button class="lnk sm" onclick="setHome(\'live\')">See map</button></div>' if banner else '')
    return f'''<header class="nb hnb"><b class="brand2">{I("coffee",16)} postup</b>{hsw("building")}<span class="nr"><a class="ib only-in" href="#me" aria-label="Profile">{av("ME",30)}</a></span></header><div class="pad hbld">
{bn}{HWEL}<div class="hbh"><h1>What people are building</h1><a class="lnk sm" href="#projects">See all projects</a></div>
<div class="pgrid hpg">{PC3}</div><a class="btn sec hall" href="#projects">{I("folder",18)} See all projects</a>
<button class="btn lg hpost" onclick="go('post')">{I("plus",18)} Post up</button>
<div class="grp hwk"><h3 class="sh">This week</h3>{THISWEEK}</div></div>{nav("m")}'''
S['home--bld']=bld(False); S['home--bld-live']=bld(True)
FULL+=['home--bld','home--bld-live']
# Comparison: projects card floating over a dimmed map (alternative, not chosen)
S['home-overlay-alt']=f'''<div class="hm hoa">{mapblock("100%",pin_cafe(30,34,'3 this week')+pin_cafe(68,58)+pin_cafe(52,20),f'<div class="mtop"><span class="brand">{I("coffee",16)} postup</span><span class="altb">Alternative · not chosen</span></div>')}
<div class="hoa-dim"></div><div class="hoa-card"><span class="altb dk">Alternative · not chosen</span><h2>What people are building</h2>
<div class="lrow" onclick="go('project')"><span class="ci pj">{I("folder",20)}</span><div class="lm"><b>Star Fox 64 mod</b><div class="l2">Maya · Corneria II playable</div></div>{I("chev",18,"mu")}</div>
<div class="lrow" onclick="go('project')"><span class="ci pj">{I("folder",20)}</span><div class="lm"><b>Pixel Garden</b><div class="l2">Tess · New crop sprites</div></div>{I("chev",18,"mu")}</div>
<div class="lrow" onclick="go('project')"><span class="ci pj">{I("folder",20)}</span><div class="lm"><b>Bus Stop Zine</b><div class="l2">Jon · Page 12 inked</div></div>{I("chev",18,"mu")}</div>
<div class="row2"><a class="btn sec" href="#projects">See all projects</a><button class="btn" onclick="go('post')">{I("plus",18)} Post up</button></div>
<button class="tx" onclick="this.closest('.hoa').classList.add('hoa-off')">Show map</button></div></div>{nav("m")}'''
# index entries
S['index']=S['index'].replace("<b>Home page (/)</b><span class=\"mu sm\">Map when live · projects when none</span>","<b>Home page (/)</b><span class=\"mu sm\">Live · Building modes</span>",1)
S['index']=S['index'].replace('<span class="mu sm">What loads at postup.now/ · changes with the scenario</span>','<span class="mu sm">What loads at postup.now/ · Live and Building modes</span>',1)
S['index']=S['index'].replace("<b>Recent map</b>",f"<b>Recent map</b>",1)
alt=f'<a class="ixr" href="#home-overlay-alt"><span class="ixi">{I("image",18)}</span><span class="lm"><b>Home overlay (alt)</b><span class="mu sm">Alternative, not chosen</span></span>{I("chev",18,"mu")}</a>'
i=S['index'].index('<a class="ixr" href="#quiet-feed">'); S['index']=S['index'][:i]+alt+S['index'][i:]
assert S['index'].count('home-overlay-alt')==1

# sections built after the first rename still carry the old label
for k in list(S): S[k]=S[k].replace(f'{I("map",22)}<span>Map</span>',f'{I("home",22)}<span>Home</span>')
assert not any('<span>Map</span></a>' in v for v in S.values())
