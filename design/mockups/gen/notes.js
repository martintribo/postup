(function(){
var ND=JSON.parse(document.getElementById("notes-data").textContent),cur=null,ovOn=null;
function wideDesk(){return document.documentElement.dataset.device==="desktop"&&innerWidth>=980}
function render(id){var n=ND[id];if(!n)return;cur=id;
document.getElementById("nid").textContent=id.indexOf("ov-")==0?id+" over #"+(location.hash.slice(1)||"index"):"#"+id;
document.getElementById("nt").textContent=n.t;document.getElementById("nbody").innerHTML=n.h;
document.getElementById("nmd").href="notes/"+id+".md";document.getElementById("nroute").hidden=id!=="home"}
function scr(){var id=location.hash.slice(1)||"home";if(!ND[id])id="home";return id}
function upd(){render(ovOn?"ov-"+ovOn:scr())}
var _ov=window.ov,_ovx=window.ovx;
window.ov=function(id){_ov(id);ovOn=document.getElementById("ov-"+id)?id:null;upd()};
window.ovx=function(){_ovx();ovOn=null;upd()};
addEventListener("hashchange",function(){ovOn=null;upd()});
window.ntog=function(force){var h=document.documentElement;
 if(force===0){h.classList.remove("noff","ncol")}
 else if(wideDesk()){h.classList.add("noff")}
 else h.classList.toggle("ncol");
 try{localStorage.setItem("pu-notes",h.classList.contains("noff")?"off":h.classList.contains("ncol")?"col":"on")}catch(e){}};
var q=new URLSearchParams(location.search).get("notes"),l=null;try{l=localStorage.getItem("pu-notes")}catch(e){}
var st=q==="0"?"off":q==="1"?"on":(l||"on");if(st==="off")document.documentElement.classList.add("noff");if(st==="col")document.documentElement.classList.add("ncol");
window.nupd=upd;upd();if(window.scenUI)scenUI();
})();
