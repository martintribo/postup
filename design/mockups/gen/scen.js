/* scenarios: signed out/in x live nearby/none (see gen/scenarios.py) */
function scen(){var h=document.documentElement,a=h.dataset.auth,l=h.dataset.live;if(a&&l)return{a:a,l:l};
var q=new URLSearchParams(location.search),A=null,L=null;try{A=localStorage.getItem("pu-auth");L=localStorage.getItem("pu-live")}catch(e){}
a=q.get("auth")||A||"out";l=q.get("live")||L||"live";if(a!=="in")a="out";if(l!=="none")l="live";h.dataset.auth=a;h.dataset.live=l;return{a:a,l:l}}
/* the chosen variant takes the base id (so #id CSS applies); the base steps aside as <id>--base */
/* view phase [M1035]: ?ph= wins, else the shared Phase toggle (localStorage pu-ph1: "1" = phase 1; all / <=2 = latest) */
function vph(){var h=document.documentElement,q=new URLSearchParams(location.search).get("ph"),v=null;if(q)v=q;else{try{v=localStorage.getItem("pu-ph1")}catch(e){}}v=v==="1"?"1":"2";h.dataset.vph=v;return v}
vph();addEventListener("storage",function(e){if(e.key==="pu-ph1"&&!new URLSearchParams(location.search).get("ph")){vph();if(window.phUI)phUI();show()}});
var ALIAS={"inbox-one":"inbox"};
function setVph(v){try{localStorage.setItem("pu-ph1",v)}catch(e){}var u=new URL(location.href);u.searchParams.delete("ph");history.replaceState(null,"",u);vph();phUI();show()}
function phUI(){var v;try{v=localStorage.getItem("pu-ph1")||"0"}catch(e){v="0"}document.querySelectorAll("[data-vp]").forEach(function(b){b.classList.toggle("on",b.dataset.vp===v)})}
document.addEventListener("DOMContentLoaded",phUI);
function homeMode(){var h=document.documentElement;if(vph()==="1")return"live";if(!h.dataset.hmode){var q=new URLSearchParams(location.search).get("mode");if(q==="live"||q==="building")h.dataset.hmode=q}return h.dataset.hmode||(scen().l==="live"?"live":"building")}
function setHome(m){document.documentElement.dataset.hmode=m;var u=new URL(location.href);u.searchParams.set("mode",m);history.replaceState(null,"",u);show();if(window.nupd)nupd();if(window.pmUI)pmUI()}
function vid(id){var s=scen(),c=[id+"--"+s.a+"-"+s.l,id+"--"+s.l,id+"--"+s.a],pick=null;
document.querySelectorAll(".scr[data-v]").forEach(function(e){e.id=e.dataset.v});
if(id==="home"){var m=homeMode();pick=m==="live"?(s.l==="live"?null:"home--map-none"):(s.l==="live"?"home--bld-live":"home--bld");c=[]}
for(var i=0;i<c.length;i++)if(document.getElementById(c[i])){pick=c[i];break}
if(pick){var b=document.getElementById(id),v=document.getElementById(pick);if(b)b.id=id+"--base";v.id=id}
document.documentElement.dataset.vr=pick||id;return id}
function scenUI(){var s=scen();document.querySelectorAll("[data-sa]").forEach(function(b){b.classList.toggle("on",b.dataset.sa===s.a)});document.querySelectorAll("[data-sl]").forEach(function(b){b.classList.toggle("on",b.dataset.sl===s.l)});document.querySelectorAll("[data-sc]").forEach(function(b){b.classList.toggle("on",b.dataset.sc===s.a+"-"+s.l)})}
function setScen(a,l){var s=scen(),h=document.documentElement;a=a||s.a;l=l||s.l;if(l!==s.l){delete h.dataset.hmode;var uu=new URL(location.href);uu.searchParams.delete("mode");history.replaceState(null,"",uu)}h.dataset.auth=a;h.dataset.live=l;try{localStorage.setItem("pu-auth",a);localStorage.setItem("pu-live",l)}catch(e){}
var u=new URL(location.href);u.searchParams.set("auth",a);u.searchParams.set("live",l);history.replaceState(null,"",u);scenUI();show();if(window.nupd)nupd()}
var OSI=null;
function signIn(dest){ovx();var cur=location.hash.slice(1);setScen("in",null);if(dest===undefined)dest=OSI;OSI=null;if(dest&&dest!==cur)go(dest)}
function osi(t,s,dest){OSI=dest||null;ov("signin");document.getElementById("osi-t").textContent=t;document.getElementById("osi-s").textContent=s||"Sign in to continue."}
function act(dest,t,s){if(scen().a==="in"){go(dest);return}osi(t,s,dest)}
function follow(b,t){if(scen().a!=="in"){osi(t,"Sign in to follow along.");return}b.classList.toggle("sec");b.textContent=b.classList.contains("sec")?"Following":"Follow"}
scen();scenUI();show();
/* the browser scrolls to the #screen anchor after load; put the screen back at its top */
addEventListener("load",function(){[0,60,200].forEach(function(t){setTimeout(function(){var p=document.querySelector(".ph");if(p)p.scrollTop=0},t)})});
