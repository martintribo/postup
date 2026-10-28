/* Phase filter shared by the flows/site views (Martin, Oct 27 2026 [M1031-draft]): "Phase 1" hides items marked data-ph="0".
   Choice lives in localStorage "pu-ph1" and syncs across open pages and iframes (storage event). */
(function(){var K="pu-ph1",h=document.documentElement;function on(){try{return localStorage.getItem(K)==="1"}catch(e){return false}}
function ap(){var o=on();h.classList.toggle("ph1only",o);document.querySelectorAll(".phbtn").forEach(function(b){b.textContent=o?"Phase: 1 only":"Phase: all";b.classList.toggle("on",o)});dispatchEvent(new Event("phchange"))}
window.phToggle=function(){try{localStorage.setItem(K,on()?"0":"1")}catch(e){}ap()};
addEventListener("storage",function(e){if(e.key===K)ap()});document.addEventListener("DOMContentLoaded",ap);ap()})();
