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
    STV[k]=dict(p=s['page'],ov=s['ov'] or '',w=_words(k),slot=_slot(k),var=_variant(k),u=surl_s(k)+'',out=[],inn=[],fl=[])
for k,es in EDGES.items():
    for t,lab,kind in es:
        STV[k]['out'].append([lab or kind,t or '',kind])
        if t: STV[t]['inn'].append([k,lab or kind,kind])
for f in FLOWS:
    for i,d in enumerate(f['sx']): STV[d['site']]['fl'].append([f['id'],i+1,f['name']])
_scr={}
for g,ps in PGROUPS: _scr.setdefault(g,[]).extend(ps)
_scr['Sheets (open in a page slot)']=sorted(OVHOST)
SCREENS=[[g,[[p,_stitle(p),sum(1 for s in SST.values() if s['page']==p or s['ov']==p)] for p in ps]] for g,ps in _scr.items()]
LBL={k:_short_state(k) for k in SST}
STATES_N=len(SST)
STCSS='''body{background:#f4f3ef}.stw{display:grid;grid-template-columns:230px 1fr;height:100vh}.pick{overflow:auto;padding:10px 12px;border-right:1px solid #e4e2dc;background:#fff;font-size:12.5px}
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
function q(){var h=new URLSearchParams(location.hash.slice(1));return{s:h.get("screen")||"home",st:h.get("st")}}
function e(t){return String(t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function lnk(k,t){var s=D.st[k];return '<a href="#screen='+(s.ov||s.p)+'&st='+encodeURIComponent(k)+'" title="'+e(D.lbl[k])+'">'+e(t||D.lbl[k])+'</a>'}
function pick(){var c=q().s,h="";D.screens.forEach(function(g){h+="<h4>"+e(g[0])+"</h4>";g[1].forEach(function(p){h+='<a href="#screen='+p[0]+'" class="'+(p[0]===c?"on":"")+'">'+e(p[1])+"<i>"+p[2]+"</i></a>"})});document.getElementById("pick").innerHTML=h}
function render(){var Q=q(),c=Q.s,ks=Object.keys(D.st).filter(function(k){var s=D.st[k];return s.p===c||s.ov===c});
 var W=dev==="phone"?390:1280,H=dev==="phone"?844:800,sc=dev==="phone"?.3:.16,tw=Math.round(W*sc),thh=Math.round(H*sc);
 var own=ks.filter(function(k){return !D.st[k].ov}).length,kid=ks.filter(function(k){return D.st[k].ov&&D.st[k].p===c}).length,asc=ks.length-own-kid;
 document.getElementById("hd").innerHTML="<h1>"+e(D.title[c]||c)+' <code style="font-size:12px">'+c+'</code></h1><span class="mu">'+ks.length+" site states"+(asc?" (as a sheet in a page’s slot)":" ("+own+" plain, "+kid+" with a sheet open in its slot)")+". Click a thumbnail to open that exact state.</span>";
 document.getElementById("grid").innerHTML=ks.map(function(k){var s=D.st[k],u=s.u.replace("device=phone","device="+dev)+"";u=u.replace("?","?notes=0&");
  var ch=s.w.map(function(w){return"<span>"+e(w)+"</span>"}).join("")+(s.slot?'<span class="sl">'+e(s.slot)+(s.ov===c?" over "+e(D.title[s.p]||s.p):"")+"</span>":"")+(s.var?'<span class="va">'+e(s.var)+"</span>":"");
  var out=s.out.map(function(o){return"<li>"+e(o[0])+' <span class="kd">→</span> '+(o[1]?lnk(o[1]):"previous screen")+' <span class="kd">'+o[2]+"</span></li>"}).join("")||"<li class=kd>none</li>";
  var inn=s.inn.map(function(o){return"<li>"+lnk(o[0],D.lbl[o[0]])+' <span class="kd">·</span> '+e(o[1])+"</li>"}).join("")||"<li class=kd>none (entry only)</li>";
  var fl=s.fl.map(function(f){return'<a href="'+f[0]+'.html#'+f[1]+'" title="'+e(f[2])+'">'+e(f[0])+" "+f[1]+"</a>"}).join("");
  return'<div class="card'+(Q.st===k?" hl":"")+'" id="c-'+k.replace(/[^\\w-]/g,"_")+'"><div class="th" style="width:'+tw+"px;height:"+thh+'px"><iframe loading="lazy" src="'+u+'" style="width:'+W+"px;height:"+H+"px;transform:scale("+sc+')" tabindex="-1"></iframe><a href="'+u.replace("notes=0&","")+'" target="_blank" title="Open this state in the mockup"></a></div><div class="inf"><b class="k">'+e(k)+'</b><div class="ch">'+ch+"</div><h5>Out ("+s.out.length+")</h5><ul>"+out+"</ul><h5>In ("+s.inn.length+")</h5><ul>"+inn+"</ul>"+(fl?'<h5>Flows</h5><div class="fl">'+fl+"</div>":"")+"</div></div>"}).join("");
 if(Q.st){var el=document.getElementById("c-"+Q.st.replace(/[^\\w-]/g,"_"));if(el)el.scrollIntoView({block:"center"})}}
function go(){pick();render()}
document.querySelectorAll(".tg button").forEach(function(b){b.onclick=function(){dev=b.dataset.d;document.querySelectorAll(".tg button").forEach(function(x){x.classList.toggle("on",x===b)});render()}});
addEventListener("hashchange",go);go();'''
_title={p:_stitle(p) for p in list(PAGES)+list(OVHOST)}
_data=json.dumps(dict(st=STV,screens=SCREENS,lbl=LBL,title=_title),ensure_ascii=False).replace('</','<\\/')
open('flows/states.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site states by screen · PostUp mockups</title><style>{PCSS}{STCSS}</style></head><body>
<div class="stw"><nav class="pick" id="pick"></nav><div class="main"><div class="top"><a href="../index.html#index">← Mockups</a><a href="sitemap.html">Site map</a><a href="site.html">Site graph</a><a href="index.html">Flows</a><span class="tg"><button data-d="phone" class="on">Phone</button><button data-d="desktop">Desktop</button></span></div>
<div class="top" id="hd" style="margin-top:6px"></div><div class="grid" id="grid"></div></div></div>
<script type="application/json" id="stdata">{_data}</script><script>{STJS}</script></body></html>''')
with open('llms.txt','a') as fh: fh.write('- [Site states by screen](flows/states.html): every state each screen appears in (conditions, open slots, links in/out, flow steps), from model/\n')
print('states view',len(PAGES)+len(OVHOST),'screens',STATES_N,'states')
