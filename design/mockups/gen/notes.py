# Notes beside each mockup. exec'd by build.py after more.py (needs S, OVS).
# Reads gen/notes.md + gen/sources/facts.jsonl; writes notes/<id>.md, notes/all.md, llms.txt;
# defines NOTES_HTML, NOTES_CSS, NOTES_JS for index.html.
import json, re, html as H, os
FACTS={}
for l in open('gen/sources/facts.jsonl'):
    l=l.strip()
    if l: d=json.loads(l); FACTS[d['id']]=d
REQ={m[1]:m[2] for m in re.finditer(r'^(\d+)\. \*\*(.+?)\*\*',open('gen/sources/requirements.md').read(),re.M)}
SRCNAME={'FS':'final-screens.md (final screens answer, Oct 2026)','TK':'mockup-takeaways.md (mockup session takeaways)','R':'requirements.md (requirements ledger)','drawn':'the mockup drawing itself','unsourced':'no source; confirm with Martin','M1018':'Martin, Oct 18 2026 (relayed by the PM): every page gets a scenario toggle (signed out/in × live nearby/none) and renders that scenario; pages that do not differ say "same in all scenarios"; mark the home page (/) clearly','M1018b':'Martin, Oct 18 2026 (relayed by the PM): Home (/) has two modes on one URL, Live (map + Live now) and Building (projects preview, See all projects, Post up, This week); default by whether anyone is live; Live · Building switch; banner when someone goes live in Building; draw the overlay-on-map version as #home-overlay-alt, alternative, not chosen','M1025':'Martin, Oct 25 2026 (relayed by the PM): a flow map, a state machine from a first-time visitor (not registered) showing how users reach the starting point of each flow','M1024':'Martin, Oct 24 2026 (relayed by the PM): keep tracking user types/scenarios and also track critical flows: a type of user arrives in a certain situation and goes through a scenario step by step; draft all important MVP flows','M1018c':'Martin, Oct 18 2026 (relayed by the PM): the Building heading is "What people are building" (not "nearby"); the list is sorted closest-first and shows the closest projects available even if none are local; never claim "nearby" unless they are'}
NOTES={}; ORDER=[]; cur=None; sec=None
for raw in open('gen/notes.md').read().split('-->',1)[1].splitlines():
    line=raw.rstrip()
    m=re.match(r'^## (\S+) \| (.+)$',line)
    if m: cur={'id':m[1],'title':m[2],'host':None,'secs':[]}; NOTES[m[1]]=cur; ORDER.append(m[1]); sec=None; continue
    if cur is None or not line.strip(): continue
    if line.startswith('host:'): cur['host']=line[5:].strip(); continue
    m=re.match(r'^### (.+)$',line)
    if m: sec=[m[1],[]]; cur['secs'].append(sec); continue
    if line.startswith('- ') and sec: sec[1].append(line[2:]); continue
    raise SystemExit(f'notes.md: cannot parse line: {line!r}')
G=NOTES.pop('_global'); ORDER.remove('_global')
# checks
BASE=[k for k in S if '--' not in k]
missing=[k for k in BASE if k not in NOTES]; extra=[k for k in ORDER if not k.startswith('ov-') and k not in S]
ovids=re.findall(r'id="ov-([\w-]+)"',OVS); missing+=['ov-'+o for o in ovids if 'ov-'+o not in NOTES]
if missing or extra: raise SystemExit(f'notes: missing {missing} extra {extra}')
TAG=r'\[(F\d{3}|FS|TK§\d|R\d+⚠?|drawn|unsourced|M1018[bc]?|M1024|M1025)\]'
def tags(t): return re.findall(TAG,t)
for n in [G]+[NOTES[k] for k in ORDER]:
    for s,bs in n['secs']:
        for b in bs:
            if not tags(b): raise SystemExit(f'notes: untagged bullet in {n["id"]}: {b}')
            for t in tags(b):
                if re.match(r'F\d',t) and t not in FACTS: raise SystemExit(f'notes: unknown fact {t}')
def unsourced(b): return '⚠' in b or '[unsourced]' in b
def tip(t):
    if re.match(r'F\d',t):
        d=FACTS[t]; who=d.get('speaker') or ''; return f'{d["gist"]} — {who}, {d["session"]}{" "+d["address"] if d.get("address") else ""}: “{d["quote"][:220]}”'
    if t.startswith('TK'): return SRCNAME['TK']+' '+t[2:]
    if t.startswith('R'): return SRCNAME['R']+' item '+t[1:].rstrip('⚠')+': '+REQ.get(t[1:].rstrip('⚠'),'')+(' (ledger marks it UNSOURCED)' if '⚠' in t else '')
    return SRCNAME.get(t,t)
def ihtml(b):
    e=H.escape(b,quote=False)
    e=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',e)
    e=re.sub(r'`#([\w-]+)`',r'<a class="nlk" href="#\1">#\1</a>',e)
    e=re.sub(r'`(.+?)`',r'<code>\1</code>',e)
    e=re.sub(TAG,lambda m:f'<span class="ntag{" nwarn" if ("⚠" in m[1] or m[1]=="unsourced") else ""}" title="{H.escape(tip(m[1]))}">{m[1]}</span>',e)
    return e
def scls(b):
    for pre,c in [('Signed out:','sc-out'),('Signed in:','sc-in'),('Live nearby:','sc-live'),('None live:','sc-none'),('Nothing this week:','sc-none')]:
        if b.startswith(pre): return c
    return ''
def body_html(n):
    return ''.join(f'<h4>{H.escape(s)}</h4><ul>'+''.join(f'<li class="{"nu " if unsourced(b) else ""}{scls(b)}">{ihtml(b)}</li>' for b in bs)+'</ul>' for s,bs in n['secs'])
def url(n, device='phone'):
    if n['id'].startswith('ov-'): return f'/mockups/?style=fresh&device={device}&ov={n["id"][3:]}#{n["host"]}'
    return f'/mockups/?style=fresh&device={device}#{n["id"]}'
def md_body(n, lvl='##'):
    return '\n'.join(f'{lvl} {s}\n'+'\n'.join(f'- {b}' for b in bs)+'\n' for s,bs in n['secs'])
def cited(ns):
    ts=[]
    for n in ns:
        for s,bs in n['secs']:
            for b in bs:
                for t in tags(b):
                    t=t.rstrip('⚠')
                    if t not in ts: ts.append(t)
    fs=sorted([t for t in ts if re.match(r'F\d',t)]); rs=sorted({t for t in ts if t.startswith('R')},key=lambda x:int(x[1:])); ot=[t for t in ['FS','M1018','M1018b','M1018c','M1024','M1025','drawn','unsourced'] if t in ts]+sorted(t for t in ts if t.startswith('TK'))
    out=[]
    for t in fs:
        d=FACTS[t]; out.append(f'- **{t}** — {d["gist"]} ({d.get("speaker") or "?"}, {d["session"]}{" "+d["address"] if d.get("address") else ""}): “{d["quote"].strip()[:400]}”')
    for t in rs: out.append(f'- **{t}** — requirements.md item {t[1:]}: {REQ.get(t[1:],"")}')
    for t in ot: out.append(f'- **{t}** — '+(SRCNAME['TK']+' §'+t[3:] if t.startswith('TK') else SRCNAME[t]))
    return '\n'.join(out)
LEGEND='Tags: F### = fact (Martin\'s words or an agreed answer), FS = final-screens.md, TK§n = mockup takeaways section, R# = requirements ledger item (⚠ = ledger marks it unsourced), drawn = shown in the mockup, unsourced = confirm with Martin. "Overrides" beat the drawing.'
GLOBAL_MD='## Global rules (every screen)\n'+md_body(G,'###')
os.makedirs('notes',exist_ok=True)
for f in os.listdir('notes'):
    if f.endswith('.md'): os.remove(os.path.join('notes',f))
def screen_md(n):
    host=f'\nShown over: #{n["host"]}' if n['host'] else ''
    return f'''# {n["title"]}
Screen id: `{n["id"]}`{host}
URL (phone): {url(n)}
URL (desktop): {url(n,"desktop")}
Styles: fresh (default), cozy, night, bold via ?style=
Scenario: ?auth=out|in&live=live|none (default out + live); see the Scenarios section

{LEGEND}

{md_body(n)}
'''
for k in ORDER:
    n=NOTES[k]
    open(f'notes/{k}.md','w').write(screen_md(n)+GLOBAL_MD+'\n## Sources cited\n'+cited([n,G])+'\n')
# demote section headings inside screens for all.md
def demote(n): return md_body(n,'###')
allmd=f'''# PostUp mockups — implementation notes (all screens)
Source of truth for building PostUp: the v1034 mockups plus these notes. Where a note says "Overrides", the note beats the drawing.
Mockup: /mockups/?style=<fresh|cozy|night|bold>&device=<phone|desktop>&auth=<out|in>&live=<live|none>#<screen>  (overlay sheets: &ov=<sheet>)
The home page (/) is `#home`, called Home: two modes on one URL, Live and Building (`?mode=live|building`); default by whether anyone's live. `#home-overlay-alt` is an alternative, not chosen. `#quiet` is the old no-live home drawing (not /); `#quiet-feed` / `#quiet-feed-b` are Nearby (/nearby).
Screens: {len([k for k in ORDER if not k.startswith("ov-")])} + {len([k for k in ORDER if k.startswith("ov-")])} overlay sheets.

{LEGEND}

{GLOBAL_MD}
'''
for k in ORDER:
    n=NOTES[k]; host=f' · shown over #{n["host"]}' if n['host'] else ''
    allmd+=f'\n---\n\n## {n["title"]} (`{k}`)\nURL: {url(n)}  ·  desktop: {url(n,"desktop")}{host}\n\n{demote(n)}'
allmd+='\n---\n\n## Sources cited\n'+cited([G]+[NOTES[k] for k in ORDER])+'\n'
open('notes/all.md','w').write(allmd)
llms=f'''# PostUp mockups

> Static mockups of the PostUp app (v1034): {len(BASE)} screens plus overlay sheets, four styles, phone and desktop. Each screen has implementation notes (purpose, behavior, links, states, copy, decisions with sources, and Overrides where a later decision beats the drawing). Read the notes with the screen.

Mockup URL pattern: /mockups/?style=<fresh|cozy|night|bold>&device=<phone|desktop>&auth=<out|in>&live=<live|none>#<screen> (overlays: &ov=<sheet>)
The home page (/) is #home, called Home, with two modes on one URL: Live and Building (?mode=live|building). #home-overlay-alt is an alternative, not chosen. #quiet is the old no-live home drawing; #quiet-feed / #quiet-feed-b are Nearby (/nearby). Project lists are headed "What people are building", sorted closest-first, showing the closest available even if none are local; never call them nearby unless they are (Martin, Oct 18).

## Notes
- [All screens in one file](notes/all.md): global rules, every screen, every source quote

## Screens
''' + '\n'.join(f'- [{k}](notes/{k}.md): {NOTES[k]["title"]}' for k in ORDER) + '\n'
open('llms.txt','w').write(llms)
UNSOURCED=[(n['id'],b) for n in [G]+[NOTES[k] for k in ORDER] for s,bs in n['secs'] for b in bs if unsourced(b)]
# ---------- in-page panel ----------
ND={k:{'t':NOTES[k]['title'],'h':body_html(NOTES[k]),'host':NOTES[k]['host']} for k in ORDER}
NOTES_HTML=f'''<aside class="notes" id="notes" aria-label="Screen notes"><div class="nh" onclick="ntog()"><b>Notes</b><span class="nid" id="nid"></span><span class="nsp"></span><a class="nmd" id="nmd" href="notes/index.md" onclick="event.stopPropagation()" target="_blank">.md</a><button class="nx" aria-label="Collapse notes"><span class="nxc">−</span></button></div>
<div class="nb2"><p class="nroute" id="nroute" hidden>Home page (/)</p><h3 id="nt"></h3><div id="nbody"></div><details class="ng"><summary>Global rules</summary>{body_html(G)}</details><p class="nlg">{H.escape(LEGEND)} · <a href="notes/all.md" target="_blank">all.md</a> · <a href="llms.txt" target="_blank">llms.txt</a></p></div></aside>
<script type="application/json" id="notes-data">{json.dumps(ND).replace("</","<\\/")}</script>'''
NOTES_CSS=open('gen/notes.css').read()
NOTES_JS=open('gen/notes.js').read()
print('notes',len(ORDER),'unsourced',len(UNSOURCED))
