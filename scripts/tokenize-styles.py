#!/usr/bin/env python3
"""Idempotent codemod: Tailwind palette classes -> PostUp design-token utilities.
Run from repo root: python3 tokenize.py [files...] (default: all src/**/*.svelte)."""
import re, sys, pathlib
NEUT='gray|slate|zinc|neutral|stone'
def color_for(util, fam, shade):
    s=int(shade) if shade else None
    if fam=='white': return {'bg':'surface','text':'on-brand','border':'surface'}.get(util,'surface')
    if fam=='black': return None  # scrims stay black
    if fam in NEUT.split('|'):
        if util=='bg': return 'bg' if s<=50 else 'surface-2' if s<=200 else 'line' if s<=400 else 'ink'
        if util in('text','placeholder','fill','stroke'):
            return 'surface' if s<=200 else 'subtle' if s<=400 else 'muted' if s<=600 else 'ink'
        return 'line'
    if fam in('blue','indigo','sky'):
        if util=='bg': return 'brand-soft' if s<=200 or s>=900 else 'brand' if s<=600 else 'brand-hover'
        return 'brand'
    if fam in('red','rose') and util!='bg' and util!='text': return 'danger'
    if fam=='red': return ('danger-soft' if s<=200 else 'danger') if util=='bg' else 'danger'
    if fam in('green','emerald','lime','teal'):
        if util=='bg': return 'brand-soft' if s<=200 or s>=900 else 'live'
        return 'live'
    # rose/purple/amber/... category chips
    if util=='bg': return 'brand-soft' if s<=200 or s>=900 else 'brand'
    if util=='text': return 'ink'
    return 'line'
UT=r'(bg|text|border(?:-[trblxy])?|ring(?:-offset)?|divide|placeholder|fill|stroke|from|to|via|outline|accent|decoration)'
COL=r'(white|black|(?:'+NEUT+r'|blue|indigo|sky|red|rose|green|emerald|purple|violet|amber|yellow|orange|teal|lime|pink|cyan|fuchsia)-(\d{2,3}))'
RX=re.compile(r'(?<![\w\-/])((?:[a-z\-]+:)*)'+UT+'-'+COL+r'(/\d+)?(?![\w\-])')
DARK=re.compile(r'(?<![\w\-])dark:[^\s"\'`}]+[ \t]?')
HEX={'color: white;':'color: var(--pu-accent-text);','#2563eb':'var(--pu-accent)','#555':'var(--pu-muted)','#666':'var(--pu-muted)','#888':'var(--pu-subtle)'}
def sub(m):
    pre,util,col,shade,op=m.groups()
    fam=col.split('-')[0]; base=util.split('-')[0]
    t=color_for(base if base not in('ring','border') else ('ring' if base=='ring' else 'border'),fam,shade)
    if t is None: return m.group(0)
    return f'{pre}{util}-{t}{op or ""}'
# Tailwind palette hex (used in <style> blocks and inline style strings) -> tokens.
TWHEX={'f9fafb':'bg','f3f4f6':'surface-2','e5e7eb':'border','d1d5db':'border','9ca3af':'subtle','6b7280':'muted','4b5563':'muted',
 '374151':'text','1f2937':'text','111827':'text','eff6ff':'accent-soft','dbeafe':'accent-soft','bfdbfe':'accent-soft','93c5fd':'accent','60a5fa':'accent','3b82f6':'accent','2563eb':'accent',
 '1d4ed8':'accent-hover','1e40af':'accent-hover','059669':'live','10b981':'live','16a34a':'live','22c55e':'live','047857':'live','d1fae5':'accent-soft','ecfdf5':'accent-soft',
 'dc2626':'danger','ef4444':'danger','b91c1c':'danger','fee2e2':'danger-soft','fef2f2':'danger-soft'}
HEXRX=re.compile(r'(?<!=")(?<!=\')#('+'|'.join(TWHEX)+r')\b',re.I)
def strip_dark_media(s):
    out=''; i=0
    while True:
        j=s.find('@media (prefers-color-scheme: dark)',i)
        if j<0: return out+s[i:]
        k=s.index('{',j); depth=1; k+=1
        while depth:
            depth+= {'{':1,'}':-1}.get(s[k],0); k+=1
        out+=s[i:j].rstrip(' \t'); i=k
def run(p):
    s=p.read_text(); o=s
    s=strip_dark_media(s); s=HEXRX.sub(lambda m:'var(--pu-'+TWHEX[m.group(1).lower()]+')',s)
    s=re.sub(r'background(-color)?:\s*(white|#fff(fff)?)\b',lambda m:'background'+(m.group(1) or '')+': var(--pu-surface)',s)
    s=DARK.sub('',s); s=RX.sub(sub,s); s=s.replace('bg-opacity-50','')
    for k,v in HEX.items(): s=s.replace(k,v) if p.name=='Map.svelte' else s
    if p.name=='Map.svelte':
        s=s.replace("return window.matchMedia('(prefers-color-scheme: dark)').matches;","return document.documentElement.dataset.theme === 'night';")
        s=s.replace("const handleChange = (e: MediaQueryListEvent) => {\n\t\t\tupdateTileLayer(e.matches);","const handleChange = () => {\n\t\t\tupdateTileLayer(isDarkMode());")
        s=s.replace("(e: MediaQueryListEvent) => updateTileLayer(e.matches)","() => updateTileLayer(isDarkMode())")
        if 'themeObserver' not in s and 'updateTileLayer(darkMode);' in s:
            s=s.replace("updateTileLayer(darkMode);","updateTileLayer(darkMode);\n\t\t// Basemap follows the active style (Night = dark tiles).\n\t\tconst themeObserver = new MutationObserver(() => updateTileLayer(isDarkMode()));\n\t\tthemeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });",1)
    s=re.sub(r'class="([^"]*?)\s+"',lambda m:'class="'+m.group(1)+'"',s)
    if s!=o: p.write_text(s); print('tokenized',p)
files=[pathlib.Path(f) for f in sys.argv[1:]] or [p for p in pathlib.Path('src').rglob('*.svelte') if 'stories' not in p.parts]
for f in files: run(f)
