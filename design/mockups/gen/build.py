# Generates ../index.html (PostUp mockups v3)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
IC={ # lucide-style paths (24x24, stroke)
'map':'<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
'folder':'<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
'plus':'<path d="M12 5v14M5 12h14"/>',
'back':'<path d="m15 18-6-6 6-6"/>','chev':'<path d="m9 18 6-6-6-6"/>',
'lock':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
'pin':'<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
'users':'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4-6"/>',
'share':'<path d="M12 3v13M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
'copy':'<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
'check':'<path d="m5 12 5 5 9-10"/>','camera':'<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
'coffee':'<path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v3M12 3v3"/>',
'nav':'<path d="m3 11 18-8-8 18-2-8z"/>','star':'<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
'x':'<path d="M18 6 6 18M6 6l12 12"/>','edit':'<path d="M4 20h4L19 9l-4-4L4 16z"/>','spark':'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
'locate':'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/><circle cx="12" cy="12" r="7"/>',
'list':'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>','image':'<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>',
'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
}
def I(n,s=18,c=''): return f'<svg class="ic {c}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[n]}</svg>'
LOCK=I('lock',14,'lk')
P={'MK':('Maya','#7c3aed'),'JR':('Jon','#e11d48'),'TS':('Tess','#0891b2'),'AL':('Ari','#d97706'),'DN':('Dev','#2563eb'),'ME':('You','#10a364')}
def av(k,s=36):
    n,c=P[k]; return f'<span class="av" style="--c:{c};width:{s}px;height:{s}px;font-size:{int(s*.4)}px">{n[0]}</span>'
def stack(ks,s=24): return '<span class="stk">'+''.join(av(k,s) for k in ks)+'</span>'
def nav(a):
    t=[('home','map','Map','m'),('project','folder','Projects','p')]
    h='<nav class="tab">'
    h+=f'<a href="#home" class="{"on" if a=="m" else ""}">{I("map",22)}<span>Map</span></a>'
    h+=f'<a href="#post" class="tp">{I("plus",22)}<span>Post up</span></a>'
    h+=f'<a href="#projects" class="{"on" if a=="p" else ""}">{I("folder",22)}<span>Projects</span></a></nav>'
    return h
def top(title,right='',back=True,clear=False):
    b=f'<button class="ib" onclick="bk()" aria-label="Back">{I("back",22)}</button>' if back else '<span class="ib"></span>'
    return f'<header class="nb{" clr" if clear else ""}">{b}<b>{title}</b><span class="nr">{right}</span></header>'

# ---------- map ----------
def mapsvg():
    roads=[('M-20 120 C 120 140, 260 90, 420 130','maj'),('M60 -20 C 90 120, 150 250, 130 420','mn'),('M300 -20 C 280 120, 330 260, 300 420','mn'),
           ('M-20 300 C 120 280, 260 330, 420 290','maj'),('M-20 210 L 420 230','mn'),('M200 -20 L 215 420','mn')]
    r=''.join(f'<path d="{d}" class="r-{c}"/>' for d,c in roads)
    return f'''<svg class="mapsvg" viewBox="0 0 400 400" preserveAspectRatio="xMidYMid slice">
<rect class="m-base" width="400" height="400" fill="#f2efe9"/>
<path d="M290 330 Q 340 300 420 320 L 420 420 L 260 420 Z" fill="#cfe3f3" class="m-water"/>
<rect x="225" y="140" width="62" height="70" rx="10" fill="#d7ecd0" class="m-park"/><rect x="20" y="230" width="90" height="55" rx="10" fill="#d7ecd0" class="m-park"/>
<g fill="#e7e2d8" class="m-bldg">{''.join(f'<rect x="{x}" y="{y}" width="40" height="34" rx="4"/>' for x,y in [(80,150),(150,150),(150,40),(240,40),(330,60),(340,160),(150,250),(240,250),(30,40),(40,320),(150,330)])}</g>
<g fill="none" stroke-linecap="round" class="m-road">{r.replace('class="r-maj"','stroke="#fff" stroke-width="11"').replace('class="r-mn"','stroke="#fff" stroke-width="6"')}</g>
<path d="M-20 120 C 120 140, 260 90, 420 130" stroke="#fde7b0" stroke-width="5" fill="none" class="m-maj"/>
<text x="20" y="112" class="mlbl">Venice Blvd</text><text x="238" y="180" class="mlbl g">Oakwood Park</text><text x="300" y="370" class="mlbl b">Marina</text>
</svg>'''
def dmapsvg():
    m=mapsvg()
    inner=m[m.index('>',m.index('<svg'))+1:m.index('<text')]
    g=f'<g id="tile">{inner}</g>'
    t=[(0,0,''),(800,0,'scale(-1,1)'),(400,800,'scale(1,-1)'),(1200,800,'scale(-1,-1)'),(400,0,''),(0,400,'scale(1,1)'),(800,400,'scale(-1,1)'),(1200,400,'')]
    uses=''.join(f'<g transform="translate({x} {y}) {tr}">{inner}</g>' for x,y,tr in t[1:])
    lbl='<text x="60" y="112" class="mlbl">Venice Blvd</text><text x="640" y="180" class="mlbl g">Oakwood Park</text><text x="1050" y="740" class="mlbl b">Marina</text><text x="420" y="512" class="mlbl">Washington Blvd</text>'
    return f'<svg class="mapsvg" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice">{g}{uses}{lbl}</svg>'
def pin_live(x,y,k,n,dest='postup'):
    return f'<button class="mk live" style="left:{x}%;top:{y}%" onclick="go(\'{dest}\')"><span class="pulse"></span>{av(k,34)}<em>{n}</em></button>'
def pin_cafe(x,y,lbl=''):
    l=f'<em>{lbl}</em>' if lbl else ''
    return f'<button class="mk cafe" style="left:{x}%;top:{y}%" onclick="go(\'cafe\')"><span class="cp">{I("coffee",15)}</span>{l}</button>'
def mapblock(h,pins,extra=''):
    return f'<div class="map" style="height:{h}">{mapsvg()}{pins}<span class="you" style="left:48%;top:56%"></span><div class="attr">Map mockup</div>{extra}</div>'

# ---------- cards ----------
def live_row(k,proj,cafe,till,mins_left):
    n,c=P[k]
    pj=f'<span class="tag" onclick="event.stopPropagation();go(\'project\')">{proj}</span>' if proj else ''
    return f'''<div class="lrow" onclick="go('postup')">{av(k,44)}<div class="lm"><div class="l1"><b>{n}</b><span class="dot"></span><span class="ok">Live</span></div>
<div class="l2"><span class="cl" onclick="event.stopPropagation();go('cafe')">{cafe}</span> · till {till}</div>{pj}</div>{I("chev",18,"mu")}</div>'''
def feed_card(k,when,dist,what,proj,cafe,img,joined=None,update=False,photo=True):
    n,c=P[k]
    dest='project' if update else 'cafe'
    if photo and img: media=f'<div class="fm" onclick="go(\'{dest}\')"><img src="img/{img}.svg" alt=""><span class="fbadge">{I("camera",12)} {n}\'s photo</span></div>'
    elif not update: media=f'<div class="fm fb" style="--c:{c}" onclick="go(\'cafe\')"><span>{I("coffee",28)}</span></div>'
    else: media=''
    tg=f'<span class="tag" onclick="go(\'project\')">{proj}</span>' if proj else ''
    where=f'<span class="mu sm">Update</span>' if update else f'<span class="cl sm" onclick="go(\'cafe\')">{I("pin",13)} {cafe}</span>'
    soc=f'<span class="soc">{stack(joined,20)}<span class="mu sm">{len(joined)} joined</span></span>' if joined else '<span></span>'
    act='' if update else f'<button class="pill" onclick="postAt(\'{cafe}\')">Post up here</button>'
    return f'''<article class="fc">{media}<div class="fbd"><div class="fh">{av(k,28)}<b>{n}</b><span class="mu sm">· {when}{" · "+dist if dist else ""}</span></div>
<p class="fw">{what}</p><div class="fmeta">{tg}{where}</div><div class="fa">{soc}{act}</div></div></article>'''

S={}
# ---------- index ----------
def ix(href,t,d,ic):
    return f'<a class="ixr" href="{href}"><span class="ixi">{I(ic,18)}</span><span class="lm"><b>{t}</b><span class="mu sm">{d}</span></span>{I("chev",18,"mu")}</a>'
S['index']=f'''{top("Mockups",back=False)}<div class="pad">
<p class="mu">Tap through PostUp's key flows. Everyone and everything here is made up.</p>
<div class="grp">{ix("#home","Home map","Live postups","map")}{ix("#cafe","Cafe","Who's here","coffee")}{ix("#post","Post up","Form → sign in → share","plus")}{ix("#postup","Join","Postup → joined","users")}{ix("#project","Project","Updates, postups","folder")}{ix("#quiet","Recent map","Recent activity","pin")}</div>
<h3 class="sh">Style</h3><div class="stsw"><button data-s="fresh" onclick="setStyle('fresh')">Fresh</button><button data-s="cozy" onclick="setStyle('cozy')">Cozy</button><button data-s="night" onclick="setStyle('night')">Night</button><button data-s="bold" onclick="setStyle('bold')">Bold</button></div><h3 class="sh">Device</h3><div class="stsw dvsw"><button data-d="phone" onclick="applyDevice(\'phone\')">Phone</button><button data-d="desktop" onclick="applyDevice(\'desktop\')">Desktop</button></div><h3 class="sh">Compare recent states</h3>
<div class="grp">{ix("#quiet","Map","Map-first","map")}{ix("#quiet-feed","Feed A","With photos","image")}{ix("#quiet-feed-b","Feed B","No photos","list")}{ix("feed-rationale.md","Rationale","Why feed","spark")}</div></div>'''

# ---------- home ----------
pins=pin_live(30,34,'MK','2')+pin_live(70,62,'TS','',dest='postup-ask')+pin_cafe(55,22)+pin_cafe(18,72)+pin_cafe(84,30)
S['home']=f'''<div class="hm">{mapblock("380px",pins,f'<div class="mtop"><span class="brand">{I("coffee",16)} postup</span><button class="ib fl" onclick="go(\'quiet\')" aria-label="Locate">{I("locate",20)}</button></div>')}
<section class="sheet-p"><span class="grab"></span><div class="sp-h"><h2>Live now</h2><span class="mu sm">3 nearby</span></div>
{live_row('MK','Star Fox 64 mod','Bean Theory','4pm',70)}{live_row('JR','','Bean Theory','5pm',130)}{live_row('TS','Pixel Garden','Grindhouse','3pm',20).replace("go('postup')","go('postup-ask')",1).replace('<span class="ok">Live</span>','<span class="ok">Live</span><span class="mu xs" style="margin-left:6px">· Ask to join</span>',1)}
<div class="sp-h" style="margin-top:12px"><h3>This week</h3></div>
<div class="lrow" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Lantern Tea</b><div class="l2">{stack(['AL','DN','MK'],20)} 3 postups</div></div>{I("chev",18,"mu")}</div></section></div>{nav("m")}'''

# ---------- recent map (quiet) ----------
qp=pin_cafe(30,34,'3 this week')+pin_cafe(68,58,'1 this week')+pin_cafe(52,20)
S['quiet']=f'''<div class="hm">{mapblock("430px",qp,f'<div class="mtop"><span class="brand">{I("coffee",16)} postup</span><button class="ib fl" onclick="go(\'quiet-feed\')" aria-label="List">{I("list",20)}</button></div>')}
<section class="sheet-p"><span class="grab"></span><div class="sp-h"><h2>Nearby this week</h2><a class="sm lnk" href="#quiet-feed">See all</a></div>
<div class="lrow" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Bean Theory</b><div class="l2">{stack(['MK','JR','AL'],20)} 3 postups · Tue</div></div>{I("chev",18,"mu")}</div>
<div class="lrow" onclick="go('project')"><span class="ci pj">{I("folder",20)}</span><div class="lm"><b>Star Fox 64 mod</b><div class="l2">New level yesterday</div></div>{I("chev",18,"mu")}</div>
<button class="btn" onclick="postAt('Bean Theory')">{I("plus",18)} Post up</button></section></div>{nav("m")}'''

# ---------- feeds ----------
def feed(id,photo):
    cards=[feed_card('MK','Yesterday','0.4 mi','New Corneria level — boss fight next','Star Fox 64 mod','Bean Theory','table1',['JR','AL'],photo=photo),
           feed_card('TS','Tue','1.1 mi','New crop sprites for a tiny farming game','Pixel Garden','Grindhouse','pixel',photo=photo),
           feed_card('JR','Mon','0.4 mi','Sketching a zine about LA bus stops','','Bean Theory','sketch',['MK'],photo=photo),
           feed_card('MK','Mon','','Ship models imported','Star Fox 64 mod','','sf64',update=True,photo=photo)]
    return f'''{top("Nearby",f'<a class="ib" href="#quiet" aria-label="Map">{I("map",20)}</a>')}<div class="pad fd">
<div class="hero"><h1>Good things happen at cafes</h1><p class="mu">{stack(['MK','TS','JR','AL'],24)} 6 postups nearby this week</p></div>
<button class="btn lg" onclick="go('post')">{I("plus",18)} Post up</button>{''.join(cards)}
<aside class="dside"><div class="dcta"><h2>Working somewhere today?</h2><p class="mu sm">Let people nearby know. Takes ten seconds.</p><button class="btn" onclick="go('post')">{I("plus",18)} Post up</button></div>
<div class="dcard"><h3>Cafes nearby</h3>
<div class="lrow" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Bean Theory</b><div class="l2">{stack(['MK','JR','AL'],20)} 3 this week</div></div>{I("chev",18,"mu")}</div>
<div class="lrow" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Grindhouse</b><div class="l2">{stack(['TS'],20)} 1 this week</div></div>{I("chev",18,"mu")}</div>
<div class="lrow" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Lantern Tea</b><div class="l2">{stack(['AL','DN'],20)} 2 this week</div></div>{I("chev",18,"mu")}</div></div>
<a class="dmapc" href="#quiet"><div class="dmt">{mapsvg()}<span class="mk cafe" style="left:30%;top:34%"><span class="cp">{I("coffee",15)}</span></span><span class="mk cafe" style="left:68%;top:58%"><span class="cp">{I("coffee",15)}</span></span></div><div class="dml"><b>Open map</b>{I("chev",18,"mu")}</div></a></aside>
<p class="mu sm ctr">You're all caught up · <a class="lnk" href="#quiet">Map</a></p></div>{nav("m")}'''
S['quiet-feed']=feed('quiet-feed',True); S['quiet-feed-b']=feed('quiet-feed-b',False)

# ---------- cafe ----------
S['cafe']=f'''<div class="hero-img"><img src="img/table1.svg" alt=""><div class="hg"></div>{top("",f'<button class="ib fl" onclick="go(\'posted\')" aria-label="Share">{I("share",20)}</button>',clear=True)}
<div class="hi-t"><h1>Bean Theory</h1><p>{I("pin",14)} 0.4 mi · Open till 7pm</p></div><span class="fbadge tr">{I("camera",12)} Maya's photo</span></div>
<div class="pad"><div class="sp-h"><h2>Here now</h2><span class="ok sm"><span class="dot"></span> 2 live</span></div>
<div class="grp">{live_row('MK','Star Fox 64 mod','Bean Theory','4pm',70).replace('<svg class="ic mu"','<button class="pill sm2" onclick="event.stopPropagation();go(\'postup\')">Join</button><svg style="display:none" class="ic mu"')}
{live_row('JR','','Bean Theory','5pm',130).replace('<svg class="ic mu"','<button class="pill sm2" onclick="event.stopPropagation();go(\'postup\')">Join</button><svg style="display:none" class="ic mu"')}</div>
<div class="gcard"><div class="gph">{I("image",22)}</div><div><b class="sm">Google place card</b><div class="mu xs">UI Kit widget · photos, rating, hours · © Google</div></div></div>
<p class="mu sm">{stack(['AL','DN','TS'],20)} 5 postups this week · <span class="cl" onclick="go('project')">Star Fox 64 mod</span> regular</p></div>
<div class="cta"><button class="btn" onclick="postAt('Bean Theory')">{I("plus",18)} Post up here</button></div>{nav("m")}'''

# ---------- post form ----------
def seg(opts,on,name):
    return '<div class="seg">'+''.join(f'<button class="{"on" if o==on else ""}">{o}</button>' for o in opts)+'</div>'
S['post']=f'''{top("Post up")}<div class="pad form">
<label>Where</label><div class="field" onclick="cyc()"><span class="ci sm">{I("coffee",16)}</span><div class="lm"><b id="pcafe">Bean Theory</b><span class="mu xs" id="pnear">Nearest · 0.4 mi</span></div><span class="lnk sm">Change</span></div>
<label>Working on</label><input class="in" value="Level editor for the mod">
<div class="chips"><button class="chip on">Star Fox 64 mod</button><button class="chip ad" onclick="go('project-new')">{I("plus",14)} Project</button><button class="chip">None</button></div>
<label>Until</label>{seg(['1h','2h','3h','4pm'],'2h','u')}
<button class="addph">{I("camera",18)} Add a photo <span class="mu xs">optional</span></button></div>
<div class="cta"><button class="btn" onclick="sheet('post-signin')">Post up {LOCK}</button></div>'''

def signin(id,title,sub,to):
    return f'''<div class="dim" onclick="bk()"></div><div class="bs"><span class="grab"></span><h2>{title}</h2><p class="mu">{sub}</p>
<button class="sso ap" onclick="go('{to}')"><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff"><path d="M16.4 12.6c0-2.4 2-3.5 2-3.6-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9-.7 0-1.8-.8-3-.8-1.5 0-3 .9-3.8 2.3-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.3 0 2-1.1 2.8-2.3.9-1.3 1.2-2.5 1.3-2.6-.1 0-2.5-.9-2.5-3.7zM14.1 5.5c.6-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1 .1 2.1-.6 2.8-1.4z"/></svg> Continue with Apple</button>
<button class="sso" onclick="go('{to}')"><svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.6a4.8 4.8 0 0 1-2.1 3.1v2.6h3.4c2-1.8 3.1-4.5 3.1-7.5z"/><path fill="#34A853" d="M12 22c2.8 0 5.2-.9 6.9-2.5l-3.4-2.6c-.9.6-2.1 1-3.5 1-2.7 0-5-1.8-5.8-4.3H2.7v2.7A10 10 0 0 0 12 22z"/><path fill="#FBBC05" d="M6.2 13.6a6 6 0 0 1 0-3.8V7.1H2.7a10 10 0 0 0 0 9z"/><path fill="#EA4335" d="M12 5.9c1.5 0 2.9.5 4 1.5l3-3A10 10 0 0 0 2.7 7.1l3.5 2.7C7 7.7 9.3 5.9 12 5.9z"/></svg> Continue with Google</button>
<button class="tx" onclick="bk()">Not now</button></div>'''
S['post-signin']=S['post']+signin('post-signin','Almost there','Sign in and your postup goes live.','posted')

# ---------- posted ----------
S['posted']=f'''{top("",f'<a class="ib" href="#home" aria-label="Close">{I("x",22)}</a>',back=False)}<div class="pad done">
<div class="okc">{I("check",34)}</div><h1>You're posted up</h1><p class="mu">Bean Theory · till 3:45pm<br><span class="tag" onclick="go('project')">Star Fox 64 mod</span></p>
<div class="link"><span>postup.now/p/7xk2</span><button class="pill" onclick="this.innerHTML='Copied'">{I("copy",14)} Copy</button></div>
<button class="btn" onclick="this.innerHTML='Link shared'">{I("share",18)} Invite friends</button>
<button class="addph wide">{I("camera",18)} Add a photo of your spot</button>
<div class="lnks"><a class="lnk" href="#home">Back to map</a><a class="lnk" href="#cafe">Cafe</a><a class="lnk" href="#project">Project</a></div></div>{nav("")}'''

# ---------- postup ----------
S['postup']=f'''{top("Postup",f'<button class="ib" onclick="go(\'posted\')" aria-label="Share">{I("share",20)}</button>')}<div class="pad">
<div class="who">{av('MK',64)}<div><h1>Maya</h1><p class="ok"><span class="dot"></span> Live · till 4pm</p></div></div>
<div class="card" onclick="go('project')"><div class="ch"><span class="tag">Star Fox 64 mod</span>{I("chev",18,"mu")}</div><p>Adding a new Corneria level. Happy to talk ROM hacking.</p></div>
<div class="lrow card" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Bean Theory</b><div class="l2">0.4 mi · 8 min walk</div></div>{I("chev",18,"mu")}</div>
<p class="mu sm">{stack(['JR'],22)} Jon is joining</p></div>
<div class="cta"><button class="btn" onclick="sheet('join-signin')">Join {LOCK}</button></div>'''
S['join-signin']=S['postup']+signin('join-signin','Join Maya','Sign in so Maya knows who\'s coming.','joined')

# ---------- joined ----------
S['joined']=f'''{top("",f'<a class="ib" href="#home" aria-label="Close">{I("x",22)}</a>',back=False)}<div class="pad done">
<div class="pair">{av('ME',56)}{av('MK',56)}</div><h1>You're joining Maya</h1><p class="mu"><span class="cl" onclick="go('cafe')">Bean Theory</span> · till 4pm</p>
<button class="btn" onclick="go('cafe')">{I("nav",18)} Directions</button><p class="mu sm">Maya's been told you're coming.</p>
<div class="lnks"><a class="lnk" href="#home">Back to map</a><a class="lnk" href="#cafe">Cafe</a><a class="lnk" href="#project">Project</a><a class="lnk dg" href="#postup">Leave</a></div></div>{nav("m")}'''

# ---------- project ----------
S['project']=f'''<div class="hero-img sm"><img src="img/sf64.svg" alt=""><div class="hg"></div>{top("",f'<a class="ib fl" href="#project-new" aria-label="New">{I("plus",20)}</a>',clear=True)}
<div class="hi-t"><span class="tag lt">Game</span><h1>Star Fox 64 mod</h1><p>by <span class="cl" onclick="go('postup')">Maya</span> · 12 postups</p></div></div>
<div class="pad"><div class="row2"><a class="btn sec" href="#project-update">{I("edit",16)} Update {LOCK}</a><a class="btn" href="#project-attach">{I("plus",16)} Post up {LOCK}</a></div>
<aside class="pside"><div class="dcard"><div class="fh">{av('MK',44)}<div class="lm"><b>Maya</b><span class="mu sm">Owner · 12 postups</span></div></div><p class="sm">Fan mod adding new levels to Star Fox 64. Usually at Bean Theory on weekdays.</p><a class="btn" href="#project-attach">{I("plus",18)} Post up for this {LOCK}</a><a class="btn sec" href="#project-update">{I("edit",16)} Post update {LOCK}</a></div>
<div class="dcard"><h3>This week</h3><p class="mu sm">{stack(['MK','JR'],22)} 2 postups · Bean Theory</p></div></aside>
<div class="sp-h"><h2>Live</h2></div>
<div class="lrow card" onclick="go('postup')">{av('MK',40)}<div class="lm"><b>Maya</b><div class="l2"><span class="cl" onclick="event.stopPropagation();go('cafe')">Bean Theory</span> · till 4pm</div></div><span class="ok sm"><span class="dot"></span> Live</span></div>
<div class="sp-h"><h2>Updates</h2></div>
<div class="tl"><div class="ti"><b>Corneria II playable</b><span class="mu sm">Yesterday · at <span class="cl" onclick="go('cafe')">Bean Theory</span></span><img src="img/table1.svg" alt="" onclick="go('cafe')"></div>
<div class="ti"><b>Ship models imported</b><span class="mu sm">Oct 9</span></div></div></div>{nav("p")}'''

def pcard(name,k,img,upd,when,cafe,n):
    nm,c=P[k]
    return f'''<article class="fc pc" onclick="go('project')"><div class="fm"><img src="img/{img}.svg" alt=""></div><div class="fbd"><b class="fw">{name}</b>
<div class="fh">{av(k,24)}<span class="sm">{nm}</span><span class="mu sm">· {when}</span></div><p class="sm">{upd}</p>
<div class="fa"><span class="mu sm">{I("pin",13)} {cafe}</span><span class="pill">{n} this week</span></div></div></article>'''
S['projects']=f'''{top("Projects",f'<a class="ib" href="#project-new" aria-label="New project">{I("plus",22)}</a>')}<div class="pad pjs">
<div class="hero"><h1>Projects</h1><p class="mu">What people are building</p></div><a class="btn newp" href="#project-new">{I("plus",18)} New project {LOCK}</a>
<div class="chips pchips"><button class="chip on">Nearby</button><button class="chip">Following</button><button class="chip">Mine</button></div>
<div class="pgrid">{pcard("Star Fox 64 mod","MK","sf64","Corneria II playable","Yesterday","Bean Theory",2)}{pcard("Pixel Garden","TS","pixel","New crop sprites","Tue","Grindhouse",1)}{pcard("Bus Stop Zine","JR","sketch","Page 12 inked","Mon","Bean Theory",2)}{pcard("Lantern Lights","AL","table2","Wiring the LEDs","Sun","Lantern Tea",1)}</div></div>{nav("p")}'''
S['project-new']=f'''{top("New project")}<div class="pad form"><button class="cover">{I("image",22)}<span class="sm">Add cover</span></button>
<label>Name</label><input class="in" value="Pixel Garden"><label>Kind</label>{seg(['Code','Game','Art','Other'],'Game','k')}
<label>One line</label><input class="in" value="A tiny pixel-art farming game"></div><div class="cta"><button class="btn" onclick="go('project')">Create</button></div>'''
S['project-update']=f'''{top("Update")}<div class="pad form"><label>Title</label><input class="in" value="Corneria II playable"><label>Notes</label><textarea class="in" rows="4">Boss fight still in progress.</textarea>
<label class="addph">{I("camera",18)} Add image<input type="file" accept="image/*" hidden></label></div><div class="cta"><button class="btn" onclick="go('project')">Post update</button></div>'''
S['project-attach']=f'''{top("Post up")}<div class="pad form"><label>Project</label><div class="field"><span class="ci sm pj">{I("folder",16)}</span><div class="lm"><b>Star Fox 64 mod</b></div></div>
<label>Where</label><div class="chips"><button class="chip on">Bean Theory</button><button class="chip">Grindhouse</button><button class="chip">Lantern Tea</button></div>
<label>When</label>{seg(['Now','Earlier today'],'Now','w')}<label>Until</label>{seg(['1h','2h','3h'],'2h','u')}
<p class="mu xs">Earlier today adds it to the cafe's recent activity.</p></div><div class="cta"><button class="btn" onclick="go('posted')">Post up</button></div>'''

CSS=open('gen/style.css').read()+open('gen/themes.css').read()+open('gen/desktop.css').read()
dpins=pin_live(38,40,'MK','2')+pin_live(58,62,'TS','')+pin_live(30,70,'AL','')+pin_cafe(48,24,'Lantern Tea')+pin_cafe(22,46)+pin_cafe(66,34)+pin_cafe(44,78,'3 this week')+pin_cafe(72,74)
def rl(h,ic,t): return f'<a href="{h}" data-r="{h[1:]}">{I(ic,22)}<span>{t}</span></a>'
DESK=f'''<aside class="rail"><a class="rlogo" href="#home">{I("coffee",22)}</a>{rl("#home","map","Map")}{rl("#quiet-feed","list","Nearby")}{rl("#projects","folder","Projects")}<a class="rpost" href="#post">{I("plus",22)}<span>Post up</span></a><span class="rsp"></span><a href="#index" data-r="index">{I("spark",20)}<span>Mockups</span></a>{av('ME',36)}</aside>
<div class="dmap">{dmapsvg()}{dpins}<span class="you" style="left:47%;top:52%"></span><div class="dsearch">{I("pin",16)} Venice &amp; Mar Vista</div><div class="attr">Map mockup</div></div>'''
exec(open('gen/more.py').read())
exec(open('gen/scenarios.py').read())
exec(open('gen/home.py').read())
exec(open('gen/notes.py').read())
exec(open('gen/menu.py').read())
exec(open('gen/flows.py').read())
JS=open('gen/app.js').read()+open('gen/scen.js').read()+open('gen/ixpage.js').read()
body=''.join(f'<section class="scr{" full" if k in FULL else " dlg" if k in DLG else ""}" id="{k}" data-v="{k}">{v}</section>' for k,v in S.items())
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#ffffff">
<title>PostUp · mockups</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Space+Grotesk:wght@500;700&family=Archivo+Black&display=swap" rel="stylesheet"><style>{CSS}{NOTES_CSS}{MENU_CSS}</style></head>
<body><div class="dev">{DESK}<div class="sb"><b>9:41</b><span class="isl"></span><span class="sbi">●●● ▴ ▮</span></div><div class="ph">{body}</div>{OVS}<span class="mock">Mockup · <span id="stn">Fresh</span></span></div>{NOTES_HTML}{MENU_HTML}<script>{JS}{NOTES_JS}{MENU_JS}</script></body></html>'''
open('index.html','w').write(html)
print('ok',len(S))
