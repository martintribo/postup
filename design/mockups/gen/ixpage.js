/* The mockup index is the site's own chrome, not a product screen: lift it out of the phone frame into a full page. [M1026] */
(function(){var ix=document.getElementById("index");if(!ix)return;document.body.appendChild(ix);ix.classList.add("ixpage");
function f(){var on=(location.hash.slice(1)||"")==="index";document.documentElement.classList.toggle("ixon",on)}
addEventListener("hashchange",f);f()})();
/* Embedded (flow player iframe, thumbs, video, ?embed=1): no mockup chrome on the phone. [M1026] */
(function(){var q=location.search;if(self!==top||/[?&](embed=1|notes=0|fvs=|fs=)/.test(q))document.documentElement.classList.add("emb")})();
