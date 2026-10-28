# Critical flows (Martin, Oct 24 2026 [M1024]). exec'd by build.py after menu.py.
# Reads gen/flowdata.py; writes flows/<id>.md, flows/<id>.html (player), flows/index.html, flows/all.md;
# appends to notes/all.md and llms.txt; adds a Flows group to the index and the floating menu.
import json, re, os, html as H
exec(open('gen/flowload.py').read())
OVHOST={o:NOTES['ov-'+o]['host'] for o in re.findall(r'id="ov-([\w-]+)"',OVS)}
ids=set()
for f in FLOWS:
    assert f['id'] not in ids, f['id']; ids.add(f['id'])
    assert f['pri'] in ('Phase 1','Unphased') and f['status'] in ('martin','draft')
    texts=[f['goal']]+[s[4] for s in f['steps']]+f['branches']+f['success']+f['decide']
    for t in texts:
        if not tags(t): raise SystemExit(f'flows: untagged line in {f["id"]}: {t}')
        for g in tags(t):
            if re.match(r'F\d',g) and g not in FACTS: raise SystemExit(f'flows: unknown fact {g} in {f["id"]}')
    for sc,a,l,x,t in f['steps']:
        if sc not in S: raise SystemExit(f'flows: unknown screen {sc} in {f["id"]}')
        assert a in ('in','out') and l in ('live','none')
        if 'ov' in x and x['ov'] not in OVHOST: raise SystemExit(f'flows: unknown sheet {x["ov"]} in {f["id"]}')
exec(open('gen/sitegraph.py').read())
FBY={f['id']:f for f in FLOWS}
def sgurl(k,dev='phone'):
    t=SST[k]; q=f'style=fresh&device={dev}&auth={t["auth"]}&live={t["live"]}'+(f'&mode={t["mode"]}' if t['mode'] else '')+(f'&ov={t["ov"]}' if t['ov'] else '')
    return f'../index.html?{q}#{t["page"]}'
def nextlist(fid,i): return [dict(t=k,l=(lab or kind),tk=tk) for k,lab,kind,tk in SG_NEXT[(fid,i)]]
def enterlist(fid,i): return [dict(f=e['f'],n=FBY[e['f']]['name'],j=e['j']+1,w=e['user'],same=e['same']) for e in SG_ENTER[(fid,i)]]
def conn_rows(fid):
    c=SG_CONN[fid]; g={}
    for i,h,j in c['out']: g.setdefault(h,{'out':[],'inn':[]})['out'].append((i+1,j+1))
    for i,h,j in c['inn']: g.setdefault(h,{'out':[],'inn':[]})['inn'].append((i+1,j+1))
    return sorted(g.items(),key=lambda x:-(len(x[1]['out'])+len(x[1]['inn'])))
MVPD={f['id']:{'n':f['name'],'m':f['pri']=='Phase 1'} for f in FLOWS}
PHJS='<script>'+open('gen/phase.js').read()+'</script>'
PHCSS='.phbtn{font:600 12px Inter,sans-serif;padding:4px 10px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}.phbtn.on{background:#10a364;color:#fff;border-color:#10a364}html.ph1only [data-ph="0"]{display:none!important}.p1b{display:inline-block;font:700 9.5px Inter,sans-serif;color:#fff;background:#10a364;border-radius:5px;padding:1px 4px;margin-left:4px;vertical-align:middle}'
PHBTN='<button class="phbtn" onclick="phToggle()">Phase: all</button>'
def p1b(on): return '<span class="p1b" title="Phase 1">P1</span>' if on else ''
MVPJS='<script>window.MVPD='+json.dumps(MVPD)+';'+open('gen/mvp.js').read()+'</script>'+PHJS
MVPCSS0=None
MVPCSS=""".mvpbar{display:inline-flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:12.5px}.mvpbar .mvpn{font-weight:700;color:#0f7a4f;white-space:nowrap}.mvpbar button{font:600 12px Inter,sans-serif;padding:5px 10px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}
label.mvpc{display:inline-flex;align-items:center;gap:4px;font:600 11.5px Inter,sans-serif;color:#0f7a4f;background:#fff;border:1px solid #bfe3cf;border-radius:99px;padding:2px 8px 2px 5px;cursor:pointer;white-space:nowrap;vertical-align:middle}label.mvpc input{margin:0;accent-color:#10a364}
.nomvp{opacity:.4}.nomvp:hover{opacity:.8}.mvponly .nomvp{display:none!important}"""+PHCSS
def mvpc(fid): return f'<label class="mvpc" title="Include in MVP"><input type="checkbox" data-mvp="{fid}">MVP</label>'
MVPBAR='<span class="mvpbar"><b class="mvpn"></b><label><input type="checkbox" class="mvpo"> Show only MVP</label><button class="mvpreset">Reset</button><button class="mvpcopy">Copy MVP list</button></span>'
MVPBAR0=MVPBAR.replace('<label><input type="checkbox" class="mvpo"> Show only MVP</label>','')
def surl(f,st,rel='../'):
    sc,a,l,x,_=st; d=x.get('device',f['start']['device'])
    q=f'style=fresh&device={d}&auth={a}&live={l}'+(f'&mode={x["mode"]}' if 'mode' in x else '')+(f'&ov={x["ov"]}' if 'ov' in x else '')
    return f'{rel}index.html?{q}#{sc}'
def murl(f,st): return surl(f,st,'/mockups/').replace('/mockups/index.html','/mockups/')
STAT={'martin':"Martin's example (Oct 24)",'draft':'Draft, inferred from the notes; confirm with Martin'}
def flow_md(f,lvl='#'):
    s=f['start']; L=lvl+'#'
    o=f"{lvl} Flow: {f['name']} (`{f['id']}`)\nPriority: **{f['pri']}** · Status: {STAT[f['status']]} [M1024]\nPlayer: /mockups/flows/{f['id']}.html\n\n"
    o+=f"{L} Persona\n- {f['persona']}\n\n{L} Starting state\n- auth={s['auth']} · live={s['live']} · device={s['device']} · entry URL `{s['url']}`\n\n{L} Goal\n- {f['goal']}\n\n{L} Steps\n"
    o+=''.join(f"{i+1}. **{d['site']}** · user: {d['user']} · action: {d['act']} · edge: {SG_HOW[(f['id'],i)]}\n   - {d['do']}\n   - next site states: "+', '.join(('**'+n['t']+'**' if n['tk'] else n['t'])+f" ({n['l']})" for n in nextlist(f['id'],i))+"\n   - enterable flows: "+(', '.join(f"{e['f']} step {e['j']} (if {e['user'] if False else e['w']})" for e in enterlist(f['id'],i)) or 'none')+"\n" for i,d in enumerate(f['sx']))
    o+=f"\n{L} Connected flows [M1025]\n"+(''.join(f"- `{h}`: branch out at "+(', '.join(f'step {a}→{b}' for a,b in v['out']) or '—')+"; merge in at "+(', '.join(f'step {a} (from its step {b})' for a,b in v['inn']) or '—')+"\n" for h,v in conn_rows(f['id'])) or '- none\n')
    o+='\n'+f'{L} Screens\n'+''.join(f"{i}. `#{st[0]}`{' + sheet `'+st[3]['ov']+'`' if 'ov' in st[3] else ''} · auth={st[1]} live={st[2]}{' mode='+st[3]['mode'] if 'mode' in st[3] else ''} — {st[4]} ({murl(f,st)})\n" for i,st in enumerate(f['steps'],1))
    for h,k in [('Branches and edge cases','branches'),('Success criteria','success'),('Needs Martin\'s decision','decide')]:
        if f[k]: o+=f"\n{L} {h}\n"+''.join(f'- {b}\n' for b in f[k])
    return o
os.makedirs('flows',exist_ok=True)
for fn in os.listdir('flows'):
    if os.path.isfile(os.path.join('flows',fn)): os.remove(os.path.join('flows',fn))
HEAD='Critical flows (Martin, Oct 24 2026 [M1024]): a type of user arrives in a certain situation and goes through a scenario step by step. Each step names the screen and the scenario params (auth, live, Home mode, sheet). Flows marked Draft were inferred from the screen notes; confirm with Martin.'
for f in FLOWS: open(f'flows/{f["id"]}.md','w').write(flow_md(f)+f'\n{LEGEND} M1024 = Martin, Oct 24 2026: track critical flows.\n')
FALL='# PostUp critical flows\n'+HEAD+'\n\n'+'\n'.join(f"- [{f['id']}]({f['id']}.md) · {f['pri']} · {f['name']}" for f in FLOWS)+'\n\n'+'\n---\n\n'.join(flow_md(f,'##') for f in FLOWS)
open('flows/all.md','w').write(FALL)
# all.md + llms.txt
with open('notes/all.md','a') as fh: fh.write('\n---\n\n# Critical flows\n'+HEAD+'\n\n'+'\n---\n\n'.join(flow_md(f,'##') for f in FLOWS))
with open('llms.txt','a') as fh: fh.write('\n## Critical flows\n'+HEAD+'\n- [All flows in one file](flows/all.md)\n'+''.join(f"- [{f['id']}](flows/{f['id']}.md): {f['name']} ({f['pri']}{', draft' if f['status']=='draft' else ''}) · player: flows/{f['id']}.html\n" for f in FLOWS))
# player pages
BRCSS='''.tree{list-style:none;padding:0;margin:6px 0}.tree>li.st{padding:6px 6px 4px;margin:0 0 4px;border-radius:12px;cursor:pointer;font-weight:400;background:none}.tree>li.st:hover{background:#f1f0eb}.tree>li.on{background:#e6f4ec}
.sr{display:flex;gap:10px;align-items:flex-start}.sn{flex:none;width:24px;height:24px;border-radius:50%;background:#10a364;color:#fff;font:700 12px/24px Inter,sans-serif;text-align:center;margin-top:2px}.sth{flex:none;width:38px;height:82px;object-fit:cover;object-position:top;border-radius:7px;border:2px solid #222;background:#fff}
.stx{display:flex;flex-direction:column;gap:2px;min-width:0}.stx b{font-size:13.5px}.su{font-size:12.5px;color:#0f7a4f;font-style:italic}.sa{font-size:11.5px;color:#6b6b67}
.bd{margin:2px 0 0 11px}.bd summary{font:600 11px Inter,sans-serif;color:#6b6b67;cursor:pointer;padding:2px 0 2px 22px;list-style:none}.bd summary::-webkit-details-marker{display:none}.bd summary:before{content:'▸ ';}.bd[open] summary:before{content:'▾ '}
.bl{margin-left:11px;border-left:2px solid #cfd8d2;padding:2px 0 2px 0}.br{position:relative;display:flex;gap:8px;align-items:center;margin:3px 0 3px 0;padding:3px 6px 3px 22px;text-decoration:none;color:#232322;border-radius:8px;font-size:12px}.br:before{content:'';position:absolute;left:0;top:50%;width:16px;border-top:2px solid #cfd8d2}.br:hover{background:#fff}
.br img{flex:none;width:22px;height:46px;object-fit:cover;object-position:top;border-radius:4px;border:1.5px solid #444;background:#fff}.bt{display:flex;flex-direction:column;min-width:0}.bt em{color:#5b3fd6;font-style:italic}.bm{color:#6b6b67;font-size:11px}.bm b{color:#232322}
.br.lp em{color:#8a5a00}.br.ex em{color:#6b6b67}.bx{flex:none;width:22px;text-align:center;color:#6b6b67}.br.sm{padding-top:1px;padding-bottom:1px}.br.sm:before{border-top-style:dotted}
.nv .tgl{margin-left:auto;font-size:12px;padding:6px 10px}.cfs{display:flex;flex-wrap:wrap;gap:5px}.cfc{font-size:12px;padding:3px 9px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;text-decoration:none;color:#232322}.cfc i{font-style:normal;color:#6b6b67;font-size:11px}'''
PCSS='''*{box-sizing:border-box}body{margin:0;font:14px/1.4 Inter,system-ui,sans-serif;color:#232322;background:#f4f3ef}a{color:#0f7a4f}
.fp{display:grid;grid-template-columns:460px 1fr;height:100vh}.side{overflow:auto;padding:14px 16px}.fh{overflow:auto;padding:14px;background:#fbfaf7;border-left:1px solid #e4e2dc;font-size:13px}.fh h3{margin-top:12px}.fh .think{background:#eef6f1;border-left:3px solid #10a364;border-radius:8px;padding:8px 10px;font-size:13.5px}.fh .how{font-size:11.5px;color:#6b6b67;margin-top:4px}.nxc{display:flex;flex-wrap:wrap;gap:4px}.nxc a,.nxc span{font:600 10.5px ui-monospace,monospace;padding:3px 6px;border-radius:6px;background:#f1efe9;color:#55544f;text-decoration:none;border:1px solid #e4e2dc}.nxc .tk{background:#10a364;color:#fff;border-color:#10a364}.nxc i{font:500 10px Inter,sans-serif;color:inherit;opacity:.75;margin-left:3px}.enc{display:block;background:#fff;border:1px solid #e4e2dc;border-radius:10px;padding:8px 10px;margin:6px 0;text-decoration:none;color:#232322}.enc:hover{border-color:#10a364}.enc b{display:block;font-size:12.5px}.enc span{font-size:11.5px;color:#6b6b67}.enc em{font-style:normal;color:#0f7a4f;font-weight:600}.cf li{margin:3px 0;font-size:12.5px}.side{overflow:auto;padding:16px;background:#fff;border-right:1px solid #e4e2dc}
.side h1{font-size:18px;margin:6px 0}.meta{font-size:12px;color:#6b6b67}.pill{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:99px;background:#e6f4ec;color:#0f7a4f;margin-right:4px}.pill.dr{background:#fff3d6;color:#8a5a00}.pill.nc{background:#eceae4;color:#55544f}
.nv{display:flex;gap:8px;align-items:center;margin:12px 0}.nv button{font:600 14px Inter,sans-serif;padding:9px 16px;border-radius:10px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}.nv button.pr{background:#10a364;border-color:#10a364;color:#fff}.nv button:disabled{opacity:.4}
.cur{background:#f7f6f2;border-radius:10px;padding:10px;margin:8px 0}.cur code{font-size:12px}
ol{padding-left:22px;margin:6px 0}ol li{padding:5px 6px;border-radius:8px;cursor:pointer;margin:2px 0}ol li.on{background:#e6f4ec;font-weight:600}ol li:hover{background:#f1f0eb}
h3{font-size:13px;margin:14px 0 4px;text-transform:uppercase;letter-spacing:.04em;color:#6b6b67}ul{padding-left:18px;margin:4px 0}.tg{font-size:10.5px;color:#8a8984}
.stage{display:flex;align-items:center;justify-content:center;overflow:hidden;padding:12px}iframe{border:0;background:#fff;border-radius:18px;box-shadow:0 8px 30px rgba(0,0,0,.15)}
iframe.phone{width:400px;height:min(860px,calc(100vh - 60px))}iframe.desktop{width:100%;height:calc(100vh - 24px)}
@media(max-width:820px){.fh{order:1;border:0}.fp{display:flex;flex-direction:column;height:auto}.side{display:contents}.top{order:0;padding:12px 14px 4px}.stage{order:1}.side>*:not(.top){order:2;padding:0 14px}.stage{padding:0 0 12px}iframe.desktop{width:100%;height:72vh;border-radius:12px}}'''
def esc(t): return re.sub(r'(\[[^\]]+\])',r'<span class="tg">\1</span>',H.escape(t,quote=False))
FBR_WEAK=set()
def _ptitle(sc): return NOTES[sc]['title'] if sc in NOTES else sc
def _site_page(site): return site.split('@')[0].split('+')[0]
ROLE={**{k:'host' for k in ['host-approve','hosting','first-post','returning-post','project-builder']},**{k:'account' for k in ['safety','delete-account','settings-notify']}}
def _role(fid): return ROLE.get(fid,'joiner')
def branches_for(f,i):
    """Branch rows under step i (0-based): other flows that leave this site state differently, loops inside this flow, exits. [M1028]"""
    xs=f['sx']; nx=xs[i+1]['site'] if i+1<len(xs) else None; rows=[]
    for e in SG_ENTER[(f['id'],i)]:
        if e['same']: continue
        if _role(e['f'])!=_role(f['id']): continue
        g=FBY[e['f']]; j=e['j']; gx=g['sx']
        why=gx[j+1]['user'] if j+1<len(gx) else e['user']
        if len(why)<12 or why==e['user']: FBR_WEAK.add((f['id'],i+1,g['id'],why))
        rows.append(dict(k='flow',why=why,act=gx[j+1]['act'] if j+1<len(gx) else '',f=g['id'],n=g['name'],j=j+2,sc=_site_page(gx[j+1]['site']) if j+1<len(gx) else _site_page(e['next'] or ''),th=f"thumbs/{g['id']}-{j+2}.webp"))
    if nx:
        for k in range(i+1):
            if xs[k]['site']==nx and k!=i+1:
                rows.append(dict(k='loop',why=xs[i+1]['user'],act=xs[i+1]['act'],j=k+1,sc=_site_page(nx),th=f"thumbs/{f['id']}-{k+1}.webp")); break
    else:
        rows.append(dict(k='end',why='Done here',act='closes the tab or stays on this page',sc=_site_page(xs[i]['site'])))
    same=[dict(f=e['f'],n=FBY[e['f']]['name'],j=e['j']+1) for e in SG_ENTER[(f['id'],i)] if e['same'] and _role(e['f'])==_role(f['id'])]
    more=len([n for n in SG_NEXT[(f['id'],i)] if not n[3]])
    return rows,same,more
def diagram(f):
    """Horizontal branching diagram [M1029]: main path left-to-right; branch chips split below/above each step; loops arc back."""
    xs=f['sx']; fid=f['id']; n=len(xs); CW,NW,NH,CHW,CHH,CG,PX=138,52,112,132,38,6,10
    B=[branches_for(f,i) for i in range(n)]
    up=[[r for r in B[i][0] if r['k']=='flow'][1::2] for i in range(n)]; dn=[[r for r in B[i][0] if r['k']=='flow'][0::2] for i in range(n)]
    loops=[(i,r) for i in range(n) for r in B[i][0] if r['k']=='loop']
    LA=34 if loops else 8; UA=max([len(u) for u in up]+[0]); DA=max([len(d) for d in dn]+[0])
    y0=LA+(UA*(CHH+CG)+22 if UA else 6); HT=y0+NH+(DA*(CHH+CG)+26 if DA else 10); W=PX*2+n*CW
    cx=lambda i:PX+i*CW+CW//2
    h=''; sv=''
    for i,d in enumerate(xs):
        rows,same,more=B[i]; x=cx(i)
        cnt=len(same)+more; tip=('Same next step in: '+', '.join(q['n'] for q in same)+'. ' if same else '')+(f'+{more} other links from this page.' if more else '')
        h+=(f'<div class="dn" data-i="{i}" style="left:{x-NW//2-6}px;top:{y0}px"><span class="dsn">{i+1}</span><img loading="lazy" src="thumbs/{fid}-{i+1}.webp" alt="">'
            +(f'<a class="dbg" href="sitemap.html#{_site_page(d["site"])}" title="{H.escape(tip)}">+{cnt}</a>' if cnt else '')
            +f'<span class="dlb">{H.escape(_ptitle(f["steps"][i][0]))}</span></div>')
        if i+1<n: sv+=f'<path class="m" d="M{x+NW//2+2} {y0+50} L{cx(i+1)-NW//2-10} {y0+50}" marker-end="url(#am)"/>'
        for side,lst in (('d',dn[i]),('u',up[i])):
            for k,r in enumerate(lst):
                cxp=x+12; 
                ty=y0+NH+18+k*(CHH+CG) if side=='d' else y0-22-(k+1)*(CHH+CG)+CG
                h+=(f'<a class="dc" href="{r["f"]}.html#{r["j"]}" style="left:{x-CHW//2+18}px;top:{ty}px" title="{H.escape(r["why"])} — {H.escape(r["act"])} → {H.escape(r["n"])}, step {r["j"]}">'
                    f'<em>{H.escape(r["why"])}</em><span>{H.escape(r["n"])} · {r["j"]}</span><img class="dct" loading="lazy" src="{r["th"]}" alt=""></a>')
                if side=='d': sv+=f'<path class="b" d="M{x} {y0+NH-6} C{x} {ty-6} {x+18} {ty-14} {x+18} {ty}" marker-end="url(#ab)"/>'
                else: sv+=f'<path class="b" d="M{x} {y0+2} C{x} {ty+CHH+6} {x+18} {ty+CHH+14} {x+18} {ty+CHH}" marker-end="url(#ab)"/>'
    for i,r in loops:
        a_,b_=cx(i),cx(r['j']-1); mid=(a_+b_)//2
        sv+=f'<path class="l" d="M{a_-6} {y0} C{a_-6} 4 {b_+6} 4 {b_+6} {y0}" marker-end="url(#al)"/>'
        h+=f'<a class="dl" href="#{r["j"]}" data-go="{r["j"]-1}" style="left:{mid-90}px;top:0" title="{H.escape(r["act"])}">↺ {H.escape(r["why"])}</a>'
    defs='<defs>'+''.join(f'<marker id="{k}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="{c}"/></marker>' for k,c in (('am','#10a364'),('ab','#9b8ae0'),('al','#c98a1a')))+'</defs>'
    return f'<div class="dg" id="dg"><div class="dw" style="width:{W}px;height:{HT}px"><svg width="{W}" height="{HT}">{defs}{sv}</svg>{h}</div></div>'
DGCSS='''.dg{overflow-x:auto;background:#fbfaf7;border-bottom:1px solid #e4e2dc;padding:6px 0}.dw{position:relative;margin:0 auto}.dg svg{position:absolute;left:0;top:0;pointer-events:none}
path.m{stroke:#10a364;stroke-width:2;fill:none}path.b{stroke:#b9acec;stroke-width:1.6;fill:none}path.l{stroke:#c98a1a;stroke-width:1.6;fill:none;stroke-dasharray:4 3}
.dn{position:absolute;width:64px;padding:3px 6px;border-radius:12px;cursor:pointer;text-align:center}.dn img{width:52px;height:96px;object-fit:cover;object-position:top;border:2.5px solid #222;border-radius:9px;background:#fff;display:block}
.dn.on{background:#d6f0e2;box-shadow:0 0 0 2px #10a364}.dn:hover{background:#eef6f1}.dsn{position:absolute;left:-4px;top:-4px;width:20px;height:20px;border-radius:50%;background:#10a364;color:#fff;font:700 11px/20px Inter,sans-serif;z-index:1}
.dlb{position:absolute;left:50%;top:104px;transform:translateX(-50%);width:128px;font-size:10.5px;line-height:1.15;color:#55544f;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.dn.on .dlb{color:#0f7a4f;font-weight:700}
.dbg{position:absolute;right:-6px;top:-6px;font:700 9.5px/16px Inter,sans-serif;padding:0 5px;border-radius:99px;background:#eceae4;color:#55544f;text-decoration:none;border:1px solid #d7d5cf}
.dc{position:absolute;width:132px;height:38px;padding:3px 8px;border-radius:10px;background:#f3f0fd;border:1px solid #d9d0f7;text-decoration:none;display:flex;flex-direction:column;justify-content:center;overflow:visible}
.dc em{font-size:11px;color:#4b33b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-style:italic}.dc span{font-size:10px;color:#6b6b67;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.dc:hover{background:#fff;border-color:#9b8ae0;z-index:5}
.dct{display:none;position:absolute;left:100%;top:-30px;margin-left:6px;width:60px;height:130px;object-fit:cover;object-position:top;border:2px solid #222;border-radius:9px;background:#fff;box-shadow:0 6px 18px rgba(0,0,0,.2)}.dc:hover .dct{display:block}
.dl{position:absolute;width:180px;text-align:center;font-size:10.5px;color:#8a5a00;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;background:#fbfaf7}
.pl{display:grid;grid-template-columns:400px 1fr;overflow:hidden}.pl .side{overflow:auto}.pl .stage{overflow:hidden;align-items:flex-start;padding-top:12px}.dt{background:#f7f6f2;border-radius:12px;padding:12px;margin:8px 0}.dt .su{display:block;font-size:14px;color:#0f7a4f;font-style:italic;margin:4px 0}
.dt .sa{font-size:12.5px;color:#55544f}.dlg{font-size:11px;color:#6b6b67;padding:4px 16px}.dlg i{font-style:normal;display:inline-block;width:14px;height:3px;vertical-align:middle;margin:0 4px 0 10px}
@media(max-width:820px){.pl{display:flex;flex-direction:column;height:auto!important;overflow:visible}.pl .stage{order:0}.pl .side{order:1;padding:0 14px}}'''
def player(f):
    def _st(k,s): return {'u':surl(f,s),'sc':s[0],'ov':s[3].get('ov',''),'p':f"auth={s[1]} · live={s[2]}"+(f" · mode={s[3]['mode']}" if 'mode' in s[3] else '')+(f" · sheet={s[3]['ov']}" if 'ov' in s[3] else ''),'t':esc(s[4]),'us':H.escape(f['sx'][k]['user']),'ac':H.escape(f['sx'][k]['act'])}
    st=[_st(k,s) for k,s in enumerate(f['steps'])]
    s=f['start']; dev=s['device']; fid=f['id']
    rows=[r for r in conn_rows(fid) if _role(r[0])==_role(fid)]
    CONN=('<h3>Connected flows</h3><div class="cfs">'+''.join(f'<a class="cfc" href="{h}.html">{H.escape(FBY[h]["name"])} <i>{len(v["out"])}↗ {len(v["inn"])}↘</i></a>' for h,v in rows)+'</div>') if rows else ''
    sec=lambda h,k:(f'<h3>{h}</h3><ul>'+''.join(f'<li>{esc(b)}</li>' for b in f[k])+'</ul>') if f[k] else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flow · {H.escape(f['name'])} · PostUp mockups</title><style>{PCSS}{BRCSS}{DGCSS}{MVPCSS}</style></head><body>
<div class="top" style="padding:10px 16px 2px"><a href="index.html">← All flows</a> · <a href="../index.html#index">Mockups</a> · <a href="sitemap.html">Site map</a> &nbsp; <b style="font-size:16px">{H.escape(f['name'])}</b> <span class="pill{'' if f['pri']=='Phase 1' else ' nc'}">{f['pri']}</span><span class="pill{' dr' if f['status']=='draft' else ''}">{'Draft' if f['status']=='draft' else "Martin's example"}</span> {mvpc(fid)} <span class="meta">{MVPBAR0}</span></div>
<div class="dlg"><i style="background:#10a364"></i>main path · click a step<i style="background:#b9acec"></i>branches into another flow (click to open)<i style="background:#c98a1a"></i>loops back · <b>+N</b> = same next step in other flows / other links <span class="tg">[M1029]</span></div>
{diagram(f)}
<div class="pl"><div class="side"><div class="nv"><button id="bk" onclick="step(i-1)">Back</button><button id="nx" class="pr" onclick="step(i+1)">Next</button><span class="meta" id="pos"></span></div>
<div class="dt"><b id="ct"></b><span class="su" id="du"></span><span class="sa" id="da"></span><div class="meta" style="margin-top:6px"><code id="cp"></code> · <a id="cu" target="_blank">open with notes</a></div></div>
<p class="meta"><b>Persona:</b> {H.escape(f['persona'])}<br><b>Start:</b> auth={s['auth']} · live={s['live']} · {dev} · entry <code>{H.escape(s['url'])}</code><br><b>Goal:</b> {esc(f['goal'])}</p>
{CONN}{sec('Edge cases','branches')}{sec('Success','success')}{sec("Needs Martin's decision",'decide')}<p class="meta"><a href="{fid}.md">{fid}.md</a> · <a href="site.html">Site graph</a></p></div>
<div class="stage"><iframe id="fr" class="{dev}" title="Mockup step"></iframe></div></div>
<script>var S={json.dumps(st)},i=0,fr=document.getElementById("fr"),y=0;fr.addEventListener("load",function(){{scrollTo(0,y);setTimeout(function(){{scrollTo(0,y)}},300)}});
function un(s){{return s.replace(/&amp;/g,"&").replace(/&#x27;/g,"'").replace(/&quot;/g,'"')}}
function step(n){{if(n<0||n>=S.length)return;i=n;y=scrollY;var x=S[i];fr.className=x.u.indexOf("device=desktop")>0?"desktop":"phone";if(window.fitpl)fitpl();fr.src=x.u.replace("#","&notes=0&fs="+i+"#");
document.getElementById("ct").innerHTML=(i+1)+". "+x.t;document.getElementById("du").textContent="“"+un(x.us)+"”";document.getElementById("da").textContent="Got here: "+un(x.ac);document.getElementById("cp").textContent="#"+x.sc+" · "+x.p;document.getElementById("cu").href=x.u;
document.getElementById("pos").textContent="Step "+(i+1)+" of "+S.length;document.getElementById("bk").disabled=i==0;document.getElementById("nx").disabled=i==S.length-1;
document.querySelectorAll(".dn").forEach(function(l){{var on=+l.dataset.i===i;l.classList.toggle("on",on);if(on){{var g=document.getElementById("dg"),r=l.offsetLeft-g.clientWidth/2+32;if(r<g.scrollLeft||l.offsetLeft+64>g.scrollLeft+g.clientWidth)g.scrollTo({{left:r,behavior:"smooth"}})}}}});history.replaceState(null,"","#"+(i+1))}}
document.getElementById("dg").addEventListener("click",function(e){{var g=e.target.closest("[data-go]");if(g){{e.preventDefault();step(+g.dataset.go);return}}if(e.target.closest("a"))return;var l=e.target.closest(".dn");if(l)step(+l.dataset.i)}});
addEventListener("keydown",function(e){{if(e.key==="ArrowRight")step(i+1);if(e.key==="ArrowLeft")step(i-1)}});
function fitpl(){{var p=document.querySelector(".pl"),dk=innerWidth>820,av=dk?innerHeight-p.offsetTop-24:Math.round(innerHeight*.8);if(dk)p.style.height=Math.max(av<380?844*.45+40:0,innerHeight-p.offsetTop)+"px";var st=fr.style;st.transformOrigin="top center";if(fr.classList.contains("phone")){{var s=Math.min(1,Math.max(.45,av/844),(dk?9e9:innerWidth-8)/390);st.width="390px";st.height="844px";st.transform="scale("+s+")";st.marginBottom=(844*(s-1))+"px";st.marginLeft=st.marginRight=(390*(s-1)/2)+"px"}}else{{st.width="";st.height=Math.max(380,av)+"px";st.transform="";st.margin=""}}}}addEventListener("resize",fitpl);fitpl();
step(Math.max(0,Math.min(S.length-1,(parseInt(location.hash.slice(1))||1)-1)));</script>{MVPJS}</body></html>'''
for f in FLOWS: open(f'flows/{f["id"]}.html','w').write(player(f))
def _row(f): return f'<li data-ph="{1 if f["phase"]==1 else 0}" data-mvpf="{f["id"]}">{mvpc(f["id"])} <a href="{f["id"]}.html"><b>{H.escape(f["name"])}</b></a>{p1b(f["phase"]==1)} <span class="pill{"" if f["pri"]=="Phase 1" else " nc"}">{f["pri"]}</span>{"<span class=\"pill dr\">Draft</span>" if f["status"]=="draft" else "<span class=\"pill\">Martin&#39;s example</span>"}<div class="meta">{H.escape(f["persona"])} · start auth={f["start"]["auth"]}, live={f["start"]["live"]}, {f["start"]["device"]}, <code>{H.escape(f["start"]["url"])}</code> · {len(f["steps"])} steps</div></li>'
UGR=[("Newcomer (signed out, never used)","newcomer"),("Registered (signed in)","registered")]
rows=''.join(f'<h2>{t} <span class="meta">{sum(1 for f in FLOWS if f["user"]==u)} flows</span></h2><ol>'+''.join(_row(f) for f in FLOWS if f["user"]==u)+'</ol>' for t,u in UGR)+('<h2>Other</h2><ol>'+''.join(_row(f) for f in FLOWS if f["user"] not in ("newcomer","registered"))+'</ol>' if any(f["user"] not in ("newcomer","registered") for f in FLOWS) else '')

open('flows/index.html','w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flows · PostUp mockups</title><style>{PCSS} .wrap{{max-width:760px;margin:0 auto;padding:20px}} .wrap li{{margin:10px 0;cursor:default}}{MVPCSS}</style></head><body><div class="wrap"><a href="../index.html#index">← Mockups</a> · <a href="grid.html">All flows grid</a> · <a href="map.html">Flow map</a><h1>Critical flows</h1><p>{PHBTN} {MVPBAR}</p><p class="meta">{esc(HEAD)} · <a href="all.md">all.md</a></p>{rows}</div>{MVPJS}</body></html>''')
# all flows on one page: one cell per step (thumbs from gen/flowthumbs.mjs)
TAPS=json.load(open('flows/thumbs/taps.json')) if os.path.exists('flows/thumbs/taps.json') else {}
GCSS=PCSS+""".gf{scroll-margin-top:var(--gbh,70px)}.gb{position:sticky;top:0;z-index:5;background:rgba(244,243,239,.95);backdrop-filter:blur(6px);border-bottom:1px solid #e4e2dc;padding:10px 16px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.gb input{flex:1;min-width:160px;font:14px Inter,sans-serif;padding:8px 12px;border:1px solid #d7d5cf;border-radius:10px}.gb button{font:600 13px Inter,sans-serif;padding:7px 12px;border-radius:99px;border:1px solid #d7d5cf;background:#fff;cursor:pointer}.gb button.on{background:#10a364;color:#fff;border-color:#10a364}
.gb select{font:13px Inter,sans-serif;padding:7px;border-radius:10px;border:1px solid #d7d5cf;max-width:220px}.gw{max-width:1600px;margin:0 auto;padding:8px 16px 40px}
body{background:#d9d6ce}.gf{margin:22px 0 8px;scroll-margin-top:70px}.gf h2{font-size:18px;margin:0 0 2px}.gf h2 a{color:inherit;text-decoration:none}.gc{display:flex;flex-wrap:nowrap;gap:14px;margin:10px -16px 0;padding:6px 16px 14px;overflow-x:auto;scroll-snap-type:x proximity;scroll-padding:16px;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 16px,#000 calc(100% - 28px),transparent)}
.cell{flex:0 0 auto;scroll-snap-align:start;width:240px;background:#fff;border:1px solid #e4e2dc;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:box-shadow .15s}.cell:hover{box-shadow:0 6px 20px rgba(0,0,0,.12)}.cell.dk{width:480px}
.fr{margin:10px 10px 0;padding:7px;background:#16161a;border-radius:30px;box-shadow:0 4px 14px rgba(0,0,0,.28),inset 0 0 0 1px #3a3a40}.fr img{width:100%;aspect-ratio:390/844;object-fit:cover;object-position:top;background:#fff;display:block;border-radius:23px}.dk .fr{border-radius:10px;padding:0 0 0;background:#2a2a2f;overflow:hidden}.dk .fr i{display:flex;gap:5px;align-items:center;height:20px;padding:0 9px}.dk .fr i b{width:8px;height:8px;border-radius:50%;background:#ff5f57}.dk .fr i b+b{background:#febc2e}.dk .fr i b+b+b{background:#28c840}.dk .fr img{aspect-ratio:1280/800;border-radius:0}
.cb{padding:8px 10px 10px}.cn{font:700 11px Inter,sans-serif;color:#0f7a4f;letter-spacing:.03em;text-transform:uppercase}.ct{font-size:12.5px;margin-top:2px}.ctap{font-size:11px;color:#6b6b67;margin-top:4px}
@media(max-width:560px){.gf{scroll-margin-top:150px}.cell{width:190px}.cell.dk{width:330px}.gw{padding:4px 10px 30px}.gc{margin:8px -10px 0;padding:6px 10px 12px;gap:10px}}"""
def cell(f,i,st):
    sc,a,l,x,t=st; tp=TAPS.get(f'{f["id"]}-{i}'); dk=(x.get('device',f['start']['device'])=='desktop')
    nc=len(SG_ENTER[(f['id'],i-1)])
    tap=(f'<div class="ctap" title="other flows enterable here">⇄ {nc} flow{"s" if nc!=1 else ""} enterable here</div>' if nc else '')+(f'<div class="ctap">● taps {"Back" if tp["back"] else "“"+H.escape(tp["label"])+"”"}</div>' if tp else '')
    return f'<a class="cell{" dk" if dk else ""}" href="{f["id"]}.html#{i}"><div class="fr">{"<i><b></b><b></b><b></b></i>" if dk else ""}<img loading="lazy" src="thumbs/{f["id"]}-{i}.webp" alt="Step {i}: #{sc}" width="{480 if dk else 240}"></div><div class="cb"><div class="cn">{i} · {H.escape(NOTES[sc]["title"] if sc in NOTES else sc)}{" + "+x["ov"] if "ov" in x else ""}</div><div class="ct">{esc(t)}</div>{tap}<div class="meta" style="font-size:10.5px">auth={a} · live={l}{" · mode="+x["mode"] if "mode" in x else ""}</div></div></a>'
GSEC=''.join(f'<section class="gf" data-ph="{1 if f["phase"]==1 else 0}" data-mvpf="{f["id"]}" id="{f["id"]}" data-p="{"must" if f["pri"]=="Phase 1" else "nice"}" data-q="{H.escape((f["name"]+" "+f["persona"]+" "+" ".join(s[0]+" "+s[4] for s in f["steps"])).lower())}"><h2><a href="{f["id"]}.html">{H.escape(f["name"])}</a> {mvpc(f["id"])}</h2><div class="meta"><span class="pill{"" if f["pri"]=="Phase 1" else " nc"}">{f["pri"]}</span>{"<span class=\"pill dr\">Draft</span>" if f["status"]=="draft" else "<span class=\"pill\">Martin&#39;s example</span>"} {H.escape(f["persona"])} · start auth={f["start"]["auth"]}, live={f["start"]["live"]}, {f["start"]["device"]}, <code>{H.escape(f["start"]["url"])}</code> · {len(f["steps"])} steps</div><div class="gc">'+''.join(cell(f,i,st) for i,st in enumerate(f['steps'],1))+'</div></section>' for f in FLOWS)
JUMP=''.join(f'<option value="{f["id"]}">{H.escape(f["name"])}</option>' for f in FLOWS)
open('flows/grid.html','w').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All flows · grid · PostUp mockups</title><style>{GCSS}{MVPCSS}</style></head><body>
<div class="gb"><a href="../index.html#index">← Mockups</a><b>All flows</b><a href="map.html">Flow map</a><a href="site.html">Site graph</a><a href="sitemap.html">Site map</a><button data-p="all" class="on">All</button><button data-p="must">MVP must</button><button data-p="nice">Nice</button><input id="q" placeholder="Search flows, screens, steps" autocomplete="off"><select id="j"><option value="">Jump to flow…</option>{JUMP}</select><span class="meta" id="cnt"></span>{MVPBAR}</div>
<div class="gw"><p class="meta">{esc(HEAD)} Each cell is one step; the green ring marks what gets tapped next. Click a cell to open the player at that step.</p>{GSEC}</div>
<script>var P="all";function f(){{var q=document.getElementById("q").value.trim().toLowerCase(),n=0,c=0;document.querySelectorAll(".gf").forEach(function(s){{var m=(P=="all"||s.dataset.p==P)&&(!q||s.dataset.q.indexOf(q)>=0);s.hidden=!m;if(m){{n++;c+=s.querySelectorAll(".cell").length}}}});document.getElementById("cnt").textContent=n+" flows · "+c+" steps"}}
document.querySelectorAll(".gb button[data-p]").forEach(function(b){{b.onclick=function(){{P=b.dataset.p;document.querySelectorAll(".gb button[data-p]").forEach(function(x){{x.classList.toggle("on",x===b)}});f()}}}});
document.getElementById("q").oninput=f;document.getElementById("j").onchange=function(e){{var s=document.getElementById(e.target.value);if(s){{s.hidden=false;s.scrollIntoView()}}e.target.value=""}};f();</script>{MVPJS}</body></html>""")
sg_write()
exec(open('gen/states.py').read())
exec(open('gen/sitemap.py').read())
exec(open('gen/flowmap.py').read())
exec(open('gen/situmap.py').read())
# index + floating menu
FIX=''.join(ix(f'flows/{f["id"]}.html',f['name'],f"{f['pri']}{' · draft' if f['status']=='draft' else ''} · {len(f['steps'])} steps",'spark') for f in FLOWS)
S['index']=S['index'].replace('<h3 class="sh">Scenario</h3>',f'<h3 class="sh">Critical flows</h3><div class="grp"><a class="ixr" href="flows/index.html"><span class="ixi">{I("list",18)}</span><span class="lm"><b>All flows</b><span class="mu sm">Who arrives, in what situation, step by step</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/site.html"><span class="ixi">{I("list",18)}</span><span class="lm"><b>Site graph</b><span class="mu sm">Pages, site states and edges</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/explore.html"><span class="ixi">{I("image",18)}</span><span class="lm"><b>Site map + states</b><span class="mu sm">Click a screen on the map, see all its states beside it</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/states.html"><span class="ixi">{I("image",18)}</span><span class="lm"><b>Site states by screen</b><span class="mu sm">Every state a screen appears in, with links in and out</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/sitemap.html"><span class="ixi">{I("image",18)}</span><span class="lm"><b>Site map</b><span class="mu sm">Every page as a thumbnail, grouped by area, with links</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/map.html"><span class="ixi">{I("nav",18)}</span><span class="lm"><b>Flow map</b><span class="mu sm">How a first-time visitor reaches each flow</span></span>{I("chev",18,"mu")}</a><a class="ixr" href="flows/grid.html"><span class="ixi">{I("image",18)}</span><span class="lm"><b>All flows grid</b><span class="mu sm">Every step of every flow at once</span></span>{I("chev",18,"mu")}</a>{FIX}</div><h3 class="sh">Scenario</h3>',1)
assert 'Critical flows' in S['index']
FMENU='<div class="pmr pmfl"><label>Flows</label><div class="pmos">'+''.join(f'<a class="pmo pmf" href="flows/{f["id"]}.html" title="{H.escape(f["pri"])}">{H.escape(f["name"])}{" · P1" if f["phase"]==1 else ""}</a>' for f in FLOWS)+'<a class="pmo pmf" href="flows/grid.html"><b>All flows grid →</b></a><a class="pmo pmf" href="flows/map.html"><b>Flow map →</b></a><a class="pmo pmf" href="flows/sitemap.html"><b>Site map →</b></a><a class="pmo pmf" href="flows/site.html"><b>Site graph →</b></a><a class="pmo pmf" href="flows/index.html"><b>Flow list →</b></a></div></div>'
MENU_HTML=MENU_HTML.replace('<div class="pmr"><label>Sheets</label>',FMENU+'<div class="pmr"><label>Sheets</label>',1)
assert 'pmfl' in MENU_HTML
MENU_CSS+='.pmf{text-decoration:none;color:inherit;display:inline-block}'
print('flows',len(FLOWS))
