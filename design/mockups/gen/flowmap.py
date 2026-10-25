# Flow map (Martin, Oct 25 2026 [M1025]): a state machine from "first-time visitor" to every flow's start.
# exec'd by flows.py (needs FLOWS, H, json, os, esc, HEAD). Writes flows/map.html and flows/map.md.
STATES=[('V0','First-time visitor<br>signed out · never registered','root'),
 ('SL','Signed out<br>someone live nearby','out'),('SN','Signed out<br>nobody live','out'),
 ('SLK','Signed out<br>on a live postup link','out'),('SEN','Signed out<br>on an ended postup link','out'),('SPJ','Signed out<br>on a project link','out'),
 ('OFF','Slow network or offline','any'),
 ('JN','Signed in<br>joined a postup','in'),('PEND','Signed in<br>ask pending','in'),('HOST','Signed in<br>hosting (live)','in'),
 ('RET','Returning user<br>signed in','in'),('RL','Signed in<br>someone live nearby','in'),('RN','Signed in<br>nobody live','in')]
EDGES=[('V0','SL','arrives at / · someone live'),('V0','SN','arrives at / · nobody live'),('V0','SLK','opens share link · live'),
 ('V0','SEN','opens share link · ended'),('V0','SPJ','opens share link · project'),('V0','OFF','network drops'),
 ('SL','JN','taps Join · signs in / registers'),('SL','SN','postups end'),('SN','HOST','posts up · signs in / registers'),
 ('SLK','JN','taps Join · signs in'),('SEN','RN','follows poster · signs in'),('SPJ','RN','follows project · signs in'),
 ('JN','RET','postup ends or leaves'),('HOST','RET','ends postup'),('RET','RL','comes back · someone live'),('RET','RN','comes back · nobody live'),
 ('RL','JN','joins'),('RL','PEND','asks to join'),('PEND','JN','gets approved'),('PEND','RL','declined or cancels'),
 ('RL','HOST','posts up'),('RN','HOST','posts up'),('OFF','RET','back online')]
BADGES=[('SL','first-visit-live',''),('SN','first-visit-none',''),('SN','first-post',''),('SLK','invite-live',''),('SEN','invite-ended',''),
 ('SPJ','invite-project',''),('OFF','loading-offline',''),('RL','cautious-joiner',''),('RL','quick-joiner',''),('RL','ask-join',''),
 ('RL','returning-post',''),('RL','desktop-browse','on a laptop'),('RL','postup-states','postup fills or ends'),('RL','safety','someone feels off'),
 ('HOST','host-approve','gets a request'),('HOST','hosting',''),('JN','leave','plans change'),('JN','chat',''),
 ('RN','project-builder',''),('RN','following',''),('RN','empty-area','area has no postups'),('RET','delete-account',''),('RET','settings-notify','')]
FB={f['id']:f for f in FLOWS}
assert sorted(b for _,b,_ in BADGES)==sorted(FB), set(FB)^{b for _,b,_ in BADGES}
# every badge reachable from the root
adj={}
for a,b,_ in EDGES: adj.setdefault(a,[]).append(b)
seen={'V0'}; st=['V0']
while st:
    for n in adj.get(st.pop(),[]):
        if n not in seen: seen.add(n); st.append(n)
assert all(s in seen for s,_,_ in BADGES), [s for s,_,_ in BADGES if s not in seen]
def mq(t): return t.replace('"','#quot;')
M=['flowchart LR']
def node(i,t,c):
    o,cl=('((','))') if c=='root' else ('(',')')
    return '  '+i+o+'"'+mq(t)+'"'+cl
M+=[node(*x) for x in STATES]
M+=[f'  {a} -->|"{mq(t)}"| {b}' for a,b,t in EDGES]
for s,fid,cond in BADGES:
    f=FB[fid]; bid='F_'+fid.replace('-','_')
    lab=('|"'+mq(cond)+'"|') if cond else ''
    M.append('  '+s+' -.->'+lab+' '+bid+'(["▶ '+mq(f['name'])+'"])')
    M.append(f'  click {bid} href "{fid}.html" "Open the {mq(f["name"])} player"')
    M.append(f'  class {bid} {"must" if f["pri"]=="MVP must" else "nice"}')
M+=[f'  class {i} {c}' for i,_,c in STATES]
M+=['  classDef root fill:#0f7a4f,color:#fff,stroke:#0b5c3b,stroke-width:3px','  classDef out fill:#fff,color:#232322,stroke:#8a8984,stroke-width:2px',
    '  classDef in fill:#e6f4ec,color:#0b4a30,stroke:#10a364,stroke-width:2px','  classDef any fill:#fff3d6,color:#5c3d00,stroke:#c48a00,stroke-width:2px',
    '  classDef must fill:#10a364,color:#fff,stroke:#0b5c3b','  classDef nice fill:#eceae4,color:#33332f,stroke:#8a8984']
MSRC='\n'.join(M)
MAPHEAD='Flow map (Martin, Oct 25 2026 [M1025]): a state machine from a first-time visitor (signed out, never registered) to the starting point of every critical flow. Nodes are user states; solid arrows are events or conditions; dashed arrows lead to a flow badge (green = MVP must, grey = nice) that opens the flow player. All 23 flows are reachable from the root.'
open('flows/map.md','w').write(f'# PostUp flow map\n{MAPHEAD}\n\nPage: /mockups/flows/map.html · grid: /mockups/flows/grid.html\n\n```mermaid\n{MSRC}\n```\n\n## Where each flow starts\n'+''.join(f'- `{fid}` ({FB[fid]["pri"]}): from state "{dict((i,t) for i,t,_ in STATES)[s].replace("<br>"," · ")}"{" when "+c if c else ""} [M1025]\n' for s,fid,c in BADGES))
open('flows/map.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flow map · PostUp mockups</title>
<style>{PCSS} body{{background:#d9d6ce}} .mb{{position:sticky;top:0;z-index:5;background:rgba(244,243,239,.96);border-bottom:1px solid #e4e2dc;padding:10px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
.mb button{{font:600 13px Inter,sans-serif;padding:6px 12px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}}
#vp{{overflow:auto;height:calc(100vh - 110px);cursor:grab;background:#fff;margin:10px;border-radius:14px;box-shadow:0 4px 14px rgba(0,0,0,.15);-webkit-overflow-scrolling:touch}}#vp.drag{{cursor:grabbing}}
#mm{{padding:20px;transform-origin:0 0;width:max-content}}#mm svg{{max-width:none!important}}#mm .clickable{{cursor:pointer}}#mm .edgeLabel p,#mm .edgeLabel span{{color:#3d3d39!important;background:#fff!important;font-size:13px}}#mm .nodeLabel p{{margin:0}}.lg{{font-size:12px;color:#55544f;margin:0 16px}}
.lg i{{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin:0 4px 0 10px;border:1px solid #8a8984}}</style></head><body>
<div class="mb"><a href="../index.html#index">← Mockups</a><b>Flow map</b><a href="grid.html">All flows grid</a><a href="index.html">Flow list</a><a href="map.md">map.md</a><span style="flex:1"></span><button onclick="z(-.15)">−</button><button onclick="z(0,1)">Fit</button><button onclick="z(.15)">+</button></div>
<p class="lg">{esc(MAPHEAD)}<br><i style="background:#0f7a4f"></i>start <i style="background:#fff"></i>signed out <i style="background:#e6f4ec;border-color:#10a364"></i>signed in <i style="background:#fff3d6"></i>any <i style="background:#10a364"></i>flow · MVP must <i style="background:#eceae4"></i>flow · nice</p>
<div id="vp"><div id="mm"><pre class="mermaid">{H.escape(MSRC)}</pre></div></div>
<script src="../vendor/mermaid.min.js"></script><script>
mermaid.initialize({{startOnLoad:false,securityLevel:"loose",theme:"base",themeVariables:{{fontFamily:"Inter,system-ui,sans-serif",fontSize:"15px",lineColor:"#6b6b67",primaryTextColor:"#232322",textColor:"#232322",nodeTextColor:"#232322",edgeLabelBackground:"#fff"}},flowchart:{{useMaxWidth:false,curve:"basis",nodeSpacing:28,rankSpacing:70}}}});
var s=1,mm=document.getElementById("mm"),vp=document.getElementById("vp");
function z(d,fit){{var sv=mm.querySelector("svg");if(!sv)return;if(fit){{s=Math.min(1,(vp.clientWidth-40)/sv.getBoundingClientRect().width*s)}}else s=Math.max(.25,Math.min(2.5,s+d));mm.style.transform="scale("+s+")";mm.style.width=(sv.getBoundingClientRect().width/1+40)+"px"}}
mermaid.run({{querySelector:".mermaid"}}).then(function(){{document.body.dataset.ready=1;z(0)}});
var dn=null;vp.addEventListener("mousedown",function(e){{if(e.target.closest(".clickable,a"))return;dn={{x:e.clientX,y:e.clientY,l:vp.scrollLeft,t:vp.scrollTop}};vp.classList.add("drag")}});
addEventListener("mousemove",function(e){{if(dn){{vp.scrollLeft=dn.l-(e.clientX-dn.x);vp.scrollTop=dn.t-(e.clientY-dn.y)}}}});addEventListener("mouseup",function(){{dn=null;vp.classList.remove("drag")}});
</script></body></html>''')
with open('llms.txt','a') as fh: fh.write(f'\n## Flow map\n{MAPHEAD}\n- [Flow map (Mermaid source + where each flow starts)](flows/map.md) · page: flows/map.html\n')
print('flowmap',len(STATES),'states',len(EDGES),'edges',len(BADGES),'badges')
