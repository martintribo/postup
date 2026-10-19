(function(){
var h=document.documentElement,P=document.getElementById("pmp"),B=document.getElementById("pmb");
function cur(){return location.hash.slice(1)||"home"}
window.pmUI=function(){ui()};function ui(){var s=scen();function on(a,v){document.querySelectorAll("#pmp [data-"+a+"]").forEach(function(b){b.classList.toggle("on",b.dataset[a]===v)})}
on("ma",s.a);on("ml",s.l);on("mhm",homeMode());on("mst",h.dataset.style);on("mdv",h.dataset.device);
document.getElementById("pmnotes").checked=!h.classList.contains("noff");
var c=cur();document.querySelectorAll("#pmp .pmi").forEach(function(b){b.classList.toggle("on",b.dataset.go===c)});
document.getElementById("pmcur").textContent=(c==="home"?"/":"#"+c)+" · "+(s.a==="in"?"in":"out")+" · "+(s.l==="live"?"live":"none")}
window.pmToggle=function(open){if(open===undefined)open=P.hidden;P.hidden=!open;B.setAttribute("aria-expanded",open);if(open){ui();var L=document.getElementById("pmlist"),a=P.querySelector(".pmi.on");P.scrollTop=0;if(a)L.scrollTop=Math.max(0,a.offsetTop-L.offsetTop-60)}};
P.addEventListener("click",function(e){var b=e.target.closest("button,a");if(!b)return;var d=b.dataset;
 if(d.mhm){setHome(d.mhm);if(cur()!=="home")go("home")}else if(d.ma)setScen(d.ma,null);else if(d.ml)setScen(null,d.ml);else if(d.mst)applyStyle(d.mst);else if(d.mdv)applyDevice(d.mdv);
 else if(d.ov)ov(d.ov);else if(d.go){go(d.go);if(innerWidth<520)pmToggle(false)}else if(b.classList.contains("pml")&&innerWidth<520)pmToggle(false);
 ui()});
document.getElementById("pmnotes").addEventListener("change",function(e){if(e.target.checked)ntog(0);else{h.classList.add("noff");try{localStorage.setItem("pu-notes","off")}catch(x){}}ui()});
document.getElementById("pmq").addEventListener("input",function(e){var q=e.target.value.trim().toLowerCase();document.querySelectorAll("#pmp .pmg").forEach(function(g){var n=0;g.querySelectorAll(".pmi").forEach(function(b){var m=!q||b.dataset.q.indexOf(q)>=0;b.hidden=!m;if(m)n++});g.hidden=n===0})});
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&!P.hidden)pmToggle(false)});
addEventListener("hashchange",ui);
if(new URLSearchParams(location.search).get("notes")==="0")h.classList.add("shot");
if(new URLSearchParams(location.search).get("menu")==="open")pmToggle(true);
ui();
})();
