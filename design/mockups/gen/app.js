var CAFES=["Bean Theory","Grindhouse","Lantern Tea"],DIST=["0.4 mi","1.1 mi","0.8 mi"],ci=0;
function setC(c){var e=document.getElementById("pcafe");if(!e)return;document.querySelectorAll("#pcafe").forEach(function(x){x.textContent=CAFES[ci]});document.querySelectorAll("#pnear").forEach(function(x){x.textContent=(c?"":"Nearest · ")+DIST[ci]})}
function postAt(n){ci=Math.max(0,CAFES.indexOf(n));setC(false);go("post")}function cyc(){ci=(ci+1)%3;setC(true)}

document.addEventListener("click",function(e){var c=e.target.closest(".chip:not(.ad),.seg button");if(c){c.parentNode.querySelectorAll(".chip,button").forEach(function(x){x.classList.remove("on")});c.classList.add("on")}});
function show(){var id=location.hash.slice(1)||"home";var s=document.getElementById(vid(id))||document.getElementById("home");document.querySelectorAll(".scr").forEach(function(e){e.classList.toggle("on",e===s)});var p=document.querySelector(".ph");p.scrollTop=0;scrollTo(0,0);setTimeout(function(){p.scrollTop=0;scrollTo(0,0)},0)}
function go(id){location.hash=id}function bk(){history.length>1?history.back():go("index")}
addEventListener("hashchange",show);show();
var STY=["fresh","cozy","night","bold"];
function applyStyle(s){if(STY.indexOf(s)<0)s="fresh";document.documentElement.dataset.style=s;try{localStorage.setItem("pu-style",s)}catch(e){}var n=document.getElementById("stn");if(n)n.textContent=s[0].toUpperCase()+s.slice(1);document.querySelectorAll(".stsw button").forEach(function(b){b.classList.toggle("on",b.dataset.s===s)});var u=new URL(location.href);if(u.searchParams.get("style")!==s){u.searchParams.set("style",s);history.replaceState(null,"",u)}}
function setStyle(s){applyStyle(s)}function cycleStyle(){var c=document.documentElement.dataset.style||"fresh";applyStyle(STY[(STY.indexOf(c)+1)%4])}
(function(){var q=new URLSearchParams(location.search).get("style");var l=null;try{l=localStorage.getItem("pu-style")}catch(e){}applyStyle(q||l||"fresh")})();
function applyDevice(d){if(d!=="desktop")d="phone";document.documentElement.dataset.device=d;try{localStorage.setItem("pu-device",d)}catch(e){}document.querySelectorAll(".dvsw button").forEach(function(b){b.classList.toggle("on",b.dataset.d===d)});var u=new URL(location.href);if(u.searchParams.get("device")!==d){u.searchParams.set("device",d);history.replaceState(null,"",u)}}
(function(){var q=new URLSearchParams(location.search).get("device");var l=null;try{l=localStorage.getItem("pu-device")}catch(e){}applyDevice(q||l||"phone")})();
function railOn(){var id=location.hash.slice(1)||"home";var m={quiet:"home",cafe:"home",postup:"home",joined:"home","quiet-feed-b":"quiet-feed"};id=m[id]||id;document.querySelectorAll(".rail a[data-r]").forEach(function(a){a.classList.toggle("on",a.dataset.r===id||(a.dataset.r==="projects"&&id.indexOf("project")==0))})}
addEventListener("hashchange",railOn);railOn();
function ov(id){document.querySelectorAll(".ov.on").forEach(function(e){e.classList.remove("on")});var e=document.getElementById("ov-"+id);if(e)e.classList.add("on")}
function ovx(){document.querySelectorAll(".ov.on").forEach(function(e){e.classList.remove("on")})}
addEventListener("hashchange",ovx);
function pick(n,d){document.querySelectorAll("#pcafe").forEach(function(x){x.textContent=n});document.querySelectorAll("#pnear").forEach(function(x){x.textContent=d});history.length>1?history.back():go("post")}
function pfilter(e){var c=e.target.closest(".chip");if(!c)return;var f=c.dataset.f,sc=c.closest(".scr"),n=0;sc.querySelectorAll(".pc").forEach(function(a){var s=(a.dataset.f||"").split(" ").indexOf(f)>=0;a.hidden=!s;if(s)n++});var em=sc.querySelector(".pempty");if(em)em.hidden=n>0}
function railOn2(){var id=location.hash.slice(1)||"home";var m={quiet:"home",cafe:"home","cafe-gfail":"home",postup:"home","postup-ask":"home",ask:"home",joined:"home","empty-area":"home","postup-ended":"home","postup-full":"home","postup-cancelled":"home","quiet-feed-b":"quiet-feed",offline:"quiet-feed",loading:"quiet-feed",activity:"inbox",chat:"inbox",settings:"me",live:"me"};var r=m[id]||id;if(r.indexOf("project")==0)r="projects";document.querySelectorAll(".rail a[data-r]").forEach(function(a){a.classList.toggle("on",a.dataset.r===r)})}
addEventListener("hashchange",railOn2);railOn2();
(function(){var o=new URLSearchParams(location.search).get("ov");if(o)setTimeout(function(){ov(o)},50)})();
