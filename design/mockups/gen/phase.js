/* Phase filter shared by the flows/site views [M1047-draft].
   window.PU_PHASES = {ids, latest, labels, badges, aliases} is injected at build time.
   data-ph is a space-separated list of phase ids the item is available in, or "all".
   Choice lives in localStorage "pu-ph1": "all" or a phase id. Legacy values 0/p0/1/2 still resolve. */
(function(){
  var C=window.PU_PHASES||{ids:["smallest","pre-mvp","mvp"],latest:"mvp",labels:{},badges:{"smallest":"0","pre-mvp":"1","mvp":"2"},aliases:{"0":"smallest","p0":"smallest","ph0":"smallest","1":"pre-mvp","2":"mvp"}};
  var K="pu-ph1",h=document.documentElement;
  function resolve(v){ if(!v||v==="0"||v==="all"||v==="latest") return "all"; return (C.aliases&&C.aliases[v])||v; }
  function v(){ try{ return resolve(localStorage.getItem(K)); }catch(e){ return "all"; } }
  function label(o){
    if(o==="all") return "Phase: all";
    var i=(C.ids||[]).indexOf(o), lab=(C.labels&&C.labels[o])||o;
    if(i<=0) return "Phase: "+lab;
    return "Phase: ≤"+((C.badges&&C.badges[o])||lab);
  }
  function ap(){
    var o=v();
    (C.ids||[]).forEach(function(id){ h.classList.remove("ph-"+id); });
    h.classList.remove("ph0only","ph1only","ph2only","ph-all");
    if(o==="all") h.classList.add("ph-all");
    else h.classList.add("ph-"+o);
    document.querySelectorAll(".phbtn").forEach(function(b){
      b.textContent=label(o);
      b.title="Click to cycle All → each phase";
      b.classList.toggle("on", o!=="all");
    });
    dispatchEvent(new Event("phchange"));
  }
  window.phToggle=function(){
    var cur=v(), ids=["all"].concat(C.ids||[]), n=ids.indexOf(cur);
    var next=ids[(n+1)%ids.length];
    try{ localStorage.setItem(K, next); }catch(e){}
    ap();
  };
  window.puResolvePhase=resolve;
  addEventListener("storage",function(e){ if(e.key===K) ap(); });
  document.addEventListener("DOMContentLoaded",ap); ap();
})();
