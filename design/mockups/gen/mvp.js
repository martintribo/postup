/* MVP picker shared by flows pages (Martin, Oct 25 [M1025]). Choices live in localStorage "pu-mvp"; seed = flow priority. */
(function(){var K="pu-mvp",D=window.MVPD,S={},h=document.documentElement;try{S=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
var ids=Object.keys(D);function on(i){return i in S?!!S[i]:D[i].m}window.mvpOn=on;
function save(){try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}}
function apply(){document.querySelectorAll("input[data-mvp]").forEach(function(c){c.checked=on(c.dataset.mvp)});
 document.querySelectorAll("[data-mvpf]").forEach(function(e){e.classList.toggle("nomvp",!on(e.dataset.mvpf))});
 var only=false;try{only=localStorage.getItem(K+"-only")==="1"}catch(e){}h.classList.toggle("mvponly",only);document.querySelectorAll(".mvpo").forEach(function(c){c.checked=only});
 var n=ids.filter(on).length;document.querySelectorAll(".mvpn").forEach(function(e){e.textContent="MVP: "+n+" of "+ids.length});dispatchEvent(new Event("mvpchange"))}
function md(){var a=ids.filter(on),b=ids.filter(function(i){return!on(i)}),f=function(i){return"- "+D[i].n+" (`"+i+"`)"+(on(i)!==D[i].m?" (changed from "+(D[i].m?"MVP must":"nice")+")":"")};
 return"PostUp MVP flows ("+a.length+" of "+ids.length+")\n\n## MVP\n"+a.map(f).join("\n")+"\n\n## Not MVP\n"+(b.map(f).join("\n")||"- (none)")+"\n"}
document.addEventListener("change",function(e){var t=e.target;if(t.dataset&&t.dataset.mvp){S[t.dataset.mvp]=t.checked;save();apply()}else if(t.classList&&t.classList.contains("mvpo")){try{localStorage.setItem(K+"-only",t.checked?"1":"0")}catch(x){}apply()}});
document.addEventListener("click",function(e){var t=e.target;if(t.closest&&t.closest("label.mvpc"))e.stopPropagation();
 if(t.classList.contains("mvpreset")){if(confirm("Reset MVP choices to the default priorities?")){S={};save();apply()}}
 if(t.classList.contains("mvpcopy")){var s=md(),done=function(){t.textContent="Copied";setTimeout(function(){t.textContent="Copy MVP list"},1500)};
  if(navigator.clipboard&&isSecureContext)navigator.clipboard.writeText(s).then(done,fb);else fb();function fb(){var x=document.createElement("textarea");x.value=s;document.body.appendChild(x);x.select();document.execCommand("copy");x.remove();done()}}},true);
addEventListener("storage",function(e){if(e.key&&e.key.indexOf(K)===0){try{S=JSON.parse(localStorage.getItem(K)||"{}")}catch(x){}apply()}});
apply()})();
