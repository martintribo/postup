/* Phase filter shared by the flows/site views [M1031-draft] [M1032]: All / Phase 0 (smallest) / Phase ≤1 (pre-MVP) / Phase ≤2 (MVP) [M1037].
   data-ph is the item's phase number (n = unphased). Choice lives in localStorage "pu-ph1" ("0"=all,"1","2","p0") and syncs across pages and iframes. */
(function(){var K="pu-ph1",h=document.documentElement,L={"0":"Phase: all","p0":"Phase: 0 (smallest)","1":"Phase: ≤1 (pre-MVP)","2":"Phase: ≤2 (MVP)"};function v(){try{var x=localStorage.getItem(K);return L[x]?x:"0"}catch(e){return"0"}}
function ap(){var o=v();h.classList.toggle("ph0only",o==="p0");h.classList.toggle("ph1only",o==="1");h.classList.toggle("ph2only",o==="2");document.querySelectorAll(".phbtn").forEach(function(b){b.textContent=L[o];b.title="Click to cycle All → 0 → ≤1 → ≤2";b.classList.toggle("on",o!=="0")});dispatchEvent(new Event("phchange"))}
window.phToggle=function(){try{localStorage.setItem(K,{"0":"p0","p0":"1","1":"2","2":"0"}[v()])}catch(e){}ap()};
addEventListener("storage",function(e){if(e.key===K)ap()});document.addEventListener("DOMContentLoaded",ap);ap()})();
