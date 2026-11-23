/* Phase filter shared by the flows/site views [M1047-draft].
   window.PU_PHASES = {ids, latest, labels, badges, aliases} is injected at build time.
   data-ph is a space-separated list of phase ids the item is available in, or "all".
   Choice lives in localStorage "pu-ph1": "all" or a phase id. Legacy values 0/p0/1/2 still resolve. */
(function(){
  var C=window.PU_PHASES||{ids:["post-and-join","share-and-chat","projects"],latest:"projects",labels:{"post-and-join":"Phase 0: Post & join","share-and-chat":"Phase 1: Share & chat","projects":"Phase 2: Projects"},badges:{"post-and-join":"0","share-and-chat":"1","projects":"2"},aliases:{"0":"post-and-join","p0":"post-and-join","ph0":"post-and-join","smallest":"post-and-join","1":"share-and-chat","p1":"share-and-chat","ph1":"share-and-chat","pre-mvp":"share-and-chat","2":"projects","p2":"projects","ph2":"projects","mvp":"projects"}};
  var K="pu-ph1",h=document.documentElement;
  function resolve(v){ if(!v||v==="0"||v==="all"||v==="latest") return "all"; return (C.aliases&&C.aliases[v])||v; }
  function v(){ try{ return resolve(localStorage.getItem(K)); }catch(e){ return "all"; } }
  function label(o){
    if(o==="all") return "Phase: all";
    return (C.labels&&C.labels[o])||o;
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
