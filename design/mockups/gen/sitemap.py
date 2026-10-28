# Visual site map (Martin, Oct 25 2026 [M1026]). exec'd by flows.py after sg_write() (needs SST, EDGES, FLOWS, NOTES, surl_s).
# Pages as phone thumbnails (flows/pages/<page>.webp, from gen/pagethumbs.mjs) in tinted, hand-placed area boxes;
# arrows = unique page-to-page links collapsed from the state edges (tap / sign-in only; back, close, tab bar, events dropped).
import json as _j, html as _H
SM_GROUPS=[('Home and browse','#e8f5ee',3,['home','quiet-feed','quiet-feed-b','quiet','home-overlay-alt','cafe']),
 ('Postup and join','#e9f0fb',5,['postup','postup-ask','ask','requested','joined','postup-full','postup-cancelled','postup-ended']),
 ('Post and host','#fdf1e4',4,['post','where','where-search','posted','live','post-edit']),
 ('Projects','#f3ecfb',3,['projects','project','project-new','project-update','project-attach']),
 ('Inbox and social','#fbeef1',4,['inbox','activity','chat','profile']),
 ('Profile and settings','#eef1f4',4,['me','settings','report','reported']),
 ('Share landings','#eaf6f6',3,['invite','invite-ended','invite-project']),
 ('System states','#f4f1e8',4,['empty-area','loading','offline','cafe-gfail'])]
_pp=[p for g in SM_GROUPS for p in g[3]]; _all=sorted({s['page'] for s in SST.values()})
assert sorted(_pp)==_all, set(_pp)^set(_all)
CW,CH,HD,PD,GX,GY=96,196,30,10,44,44
_rows=[SM_GROUPS[:4],SM_GROUPS[4:]]; POS={}; BOX=[]; y=0
for row in _rows:
    x=0; rh=0
    for name,tint,cols,ps in row:
        nr=-(-len(ps)//cols); w=cols*CW+2*PD; h=HD+nr*CH+PD
        BOX.append(dict(n=name,c=tint,x=x,y=y,w=w,h=h))
        for i,p in enumerate(ps): POS[p]=(x+PD+(i%cols)*CW, y+HD+(i//cols)*CH)
        x+=w+GX; rh=max(rh,h)
    y+=rh+GY
WW=max(b['x']+b['w'] for b in BOX); WH=y-GY
TABL={'Home','Nearby','Projects','Inbox','Post up','Map','S',''}
L={}; DROP={'back':0,'close':0,'tab bar':0,'event':0,'condition':0,'mode':0}
for s,es in EDGES.items():
    a=SST[s]['page']
    for e in es:
        t,lab,k=e[0],e[1],e[2]
        if t not in SST: continue
        b=SST[t]['page']
        if a==b: continue
        if k in('tap','sign-in','sheet'):
            if lab in TABL: DROP['tab bar']+=1; continue
            L.setdefault((a,b),set()).add(lab or k)
        else: DROP[{'cond':'condition'}.get(k,k)]=DROP.get({'cond':'condition'}.get(k,k),0)+1
def _title(p):
    s=NOTES[p]['title'] if p in NOTES else p
    return s
SHEETS={}
for k,s in SST.items():
    if s['ov']: SHEETS.setdefault(s['page'],set()).add(s['ov'])
FUSE={}
for f in FLOWS:
    for i,d in enumerate(f['sx']):
        p=d['site'].split('@')[0].split('+')[0]
        FUSE.setdefault(p,[]).append([f['id'],f['name'],i])
_pick={}
_rk=lambda k:(0 if '@in.live' in k else 1 if '@in.' in k else 2)+(5 if '+' in k else 0)+(1 if k.endswith('.building') else 0)
for k,s in SST.items():
    if s['page'] not in _pick or _rk(k)<_rk(_pick[s['page']]): _pick[s['page']]=k
DATA=dict(pos=POS,box=BOX,W=WW,H=WH,cw=CW,ch=CH,
  pages={p:dict(t=_title(p),s=re.split(r' — ',_title(p))[0].replace(' (/)',''),g=g[0],sh=sorted(SHEETS.get(p,())),fl=FUSE.get(p,[]),th=_pick[p],
    st=[[k,('signed in' if SST[k]['auth']=='in' else 'signed out')+' · '+('live' if SST[k]['live']=='live' else 'no one live')+(' · '+SST[k]['mode'] if SST[k]['mode'] else '')+(' · sheet '+SST[k]['ov'] if SST[k]['ov'] else ''),surl_s(k)] for k in sorted((k for k in SST if SST[k]['page']==p),key=lambda k:(bool(SST[k]['ov']),SST[k]['auth']!='in',SST[k]['live']!='live',k))]) for g in SM_GROUPS for p in g[3]},
  links=[[a,b,[x[:38]+('…' if len(x)>38 else '') for x in sorted(v)[:3]]] for (a,b),v in sorted(L.items())])
_drop=', '.join(f'{v} {k}' for k,v in DROP.items() if v)
_nstate=len(SST); _nedge=sum(len(v) for v in EDGES.values())
SMHTML=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site map · PostUp mockups</title>
<style>*{{box-sizing:border-box}}body{{margin:0;font:13px/1.35 Inter,system-ui,sans-serif;color:#232322;background:#f6f5f1;overflow:hidden;height:100vh}}
.bar{{position:fixed;top:0;left:0;right:0;height:48px;display:flex;align-items:center;gap:14px;padding:0 16px;background:#fff;border-bottom:1px solid #e4e2dc;z-index:5}}
.bar a{{color:#0b7a4b;text-decoration:none}}.bar b{{font-size:15px}}.bar .mu{{color:#77756f;font-size:12px}}.sp{{flex:1}}
.zb{{display:flex;gap:4px}}.zb button{{font:inherit;border:1px solid #d8d6cf;background:#fff;border-radius:8px;padding:4px 10px;cursor:pointer}}
#vp{{position:fixed;top:48px;left:0;right:0;bottom:0;cursor:grab}}#vp.drag{{cursor:grabbing}}#w{{position:absolute;left:0;top:0;transform-origin:0 0}}
.box{{position:absolute;border-radius:16px;border:1px solid rgba(0,0,0,.06)}}.box h3{{margin:0;padding:8px 12px 0;font-size:13px;letter-spacing:.02em;color:#3d3b36}}
.pg{{position:absolute;width:{CW}px;height:{CH}px;padding:4px 6px;cursor:pointer;border-radius:10px}}.pg:hover{{background:rgba(255,255,255,.6)}}
.pg .ph{{width:66px;height:143px;margin:0 auto;border:3px solid #222;border-radius:12px;overflow:hidden;background:#fff;position:relative}}.pg img{{width:100%;display:block}}
.pg .t{{font-size:11px;line-height:1.2;font-weight:600;text-align:center;margin-top:4px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.pg .sh{{position:absolute;top:2px;right:4px;background:#232322;color:#fff;border-radius:999px;font-size:9.5px;padding:1px 6px;font-weight:600}}
.pg.sel{{background:#fff;box-shadow:0 0 0 2px #10a364;z-index:3}}.pg{{transform-origin:50% 40%}}.pg.nb{{z-index:2;background:rgba(255,255,255,.85)}}.box{{transition:opacity .5s}}#w.foc .box{{opacity:.18}}
svg{{position:absolute;left:0;top:0;overflow:visible;pointer-events:none}}path.l{{fill:none;stroke:#8d8a82;stroke-width:1;opacity:.16}}
path.l.out{{stroke:#10a364;opacity:.95;stroke-width:2}}path.l.in{{stroke:#3a6fd8;opacity:.95;stroke-width:2}}path.l.off{{opacity:.06}}
#pn{{position:fixed;top:48px;right:0;bottom:0;width:360px;background:#fff;border-left:1px solid #e4e2dc;overflow:auto;padding:16px;z-index:4;transform:translateX(100%);transition:transform .15s}}#pn.on{{transform:none}}
#pn h2{{margin:0 0 2px;font-size:17px}}#pn h4{{margin:14px 0 6px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#77756f}}
.chip{{display:inline-block;margin:0 4px 4px 0;padding:3px 8px;border:1px solid #d8d6cf;border-radius:999px;font-size:11.5px;color:#232322;text-decoration:none}}.chip:hover{{border-color:#10a364}}
.lk{{display:block;padding:4px 0;color:#232322;text-decoration:none;cursor:pointer;border-bottom:1px solid #f0efea}}.lk i{{font-style:normal;color:#77756f;font-size:11.5px}}.lk:hover b{{color:#0b7a4b}}
.x{{position:absolute;top:10px;right:12px;border:0;background:none;font-size:20px;cursor:pointer}}.lg{{font-size:11.5px;color:#77756f}}.sw{{display:inline-block;width:18px;height:3px;vertical-align:middle;margin:0 4px 0 8px}}
</style></head><body>
<div class="bar"><a href="index.html">← All flows</a><a href="site.html">Site graph (tables)</a><a href="states.html">States by screen</a><b>Site map</b><span class="mu">{len(_pp)} pages · {len(L)} page-to-page links (from {_nedge} edges over {_nstate} states) · sheets as badges · click a page</span><span class="sp"></span>
<span class="lg"><span class="sw" style="background:#10a364"></span>goes to<span class="sw" style="background:#3a6fd8"></span>comes from</span>
<div class="zb"><button onclick="Z(1.2)">+</button><button onclick="Z(1/1.2)">−</button><button onclick="fit()">Fit</button></div></div>
<div id="vp"><div id="w"></div></div>
<div id="pn"><button class="x" onclick="sel(null)" aria-label="Close">×</button><div id="pc"></div></div>
<script>var D={_j.dumps(DATA)};var DROP={_j.dumps(_drop)};
var w=document.getElementById('w'),vp=document.getElementById('vp'),s=1,tx=0,ty=0,cur=null;w.style.width=D.W+'px';w.style.height=D.H+'px';
function esc(t){{return String(t).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
var h='';D.box.forEach(function(b){{h+='<div class="box" style="left:'+b.x+'px;top:'+b.y+'px;width:'+b.w+'px;height:'+b.h+'px;background:'+b.c+'"><h3>'+esc(b.n)+'</h3></div>'}});
var sv='<svg width="'+D.W+'" height="'+D.H+'"><defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L8 4L0 8z" fill="#8d8a82"/></marker></defs>';
function c(p){{var q=D.pos[p];return[q[0]+D.cw/2,q[1]+80]}}
D.links.forEach(function(l,i){{var a=c(l[0]),b=c(l[1]),mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],k=.18;
 sv+='<path class="l" data-a="'+l[0]+'" data-b="'+l[1]+'" marker-end="url(#ah)" d="M'+a[0]+' '+a[1]+' Q'+(mx-dy*k)+' '+(my+dx*k)+' '+b[0]+' '+b[1]+'"/>'}});
h+=sv+'</svg>';
Object.keys(D.pos).forEach(function(p){{var q=D.pos[p],P=D.pages[p];h+='<div class="pg" data-p="'+p+'" style="left:'+q[0]+'px;top:'+q[1]+'px" title="'+esc(P.t)+' (#'+p+')"><div class="ph"><img loading="lazy" src="pages/'+p+'.webp" alt=""></div>'+(P.sh.length?'<span class="sh" title="Sheets: '+esc(P.sh.join(', '))+'">◱ '+P.sh.length+'</span>':'')+'<div class="t">'+esc(P.s)+'</div></div>'}});
w.innerHTML=h;
function ap(){{w.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')'}}
function Z(f,cx,cy){{cx=cx==null?vp.clientWidth/2:cx;cy=cy==null?vp.clientHeight/2:cy;var ns=Math.max(.2,Math.min(4,s*f));tx=cx-(cx-tx)*ns/s;ty=cy-(cy-ty)*ns/s;s=ns;ap()}}
vp.addEventListener('wheel',function(e){{e.preventDefault();var r=vp.getBoundingClientRect();Z(Math.exp(-e.deltaY*.0015),e.clientX-r.left,e.clientY-r.top)}},{{passive:false}});
var dr=null,mv=0;vp.addEventListener('mousedown',function(e){{dr=[e.clientX-tx,e.clientY-ty];mv=0;vp.classList.add('drag')}});
addEventListener('mousemove',function(e){{if(!dr)return;mv++;tx=e.clientX-dr[0];ty=e.clientY-dr[1];ap()}});addEventListener('mouseup',function(){{dr=null;vp.classList.remove('drag')}});
vp.addEventListener('click',function(e){{if(mv>3)return;var g=e.target.closest('.pg');sel(g?g.dataset.p:null)}});addEventListener('keydown',function(e){{if(e.key==='Escape')sel(null)}});
function row(p,labs){{return '<a class="lk" onclick="sel(\\''+p+'\\')"><b>'+esc(D.pages[p].t)+'</b> <i>#'+p+(labs?' · '+esc(labs.join(' / ')):'')+'</i></a>'}}
function sel0(p){{cur=p;location.replace('#'+(p||''));document.getElementById('pn').classList.toggle('on',!!p);
 document.querySelectorAll('.pg').forEach(function(g){{g.classList.toggle('sel',g.dataset.p===p);g.classList.toggle('nb',!!p&&g.dataset.p!==p&&D.links.some(function(l){{return(l[0]===p&&l[1]===g.dataset.p)||(l[1]===p&&l[0]===g.dataset.p)}}));g.classList.toggle('dim',!!p&&g.dataset.p!==p&&!D.links.some(function(l){{return(l[0]===p&&l[1]===g.dataset.p)||(l[1]===p&&l[0]===g.dataset.p)}}))}});
 document.querySelectorAll('path.l').forEach(function(l){{var o=p&&l.dataset.a===p,i=p&&l.dataset.b===p;l.classList.toggle('out',!!o);l.classList.toggle('in',!!i);l.classList.toggle('off',!!p&&!o&&!i)}});
 if(!p)return;var P=D.pages[p],o=D.links.filter(function(l){{return l[0]===p}}),n=D.links.filter(function(l){{return l[1]===p}});
 var x='<h2>'+esc(P.t)+'</h2><div class="lg">#'+p+' · '+esc(P.g)+'</div>';
 x+='<h4>States ('+P.st.length+') · open the mockup</h4>'+P.st.map(function(t){{return '<a class="chip" target="_blank" href="'+t[2]+'">'+esc(t[1])+'</a>'}}).join('');
 if(P.sh.length)x+='<h4>Sheets on this page</h4>'+P.sh.map(function(t){{return '<span class="chip">◱ '+esc(t)+'</span>'}}).join('');
 x+='<h4>Goes to ('+o.length+')</h4>'+(o.map(function(l){{return row(l[1],l[2])}}).join('')||'<div class="lg">No page links out besides back, close and the tab bar.</div>');
 x+='<h4>Comes from ('+n.length+')</h4>'+(n.map(function(l){{return row(l[0],l[2])}}).join('')||'<div class="lg">Only reached by a link from outside, an event, or the tab bar.</div>');
 x+='<h4>Flows that use it ('+P.fl.length+')</h4>'+(P.fl.map(function(f){{return '<a class="lk" href="'+f[0]+'.html#'+f[2]+'"><b>'+esc(f[1])+'</b> <i>step '+(f[2]+1)+'</i></a>'}}).join('')||'<div class="lg">No flow passes through this page yet.</div>');
 x+='<h4>Not drawn</h4><div class="lg">Links left off the map: '+esc(DROP)+'. See the Site graph tables for every edge.</div>';
 document.getElementById('pc').innerHTML=x}}

/* Focus layout (Martin, Oct 25 2026: connected pages move next to the one you click) [M1027]: the clicked page moves to the centre, pages it links to go right, pages linking to it go left,
   pages linked both ways go above/below; the rest fade in place. Nodes, arrows and the view tween together (rAF, 500ms). */
var NP={{}},OP={{}};Object.keys(D.pos).forEach(function(p){{NP[p]=D.pos[p].slice();OP[p]=[1,1]}});
var EL={{}};document.querySelectorAll('.pg').forEach(function(g){{EL[g.dataset.p]=g}});var PL=[].slice.call(document.querySelectorAll('path.l'));
function ctr(p){{var q=NP[p];return[q[0]+D.cw/2,q[1]+80]}}
function draw(){{Object.keys(NP).forEach(function(p){{var g=EL[p],q=NP[p],o=OP[p];g.style.left=q[0]+'px';g.style.top=q[1]+'px';g.style.opacity=o[0];g.style.transform='scale('+o[1]+')'}});
 PL.forEach(function(l){{var a=ctr(l.dataset.a),b=ctr(l.dataset.b),mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1],k=.18;l.setAttribute('d','M'+a[0]+' '+a[1]+' Q'+(mx-dy*k)+' '+(my+dx*k)+' '+b[0]+' '+b[1])}});ap()}}
function target(p){{var T={{}},O={{}};Object.keys(D.pos).forEach(function(q){{T[q]=D.pos[q].slice();O[q]=[p?.15:1,p?.8:1]}});if(!p)return[T,O,null];
 var out={{}},inn={{}};D.links.forEach(function(l){{if(l[0]===p)out[l[1]]=1;if(l[1]===p)inn[l[0]]=1}});
 var both=Object.keys(out).filter(function(q){{return inn[q]}}),R=Object.keys(out).filter(function(q){{return!inn[q]}}),L=Object.keys(inn).filter(function(q){{return!out[q]}});
 var cx=D.W/2-D.cw/2,cy=D.H/2-D.ch/2,PR=4,GXc=D.cw*1.2,GYc=D.ch*1.02,mr=Math.min(PR,Math.max(R.length,L.length,1));
 function col(list,dir){{list.forEach(function(q,i){{var c=Math.floor(i/PR),n=Math.min(PR,list.length-c*PR),r=i%PR;T[q]=[cx+dir*(1.7+c)*GXc+dir*Math.abs(r-(n-1)/2)*-14,cy+(r-(n-1)/2)*GYc]}})}}
 col(R,1);col(L,-1);var top=both.filter(function(_,i){{return i%2===0}}),bot=both.filter(function(_,i){{return i%2}});
 [[top,-1],[bot,1]].forEach(function(z){{z[0].forEach(function(q,i){{T[q]=[cx+(i-(z[0].length-1)/2)*GXc,cy+z[1]*(mr/2+.6)*GYc]}})}});
 T[p]=[cx,cy];var cl=[p].concat(R,L,both);cl.forEach(function(q){{O[q]=[1,1]}});
 var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;cl.forEach(function(q){{x0=Math.min(x0,T[q][0]);y0=Math.min(y0,T[q][1]);x1=Math.max(x1,T[q][0]+D.cw);y1=Math.max(y1,T[q][1]+D.ch)}});return[T,O,[x0,y0,x1,y1]]}}
function view(bb){{var W=vp.clientWidth-(cur?360:0),H=vp.clientHeight;if(!bb)bb=[0,0,D.W,D.H];var bw=bb[2]-bb[0],bh=bb[3]-bb[1],ns=Math.min((W-60)/bw,(H-60)/bh,cur?1.3:1.6);return[ns,(W-bw*ns)/2-bb[0]*ns,(H-bh*ns)/2-bb[1]*ns]}}
var anim=0;function layout(p){{var tg=target(p),v=view(tg[2]),S0={{}},Q0={{}},s0=s,tx0=tx,ty0=ty,t0=performance.now(),id=++anim;
 Object.keys(NP).forEach(function(q){{S0[q]=NP[q].slice();Q0[q]=OP[q].slice()}});document.getElementById('w').classList.toggle('foc',!!p);
 (function step(now){{if(id!==anim)return;var u=Math.min(1,(now-t0)/500),e=u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;
  Object.keys(NP).forEach(function(q){{for(var j=0;j<2;j++){{NP[q][j]=S0[q][j]+(tg[0][q][j]-S0[q][j])*e;OP[q][j]=Q0[q][j]+(tg[1][q][j]-Q0[q][j])*e}}}});
  s=s0+(v[0]-s0)*e;tx=tx0+(v[1]-tx0)*e;ty=ty0+(v[2]-ty0)*e;draw();if(u<1)requestAnimationFrame(step)}})(performance.now())}}
function sel(p){{sel0(p);layout(p)}}
function fit(){{var v=view(target(cur)[2]);s=v[0];tx=v[1];ty=v[2];ap()}}
addEventListener('resize',fit);draw();fit();var hp=location.hash.slice(1);if(hp&&D.pages[hp])sel(hp)
</script></body></html>'''
open('flows/sitemap.html','w').write(SMHTML)
print('sitemap',len(_pp),'pages',len(L),'links')
