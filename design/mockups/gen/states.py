# States view (Martin, Oct 27 2026 [M1031-draft]): flows/states.html — every site state a screen appears in, as scaled live
# mockup thumbnails with plain-words conditions, incoming/outgoing links and flow steps. Generated from the model (SST/EDGES
# built from model/ in sitegraph.py, FLOWS from model/flows); no hand data. exec'd by flows.py after sg_write().
def _short(t): return re.sub(r'^Sheet · ','',t).split(' (')[0]
def _stitle(x): return _short(NOTES[x]['title'] if x in NOTES else NOTES['ov-'+x]['title'] if 'ov-'+x in NOTES else x)
def _words(k):
    s=SST[k]; w=['Signed in' if s['auth']=='in' else 'Signed out','someone live nearby' if s['live']=='live' else 'no one live nearby']
    if s['mode']: w.append(('Live' if s['mode']=='live' else 'Building')+' tab')
    return w
def _slot(k):
    s=SST[k]; return f'{_stitle(s["ov"])} sheet open' if s['ov'] else ''
def _variant(k):
    s=SST[k]; v=M.rendered_id(SC[s['page']],s['auth'],s['live'],s['mode'])
    return '' if v==s['page'] else f'drawn as #{v}'
def _short_state(k):
    s=SST[k]; return _stitle(s['page'])+(f' + {_stitle(s["ov"])}' if s['ov'] else '')+' · '+', '.join(_words(k))
STV={}
for k,s in SST.items():
    STV[k]=dict(ph=ph1(k,'st'),p=s['page'],ov=s['ov'] or '',w=_words(k),slot=_slot(k),var=_variant(k),u=surl_s(k)+'',out=[],inn=[],fl=[])
for k,es in EDGES.items():
    for t,lab,kind in es:
        STV[k]['out'].append([lab or kind,t or '',kind])
        if t: STV[t]['inn'].append([k,lab or kind,kind])
for f in FLOWS:
    for i,d in enumerate(f['sx']): STV[d['site']]['fl'].append([f['id'],i+1,f['name']])
_scr={}
for g,ps in PGROUPS: _scr.setdefault(g,[]).extend(ps)
_scr['Sheets (open in a page slot)']=sorted(OVHOST)
SCREENS=[[g,[[p,_stitle(p),ph1(p),sum(1 for s in SST.values() if s['page']==p or s['ov']==p)] for p in ps]] for g,ps in _scr.items()]
LBL={k:_short_state(k) for k in SST}
STATES_N=len(SST)
STCSS='''.cap{display:none}.grid.big{gap:12px;justify-content:start}.grid.big .card{flex-direction:column;padding:4px;gap:3px}.grid.big .inf{display:none}.grid.big .cap{display:block;font-size:11px;color:#55544f;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 2px}.grid.big .th{border-radius:12px}
.emb .stw{grid-template-columns:1fr}.emb .pick,.emb .top a{display:none}.emb .grid{grid-template-columns:repeat(auto-fill,minmax(360px,1fr))}body{background:#f4f3ef}.stw{display:grid;grid-template-columns:230px 1fr;height:100vh}.pick{overflow:auto;padding:10px 12px;border-right:1px solid #e4e2dc;background:#fff;font-size:12.5px}
.pick h4{margin:10px 0 3px;font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;color:#6b6b67}.pick a{display:flex;justify-content:space-between;padding:2px 6px;border-radius:6px;text-decoration:none;color:#232322}.pick a.on{background:#10a364;color:#fff}.pick a i{font-style:normal;color:#8a8984;font-size:11px}.pick a.on i{color:#e6fff2}
.main{overflow:auto;padding:10px 16px 40px}.top{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:12.5px}.top h1{font-size:18px;margin:0}.top .mu{color:#6b6b67}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:10px;margin-top:10px}
.card{background:#fff;border:1px solid #e4e2dc;border-radius:12px;padding:8px;display:flex;gap:9px;scroll-margin:12px}.card.hl{outline:3px solid #10a364}
.th{flex:none;position:relative;overflow:hidden;border-radius:10px;border:1px solid #ddd;background:#fafafa;cursor:pointer}.th iframe{position:absolute;left:0;top:0;border:0;transform-origin:0 0;pointer-events:none}
.th a{position:absolute;inset:0;z-index:2}.inf{min-width:0;font-size:11.5px;line-height:1.35}.inf b.k{font:600 10.5px ui-monospace,monospace;color:#6b6b67;display:block;margin-bottom:2px;word-break:break-all}
.ch{display:flex;flex-wrap:wrap;gap:3px;margin-bottom:4px}.ch span{padding:1px 6px;border-radius:5px;background:#eef6f1;color:#0f7a4f;font-weight:600}.ch span.sl{background:#efeafc;color:#4a3d8f}.ch span.va{background:#fff3d6;color:#8a5a00}
.inf h5{margin:4px 0 1px;font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:#8a8984}.inf ul{list-style:none;margin:0;padding:0;max-height:96px;overflow:auto}.inf li{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.inf li a{color:#0f7a4f;text-decoration:none}.inf li a:hover{text-decoration:underline}.kd{color:#8a8984}.fl a{display:inline-block;margin:0 4px 0 0;padding:0 5px;border-radius:5px;background:#e9f0fb;color:#24508f;text-decoration:none}
.tg button{font:600 12px Inter,sans-serif;padding:4px 10px;border-radius:8px;border:1px solid #d9d6cf;background:#fff;cursor:pointer}.tg button.on{background:#232322;color:#fff}'''
STJS='''var D=JSON.parse(document.getElementById("stdata").textContent),dev="phone";
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
var HP=new URLSearchParams(location.hash.slice(1)),DET=HP.get("d")!==null?HP.get("d")!=="0":ls("st-det")!=="0",SZ=HP.get("z")||ls("st-z")||"M";ls("st-det",DET?"1":"0");ls("st-z",SZ);
function sethash(){var h=new URLSearchParams(location.hash.slice(1));h.set("d",DET?"1":"0");h.set("z",SZ);history.replaceState(null,"","#"+h.toString().replace(/%40/g,"@"))}
function q(){var h=new URLSearchParams(location.hash.slice(1));return{s:h.get("screen")||"home",st:h.get("st")}}
function e(t){return String(t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function lnk(k,t){var s=D.st[k];return '<a href="#screen='+(s.ov||s.p)+'&st='+encodeURIComponent(k)+'" title="'+e(D.lbl[k])+'">'+e(t||D.lbl[k])+'</a>'}
function pick(){var c=q().s,h="";D.screens.forEach(function(g){h+="<h4>"+e(g[0])+"</h4>";g[1].forEach(function(p){h+='<a data-ph="'+p[2]+'" href="#screen='+p[0]+'" class="'+(p[0]===c?"on":"")+'">'+e(p[1])+(p[2]!=null?'<span class="p1b'+(p[2]>1?' p2':p[2]<1?' p0':'')+'">P'+p[2]+'</span>':"")+"<i>"+p[3]+"</i></a>"})});document.getElementById("pick").innerHTML=h}
function vsel(){try{return localStorage.getItem("pu-ph1")||"0"}catch(e){return"0"}}
addEventListener("phchange",function(){if(window.D&&document.getElementById("grid"))render()});
function render(){var Q=q(),c=Q.s,ks=Object.keys(D.st).filter(function(k){var s=D.st[k];return s.p===c||s.ov===c});
 var VS=D.vers.indexOf(c)>=0&&vsel()==="0";/* All: list each phase version [M1035] */
 var W=dev==="phone"?390:1280,H=dev==="phone"?844:800,sc=dev==="phone"?.3:.16;
 var G=document.getElementById("grid");G.classList.toggle("big",!DET);
 if(!DET){var cols={S:dev==="phone"?5:3,M:dev==="phone"?3:2,L:dev==="phone"?2:1}[SZ],aw=G.clientWidth||innerWidth-40;sc=Math.min((aw-12*(cols-1))/cols/W,(innerHeight-90)/H*(SZ==="L"?1:9));G.style.gridTemplateColumns="repeat("+cols+","+Math.floor(W*sc)+"px)"}else G.style.gridTemplateColumns="";
 var tw=Math.round(W*sc),thh=Math.round(H*sc);
 var own=ks.filter(function(k){return !D.st[k].ov}).length,kid=ks.filter(function(k){return D.st[k].ov&&D.st[k].p===c}).length,asc=ks.length-own-kid;
 document.getElementById("hd").innerHTML="<h1>"+e(D.title[c]||c)+' <code style="font-size:12px">'+c+'</code></h1><span class="mu">'+ks.length+" site states"+(asc?" (as a sheet in a page’s slot)":" ("+own+" plain, "+kid+" with a sheet open in its slot)")+". Click a thumbnail to open that exact state.</span>";
 document.getElementById("grid").innerHTML=(VS?[].concat.apply([],ks.map(function(k){return[k+"|0",k+"|1",k+"|2"]})):ks).map(function(kk){var k=kk.split("|")[0],vp=kk.split("|")[1],s=D.st[k],u=s.u.replace("device=phone","device="+dev)+"";u=u.replace("?","?notes=0&"+(vp?"ph="+vp+"&":""));
  var ch=s.w.map(function(w){return"<span>"+e(w)+"</span>"}).join("")+(s.slot?'<span class="sl">'+e(s.slot)+(s.ov===c?" over "+e(D.title[s.p]||s.p):"")+"</span>":"")+(s.var?'<span class="va">'+e(s.var)+"</span>":"");
  var out=s.out.map(function(o){return"<li>"+e(o[0])+' <span class="kd">→</span> '+(o[1]?lnk(o[1]):"previous screen")+' <span class="kd">'+o[2]+"</span></li>"}).join("")||"<li class=kd>none</li>";
  var inn=s.inn.map(function(o){return"<li>"+lnk(o[0],D.lbl[o[0]])+' <span class="kd">·</span> '+e(o[1])+"</li>"}).join("")||"<li class=kd>none (entry only)</li>";
  var fl=s.fl.map(function(f){return'<a href="'+f[0]+'.html#'+f[1]+'" title="'+e(f[2])+'">'+e(f[0])+" "+f[1]+"</a>"}).join("");
  return'<div data-ph="'+s.ph+'" class="card'+(Q.st===k?" hl":"")+'" id="c-'+k.replace(/[^\\w-]/g,"_")+'"><div class="th" style="width:'+tw+"px;height:"+thh+'px"><iframe loading="lazy" src="'+u+'" style="width:'+W+"px;height:"+H+"px;transform:scale("+sc+')" tabindex="-1"></iframe><a href="'+u.replace("notes=0&","")+'" target="_blank" title="Open this state in the mockup"></a></div><div class="cap" title="'+e(D.lbl[k])+'">'+(vp?'<b>P'+vp+' version</b> · ':'')+e(s.w.join(", ")+(s.slot?" · "+s.slot:"")+(s.var?" · "+s.var:""))+'</div><div class="inf"><b class="k">'+e(k)+(s.ph!=null?' <span class="p1b'+(s.ph>1?' p2':s.ph<1?' p0':'')+'">P'+s.ph+'</span>':"")+'</b><div class="ch">'+ch+"</div><h5>Out ("+s.out.length+")</h5><ul>"+out+"</ul><h5>In ("+s.inn.length+")</h5><ul>"+inn+"</ul>"+(fl?'<h5>Flows</h5><div class="fl">'+fl+"</div>":"")+"</div></div>"}).join("");
 if(!Q.st){document.querySelector(".main").scrollTop=0;scrollTo(0,0)}
 if(Q.st){var el=document.getElementById("c-"+Q.st.replace(/[^\\w-]/g,"_"));if(el)el.scrollIntoView({block:"center"})}}
var EMB=/[?&]embed=1/.test(location.search);if(EMB)document.documentElement.classList.add("emb");
function go(){pick();render();if(EMB&&!go.q){var Q=q();parent.postMessage({st:Q.s,k:Q.st},"*")}go.q=0}
addEventListener("message",function(e){var d=e.data||{};if(d.show){var Q=q();if(Q.s===d.show&&(Q.st||"")===(d.k||""))return;go.q=1;location.hash="screen="+d.show+(d.k?"&st="+encodeURIComponent(d.k):"")}});
document.querySelectorAll(".tg button[data-d]").forEach(function(b){b.onclick=function(){dev=b.dataset.d;document.querySelectorAll(".tg button[data-d]").forEach(function(x){x.classList.toggle("on",x===b)});render()}});
function ui(){var d=document.getElementById("det");d.classList.toggle("on",DET);d.textContent="Details: "+(DET?"on":"off");document.querySelectorAll(".tg button[data-z]").forEach(function(x){x.classList.toggle("on",x.dataset.z===SZ);x.hidden=DET})}
document.getElementById("det").onclick=function(){DET=!DET;ls("st-det",DET?"1":"0");sethash();ui();render()};
document.querySelectorAll(".tg button[data-z]").forEach(function(b){b.onclick=function(){SZ=b.dataset.z;ls("st-z",SZ);sethash();ui();render()}});
addEventListener("resize",function(){if(!DET)render()});ui();
addEventListener("hashchange",go);go();'''
_title={p:_stitle(p) for p in list(PAGES)+list(OVHOST)}
_data=json.dumps(dict(vers=VERS,st=STV,screens=SCREENS,lbl=LBL,title=_title),ensure_ascii=False).replace('</','<\\/')
open('flows/states.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site states by screen · PostUp mockups</title><style>{PCSS}{STCSS}{PHCSS}</style></head><body>
<div class="stw"><nav class="pick" id="pick"></nav><div class="main"><div class="top"><a href="../index.html#index">← Mockups</a><a href="sitemap.html">Site map</a><a href="site.html">Site graph</a><a href="index.html">Flows</a><span class="tg"><button data-d="phone" class="on">Phone</button><button data-d="desktop">Desktop</button></span><span class="tg"><button id="det">Details: on</button><button data-z="S">S</button><button data-z="M">M</button><button data-z="L">L</button></span>{PHBTN}</div>
<div class="top" id="hd" style="margin-top:6px"></div><div class="grid" id="grid"></div></div></div>
<script type="application/json" id="stdata">{_data}</script>{PHJS}<script>{STJS}</script></body></html>''')
with open('llms.txt','a') as fh: fh.write('- [Site states by screen](flows/states.html): every state each screen appears in (conditions, open slots, links in/out, flow steps), from model/\n')
print('states view',len(PAGES)+len(OVHOST),'screens',STATES_N,'states')

EXCSS="""*{box-sizing:border-box}html,body{margin:0;height:100%;font:13px Inter,system-ui,sans-serif;background:#f4f3ef}.xb{height:40px;display:flex;align-items:center;gap:14px;padding:0 14px;background:#fff;border-bottom:1px solid #e4e2dc}
.xb a{color:#0b7a4b;text-decoration:none}.xb b{font-size:15px}.xb .mu{color:#77756f;font-size:12px}.sp2{display:flex;height:calc(100vh - 40px)}.sp2 iframe{border:0;height:100%;display:block}
#L{width:40%;min-width:240px}#R{flex:1;min-width:0}.gut{width:7px;cursor:col-resize;background:#e4e2dc;flex:none}.gut:hover{background:#10a364}
@media(max-width:820px){.sp2{flex-direction:column;height:auto}#L{width:100%!important;height:55vh}#R{height:100vh}.gut{display:none}}"""
EXJS="""var L=document.getElementById("L"),R=document.getElementById("R"),cur={};
function hp(){var h=new URLSearchParams(location.hash.slice(1));return{s:h.get("screen")||"home",k:h.get("st")||""}}
function push(s,k){cur={s:s,k:k||""};history.replaceState(null,"","#screen="+s+(k?"&st="+encodeURIComponent(k):""))}
addEventListener("message",function(e){var d=e.data||{};
 if(d.sm&&e.source===L.contentWindow){if(d.sm===cur.s)return;push(d.sm,"");R.contentWindow.postMessage({show:d.sm},"*")}
 if(d.st&&e.source===R.contentWindow){if(d.st===cur.s&&(d.k||"")===cur.k)return;var ch=d.st!==cur.s;push(d.st,d.k);if(ch)L.contentWindow.postMessage({pick:d.st},"*")}});
var H=hp();push(H.s,H.k);L.src="sitemap.html?embed=1#"+H.s;R.src="states.html?embed=1#screen="+H.s+(H.k?"&st="+encodeURIComponent(H.k):"");
addEventListener("hashchange",function(){var H=hp();push(H.s,H.k);L.contentWindow.postMessage({pick:H.s},"*");R.contentWindow.postMessage({show:H.s,k:H.k},"*")});
var g=document.querySelector(".gut");g.onmousedown=function(e){e.preventDefault();L.style.pointerEvents=R.style.pointerEvents="none";
 function mv(e){L.style.width=Math.max(15,Math.min(80,e.clientX/innerWidth*100))+"%"}function up(){removeEventListener("mousemove",mv);removeEventListener("mouseup",up);L.style.pointerEvents=R.style.pointerEvents=""}
 addEventListener("mousemove",mv);addEventListener("mouseup",up)};"""
open('flows/explore.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site map + states · PostUp mockups</title><style>{EXCSS}{PHCSS}</style></head><body>
<div class="xb"><a href="../index.html#index">← Mockups</a><b>Site map + states</b><span class="mu">Click a screen on the map; its {STATES_N} site states total, per screen on the right. Drag the divider to resize.</span><span style="flex:1"></span>{PHBTN}<a href="sitemap.html">Site map</a><a href="states.html">States list</a><a href="site.html">Site graph</a></div>
<div class="sp2"><iframe id="L" title="Site map"></iframe><div class="gut" title="Drag to resize"></div><iframe id="R" title="States of the selected screen"></iframe></div>{PHJS}<script>{EXJS}</script></body></html>''')
with open('llms.txt','a') as fh: fh.write('- [Site map + states (split view)](flows/explore.html): click a screen on the map, see all its site states\n')
