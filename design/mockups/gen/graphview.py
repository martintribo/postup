# One-screen flow graph (Martin, Oct 31 2026 [M1041]): every way into a flow (start branches) on the left, every way out
import model as _MD  # [M1043]
# (outcomes) on the right, screen states as nodes with phone thumbnails and taps as labelled edges. Works for any flow with
# outcomes: flows/graph.html#<flow id>. Laid out in the browser (left to right by distance from an entry); zoom, pan, fit;
# details hide when zoomed out; click a node to open the player at that step; follows the Phase toggle. exec'd by flows.py.
def _gclean(t): return re.sub(r'\s*\[[^\]]+\]','',t or '')
GDATA={}
for f in FLOWS_TOP:
    ps=[]; _ent=_MD.goal_entries(_FL,f['id']); _eof={k:e for e,ks in _ent.items() for k in ks}
    for o in f['outs']:
        g=FBY[o['id']]
        ps.append(dict(id=g['id'],l=_gclean(olab(o)),e=_gclean(o['entry']),ph=o['phase'],r=g['result'] or '',en=_eof.get(g['id'],'main'),pr=g['prog'],
            st=[dict(s=d['site'],h=_gclean(d['how']).replace('tap: ','').replace('entry',''),a=d['act'],t=_ptitle(_site_page(d['site']))+(' + '+parse_site(d['site'])['ov'] if parse_site(d['site'])['ov'] else '')) for d in g['sx']]))
    cov={}
    if _FL[f['id']].get('goals'):  # goal-by-entry coverage [M1043]: can = goal screens reachable by real links from that entry
        _exc={(x.get('entry'),x.get('goal')):_gclean(x.get('reason','')) for x in _FL[f['id']].get('goal_exceptions',[])}
        for e,ks in _ent.items():
            cov[e]={gid:dict(can=bool(_MD.goal_reachable(_SC,_FL,ks,g,_MD.entry_phase(_FL,ks,g,_FL[f['id']]))),ex=_exc.get((e,gid),'')) for gid,g in GOALS_U.get(f['user'],GOALS).items()}
    GDATA[f['id']]=dict(n=f['name'],u=f['user'],ph=f['phase'],p=ps,cov=cov)
GMETA=[dict(id=k,l=g['label'],c=g['color'],ph=g.get('phase'),lk=_gclean(g.get('likely','')),t={u:[dict(id=m['id'],l=m.get('label',m['id'])) for m in GOALS_U[u][k]['ms']] for u in GOALS_U}) for k,g in GOALS.items()]  # per user type [M1042] [M1044]
UMETA=[dict(id=u,l=d.get('label',u),m=d.get('main_flow')) for u,d in USERS_D.items()]  # each user type's main flow [M1044]
_GOPTS=''.join(f'<option value="{f["id"]}">{H.escape(f["name"])}{" · "+str(len(f["outs"]))+" outcomes" if len(f["outs"])>1 else ""}</option>' for f in FLOWS_TOP)
GCSS2='''*{box-sizing:border-box}html,body{margin:0;height:100%;overflow:hidden;font:13px/1.35 Inter,system-ui,sans-serif;color:#232322;background:#f4f3ef}a{color:#0f7a4f}
.gb{position:absolute;left:0;right:0;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:8px 12px;background:rgba(244,243,239,.96);border-bottom:1px solid #e4e2dc}.gb b{font-size:15px}
.gb select{font:13px Inter,sans-serif;padding:5px;border-radius:9px;border:1px solid #d7d5cf;max-width:260px}.gb button{font:600 12px Inter,sans-serif;padding:4px 10px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}
.ub{display:inline-flex;border:1px solid #d7d5cf;border-radius:99px;overflow:hidden}.ub a{padding:4px 12px;font:600 12px Inter,sans-serif;color:#33332f;text-decoration:none}.ub a.on{background:#232322;color:#fff}
#vp{position:absolute;left:0;right:0;bottom:0;top:var(--gbh,48px);overflow:hidden;cursor:grab;touch-action:none}#vp.drag{cursor:grabbing}#cv{position:absolute;left:0;top:0;transform-origin:0 0}
#cv svg{position:absolute;left:0;top:0;overflow:visible}path.e{fill:none;stroke:#9fb7aa;stroke-width:1.6}path.e.bk{stroke:#d9b26b;stroke-dasharray:5 4}
.el{position:absolute;transform:translate(-50%,-50%);font-size:10.5px;color:#3f5d4e;background:rgba(244,243,239,.92);padding:0 4px;border-radius:5px;white-space:nowrap;max-width:150px;overflow:hidden;text-overflow:ellipsis;pointer-events:none}
.nd{position:absolute;width:92px;text-align:center;cursor:pointer;text-decoration:none;color:#232322}.nd img{width:70px;height:152px;object-fit:cover;object-position:top;border:2.5px solid #222;border-radius:11px;background:#fff;display:block;margin:0 auto}
.nd:hover img{border-color:#10a364;box-shadow:0 0 0 3px #bfe3cf}.nt{font-size:10.5px;line-height:1.15;margin-top:3px;font-weight:600}.nk{font:10px ui-monospace,monospace;color:#8a8984;word-break:break-all}
.en{position:absolute;right:100%;top:50px;margin-right:10px;width:150px;display:flex;flex-direction:column;gap:4px}.en a{display:block;font:600 11px Inter,sans-serif;text-align:left;background:#0f7a4f;color:#fff;border-radius:9px;padding:5px 8px;text-decoration:none}
.ou{position:absolute;left:100%;top:30px;margin-left:8px;width:150px;display:flex;flex-direction:column;gap:4px}.ou a{display:block;font:700 11px Inter,sans-serif;text-align:left;background:#ffe9c7;border:1px solid #f1c27a;color:#7a3e00;border-radius:9px;padding:4px 8px;text-decoration:none}
.gs{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;margin-top:3px}.gs span{font:700 9.5px Inter,sans-serif;color:#fff;border-radius:99px;padding:1px 6px;white-space:nowrap}
.ou a.dr{background:#eceae4;border-color:#d7d5cf;color:#55544f}.ou a.gl{background:#dff3e8;border-color:#10a364;color:#0b5e3c}.ou a small{display:block;font-weight:500;font-size:10px;opacity:.85}
path.g{fill:none;stroke-width:3.4;opacity:.85}.dim path.e,.dim .el{opacity:.25}.gf button{border-width:2px}.gf button.on{color:#fff}
#sum{position:absolute;right:10px;bottom:10px;z-index:6;width:330px;max-height:calc(100% - 20px);overflow:auto;background:#fff;border:1px solid #e4e2dc;border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.12);padding:10px 12px;font-size:12px}
#sum table.cg{border-collapse:collapse;width:100%;font-size:11px;margin:2px 0 4px}#sum .cg th,#sum .cg td{border:1px solid #eceae4;padding:3px 4px;text-align:center}#sum .cg td:first-child{text-align:left;color:#3b3a36;max-width:130px}
#sum .cg .ok{background:#dff3e8;color:#0b5e3c;font-weight:700}#sum .cg .gap{background:#fde2e0;color:#b42318;font-weight:700}#sum .cg .na{color:#9a9890}#sum .cg .ex{background:#fff4d6;color:#8a5a00}
#sum h4{margin:8px 0 2px;font-size:12.5px}#sum h4 i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px}#sum p{margin:2px 0;color:#55544f}#sum ul{margin:2px 0 4px;padding-left:16px}#sum .x{float:right;border:0;background:none;cursor:pointer;font-size:14px}#sum.min>*:not(.hd){display:none}
.lo .el,.lo .nk,.lo .gs{display:none}@media(max-width:700px){#sum{width:auto;left:8px;max-height:38%}}.lo2 .nt{display:none}.lg{font-size:11px;color:#6b6b67}.lg i{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin:0 3px 0 8px}
@media(max-width:700px){.gb{gap:5px;padding:6px 8px}.gb .lg,.gb .hd{display:none}}'''
GJS=r'''var D=JSON.parse(document.getElementById("gdata").textContent),UM=JSON.parse(document.getElementById("umeta").textContent),GM=JSON.parse(document.getElementById("gmeta").textContent),GF="all",F,S=1,X=0,Y=0,W=0,HH=0;
function gvis(g){var v=vph();return v===null?true:(g.ph==null||g.ph<=v)}function GB(id){return GM.filter(function(g){return g.id===id})[0]}
function MS(g){return g.t[D[F].u]||[]}
function mlab(mid){var l=mid;GM.forEach(function(g){MS(g).forEach(function(m){if(m.id===mid)l=m.l})});return l}
function vph(){var c=document.documentElement.classList;return c.contains("ph0only")?0:c.contains("ph1only")?1:c.contains("ph2only")?2:null}
function vis(p){var v=vph();return v===null||(p.ph!==null&&p.ph<=v)}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function build(){var id=location.hash.slice(1);if(!D[id])id=(UM.filter(function(u){return D[u.m]})[0]||{}).m||Object.keys(D)[0];F=id;document.getElementById("sel").value=id;
 document.getElementById("ub").innerHTML=UM.filter(function(u){return D[u.m]}).map(function(u){return'<a href="#'+u.m+'" class="'+(D[id].u===u.id?"on":"")+'">'+esc(u.l)+"</a>"}).join("");
 var ps=D[id].p.filter(vis),N={},E={},order=[];
 ps.forEach(function(p){p.st.forEach(function(s,k){if(!N[s.s]){N[s.s]={k:s.s,t:s.t,img:"thumbs/"+p.id+"-"+(k+1)+".webp",go:p.id+".html#"+(k+1),en:[],ou:[],d:1e9};order.push(s.s)}
  var nd=N[s.s];nd.pr=nd.pr||{};Object.keys(p.pr[k]||{}).forEach(function(g){nd.pr[g]=Math.max(nd.pr[g]||0,p.pr[k][g])});
  if(k>0){var a=p.st[k-1].s,ek=a+">"+s.s;if(!E[ek])E[ek]={a:a,b:s.s,h:[],g:[]};if(s.h&&E[ek].h.indexOf(s.h)<0)E[ek].h.push(s.h);var gr=p.r.indexOf("goal:")===0?p.r.slice(5):null;if(gr&&E[ek].g.indexOf(gr)<0)E[ek].g.push(gr)}});
  var f=N[p.st[0].s];if(p.e||!p.st.length)f.en.push({l:p.e||"Start",go:p.id+".html#1"});var z=N[p.st[p.st.length-1].s];z.ou.push({l:p.l,r:p.r,go:p.id+".html#"+p.st.length})});
 var adj={};Object.keys(E).forEach(function(k){var e=E[k];(adj[e.a]=adj[e.a]||[]).push(e.b)});
 var q=[];order.forEach(function(k){if(N[k].en.length){N[k].d=0;q.push(k)}});while(q.length){var a=q.shift();(adj[a]||[]).forEach(function(b){if(N[b].d>N[a].d+1){N[b].d=N[a].d+1;q.push(b)}})}
 var cols={};order.forEach(function(k){var d=N[k].d<1e9?N[k].d:0;(cols[d]=cols[d]||[]).push(k)});
 var CW=250,RH=215,PX=180,PY=20,maxr=0;Object.keys(cols).forEach(function(d){cols[d].forEach(function(k,r){N[k].x=PX+d*CW;N[k].y=PY+r*RH;maxr=Math.max(maxr,r)})});
 W=PX+Object.keys(cols).length*CW+190;HH=PY+(maxr+1)*RH;
 var sv="",h="",lb="";Object.keys(E).forEach(function(k){var e=E[k],a=N[e.a],b=N[e.b],x1=a.x+92,y1=a.y+80,x2=b.x,y2=b.y+80,bk=b.x<=a.x,d;
  if(bk){var top=Math.min(a.y,b.y)-18;d="M"+(a.x+46)+" "+a.y+" C"+(a.x+46)+" "+top+" "+(b.x+46)+" "+top+" "+(b.x+46)+" "+b.y;lb+='<div class="el" style="left:'+((a.x+b.x)/2+46)+"px;top:"+(top+4)+'px">↺ '+esc(e.h.join(" / "))+"</div>"}
  else{var mx=(x1+x2)/2;d="M"+x1+" "+y1+" C"+mx+" "+y1+" "+mx+" "+y2+" "+x2+" "+y2;lb+='<div class="el" style="left:'+mx+"px;top:"+((y1+y2)/2)+'px" title="'+esc(e.h.join(" / "))+'">'+esc(e.h.join(" / "))+"</div>"}
  sv+='<path class="e'+(bk?" bk":"")+'" d="'+d+'" marker-end="url(#ah)"/>';
  e.g.forEach(function(gid,j){var g=GB(gid);if(!g||!gvis(g)||(GF!=="all"&&GF!==gid))return;sv+='<path class="g" style="stroke:'+g.c+'" transform="translate(0,'+(j*3.5-2)+')" d="'+d+'"/>'})});
 order.forEach(function(k){var n=N[k];h+='<div class="nd" style="left:'+n.x+"px;top:"+n.y+'px" data-go="'+n.go+'" title="'+esc(n.k)+'" role="link" tabindex="0"><img loading="lazy" src="'+n.img+'" alt=""><div class="nt">'+esc(n.t)+'</div><div class="nk">'+esc(n.k)+"</div>"+badges(n)+
  (n.en.length?'<div class="en">'+n.en.map(function(x){return'<a href="'+x.go+'">⇢ '+esc(x.l)+"</a>"}).join("")+"</div>":"")+(n.ou.length?'<div class="ou">'+n.ou.map(function(x){var g=x.r.indexOf("goal:")===0?GB(x.r.slice(5)):null;return g?'<a class="gl" href="'+x.go+'" style="border-color:'+g.c+'">✓ '+esc(g.l)+'<small>'+esc(x.l)+'</small></a>':'<a class="dr" href="'+x.go+'">✕ Drop-off: '+esc(x.l)+(x.r?'<small>at '+esc(mlab(x.r.slice(5)))+'</small>':'')+'</a>'}).join("")+"</div>":"")+"</div>"});
 document.getElementById("cv").classList.toggle("dim",GF!=="all");document.getElementById("cv").innerHTML='<svg width="'+W+'" height="'+HH+'"><defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="#7fa392"/></marker></defs>'+sv+"</svg>"+h+lb;
 document.getElementById("wk").href="walk.html#user="+D[id].u;document.getElementById("cnt").textContent=ps.filter(function(p){return p.e}).length+" ways in · "+ps.length+" outcomes · "+order.length+" screen states";document.title="Graph · "+D[id].n+" · PostUp mockups";summary(ps,D[id].cov);legend();fit()}
function badges(n){var h="";GM.forEach(function(g){if(!gvis(g)||(GF!=="all"&&GF!==g.id))return;var p=(n.pr||{})[g.id]||0;if(p>0)h+='<span style="background:'+g.c+'" title="'+esc(MS(g).slice(0,p).map(function(m){return m.l}).join(" → "))+'">'+p+"/"+MS(g).length+" "+esc(g.l)+"</span>"});return h?'<div class="gs">'+h+"</div>":""}
function legend(){document.getElementById("gf").innerHTML='<button class="'+(GF==="all"?"on":"")+'" style="'+(GF==="all"?"background:#232322;color:#fff":"")+'" onclick="setGF(\'all\')">All goals</button>'+GM.filter(gvis).map(function(g){var on=GF===g.id;return'<button class="'+(on?"on":"")+'" style="border-color:'+g.c+";"+(on?"background:"+g.c:"color:"+g.c)+'" onclick="setGF(\''+g.id+'\')">'+esc(g.l)+"</button>"}).join("")}
function setGF(g){GF=g;build()}
function grid(ps,cov){var es=Object.keys(cov||{});if(!es.length)return"";var gs=GM.filter(gvis),lab={};ps.forEach(function(p){if(p.e&&!lab[p.en])lab[p.en]=p.e});
 var h='<table class="cg"><tr><th>Entry</th>'+gs.map(function(g){return'<th style="color:'+g.c+'">'+esc(g.l)+"</th>"}).join("")+"</tr>";
 es.forEach(function(e){if(!ps.some(function(p){return p.en===e}))return;h+='<tr><td>'+esc(lab[e]||e)+"</td>"+gs.map(function(g){var n=ps.filter(function(p){return p.en===e&&p.r==="goal:"+g.id}).length,c=cov[e][g.id];
  return n?'<td class="ok" title="'+n+' path(s) from this entry reach '+esc(g.l)+'">✓'+(n>1?" "+n:"")+"</td>":c.ex?'<td class="ex" title="'+esc(c.ex)+'">exception</td>':c.can?'<td class="gap" title="Reachable by links, but no path: a gap">✕ gap</td>':'<td class="na" title="Not reachable from this entry by any link">n/a</td>'}).join("")+"</tr>"});
 return'<p style="margin-top:6px"><b>Goal by entry</b></p>'+h+"</table>"}
function summary(ps,cov){var h='<div class="hd"><b>Goals on this flow</b><button class="x" onclick="this.closest(\'#sum\').classList.toggle(\'min\')">▾</button></div>'+grid(ps,cov),drops={};
 ps.forEach(function(p){if(p.r.indexOf("drop:")===0){var m=p.r.slice(5);(drops[m]=drops[m]||[]);if(drops[m].indexOf(p.l)<0)drops[m].push(p.l)}});
 GM.forEach(function(g){if(!gvis(g))return;var reach=ps.filter(function(p){return p.r==="goal:"+g.id});var ids=MS(g).map(function(m){return m.id});
  var dd=Object.keys(drops).filter(function(m){return ids.indexOf(m)>=0}).sort(function(a,b){return drops[b].length-drops[a].length});
  h+='<h4><i style="background:'+g.c+'"></i>'+esc(g.l)+": "+reach.length+(reach.length===1?" path reaches it":" paths reach it")+"</h4>"+(reach.length?"<p>"+reach.map(function(p){return esc(p.l)}).join(" · ")+"</p>":'<p style="color:#c0392b">No path reaches it in this phase.</p>')+(g.lk?"<p><i>"+esc(g.lk)+"</i></p>":"")+
   (dd.length?"<p>Drop-offs on this track:</p><ul>"+dd.map(function(m){return"<li>at <b>"+esc(mlab(m))+"</b> ("+(ids.indexOf(m)+1)+"/"+ids.length+"): "+drops[m].map(esc).join(", ")+"</li>"}).join("")+"</ul>":"")});
 var s=document.getElementById("sum"),mn=s.classList.contains("min");s.innerHTML=h;if(mn)s.classList.add("min")}
function ap(){var c=document.getElementById("cv");c.style.transform="translate("+X+"px,"+Y+"px) scale("+S+")";c.classList.toggle("lo",S<.62);c.classList.toggle("lo2",S<.38)}
function fit(){var v=document.getElementById("vp");S=Math.min(1.2,(v.clientWidth-10)/W,(v.clientHeight-10)/HH);if(innerWidth<700)S=Math.max(S,.42);X=Math.max(5,(v.clientWidth-W*S)/2);Y=5;ap()}
function zoom(f,cx,cy){var v=document.getElementById("vp").getBoundingClientRect();cx=cx==null?v.width/2:cx-v.left;cy=cy==null?v.height/2:cy-v.top;var n=Math.max(.15,Math.min(2.5,S*f));X=cx-(cx-X)*n/S;Y=cy-(cy-Y)*n/S;S=n;ap()}
(function(){var v=document.getElementById("vp"),dn=null,mv=0;v.addEventListener("wheel",function(e){e.preventDefault();zoom(e.deltaY<0?1.12:1/1.12,e.clientX,e.clientY)},{passive:false});
 v.addEventListener("pointerdown",function(e){dn=[e.clientX,e.clientY,X,Y];mv=0});addEventListener("pointermove",function(e){if(!dn)return;var dx=e.clientX-dn[0],dy=e.clientY-dn[1];if(Math.abs(dx)+Math.abs(dy)>4){mv=1;v.classList.add("drag")}X=dn[2]+dx;Y=dn[3]+dy;if(mv)ap()});
 addEventListener("pointerup",function(){dn=null;v.classList.remove("drag")});v.addEventListener("click",function(e){if(mv){e.preventDefault();e.stopPropagation();mv=0}},true)})();
document.getElementById("cv").addEventListener("click",function(e){if(e.target.closest("a"))return;var n=e.target.closest(".nd");if(n)location.href=n.dataset.go});
document.getElementById("sel").onchange=function(e){location.hash=e.target.value};addEventListener("hashchange",build);addEventListener("phchange",function(){if(window.D)build()});addEventListener("resize",fit);
document.documentElement.style.setProperty("--gbh",document.querySelector(".gb").offsetHeight+"px");build();'''
_gj=json.dumps(GDATA,ensure_ascii=False).replace('</','<\\/')
open('flows/graph.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flow graph · PostUp mockups</title><style>{PHCSS}{GCSS2}</style></head><body>
<div class="gb"><a href="map.html">← Flow map</a><b>Flow graph</b><a id="wk" href="walk.html" title="Step through the real screens [M1045]">Walk through →</a><span class="ub" id="ub" title="Each user type's main goal-tracked flow (users.toml)"></span><select id="sel">{_GOPTS}</select>{PHBTN}<button onclick="zoom(1/1.25)">−</button><button onclick="zoom(1.25)">+</button><button onclick="fit()">Fit</button><span class="meta" id="cnt"></span>
<span class="lg"><i style="background:#0f7a4f"></i>way in<i style="background:#dff3e8;border:1px solid #10a364"></i>goal reached<i style="background:#eceae4;border:1px solid #d7d5cf"></i>drop-off<i style="background:#d9b26b"></i>goes back</span><span class="gf" id="gf"></span><span class="lg hd">Drag to pan, scroll to zoom; click a screen to open the player at that step. [M1041]</span></div>
<div id="vp"><div id="cv"></div></div><div id="sum"></div><script type="application/json" id="gdata">{_gj}</script><script type="application/json" id="umeta">{json.dumps(UMETA,ensure_ascii=False)}</script><script type="application/json" id="gmeta">{json.dumps(GMETA,ensure_ascii=False)}</script>{PHJS}<script>{GJS}</script></body></html>''')
with open('llms.txt','a') as fh: fh.write('- [Flow graph](flows/graph.html): one-screen graph of a flow, its ways in and its outcomes; opens each user type main flow (users.toml main_flow) [M1041] [M1044]\n')
print('graph view',len(GDATA),'flows')
