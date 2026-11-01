# flows/walk.html page [M1045]. exec'd by walk.py (needs WALK, _wmeta, PHJS, json, H).
WCSS=r'''*{box-sizing:border-box}html,body{margin:0;height:100%}body{font:13px/1.4 Inter,system-ui,sans-serif;color:#232322;background:#f4f3ef;overflow:hidden}
a{color:#0f7a4f}button{font:inherit;color:inherit}
.tb{height:54px;display:flex;align-items:center;gap:10px;padding:0 14px;background:#fff;border-bottom:1px solid #e4e2dc;position:relative;z-index:4}
.tb .bk{text-decoration:none;font-weight:600;font-size:12.5px;white-space:nowrap}.tb h1{font-size:15px;margin:0 6px 0 0;white-space:nowrap}
.seg{display:inline-flex;background:#eeece6;border-radius:99px;padding:3px;gap:2px}.seg button{border:0;background:none;padding:5px 12px;border-radius:99px;font-weight:600;font-size:12px;cursor:pointer;color:#55544f;white-space:nowrap}
.seg button.on{background:#fff;color:#232322;box-shadow:0 1px 3px rgba(0,0,0,.12)}.seg button:disabled{opacity:.4;cursor:default}
select{font:600 12px Inter,sans-serif;padding:6px 28px 6px 10px;border-radius:99px;border:1px solid #d7d5cf;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%2355544f' fill='none' stroke-width='1.5'/%3E%3C/svg%3E") no-repeat right 10px center;appearance:none;max-width:230px}
.sp{flex:1}.btn{border:1px solid #d7d5cf;background:#fff;border-radius:99px;padding:6px 12px;font-weight:600;font-size:12px;cursor:pointer;white-space:nowrap;display:inline-flex;gap:6px;align-items:center}
.btn:hover{border-color:#10a364}.btn.pri{background:#10a364;border-color:#10a364;color:#fff}.btn:disabled{opacity:.4;cursor:default}
.lbl{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8a8984}
.main{position:absolute;top:54px;left:0;right:380px;bottom:0;display:flex;gap:22px;align-items:stretch;justify-content:center;padding:18px 22px 14px;overflow:hidden}
.stage{display:flex;flex-direction:column;align-items:center;gap:10px;min-width:0}
.phone{position:relative;flex:none;border-radius:46px;background:#1d1d1f;padding:11px;box-shadow:0 20px 50px rgba(0,0,0,.18),0 2px 6px rgba(0,0,0,.12)}
.phone .scr{width:390px;height:844px;border-radius:36px;overflow:hidden;background:#fff;position:relative;transform-origin:0 0}
.phone iframe{border:0;width:390px;height:844px;display:block;background:#fff}.phone .ld{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none;transition:opacity .15s}.phone.loading .ld{opacity:.55}
.ctl{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center}.ctl .pos{font-weight:600;color:#55544f;min-width:90px;text-align:center;font-size:12px}
.nx{width:330px;flex:none;display:flex;flex-direction:column;gap:10px;overflow:auto;padding:2px 2px 20px}
.cur{background:#fff;border:1px solid #e4e2dc;border-radius:16px;padding:12px 14px}.cur h2{font-size:17px;margin:2px 0 6px;letter-spacing:-.01em}
.chips{display:flex;flex-wrap:wrap;gap:5px}.chip{font-size:11px;font-weight:600;border-radius:99px;padding:2px 8px;background:#eeece6;color:#55544f;white-space:nowrap}
.chip.in{background:#dff3e8;color:#0b5e3c}.chip.lv{background:#e7f0ff;color:#1d4ed8}
.ch{display:block;width:100%;text-align:left;background:#fff;border:1px solid #e4e2dc;border-radius:14px;padding:10px 12px 10px 42px;cursor:pointer;position:relative;transition:border-color .12s,box-shadow .12s,transform .06s}
.ch:hover,.ch.hot{border-color:#10a364;box-shadow:0 0 0 3px #d5efe1}.ch:active{transform:scale(.99)}
.ch .n{position:absolute;left:11px;top:10px;width:22px;height:22px;border-radius:50%;background:#10a364;color:#fff;font:700 11.5px/22px Inter,sans-serif;text-align:center}
.ch.off .n{background:#b9b7b0}.ch b{font-size:13.5px;display:block}.ch .to{color:#77756f;font-size:11.5px;margin-top:1px}.ch .tg{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px}
.tg span{font-size:10.5px;font-weight:700;border-radius:99px;padding:1px 7px;white-space:nowrap}.tg .gl{color:#fff}.tg .dr{background:#eceae4;color:#55544f}.tg .cl{background:#fff;border:1.5px solid}
.ch .vr{margin-top:7px;display:flex;flex-direction:column;gap:4px}.ch .vr button{all:unset;cursor:pointer;font-size:11.5px;color:#7a3e00;background:#fff4e0;border:1px solid #f1c27a;border-radius:9px;padding:4px 8px}
.ch .vr button:hover{background:#ffe9c7}.ch.bkc{padding-top:8px;padding-bottom:8px}.ch .ofs{font-size:10.5px;color:#b45309;font-weight:600;margin-top:4px}
.dead{background:#fde2e0;border:1px solid #f4b4ad;color:#8f1d14;border-radius:14px;padding:10px 12px;font-weight:600}
.gp{font-size:11.5px;color:#77756f}
.pn{position:absolute;top:54px;right:0;width:380px;bottom:0;background:#fff;border-left:1px solid #e4e2dc;display:flex;flex-direction:column}
.pn .hd{display:none}.pn .bd{overflow:auto;padding:14px 16px 30px;flex:1}.sec{margin-bottom:18px}.sec>.lbl{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.gl2{display:flex;flex-direction:column;gap:8px}.go{border:1px solid #e4e2dc;border-radius:13px;padding:9px 11px;position:relative}
.go .t{display:flex;align-items:center;gap:7px;font-weight:700;font-size:13px}.go .t i{width:10px;height:10px;border-radius:50%;flex:none}.go .st{margin-left:auto;font-size:11px;font-weight:700;border-radius:99px;padding:2px 8px}
.go.rc .st{background:#dff3e8;color:#0b5e3c}.go.ok .st{background:#e7f0ff;color:#1d4ed8}.go.no{opacity:.7}.go.no .st{background:#eceae4;color:#77756f}.go.rc{border-color:#10a364;background:#f6fcf8}
.ms{display:flex;gap:3px;margin:7px 0 4px}.ms span{flex:1;height:5px;border-radius:3px;background:#eceae4}.go .ml{font-size:11px;color:#77756f}.go .jb{margin-top:6px}
.trail{list-style:none;margin:0;padding:0;position:relative}.trail li{position:relative;padding:0 0 10px 26px;cursor:pointer}.trail li:before{content:"";position:absolute;left:8px;top:16px;bottom:-2px;width:2px;background:#e4e2dc}.trail li:last-child:before{display:none}
.trail li i{position:absolute;left:1px;top:2px;width:16px;height:16px;border-radius:50%;background:#fff;border:2px solid #b9b7b0;font:700 8.5px/12px Inter;text-align:center;font-style:normal;color:#77756f}
.trail li.on i{background:#10a364;border-color:#10a364;color:#fff}.trail li.fut{opacity:.45}.trail li .v{font-size:11px;color:#77756f}.trail li b{font-size:12.5px;font-weight:600}.trail li:hover b{color:#0f7a4f}
.trail li .gk{font-size:10px;font-weight:700;color:#fff;border-radius:99px;padding:0 6px;margin-left:4px}
.dp{border:1px dashed #d7d5cf;border-radius:12px;padding:8px 10px;margin-bottom:6px}.dp b{font-size:12.5px}.dp p{margin:3px 0 0;font-size:12px;color:#55544f}
.nt h4{margin:8px 0 3px;font-size:12px}.nt ul{margin:0;padding-left:16px}.nt li{margin:2px 0;font-size:12px;color:#3b3a36}
.src{display:inline-block;font:600 9.5px ui-monospace,monospace;color:#0f7a4f;background:#eef7f2;border-radius:5px;padding:0 4px;margin-left:2px;cursor:help;vertical-align:1px}.src.uns{color:#b42318;background:#fde2e0}
.emp{color:#9a9890;font-size:12px}.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);background:#232322;color:#fff;padding:9px 14px;border-radius:12px;font-weight:600;opacity:0;transition:.2s;z-index:20;pointer-events:none;max-width:90vw}.toast.on{opacity:1;transform:translateX(-50%)}
.kb{font-size:11px;color:#9a9890;text-align:center}.kb kbd{font:600 10px ui-monospace,monospace;border:1px solid #d7d5cf;border-bottom-width:2px;border-radius:4px;padding:0 4px;background:#fff;color:#55544f}
.uc{font-size:11.5px;color:#77756f}.uc summary{cursor:pointer}
@media(max-width:1180px){.main{flex-direction:column;align-items:center;overflow:auto;justify-content:flex-start}.nx{width:min(430px,100%);overflow:visible}}
@media(max-width:860px){body{overflow:auto}.tb{height:auto;flex-wrap:wrap;padding:8px 10px;gap:6px}.tb h1{display:none}.tb .sp{display:none}.main{position:static;padding:12px 10px 120px}
 .pn{position:fixed;top:auto;left:0;right:0;width:auto;height:76vh;border:0;border-radius:20px 20px 0 0;box-shadow:0 -10px 30px rgba(0,0,0,.18);transform:translateY(calc(76vh - 92px));transition:transform .25s;z-index:10}
 .pn.open{transform:none}.pn .hd{display:block;padding:8px 16px 8px;cursor:pointer;border-bottom:1px solid #eceae4}.pn .hd .grab{display:block;width:40px;height:5px;border-radius:3px;background:#d7d5cf;margin:0 auto 8px}
 .pn .hd .sm{display:flex;gap:6px;overflow:hidden}.pn .hd .sm span{font-size:11px;font-weight:700;border-radius:99px;padding:3px 9px;white-space:nowrap}.kb{display:none}.ctl .btn{padding:6px 10px}.ctl .pos{min-width:0}}
'''
WJS=r'''var META=JSON.parse(document.getElementById("wmeta").textContent),G=null,U,W,PH,TR=[],POS=0,HS=true,PLAY=null,DIST={},CACHE={};
function $(s){return document.querySelector(s)}function esc(t){return String(t==null?"":t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function src(t){/* source tags -> chips with hover text */return esc(t).replace(/\s*\[([^\]]+)\]/g,function(m,k){var tip=META._src[k]||k;return' <span class="src'+(/unsourced|⚠/.test(k)?" uns":"")+'" title="'+esc(tip)+'">'+esc(k)+"</span>"}).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>")}
function plain(t){return String(t||"").replace(/\s*\[[^\]]+\]/g,"")}
function toast(t){var e=$(".toast");e.textContent=t;e.classList.add("on");clearTimeout(toast.t);toast.t=setTimeout(function(){e.classList.remove("on")},2600)}
function UM(){return META[U]}function goals(){return UM().goals.filter(function(g){return g.ph<=PH})}function GB(id){return UM().goals.filter(function(g){return g.id===id})[0]}
function way(){return G.w.filter(function(w){return w.id===W})[0]}function oc(id){return UM().outs.filter(function(o){return o.id===id})[0]}
function parseHash(){var q={};location.hash.slice(1).split("&").forEach(function(kv){var i=kv.indexOf("=");if(i>0)q[kv.slice(0,i)]=decodeURIComponent(kv.slice(i+1))});return q}
function writeHash(){var p=TR.slice(1).map(function(s){return encodeURIComponent(s.r)}).join(","),h="user="+U+"&way="+W+"&ph="+PH+(p?"&path="+p:"")+(POS<TR.length-1?"&at="+POS:"");history.replaceState(null,"","#"+h)}
function load(u,ph,cb){var k=u+"-"+ph;if(CACHE[k])return cb(CACHE[k]);fetch("walk/"+k+".json").then(function(r){return r.json()}).then(function(d){CACHE[k]=d;cb(d)})}
/* distance in taps to complete each goal from every state: reverse BFS from goal end states and goal-completing taps */
function dists(){DIST={};var n=G.n,rev=n.map(function(){return[]});n.forEach(function(N,i){(N.e||[]).forEach(function(e){if(e.t>=0)rev[e.t].push(i)})});
 UM().goals.forEach(function(g){var d=n.map(function(){return 1/0}),L0=[],L1=[];n.forEach(function(N,i){if((N.gs||[]).indexOf(g.id)>=0){d[i]=0;L0.push(i)}else if((N.e||[]).some(function(e){return(e.g||[]).indexOf(g.id)>=0})){d[i]=1;L1.push(i)}});
  var q=L0.concat(L1),h=0;q.sort(function(a,b){return d[a]-d[b]});while(h<q.length){var a=q[h++];rev[a].forEach(function(b){if(d[b]>d[a]+1){d[b]=d[a]+1;q.push(b)}})}DIST[g.id]=d})}
function start(){var w=way();return w&&w.ok?w.n:-1}
function replay(refs){var s=start();TR=[{n:s}];var stack=[s],cut=null;for(var i=0;i<refs.length;i++){var N=G.n[TR[TR.length-1].n],e=(N.e||[]).filter(function(x){return x.r===refs[i]})[0];
  if(!e){cut=i+1;break}var t;if(e.t<0){if(stack.length>1)stack.pop();t=stack[stack.length-1]}else{t=e.t;stack.push(t)}TR.push({n:t,e:e,r:e.r})}
 return cut}
function navStack(){var st=[TR[0].n];for(var i=1;i<=POS;i++){var e=TR[i].e;if(e.t<0){if(st.length>1)st.pop()}else st.push(TR[i].n)}return st}
function take(e){stopPlay(1);if(innerWidth<=860)scrollTo({top:0,behavior:"smooth"});var t;if(e.t<0){var st=navStack();if(st.length>1)st.pop();t=st[st.length-1]}else t=e.t;TR=TR.slice(0,POS+1);TR.push({n:t,e:e,r:e.r});POS=TR.length-1;render()}
function setPos(p){POS=Math.max(0,Math.min(TR.length-1,p));render()}
/* goal state along the trail: reached (held, end state, or goal tap), milestones in order, taps left from here */
function gstate(g){var held=(way().hold||[]).indexOf(g.id)>=0,ms=g.ms.map(function(m){return m.id}),p=held?ms.length:0,rc=held;
 for(var i=0;i<=POS;i++){var N=G.n[TR[i].n],e=TR[i].e,h=((N.h||{})[g.id]||[]).concat(e&&e.adv||[]);while(p<ms.length&&h.indexOf(ms[p])>=0)p++;if((N.gs||[]).indexOf(g.id)>=0||(e&&(e.g||[]).indexOf(g.id)>=0))rc=true}
 if(rc)p=ms.length;var d=DIST[g.id][TR[POS].n],d0=DIST[g.id][TR[0].n];return{rc:rc,p:p,n:ms.length,d:d,lost:!rc&&d===1/0&&d0<1/0,never:!rc&&d0===1/0}}
function choices(){var N=G.n[TR[POS].n],cur=TR[POS].n,by={},out=[],st=navStack();
 (N.e||[]).forEach(function(e){var t=e.t<0?(st.length>1?st[st.length-2]:-2):e.t;if(t===cur&&e.t>=0)return;var base=e.r.split("!")[0];
  if(e.cond){var b=by["b"+base];(b?b.vr:(by["v"+base]=by["v"+base]||[])).push(e);return}
  var k=e.t<0?"back":"t"+t;if(!by[k]){by[k]={t:t,es:[],vr:by["v"+base]||[],bk:e.t<0};out.push(by[k])}by[k].es.push(e);by["b"+base]=by[k]});
 SELF=[];(N.e||[]).forEach(function(e){if(e.t===cur)SELF.push(e.a+"|"+(e.to||"")+"|"+(e.si?"in":""))});
 out.forEach(function(c){c.ks=c.es.map(function(e){return e.a+"|"+(e.to||"")+"|"+(e.si?"in":"")});var sv={};c.vr=c.vr.filter(function(v){var k=v.cond+v.t;if(sv[k])return false;return sv[k]=1})});return out.sort(function(a,b){return(a.bk?1:0)-(b.bk?1:0)||(a.es[0].ch?1:0)-(b.es[0].ch?1:0)})}
function tags(c,e){var h="",cur=TR[POS].n;(c.es.concat(c.vr)).forEach(function(e){(e.oc||[]).forEach(function(id){var o=oc(id);if(!o||o.ph>PH)return;var g=o.r.indexOf("goal:")===0?GB(o.r.slice(5)):null;
  var s=g?'<span class="gl" style="background:'+g.c+'" title="'+esc(plain(o.w))+'">✓ '+esc(o.l)+"</span>":'<span class="dr" title="'+esc(plain(o.w))+'">✕ '+esc(o.l)+"</span>";if(h.indexOf(s)<0)h+=s})});
 if(c.t>=0)goals().forEach(function(g){if(gstate(g).rc)return;var a=DIST[g.id][cur],b=DIST[g.id][c.t],fin=c.es.some(function(e){return(e.g||[]).indexOf(g.id)>=0})||(G.n[c.t].gs||[]).indexOf(g.id)>=0;
  if(fin)h+='<span class="gl" style="background:'+g.c+'">★ completes '+esc(g.l)+"</span>";else if(b<a)h+='<span class="cl" style="border-color:'+g.c+";color:"+g.c+'">'+esc(g.l)+" · "+b+" tap"+(b>1?"s":"")+"</span>";else if(a<1/0&&b===1/0)h+='<span class="dr">loses '+esc(g.l)+"</span>"});
 return h?'<div class="tg">'+h+"</div>":""}
var CH=[],SELF=[];
function render(){if(!G)return;var N=G.n[TR[POS].n];writeHash();
 $("#pos").textContent="Step "+(POS+1)+" of "+TR.length;$("#bb").disabled=POS===0;$("#fb").disabled=POS>=TR.length-1;
 var fr=$("#fr"),u="../index.html?style=fresh&device=phone&embed=1&auth="+N.a+"&live="+N.lv+(N.p==="home"&&N.m?"&mode="+N.m:"")+(N.o?"&ov="+N.o:"")+"&ph="+PH+"#"+N.p;
 if(fr.dataset.u!==u){fr.dataset.u=u;$(".phone").classList.add("loading");fr.src=u}else hot();
 var c=$("#cur");c.innerHTML='<div class="lbl">Now on</div><h2>'+esc(N.t)+'</h2><div class="chips"><span class="chip'+(N.a==="in"?" in":"")+'">'+(N.a==="in"?"Signed in":"Signed out")+'</span><span class="chip'+(N.lv==="live"?" lv":"")+'">'+(N.lv==="live"?"Someone live nearby":"Nobody live nearby")+"</span>"+(N.m?'<span class="chip">Home: '+esc(N.m)+" mode</span>":"")+(N.c?'<span class="chip" title="After signing in, the sheet continues to this screen">then → '+esc(N.c)+"</span>":"")+'</div><div class="gp" style="margin-top:6px">'+esc(N.k)+"</div>";
 CH=choices();var h="",fw=CH.filter(function(x){return!x.bk});
 if(!fw.length)h+='<div class="dead">⚠ Dead end: nothing on this screen leads forward in the model. Only '+(CH.length?"Back":"rewinding")+" gets the user out.</div>";
 h+='<div class="lbl">Next: '+fw.length+" way"+(fw.length===1?"":"s")+" on</div>";
 CH.forEach(function(x,i){var e=x.es[0],labs=[];x.es.forEach(function(e){if(labs.indexOf(e.l)<0)labs.push(e.l)});var T=x.t>=0?G.n[x.t].t:x.t===-1?"previous screen":"leaves the site";
  h+='<div class="ch'+(x.bk?" bkc":"")+'" data-i="'+i+'" tabindex="0"><span class="n">'+(i+1)+"</span><b>"+esc(labs.join(" / "))+"</b>"+'<div class="to">'+(x.bk?"↩ back to ":e.ch?"tab bar → ":"→ ")+esc(T)+"</div>"+tags(x)+'<div class="ofs" hidden>Not drawn on this screen: no visible control does this.</div>'+
  (x.vr.length?'<div class="vr">'+x.vr.map(function(v,j){return'<button data-v="'+j+'">If '+esc(v.cond)+" → "+esc(G.n[v.t]?G.n[v.t].t:"")+(v.oc&&v.oc.length?" · "+esc((oc(v.oc[0])||{}).l||""):"")+"</button>"}).join("")+"</div>":"")+"</div>"});
 $("#chs").innerHTML=h;panel()}
function panel(){var N=G.n[TR[POS].n],h='<div class="sec"><div class="lbl">Goals <span class="gp" style="text-transform:none;letter-spacing:0">'+esc(UM().l)+" · phase "+PH+"</span></div><div class=\"gl2\">",sm="";
 goals().forEach(function(g){var s=gstate(g),cls=s.rc?"rc":s.d<1/0?"ok":"no",lab=s.rc?"Reached":s.d<1/0?s.d+" tap"+(s.d>1?"s":"")+" away":s.lost?"No longer reachable":"Not reachable";
  h+='<div class="go '+cls+'"><div class="t"><i style="background:'+g.c+'"></i>'+esc(g.l)+'<span class="st">'+lab+'</span></div><div class="ms">'+g.ms.map(function(m,j){return'<span title="'+esc(m.l)+'" style="'+(j<s.p?"background:"+g.c:"")+'"></span>'}).join("")+'</div><div class="ml">'+(s.p<s.n?"Next milestone: "+esc(g.ms[s.p].l)+" ("+s.p+"/"+s.n+")":"All "+s.n+" milestones")+(g.lk&&!s.rc?' · <span title="'+esc(plain(g.lk))+'">likely?</span>':"")+"</div>"+
  (!s.rc&&s.d<1/0?'<button class="btn jb" data-g="'+g.id+'">▶ Play shortest path ('+s.d+")</button>":"")+(s.lost?'<div class="ml" style="color:#b42318">The path so far closed this goal off: nothing reachable from here completes it.</div>':"")+"</div>";
  sm+='<span style="background:'+(s.rc?g.c:"#eeece6")+";color:"+(s.rc?"#fff":g.c)+'">'+(s.rc?"✓ ":"")+esc(g.l)+(s.rc?"":s.d<1/0?" · "+s.d:" · ✕")+"</span>"});
 h+="</div></div>";
 h+='<div class="sec"><div class="lbl">Path <span><button class="btn" id="cp" style="padding:3px 9px">Copy link</button></span></div><ol class="trail">'+TR.map(function(s,i){var M=G.n[s.n],gk="";goals().forEach(function(g){if(s.e&&(s.e.g||[]).indexOf(g.id)>=0)gk+='<span class="gk" style="background:'+g.c+'">'+esc(g.l)+"</span>"});
  return'<li data-p="'+i+'" class="'+(i===POS?"on":i>POS?"fut":"")+'"><i>'+(i+1)+"</i><b>"+esc(M.t)+"</b>"+gk+'<div class="v">'+(i?(s.e.t<0?"Back":"tapped “"+esc(s.e.l)+"”"+(s.e.cond?" if "+esc(s.e.cond):"")):"Arrives: "+esc(way().l))+"</div></li>"}).join("")+"</ol></div>";
 var dr=(G.dr||[]).filter(function(d){var o=oc(d.o);return o&&o.end===N.k});
 h+='<div class="sec"><div class="lbl">Possible drop-offs here</div>'+(dr.length?dr.map(function(d){var o=oc(d.o),ms=null;goals().forEach(function(g){g.ms.forEach(function(m,j){if(m.id===d.m&&!ms)ms=m.l+" ("+(j+1)+"/"+g.ms.length+" of "+g.l+")"})});return'<div class="dp"><b>✕ '+esc(o.l)+"</b>"+(ms?'<span class="gp"> · furthest: '+esc(ms)+"</span>":"")+"<p>"+src(o.w)+"</p></div>"}).join(""):'<div class="emp">No modelled drop-off ends on this screen. If users could leave here, add an outcome to '+esc(UM().mfn)+".</div>")+"</div>";
 var sc=[N.p].concat(N.o?[N.o]:[]);h+='<div class="sec nt"><div class="lbl">Notes for this screen</div>'+sc.map(function(k){var d=META._scr[k];if(!d)return"";return"<div><b>"+esc(d.t)+"</b>"+d.s.map(function(s){return"<h4>"+esc(s[0])+"</h4><ul>"+s[1].map(function(l){return"<li>"+src(l)+"</li>"}).join("")+"</ul>"}).join("")+"</div>"}).join("")+'<div class="uc" id="uc"></div></div>';
 $("#pb").innerHTML=h;$("#psm").innerHTML=sm}
/* hotspots: find the drawn controls on the live screen that do each choice (same parse rules as gen/htmllinks.py) */
function keys(el,N){var js=el.getAttribute("onclick")||"",hr=el.getAttribute("href")||"",tg=[],m,re=/\b(go|ov|signIn|setHome|act)\('([\w-]*)'/g,own=N.o||N.p,sh=!!N.o,out=N.a==="out";
 while((m=re.exec(js)))tg.push([m[1],m[2]]);if(/\bsignIn\(\)/.test(js))tg.push(["signIn",""]);if(/\bpostAt\(/.test(js))tg.push(["go","post"]);if(/\bfollow\(/.test(js))tg.push(["follow",""]);if(/\bbk\(\)/.test(js)||/\bpick\(/.test(js))tg.push(["back",""]);
 if(/\bovx\(\)/.test(js)&&!tg.length)tg.push(["ovx",""]);var hm=hr.match(/^#([\w-]+)$/);if(hm&&hm[1]!=="index")tg.push(["go",hm[1]]);
 return tg.map(function(x){var k=x[0],t=x[1];return(k==="go"?"replace|"+t.split("--")[0]:k==="ov"?(sh?"swap|":"open|")+t:k==="ovx"?"close|":k==="act"?(out?"open|signin":"replace|"+t):k==="follow"?(out?"open|signin":"swap|"+own):k==="signIn"?((sh&&!t)?"close|":"replace|"+(t||own)):k==="setHome"?"swap|home":"back|")+"|"+(k==="signIn"?"in":"")})}
function vis(el){var r=el.getBoundingClientRect();if(r.width<2||r.height<2)return false;var w=el.ownerDocument.defaultView,s=w.getComputedStyle(el);return s.visibility!=="hidden"&&s.display!=="none"&&el.closest(".scr.on,.ov.on")}
function hot(){var fr=$("#fr"),d;try{d=fr.contentDocument}catch(e){return}if(!d||!d.body)return;var N=G.n[TR[POS].n];
 if(!d.getElementById("wk-st")){var s=d.createElement("style");s.id="wk-st";s.textContent=".wk-hs{outline:2.5px solid #10a364!important;outline-offset:1px;box-shadow:0 0 0 5px rgba(16,163,100,.16)!important;cursor:pointer!important}.wk-hs.wk-hot{outline-color:#f59e0b!important;box-shadow:0 0 0 6px rgba(245,158,11,.3)!important}.wk-off .wk-hs{outline:0!important;box-shadow:none!important}.wk-off .wk-hs:after{display:none!important}.wk-hs[data-wk]:after{content:attr(data-wk);position:absolute;right:-6px;top:-6px;z-index:50;min-width:18px;height:18px;padding:0 4px;border-radius:9px;background:#10a364;color:#fff;font:700 11px/18px Inter,sans-serif;text-align:center;pointer-events:none}.wk-rel{position:relative}";d.head.appendChild(s);
  d.addEventListener("click",function(ev){var el=ev.target.closest("[data-wki]");var c=ev.target.closest("a,button,[onclick],label");if(!c)return;ev.preventDefault();ev.stopPropagation();if(el){var x=CH[+el.dataset.wki];if(x)take(x.es[0])}else toast("That control has no link in the model: it does nothing in the walkthrough.")},true)}
 d.documentElement.classList.toggle("wk-off",!HS);d.querySelectorAll(".wk-hs").forEach(function(e){e.classList.remove("wk-hs","wk-hot","wk-rel");e.removeAttribute("data-wk");e.removeAttribute("data-wki")});
 var root=N.o?d.getElementById("ov-"+N.o):d.querySelector(".scr.on");if(!root)return;var found={},un=[];
 root.querySelectorAll("a[href],button,[onclick]").forEach(function(el){if(!vis(el))return;var ks=keys(el,N);if(ks.some(function(k){return SELF.indexOf(k)>=0})&&!CH.some(function(c){return c.ks.some(function(k){return ks.indexOf(k)>=0})}))return;if(!ks.length){if(el.tagName!=="BUTTON"||el.closest(".seg,.chips"))return;un.push((el.textContent||el.getAttribute("aria-label")||"").trim().slice(0,30));return}
  for(var i=0;i<CH.length;i++){if(CH[i].ks.some(function(k){return ks.indexOf(k)>=0})){var an=el.parentElement&&el.parentElement.closest("[data-wki]");if(an&&+an.dataset.wki===i)return;el.classList.add("wk-hs");el.dataset.wki=i;el.dataset.wk=i+1;if(d.defaultView.getComputedStyle(el).position==="static")el.classList.add("wk-rel");found[i]=1;return}}
  un.push((el.textContent||el.getAttribute("aria-label")||"").trim().slice(0,30))});
 document.querySelectorAll(".ch").forEach(function(c){var i=+c.dataset.i;c.classList.toggle("off",!found[i]&&!CH[i].bk);var o=c.querySelector(".ofs");if(o)o.hidden=!!found[i]||CH[i].bk});
 var uc=$("#uc");if(uc)uc.innerHTML=un.length?"<details><summary>"+un.length+" drawn control"+(un.length>1?"s":"")+" with no model link</summary>"+un.map(esc).join(" · ")+"</details>":""}
function hl(i,on){var d;try{d=$("#fr").contentDocument}catch(e){}if(d)d.querySelectorAll('[data-wki="'+i+'"]').forEach(function(e){e.classList.toggle("wk-hot",on)})}
function bfs(gid){var from=TR[POS].n,n=G.n,par={},q=[from];par[from]=null;for(var h=0;h<q.length;h++){var a=q[h];if(a!==from&&(n[a].gs||[]).indexOf(gid)>=0)return path(par,a,null);
  var es=n[a].e||[];for(var j=0;j<es.length;j++){var e=es[j];if(e.t<0)continue;if((e.g||[]).indexOf(gid)>=0)return path(par,a,e);if(!(e.t in par)){par[e.t]={a:a,e:e};q.push(e.t)}}}return null}
function path(par,a,last){var p=last?[last]:[];while(par[a]){p.unshift(par[a].e);a=par[a].a}return p}
function play(gid){stopPlay();var p=bfs(gid);if(!p){toast("No path from here.");return}var g=GB(gid);toast("Playing the shortest path to "+g.l+": "+p.length+" tap"+(p.length>1?"s":""));
 var i=0;function nx(){if(i>=p.length){PLAY=null;return}var e=p[i++],t=e.t;TR=TR.slice(0,POS+1);TR.push({n:t,e:e,r:e.r});POS=TR.length-1;render();PLAY=setTimeout(nx,1100)}PLAY=setTimeout(nx,250)}
function stopPlay(q){if(PLAY){clearTimeout(PLAY);PLAY=null}}
function fit(){var ph=$(".phone"),s=$(".phone .scr"),mob=innerWidth<=860,avH=mob?innerHeight*0.72:innerHeight-54-36-44,avW=mob?innerWidth-24:9999,k=Math.min(1,(avH-22)/844,(avW-22)/390);
 s.style.transform="scale("+k+")";ph.style.width=(390*k+22)+"px";ph.style.height=(844*k+22)+"px";s.style.marginBottom=(844*k-844)+"px";s.style.borderRadius=(36/k)+"px"}
function setup(cb){var q=parseHash();U=META._users.indexOf(q.user)>=0?q.user:META._users[0];PH=META._phases.indexOf(+q.ph)>=0&&q.ph!==undefined&&q.ph!==""?+q.ph:0;
 load(U,PH,function(d){G=d;dists();var ws=G.w;W=(ws.filter(function(w){return w.id===q.way&&w.ok})[0]||ws.filter(function(w){return w.ok})[0]).id;
  var cut=replay(q.path?q.path.split(",").filter(Boolean):[]);POS=q.at!=null&&q.at!==""?Math.min(+q.at,TR.length-1):TR.length-1;
  $("#us").innerHTML=META._users.map(function(u){return'<button data-u="'+u+'" class="'+(u===U?"on":"")+'" title="'+esc(META[u].sub)+'">'+esc(META[u].l)+"</button>"}).join("");
  $("#ps").innerHTML=META._phases.map(function(p){return'<button data-p="'+p+'" class="'+(p===PH?"on":"")+'">Phase '+p+"</button>"}).join("");
  $("#ws").innerHTML=ws.map(function(w){return'<option value="'+w.id+'"'+(w.id===W?" selected":"")+(w.ok?"":" disabled")+' title="'+esc(plain(w.w))+'">'+esc(w.l)+(w.ok?"":" (later phase)")+"</option>"}).join("");
  document.title="Walkthrough · "+META[U].l+" · "+way().l+" · PostUp mockups";if(cut)toast("Path cut at step "+(cut+1)+": that tap isn't available in phase "+PH+".");render();if(cb)cb()})}
function nav(o){var q=parseHash();Object.keys(o).forEach(function(k){q[k]=o[k]});if(o.user||o.way)delete q.path,delete q.at;if(!("path" in o)&&o.user)delete q.path;
 location.hash=Object.keys(q).filter(function(k){return q[k]!==undefined&&q[k]!==""}).map(function(k){return k+"="+encodeURIComponent(q[k])}).join("&")}
document.addEventListener("click",function(ev){var t=ev.target,b;
 if((b=t.closest("[data-u]")))return nav({user:b.dataset.u});if((b=t.closest("#ps [data-p]")))return nav({ph:b.dataset.p});
 if((b=t.closest(".vr button"))){var c=CH[+b.closest(".ch").dataset.i];return take(c.vr[+b.dataset.v])}
 if((b=t.closest(".ch")))return take(CH[+b.dataset.i].es[0]);if((b=t.closest(".trail li")))return setPos(+b.dataset.p);
 if((b=t.closest(".jb")))return play(b.dataset.g);if(t.closest("#cp")){navigator.clipboard&&navigator.clipboard.writeText(location.href);return toast("Link to this exact path copied.")}
 if(t.closest(".pn .hd"))$(".pn").classList.toggle("open")});
document.addEventListener("mouseover",function(ev){var c=ev.target.closest(".ch");document.querySelectorAll(".ch.hot").forEach(function(x){if(x!==c){x.classList.remove("hot");hl(x.dataset.i,false)}});if(c&&!c.classList.contains("hot")){c.classList.add("hot");hl(c.dataset.i,true)}});
$("#ws").onchange=function(e){nav({way:e.target.value,path:""})};$("#bb").onclick=function(){stopPlay();setPos(POS-1)};$("#fb").onclick=function(){stopPlay();setPos(POS+1)};$("#rs").onclick=function(){stopPlay();TR=TR.slice(0,1);POS=0;render()};
$("#hb").onclick=function(){HS=!HS;this.classList.toggle("pri",HS);hot()};
document.addEventListener("keydown",function(e){if(/INPUT|SELECT|TEXTAREA/.test(e.target.tagName))return;if(e.key==="ArrowLeft"){stopPlay();setPos(POS-1)}else if(e.key==="ArrowRight"){stopPlay();setPos(POS+1)}else if(/^[1-9]$/.test(e.key)&&CH[+e.key-1])take(CH[+e.key-1].es[0]);else if(e.key==="h"){$("#hb").click()}else return;e.preventDefault()});
$("#fr").addEventListener("load",function(){setTimeout(function(){$(".phone").classList.remove("loading");hot()},180)});
addEventListener("hashchange",function(){var q=parseHash();if(q.user!==U||+q.ph!==PH||q.way!==W)setup()});addEventListener("resize",fit);fit();setup();'''
open('flows/walk.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Walkthrough · PostUp mockups</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"><style>{WCSS}</style></head><body>
<header class="tb"><a class="bk" href="map.html">← Flow map</a><h1>Walkthrough</h1><span class="seg" id="us" title="User type (users.toml)"></span><select id="ws" title="Way in (ways.toml)"></select><span class="seg" id="ps" title="Phase"></span><span class="sp"></span><a class="btn" href="graph.html">Graph</a></header>
<main class="main"><div class="stage"><div class="phone"><div class="scr"><iframe id="fr" title="Mockup screen"></iframe><div class="ld"></div></div></div>
<div class="ctl"><button class="btn" id="bb" title="Previous step (←)">◀ Back</button><span class="pos" id="pos"></span><button class="btn" id="fb" title="Next step (→)">Forward ▶</button><button class="btn" id="rs" title="Back to the way in">↺ Restart</button><button class="btn pri" id="hb" title="Show tappable areas (H)">Hotspots</button></div>
<div class="kb"><kbd>←</kbd> <kbd>→</kbd> step · <kbd>1</kbd>–<kbd>9</kbd> choose · <kbd>H</kbd> hotspots · click a highlighted control on the phone</div></div>
<div class="nx"><div class="cur" id="cur"></div><div id="chs" style="display:flex;flex-direction:column;gap:8px"></div></div></main>
<aside class="pn"><div class="hd"><span class="grab"></span><div class="sm" id="psm"></div></div><div class="bd" id="pb"></div></aside><div class="toast"></div>
<script type="application/json" id="wmeta">{json.dumps(_wmeta,ensure_ascii=False).replace("</","<\\/")}</script><script>{WJS}</script></body></html>''')
with open('llms.txt','a') as fh: fh.write('- [Walkthrough](flows/walk.html): step through the real screens as a user type from a way in, with goals, drop-offs and notes per step; #user=&way=&ph=&path= [M1045]\n')
