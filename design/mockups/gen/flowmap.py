# Flow map (Martin, Oct 25 2026 [M1025]): a state machine from "first-time visitor" to every flow's start.
# exec'd by flows.py (needs FLOWS, H, json, os, esc, HEAD). Writes flows/map.html and flows/map.md.
STATES=[('V0','First-time visitor<br>signed out · never registered','root'),
 ('IST','Stumbled on it<br>no idea what PostUp is','intent'),('ICU','Curious about content<br>live now or past','intent'),('IPO','Came to post up<br>wants to go live now','intent'),('ILK','Opened a share link<br>arrives with context','intent'),
 ('SPO','Signed out<br>on the Post up form','out'),
 ('SL','Signed out<br>someone live nearby','out'),('SN','Signed out<br>nobody live','out'),
 ('SLK','Signed out<br>on a live postup link','out'),('SEN','Signed out<br>on an ended postup link','out'),('SPJ','Signed out<br>on a project link','out'),
 ('OFF','Slow network or offline','any'),
 ('JN','Signed in<br>joined a postup','in'),('PEND','Signed in<br>ask pending','in'),('HOST','Signed in<br>hosting (live)','in'),
 ('RET','Returning user<br>signed in','in'),('RL','Signed in<br>someone live nearby','in'),('RN','Signed in<br>nobody live','in')]
EDGES=[('V0','IST','no idea'),('V0','ICU','curious'),('V0','IPO','wants to post'),('V0','ILK','has a link'),('V0','OFF','network drops'),
 ('IST','SL','someone live'),('IST','SN','nobody live'),('ICU','SL','someone live'),('ICU','SN','nobody live'),('IPO','SPO','taps Post up'),
 ('ILK','SLK','live'),('ILK','SEN','ended'),('ILK','SPJ','project'),('SN','SPO','taps Post up'),('SPO','HOST','Post up · signs in'),
 ('SL','JN','taps Join · signs in / registers'),('SL','SN','postups end'),
 ('SLK','JN','taps Join · signs in'),('SEN','RN','follows poster · signs in'),('SPJ','RN','follows project · signs in'),
 ('JN','RET','postup ends or leaves'),('HOST','RET','ends postup'),('RET','RL','comes back · someone live'),('RET','RN','comes back · nobody live'),
 ('RL','JN','joins'),('RL','PEND','asks to join'),('PEND','JN','gets approved'),('PEND','RL','declined or cancels'),
 ('RL','HOST','posts up'),('RN','HOST','posts up'),('OFF','RET','back online')]
BADGES=[('ICU','look-around','curious or no idea, joins'),('SN','empty-area-newcomer','nobody live'),('IPO','first-post',''),('SLK','invite-live',''),
 ('SPJ','invite-project',''),('OFF','loading-offline',''),('RL','join',''),('RL','ask-join',''),
 ('RL','returning-post',''),('RL','desktop-browse','on a laptop'),('RL','postup-states','postup fills or ends'),('RL','safety','someone feels off'),
 ('HOST','host-approve','gets a request'),('HOST','hosting',''),('JN','leave','plans change'),('JN','chat',''),
 ('RN','project-builder',''),('RN','following',''),('RN','empty-area','area has no postups'),('RET','delete-account',''),('RET','settings-notify',''),('RET','catch-up','comes back later')]
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
    M.append(f'  class {bid} {"must" if f["phase"] else "nice"}')
M+=[f'  class {i} {c}' for i,_,c in STATES]
M+=['  classDef root fill:#0f7a4f,color:#fff,stroke:#0b5c3b,stroke-width:3px','  classDef out fill:#fff,color:#232322,stroke:#8a8984,stroke-width:2px',
    '  classDef in fill:#e6f4ec,color:#0b4a30,stroke:#10a364,stroke-width:2px','  classDef any fill:#fff3d6,color:#5c3d00,stroke:#c48a00,stroke-width:2px',
    '  classDef must fill:#10a364,color:#fff,stroke:#0b5c3b','  classDef nice fill:#eceae4,color:#33332f,stroke:#8a8984']
MSRC='\n'.join(M)
MAPHEAD='Flow map (Martin, Oct 25 2026 [M1025]): a state machine from a first-time visitor (signed out, never registered) to the starting point of every critical flow. User states are grouped into four boxes, left to right: Arrive (first-time visitors split by intent: stumbled on it, curious about content, came to post up, opened a share link), Signed out browsing, Signed in, Doing something. Arrows are events or conditions (dashed = going back). Each flow’s badge sits inside the state where it starts (green = MVP must, grey = nice) and opens the flow player. All '+str(len(FLOWS))+' flows are reachable from the root.'
# ---- grouped, hand-placed layout (Martin, Oct 25: "box the nodes into high level boxes" [M1025]) ----
GROUPS=[('arrive','1 · Arrive (by intent)',['V0','IST','ICU','IPO','ILK','OFF']),('out','2 · Signed out, browsing',['SL','SN','SPO','SLK','SEN','SPJ']),
 ('in','3 · Signed in',['RL','RN','RET']),('doing','4 · Doing something',['PEND','JN','HOST'])]
assert sorted(x for _,_,xs in GROUPS for x in xs)==sorted(i for i,_,_ in STATES)
SHORT={('V0','IST'):'',('V0','ICU'):'',('V0','IPO'):'',('V0','ILK'):'',('V0','OFF'):'',('IST','SL'):'someone live',('IST','SN'):'nobody live',('ICU','SL'):'someone live',('ICU','SN'):'nobody live',
 ('IPO','SPO'):'taps Post up',('ILK','SLK'):'live',('ILK','SEN'):'ended',('ILK','SPJ'):'project',('SN','SPO'):'Post up',('SPO','HOST'):'Post up · signs in',('SL','JN'):'Join · signs in',('SL','SN'):'postups end',('SLK','JN'):'Join · signs in',
 ('SEN','RN'):'Follow · signs in',('SPJ','RN'):'Follow · signs in',('JN','RET'):'ends · leaves',('HOST','RET'):'ends',('RET','RL'):'',
 ('RET','RN'):'nobody live',('RL','JN'):'joins',('RL','PEND'):'asks',('PEND','JN'):'approved',('PEND','RL'):'declined',('RL','HOST'):'posts up',
 ('RN','HOST'):'posts up',('OFF','RET'):'back online'}
assert set(SHORT)=={(a,b) for a,b,_ in EDGES}
SN_={i:t for i,t,_ in STATES}
def badge(fid,cond):
    f=FB[fid]; return f'<div class="bdw" data-mvpf="{fid}">{mvpc(fid)}<a class="bd {"must" if f["phase"] else "nice"}" href="{fid}.html" title="{H.escape(f["pri"])}{" · when "+H.escape(cond) if cond else ""}">▶ {H.escape(f["name"])}{"<small>"+H.escape(cond)+"</small>" if cond else ""}</a></div>'
def card(i):
    c=dict((x,c) for x,_,c in STATES)[i]; bs=''.join(badge(fid,cond) for s,fid,cond in BADGES if s==i)
    return f'<div class="st {c}" id="st-{i}"><div class="sn">{SN_[i]}</div>{"<div class=bds>"+bs+"</div>" if bs else ""}</div>'
COLS=''.join(f'<section class="gp g-{g}"><h2>{H.escape(t)}</h2>{"".join(card(i) for i in xs)}</section>' for g,t,xs in GROUPS)
EJ=json.dumps([[a,b,SHORT[(a,b)]] for a,b,_ in EDGES]); GJ=json.dumps({i:k for k,(_,_,xs) in enumerate(GROUPS) for i in xs}); OJ=json.dumps({i:n for _,_,xs in GROUPS for n,i in enumerate(xs)})
open('flows/map-states.html','w').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flow map · PostUp mockups</title>
<style>{PCSS} body{{background:#efede7}} .mb{{position:sticky;top:0;left:0;z-index:5;background:rgba(244,243,239,.96);border-bottom:1px solid #e4e2dc;padding:10px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
.lg{{font-size:12px;color:#55544f;margin:8px 20px 0;max-width:1300px}}.lg i{{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin:0 4px 0 10px;border:1px solid #8a8984}}
.wrap{{overflow-x:auto}}.map{{position:relative;display:grid;grid-template-columns:230px 1fr 1fr 1fr;gap:0 118px;min-width:1340px;max-width:1500px;margin:0 auto;padding:64px 24px 96px;box-sizing:border-box;align-items:start}}
.gp{{border-radius:18px;padding:12px 12px 14px;display:flex;flex-direction:column;gap:30px;position:relative;z-index:1;min-height:100%;box-sizing:border-box}}.gp h2{{font-size:13px;letter-spacing:.05em;text-transform:uppercase;margin:0 0 -18px;color:#33332f}}
.g-arrive{{background:#dfeee6;justify-content:center}}.g-out{{background:#e6e4de}}.g-in{{background:#dcefe4}}.g-doing{{background:#fbecd0}}
.st{{background:#fff;border:2px solid #8a8984;border-radius:12px;padding:8px 10px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}.st.in{{border-color:#10a364}}.st.any{{border-color:#c48a00;background:#fff8e6}}
.st.intent{{border-color:#0f7a4f;border-style:dashed;background:#f3fbf6}}.st.root{{background:#0f7a4f;border-color:#0b5c3b;color:#fff;border-radius:50px;text-align:center;padding:16px 10px}}.sn{{font-weight:600;font-size:13.5px;line-height:1.3}}
.bds{{display:flex;flex-direction:column;gap:4px;margin-top:7px}}.bd{{display:block;font:600 12px/1.3 Inter,sans-serif;padding:5px 9px;border-radius:99px;text-decoration:none;color:#fff;background:#10a364}}.bd.nice{{background:#e2dfd7;color:#33332f}}.bd:hover{{filter:brightness(1.08);box-shadow:0 2px 6px rgba(0,0,0,.2)}}
.bd small{{display:block;font-weight:500;font-size:10.5px;opacity:.85}}svg.ar{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:2;overflow:visible}}
svg.ar path{{fill:none;stroke:#55544f;stroke-width:1.6}}svg.ar path.bk{{stroke:#b0562b;stroke-dasharray:5 4}}svg.ar text{{font:600 11px Inter,sans-serif;fill:#33332f}}svg.ar text.bk{{fill:#b0562b}}svg.ar rect{{fill:#fff;opacity:.95}}{MVPCSS}.bdw{{position:relative}}.bdw label.mvpc{{position:absolute;right:4px;top:50%;transform:translateY(-50%);padding:1px 6px 1px 4px;font-size:10.5px;z-index:2}}.bdw .bd{{padding-right:62px}}</style></head><body>
<div class="mb"><a href="../index.html#index">← Mockups</a><a href="map.html">Situations map</a><b>Flow map (user states)</b><a href="grid.html">All flows grid</a><a href="index.html">Flow list</a><a href="map.md">map.md</a><span style="flex:1"></span>{MVPBAR}</div>
<p class="lg">{esc(MAPHEAD)}<br><i style="background:#0f7a4f"></i>start <i style="background:#fff"></i>signed out <i style="background:#fff;border-color:#10a364"></i>signed in <i style="background:#fff8e6;border-color:#c48a00"></i>any <i style="background:#10a364"></i>flow · MVP must <i style="background:#e2dfd7"></i>flow · nice · solid = forward · <span style="color:#b0562b">dashed = back</span></p>
<div class="wrap"><div class="map" id="map">{COLS}<svg class="ar" id="ar"></svg></div></div>
<script>var E={EJ},G={GJ},O={OJ};
function draw(){{var m=document.getElementById("map"),sv=document.getElementById("ar"),M=m.getBoundingClientRect(),out=[],lab=[];
function R(i){{var r=document.getElementById("st-"+i).getBoundingClientRect();return{{l:r.left-M.left,r:r.right-M.left,t:r.top-M.top,b:r.bottom-M.top,cx:(r.left+r.right)/2-M.left,cy:(r.top+r.bottom)/2-M.top}}}}
var gp=[...m.querySelectorAll(".gp")].map(function(g){{var r=g.getBoundingClientRect();return{{l:r.left-M.left,r:r.right-M.left,t:r.top-M.top,b:r.bottom-M.top}}}});
var top=Math.min.apply(0,gp.map(function(g){{return g.t}})),bot=Math.max.apply(0,gp.map(function(g){{return g.b}}));
// ports: spread arrows on each side
var ports={{}};function port(i,side,k){{(ports[i+side]=ports[i+side]||[]).push(k)}}
E.forEach(function(e,k){{var a=G[e[0]],b=G[e[1]];e.k=k;e.t=a===b?"v":b===a+1?"f":b>a+1?"s":"b";
 if(e.t==="f"||e.t==="s"){{port(e[0],"R",k);port(e[1],"L",k)}}if(e.t==="b"){{port(e[0],"L",k);port(e[1],"R",k)}}}});
function py(i,side,k){{var r=R(i),l=ports[i+side],n=l.length,j=l.indexOf(k);var h=Math.min(r.b-r.t-16,26*(n));return r.cy-h/2+h*(j+.5)/n}}
function L(x,y,t,c){{lab.push([x,y,t,c||""])}}
var lane={{top:0,bot:0}},gl={{}};
E.forEach(function(e){{var a=R(e[0]),b=R(e[1]),k=e.k;
 if(e.t==="v"){{var dn=O[e[1]]>O[e[0]],adj=Math.abs(O[e[1]]-O[e[0]])==1;if(adj){{var x=dn?a.l+28:a.r-28,y1=dn?a.b:a.t,y2=dn?b.t:b.b;out.push('<path d="M'+x+' '+y1+'V'+y2+'" marker-end="url(#ah)"/>');if(e[2])L(x+6,(y1+y2)/2+4,e[2],"st")}}
  else{{var g=gp[G[e[0]]],xm=g.l+5,ya=a.t+12+(dn?(a.b-a.t-24):0),yb=b.cy;out.push('<path d="M'+(a.l)+' '+ya+'H'+xm+'V'+yb+'H'+b.l+'" marker-end="url(#ah)"/>');if(e[2])L(xm+4,yb-6,e[2],"st")}}}}
 else if(e.t==="f"){{var y1=py(e[0],"R",k),y2=py(e[1],"L",k),x1=a.r,x2=b.l,c=(x2-x1)*.5;out.push('<path d="M'+x1+' '+y1+'C'+(x1+c)+' '+y1+' '+(x2-c)+' '+y2+' '+x2+' '+y2+'" marker-end="url(#ah)"/>');if(e[2])L((x1+x2)/2,(y1+y2)/2,e[2])}}
 else if(e.t==="s"){{var y1=py(e[0],"R",k),y2=py(e[1],"L",k),x1=a.r,x2=b.l,ga=gp[G[e[0]]].r,gb=gp[G[e[1]]-1].r,useTop=y1<(top+bot)/2;
  var off=(gl[ga]=(gl[ga]||0)+1),off2=(gl["b"+gb]=(gl["b"+gb]||0)+1),xa=ga+14*off,xb=gb+118-14*off2,yl=useTop?top-14-14*(lane.top++):bot+16+14*(lane.bot++);
  out.push('<path d="M'+x1+' '+y1+'H'+xa+'V'+yl+'H'+xb+'V'+y2+'H'+x2+'" marker-end="url(#ah)"/>');L((xa+xb)/2,yl+(useTop?-4:12),e[2])}}
 else {{var y1=py(e[0],"L",k)+0,y2=py(e[1],"R",k),x1=a.l,x2=b.r,xl=x2+30+16*((gl["k"+x2]=(gl["k"+x2]||0)+1)-1);out.push('<path class="bk" d="M'+x1+' '+y1+'H'+xl+'V'+y2+'H'+x2+'" marker-end="url(#ab)"/>');L((xl+x1)/2+6,y1-5,e[2],"bk")}}}});
 var tx=lab.map(function(l){{var w=l[2].length*6+8,x=l[3]==="st"?l[0]:l[0]-w/2;return'<rect x="'+(x-2)+'" y="'+(l[1]-11)+'" width="'+w+'" height="15" rx="4"/><text x="'+(x+2)+'" y="'+l[1]+'" class="'+l[3]+'">'+l[2]+'</text>'}}).join("");
 sv.innerHTML='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#55544f" stroke="none"/></marker><marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#b0562b" stroke="none"/></marker></defs>'+out.join("")+tx;document.body.dataset.ready=1}}
addEventListener("load",draw);addEventListener("mvpchange",function(){{if(document.body.dataset.ready)draw()}});addEventListener("resize",draw);if(document.fonts)document.fonts.ready.then(draw);</script>{MVPJS}</body></html>""")
# map.md: Mermaid source with the same groups (subgraphs)
MS=['flowchart LR']
for g,t,xs in GROUPS: MS+=[f'  subgraph {g}["{t}"]','    direction TB']+['  '+node(i,t2,c) for i in xs for (j,t2,c) in STATES if j==i]+['  end']
MS+=[f'  {a} -->|"{SHORT[(a,b)]}"| {b}' for a,b,_ in EDGES]
for s_,fid,cond in BADGES:
    bid='F_'+fid.replace('-','_'); MS.append(f'  {s_} -.-> {bid}(["▶ {mq(FB[fid]["name"])}"])'); MS.append(f'  click {bid} href "{fid}.html"')
MSRC='\n'.join(MS)
open('flows/map.md','w').write(f'# PostUp flow map\n{MAPHEAD}\n\nPage: /mockups/flows/map.html (grouped boxes, hand-placed) · grid: /mockups/flows/grid.html\n\n## Groups\n'+''.join(f'- **{t}**: '+', '.join(SN_[i].replace("<br>"," · ") for i in xs)+' [M1025]\n' for g,t,xs in GROUPS)+f'\n```mermaid\n{MSRC}\n```\n\n## Where each flow starts\n'+''.join(f'- `{fid}` ({FB[fid]["pri"]}): from state "{SN_[s_].replace("<br>"," · ")}"{" when "+c if c else ""} [M1025]\n' for s_,fid,c in BADGES))
with open('llms.txt','a') as fh: fh.write(f'\n## Flow map\n{MAPHEAD}\n- [Flow map (Mermaid source + where each flow starts)](flows/map.md) · page: flows/map.html\n')
print('flowmap',len(STATES),'states',len(EDGES),'edges',len(BADGES),'badges')
