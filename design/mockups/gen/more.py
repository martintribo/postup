# Extra screens + fixes (Oct 14 review decisions). exec'd by build.py after base screens.
import re
P['ME']=('Sam','#10a364')
IC.update({'more':'<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
 'inbox':'<path d="M4 4h16v12H8l-4 4z"/>','gear':'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
 'flag':'<path d="M5 21V4h11l-1.5 4L16 12H5"/>','ban':'<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>','send':'<path d="M4 12 20 4l-6 16-3-7z"/>',
 'bell':'<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>','search':'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>','wifi':'<path d="M2 8.5a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8.5 15.5a5 5 0 0 1 7 0"/><path d="M12 19h.01"/><path d="M3 3l18 18"/>',
 'refresh':'<path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/>','msg':'<path d="M4 5h16v11H9l-5 4z"/>','ext':'<path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/>'})
NB=f'<button class="ib" onclick="bk()" aria-label="Back">{I("back",22)}</button>'
def nav(a):
    it=[('#home','map','Map','m'),('#quiet-feed','list','Nearby','n'),None,('#projects','folder','Projects','p'),('#inbox','inbox','Inbox','i')]
    h='<nav class="tab t5">'
    for x in it:
        if x is None: h+=f'<a href="#post" class="tp">{I("plus",22)}<span>Post up</span></a>'; continue
        hr,ic,t,k=x; dot='<i class="bdg"></i>' if k=='i' else ''
        h+=f'<a href="{hr}" class="{"on" if a==k else ""}">{dot}{I(ic,22)}<span>{t}</span></a>'
    return h+'</nav>'
TAB={'home':'m','quiet':'m','cafe':'m','postup':'m','joined':'m','posted':'','quiet-feed':'n','quiet-feed-b':'n','projects':'p','project':'p'}
for k,a in TAB.items(): S[k]=re.sub(r'<nav class="tab">.*?</nav>',nav(a),S[k],flags=re.S)
# root tabs: no back
for k in ['quiet-feed','quiet-feed-b','projects']: S[k]=S[k].replace(NB,'<span class="ib"></span>',1)
# feed: names -> profile, welcome strip
WEL=f'<div class="welcome" id="wel-{{}}"><span class="ci sm">{I("coffee",16)}</span><p>Post up at a cafe. See who\'s working nearby.</p><button class="ib" onclick="this.parentNode.remove()" aria-label="Dismiss">{I("x",18)}</button></div>'
for k in ['quiet-feed','quiet-feed-b']:
    S[k]=re.sub(r'<div class="fh">(<span class="av")',r'<div class="fh lk2" onclick="go(\'profile\')">\1',S[k])
    S[k]=S[k].replace('<div class="hero">',WEL.format(k)+'<div class="hero">',1)
    S[k]=S[k].replace(f'<a class="ib" href="#quiet" aria-label="Map">',f'<a class="ib" href="#me" aria-label="Profile">{av("ME",30)}</a><a style="display:none" href="#quiet">',1)
# share / directions / leave / more
S['cafe']=S['cafe'].replace('onclick="go(\'posted\')" aria-label="Share"','onclick="ov(\'share\')" aria-label="Share"')
S['postup']=S['postup'].replace(f'<button class="ib" onclick="go(\'posted\')" aria-label="Share">{I("share",20)}</button>',f'<button class="ib" onclick="ov(\'share\')" aria-label="Share">{I("share",20)}</button><button class="ib" onclick="ov(\'more\')" aria-label="More">{I("more",20)}</button>')
S['postup']=S['postup'].replace('<div class="who">{}'.format(av('MK',64)),'<div class="who lk2" onclick="go(\'profile\')">'+av('MK',64))
S['postup']=S['postup'].replace('<p class="mu sm">'+stack(['JR'],22)+' Jon is joining</p>','<p class="mu sm">'+stack(['JR'],22)+' Jon is joining · Anyone can join</p>')
S['join-signin']=S['postup']+signin('join-signin','Join Maya','Sign in so Maya knows who\'s coming.','joined')
S['joined']=S['joined'].replace('<button class="btn" onclick="go(\'cafe\')">','<a class="btn sec" href="#chat">'+I("msg",18)+' Group chat</a><button class="btn" onclick="ov(\'dirs\')">')
S['joined']=S['joined'].replace('<a class="lnk dg" href="#postup">Leave</a>','<a class="lnk dg" href="#" onclick="event.preventDefault();ov(\'leave\')">Leave</a>')
S['posted']=S['posted'].replace('<a class="lnk" href="#home">Back to map</a>','<a class="lnk" href="#live">Manage postup</a><a class="lnk" href="#home">Map</a>')
S['posted']=S['posted'].replace('onclick="this.innerHTML=\'Link shared\'"','onclick="ov(\'share\')"')
S['project-attach']=S['project-attach'].replace('onclick="go(\'posted\')">Post up</button>','onclick="go(\'attach-signin\')">Post up '+LOCK+'</button>').replace("seg(['Now','Earlier today']","seg(['Now','I was here earlier']").replace('Earlier today','I was here earlier')
S['attach-signin']=S['project-attach']+signin('attach-signin','Almost there','Sign in to post up for this project.','posted')
S['project']=S['project'].replace('by <span class="cl" onclick="go(\'postup\')">Maya</span>','by <span class="cl" onclick="go(\'profile\')">Maya</span>')
# projects filter
fl=['nearby following','nearby','nearby following','nearby']
parts=S['projects'].split('<article class="fc pc"')
S['projects']=parts[0]+''.join(f'<article data-f="{fl[i]}" class="fc pc"'+p for i,p in enumerate(parts[1:]))
S['projects']=S['projects'].replace('<div class="chips pchips">','<div class="chips pchips" onclick="pfilter(event)">').replace('<button class="chip on">Nearby</button><button class="chip">Following</button><button class="chip">Mine</button>','<button class="chip on" data-f="nearby">Nearby</button><button class="chip" data-f="following">Following</button><button class="chip" data-f="mine">Mine</button>')
S['projects']=S['projects'].replace('</div></div><nav',f'<div class="estate pempty" hidden><span class="ci pj">{I("folder",22)}</span><h2>No projects yet</h2><p class="mu">Add what you\'re working on so people know what to ask about.</p><a class="btn" href="#project-new">{I("plus",18)} New project {LOCK}</a></div></div></div><nav',1)
# post form: where sheet + join setting
S['post']=S['post'].replace('<div class="field" onclick="cyc()">','<div class="field" onclick="go(\'where\')">')
S['post']=S['post'].replace("<label>Until</label>"+seg(['1h','2h','3h','4pm'],'2h','u'),"<label>Until</label>"+seg(['1h','2h','3h','4pm'],'2h','u')+"<label>Who can join</label>"+seg(['Anyone can join','Ask to join'],'Anyone can join','j')+'<p class="mu xs">You\'ll get an alert whenever someone joins.</p>')
S['post-signin']=S['post']+signin('post-signin','Almost there','Sign in and your postup goes live.','posted')
def cafe_row(n,d,extra=''):
    return f'<button class="lrow wr" onclick="pick(\'{n}\',\'{d}\')"><span class="ci sm">{I("coffee",16)}</span><div class="lm"><b>{n}</b><span class="l2">{d}{extra}</span></div></button>'
def where(q):
    if q: lst=f'<p class="sh">Results</p>'+cafe_row('Sunbeam Coffee','1.6 mi · Abbot Kinney')+cafe_row('Sunset Roasters','2.3 mi · Mar Vista')+'<p class="gattr">powered by <b>Google</b></p>'
    else: lst='<p class="sh">Nearby</p>'+cafe_row('Bean Theory','0.4 mi',' · 2 live')+cafe_row('Lantern Tea','0.8 mi')+cafe_row('Grindhouse','1.1 mi')+cafe_row('Sunbeam Coffee','1.6 mi')
    val=' value="sun"' if q else ''
    return S['post']+f'''<div class="dim" onclick="bk()"></div><div class="bs tall"><span class="grab"></span><h2>Where are you?</h2>
<label class="srch">{I("search",18)}<input class="in" placeholder="Search cafes"{val} onclick="go('where-search')" oninput="if(this.value)go('where-search')"></label>{lst}</div>'''
S['where']=where(False); S['where-search']=where(True)
S['post-edit']=S['post'].replace('<b>Post up</b>','<b>Edit postup</b>',1).replace('onclick="sheet(\'post-signin\')">Post up '+LOCK+'</button>','onclick="go(\'live\')">Save</button>')

# ---------- live (manage) ----------
S['live']=f'''{top("You're live",f'<button class="ib" onclick="ov(\'share\')" aria-label="Share">{I("share",20)}</button>')}<div class="pad">
<div class="card livec"><div class="ring" style="--p:.58"><b>1:42</b><span class="xs mu">left</span></div><div class="lm"><b>Bean Theory</b><span class="mu sm">Till 3:45pm</span><span class="tag" onclick="go('project')">Star Fox 64 mod</span></div></div>
<div class="row2"><button class="btn sec" onclick="this.innerHTML='Till 4:15pm ✓'">{I("clock",16)} +30 min</button><a class="btn sec" href="#post-edit">{I("edit",16)} Edit</a></div>
<label class="lab">Who can join</label>{seg(['Anyone can join','Ask to join'],'Ask to join','j')}
<div class="sp-h"><h2>Requests</h2><span class="mu sm">1</span></div>
<div class="card req"><div class="fh lk2" onclick="go('profile')">{av('DN',36)}<b>Dev</b><span class="mu sm">· 2 min ago</span></div><p>"Also making a game — would love to compare notes."</p>
<div class="row2"><button class="btn sec" onclick="this.closest('.req').innerHTML='<p class=mu>Declined</p>'">Decline</button><button class="btn" onclick="this.closest('.req').innerHTML='<p class=ok>Dev can join ✓</p>'">Approve</button></div></div>
<div class="sp-h"><h2>Joined</h2><span class="mu sm">1</span></div>
<div class="lrow card" onclick="go('profile')">{av('JR',40)}<div class="lm"><b>Jon</b><div class="l2">On the way · 10 min</div></div>{I("chev",18,"mu")}</div>
<a class="btn sec" href="#chat">{I("msg",18)} Group chat</a>
<button class="tx dg" onclick="ov('endlive')">End postup</button></div>{nav("")}'''

# ---------- ask to join ----------
pa=f'''{top("Postup",f'<button class="ib" onclick="ov(\'share\')" aria-label="Share">{I("share",20)}</button><button class="ib" onclick="ov(\'more\')" aria-label="More">{I("more",20)}</button>')}<div class="pad">
<div class="who lk2" onclick="go('profile')">{av('TS',64)}<div><h1>Tess</h1><p class="ok"><span class="dot"></span> Live · till 3pm</p></div></div>
<div class="card" onclick="go('project')"><div class="ch"><span class="tag">Pixel Garden</span>{I("chev",18,"mu")}</div><p>Drawing crop sprites. Quiet focus session, but say hi.</p></div>
<div class="lrow card" onclick="go('cafe')"><span class="ci">{I("coffee",20)}</span><div class="lm"><b>Grindhouse</b><div class="l2">1.1 mi · 22 min walk</div></div>{I("chev",18,"mu")}</div>
<p class="mu sm">{I("lock",14)} Tess approves who joins</p></div>
<div class="cta"><button class="btn" onclick="go('ask-signin')">Ask to join {LOCK}</button></div>'''
S['postup-ask']=pa
S['ask-signin']=pa+signin('ask-signin','Ask Tess','Sign in so Tess knows who\'s asking.','ask')
S['ask']=pa+f'''<div class="dim" onclick="bk()"></div><div class="bs"><span class="grab"></span><h2>Ask to join</h2><p class="mu">Tell Tess a little about you. She'll get an alert.</p>
<textarea class="in" rows="3">Working on a pixel game too — happy to share tips.</textarea><button class="btn" onclick="go('requested')">{I("send",18)} Send request</button><button class="tx" onclick="bk()">Cancel</button></div>'''
S['requested']=f'''{top("",f'<a class="ib" href="#home" aria-label="Close">{I("x",22)}</a>',back=False)}<div class="pad done">
<div class="okc">{I("send",30)}</div><h1>Request sent</h1><p class="mu">Tess gets an alert and can say yes or no.<br>We'll let you know.</p>
<a class="btn" href="#quiet-feed">See who else is nearby</a><div class="lnks"><a class="lnk" href="#postup-ask">View postup</a><a class="lnk dg" href="#postup-ask">Cancel request</a></div></div>{nav("")}'''

# ---------- postup states ----------
def pstate(id,title,sub):
    return f'''{top("Postup",f'<button class="ib" onclick="ov(\'more\')" aria-label="More">{I("more",20)}</button>')}<div class="pad">
<div class="who lk2 dimmed" onclick="go('profile')">{av('MK',64)}<div><h1>Maya</h1><p class="mu">Bean Theory</p></div></div>
<div class="estate"><span class="ci">{I("clock",22)}</span><h2>{title}</h2><p class="mu">{sub}</p><a class="btn" href="#quiet-feed">See what's nearby</a><button class="btn sec" onclick="follow(this,'Follow Maya')">Follow Maya for next time</button><a class="lnk sm" href="#home">Go to Home</a></div></div>{nav("m")}'''
S['postup-ended']=pstate('postup-ended','This postup ended','Maya wrapped up at 4pm.')
S['postup-full']=pstate('postup-full','This postup is full','Maya isn\'t taking more people right now.')
S['postup-cancelled']=pstate('postup-cancelled','Maya cancelled this postup','Plans change. Others are working nearby.')

# ---------- invite landing ----------
S['invite']=f'''<header class="nb"><span class="ib"></span><b class="brand2">{I("coffee",16)} postup</b><span class="nr"></span></header><div class="pad done inv">
<div class="pair">{av('MK',72)}</div><h1>Maya is working at Bean Theory till 4. Join her?</h1>
<p><span class="tag" onclick="go('project')">Star Fox 64 mod</span></p>
<button class="btn" onclick="go('join-signin')">Join Maya {LOCK}</button><a class="btn sec" href="#cafe">{I("pin",16)} Bean Theory · 0.4 mi</a>
<p class="mu sm">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p></div>'''
S['invite-ended']=f'''<header class="nb"><span class="ib"></span><b class="brand2">{I("coffee",16)} postup</b><span class="nr"></span></header><div class="pad done inv">
<div class="pair dimmed">{av('MK',72)}</div><h1>This postup ended</h1><p class="mu">Maya was at Bean Theory earlier today.</p>
<a class="btn" href="#quiet-feed">See what's nearby</a><button class="btn sec" onclick="follow(this,'Follow Maya')">Follow Maya for next time</button><a class="lnk sm" href="#home">Go to Home</a>
<p class="mu sm">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p></div>'''

# ---------- empty area ----------
ep=pin_cafe(30,36)+pin_cafe(66,54)+pin_cafe(50,22)
S['empty-area']=f'''<div class="hm">{mapblock("380px",ep,f'<div class="mtop"><span class="brand">{I("pin",16)} Echo Park</span><a class="ib fl" href="#me" aria-label="Profile">{av("ME",30)}</a></div>')}
<section class="sheet-p"><span class="grab"></span><div class="sp-h"><h2>Nobody's live nearby</h2></div><p class="mu sm">No one is posted up around Echo Park right now. Here's what people did nearby lately.</p>
<h3 class="sh">Recently nearby</h3><div class="grp"><div class="lrow" onclick="go('profile')">{av('MK',32)}<div class="lm"><b class="sm">Maya posted up at Bean Theory</b><span class="xs mu">Tue · 3 joined</span></div></div><div class="lrow" onclick="go('profile')">{av('JR',32)}<div class="lm"><b class="sm">Jon posted up at Lot 1 Coffee</b><span class="xs mu">Mon · 2 joined</span></div></div></div>
<h3 class="sh">Be the first here today</h3>
{cafe_row('Stories Cafe','0.3 mi').replace("pick(","postAt(")}{cafe_row('Lot 1 Coffee','0.6 mi').replace("pick(","postAt(")}
<button class="btn" onclick="go('post')">{I("plus",18)} Post up</button></section></div>{nav("m")}'''

# ---------- cafe google fail ----------
S['cafe-gfail']=S['cafe'].replace(re.search(r'<div class="gcard">.*?</div></div></div>',S['cafe'],re.S).group(0),
 f'<div class="gcard fail"><div class="gph">{I("image",22)}</div><div class="lm"><b class="sm">Details unavailable</b><span class="mu xs">Couldn\'t load photos and hours right now.</span><span class="row3"><a class="lnk xs" href="#" onclick="event.preventDefault();ov(\'dirs\')">{I("ext",12)} Open in Maps</a><a class="lnk xs" href="#cafe">{I("refresh",12)} Retry</a></span></div></div>')

# ---------- loading / offline ----------
sk='<article class="fc skel"><div class="fm sh1"></div><div class="fbd"><i class="sk w40"></i><i class="sk w80"></i><i class="sk w60"></i></div></article>'
S['loading']=f'''{top("Nearby")}<div class="pad fd"><div class="hero"><i class="sk w70 h28"></i><i class="sk w50"></i></div>{sk*3}</div>{nav("n")}'''.replace(NB,'<span class="ib"></span>',1)
S['offline']=S['quiet-feed'].replace('<div class="welcome"',f'<div class="offl">{I("wifi",16)}<span>You\'re offline · showing what we had</span><a class="lnk sm" href="#quiet-feed">Retry</a></div><div hidden class="welcome"',1).replace('id="wel-quiet-feed"','')

# ---------- chat / inbox / activity ----------
def msg(k,t,time,me=False):
    if me: return f'<div class="mg me"><p>{t}</p><span class="xs mu">{time}</span></div>'
    n,c=P[k]
    return f'<div class="mg">{av(k,30)}<div><span class="xs mu"><b>{n}</b> · {time}</span><div class="bub"><p>{t}</p><button class="ib xs2" onclick="ov(\'msg\')" aria-label="Message options">{I("more",16)}</button></div></div></div>'
S['chat']=f'''{top("Maya's postup",f'<button class="ib" onclick="ov(\'more\')" aria-label="More">{I("more",20)}</button>')}
<div class="chhd" onclick="go('postup')">{stack(['MK','JR','ME'],22)}<span class="sm">Bean Theory · till 4pm · 3 people</span>{I("chev",16,"mu")}</div>
<div class="pad chat"><p class="xs mu ctr">Only people in this postup can see this chat.</p>
{msg('MK','Hey! Here till 4 — come say hi.','2:05pm')}{msg('JR','On my way, about 10 min.','2:09pm')}{msg('ME','See you soon!','2:11pm',True)}{msg('MK','Grabbing another coffee if anyone wants one ☕','2:20pm')}</div>
<div class="cbar"><input class="in" placeholder="Message"><button class="btn sq" aria-label="Send">{I("send",18)}</button></div>'''
def ihead(on):
    return f'''{top("Inbox",'',back=False)}<div class="pad"><div class="seg lnkseg"><a href="#inbox" class="{"on" if on=="c" else ""}">Chats</a><a href="#activity" class="{"on" if on=="a" else ""}">Activity <i class="bdg2">2</i></a></div>'''
S['inbox']=ihead('c')+f'''<div class="grp">
<div class="lrow" onclick="go('chat')">{av('MK',44)}<div class="lm"><b>Maya's postup</b><div class="l2">Maya: Grabbing another coffee…</div></div><span class="xs mu">2:20</span></div>
<div class="lrow" onclick="go('chat')">{av('ME',44)}<div class="lm"><b>Your postup</b><div class="l2">Jon: On the way</div></div><span class="xs mu">1:58</span></div>
<div class="lrow dimmed" onclick="go('postup-ended')">{av('TS',44)}<div class="lm"><b>Tess's postup</b><div class="l2">Ended · Tue</div></div><span class="xs mu">Tue</span></div></div></div>{nav("i")}'''
# Phase 1 Inbox: ONE list, no tabs [M1033]. Rows = postup chats newest first, unread dot; postup alerts show in the row preview (system lines in that chat) or as their own row when not tied to a chat.
def irow(k,title,prev,time,dest,unread=False,dim=False,sysl=''):
    s=f'<span class="sysl">{sysl}</span> · ' if sysl else ''
    u='<i class="udot"></i>' if unread else ''
    return f'<div class="lrow{" dimmed" if dim else ""}" onclick="go(\'{dest}\')">{av(k,44)}<div class="lm"><b>{title}</b><div class="l2">{s}{prev}</div></div><span class="ir"><span class="xs mu">{time}</span>{u}</span></div>'
S['inbox-one']=f'''{top("Inbox",'',back=False)}<div class="pad"><div class="grp">
{irow('MK',"Maya's postup · Bean Theory","Maya: Grabbing another coffee…",'2:20','chat',True)}
{irow('ME',"Your postup · Lot 1 Coffee","Jon: On the way",'1:58','chat',True,sysl='Jon joined')}
{irow('TS',"Tess's postup · Grindhouse","Tess: Thanks all!",'Tue','postup-ended',dim=True,sysl='Postup ended')}
</div></div>{nav("i")}'''
def act(k,txt,time,dest,ic):
    return f'<div class="lrow" onclick="go(\'{dest}\')">{av(k,40)}<div class="lm"><span class="sm">{txt}</span><span class="xs mu">{time}</span></div><span class="ixi">{I(ic,16)}</span></div>'
S['activity']=ihead('a')+'<div class="grp">'+act('MK','<b>Maya</b> posted up at Bean Theory','Just now','postup','coffee')+act('DN','<b>Dev</b> asked to join your postup','2 min ago','live','users')+act('JR','<b>Jon</b> joined your postup','14 min ago','live','check')+act('MK','<b>Maya</b>: Hey! Here till 4 — come say hi.','20 min ago','chat','msg')+act('TS','<b>Tess</b> said yes to your request','Yesterday','postup-ask','check')+act('AL','<b>Ari</b> followed you','Mon','profile','users')+f'</div></div>{nav("i")}'

# Inbox has two phase versions [M1035]: phase 1 = one list (was #inbox-one, [M1033]); phase 2 = Chats | Activity tabs.
_TOP=top("Inbox",'',back=False); _NV=nav("i")
assert S['inbox'].startswith(_TOP) and S['inbox'].endswith(_NV) and S['inbox-one'].startswith(_TOP) and S['inbox-one'].endswith(_NV)
S['inbox']=_TOP+'<div class="p1only">'+S['inbox-one'][len(_TOP):-len(_NV)]+'</div><div class="p2only">'+S['inbox'][len(_TOP):-len(_NV)]+'</div>'+_NV
del S['inbox-one']
# ---------- profiles ----------
def ppast(d,c,w): return f'<div class="lrow" onclick="go(\'cafe\')"><span class="ci sm">{I("coffee",16)}</span><div class="lm"><b class="sm">{w}</b><span class="l2">{c} · {d}</span></div></div>'
def prof(k,me):
    n,c=P[k]
    right=f'<a class="ib" href="#settings" aria-label="Settings">{I("gear",20)}</a>' if me else f'<button class="ib" onclick="ov(\'more\')" aria-label="More">{I("more",20)}</button>'
    live=(f'<a class="card livec sm2c" href="#live"><div class="ring sm" style="--p:.58"><b>1:42</b></div><div class="lm"><b>You\'re live at Bean Theory</b><span class="mu sm">Till 3:45pm · 1 request</span></div>{I("chev",18,"mu")}</a>' if me else
          f'<a class="card livec sm2c" href="#postup"><span class="dot"></span><div class="lm"><b>Live at Bean Theory</b><span class="mu sm">Till 4pm · Star Fox 64 mod</span></div>{I("chev",18,"mu")}</a>')
    bio='Building a tide clock. Mornings at Lantern Tea.' if me else 'Making a Star Fox 64 fan mod. Weekday mornings at Bean Theory.'
    act=f'<a class="btn sec" href="#me">{I("edit",16)} Edit profile</a>' if me else f'<button class="btn" onclick="this.classList.toggle(\'sec\');this.textContent=this.classList.contains(\'sec\')?\'Following\':\'Follow\'">Follow</button>'
    projs=(f'<div class="lrow" onclick="go(\'project-new\')"><span class="ci sm pj">{I("folder",16)}</span><div class="lm"><b class="sm">Tide Clock</b><span class="l2">Updated Sun</span></div></div>' if me else
           f'<div class="lrow" onclick="go(\'project\')"><span class="ci sm pj">{I("folder",16)}</span><div class="lm"><b class="sm">Star Fox 64 mod</b><span class="l2">Updated yesterday</span></div></div>')
    return f'''{top("",right)}<div class="pad prof">{live}
<div class="phd">{av(k,88)}<h1>{n}</h1><p class="mu">{bio}</p><p class="mu sm">{"8" if me else "12"} postups · since Sep</p>{act}</div>
<h3 class="sh">Regular cafes</h3><div class="chips"><button class="chip" onclick="go('cafe')">{"Lantern Tea" if me else "Bean Theory"}</button><button class="chip" onclick="go('cafe')">Grindhouse</button></div>
<div class="p2only"><h3 class="sh">Projects</h3><div class="grp">{projs}</div></div>
<h3 class="sh">Past postups</h3><div class="grp">{ppast("Mon","Bean Theory","Ship models imported")}{ppast("Oct 9","Lantern Tea","Level editor")}</div></div>'''
S['profile']=prof('MK',False); S['me']=prof('ME',True)
def tgl(t,on=True): return f'<label class="lrow tgr"><span class="lm sm">{t}</span><input type="checkbox" class="tg" {"checked" if on else ""}></label>'
S['settings']=f'''{top("Settings")}<div class="pad"><h3 class="sh">Notifications</h3><div class="grp">{tgl("Join requests")}{tgl("Someone joins your postup")}{tgl("Messages")}{tgl("People you follow post up",False)}</div>
<h3 class="sh">Account</h3><div class="grp"><div class="lrow"><span class="lm sm">Blocked people</span><span class="mu sm">1</span>{I("chev",18,"mu")}</div><button class="lrow wr" onclick="setScen('out',null);go('home')"><span class="lm sm">Sign out</span></button><button class="lrow wr dg" onclick="ov('delacct')"><span class="lm sm">Delete account</span></button></div></div>'''
REASONS=['Spam or fake','Harassment','Inappropriate photo','Not at a public place','Something else']
S['report']=f'''{top("Report")}<div class="pad form"><h2>What's wrong?</h2><div class="grp">'''+''.join(f'<label class="lrow tgr"><span class="lm sm">{r}</span><input type="radio" name="rr" class="rd" {"checked" if i==1 else ""}></label>' for i,r in enumerate(REASONS))+f'''</div>
<label>Anything else? <span class="mu">optional</span></label><textarea class="in" rows="3" placeholder="Add details"></textarea></div><div class="cta"><button class="btn" onclick="go('reported')">Send report</button></div>'''
S['reported']=f'''{top("",f'<a class="ib" href="#home" aria-label="Close">{I("x",22)}</a>',back=False)}<div class="pad done"><div class="okc">{I("flag",30)}</div><h1>Thanks for telling us</h1><p class="mu">We'll review it. They won't know you reported them.</p>
<button class="btn sec" onclick="ov('block')">{I("ban",16)} Block Maya too</button><a class="btn" href="#home">Done</a></div>'''

# ---------- index ----------
def grp(t,items): return f'<h3 class="sh">{t}</h3><div class="grp">'+''.join(ix(*x) for x in items)+'</div>'
S['index']=f'''{top("Mockups",back=False)}<div class="pad"><p class="mu">Tap through PostUp's flows. Everyone and everything here is made up.</p>
<h3 class="sh">Style</h3><div class="stsw"><button data-s="fresh" onclick="setStyle('fresh')">Fresh</button><button data-s="cozy" onclick="setStyle('cozy')">Cozy</button><button data-s="night" onclick="setStyle('night')">Night</button><button data-s="bold" onclick="setStyle('bold')">Bold</button></div>
<h3 class="sh">Device</h3><div class="stsw dvsw"><button data-d="phone" onclick="applyDevice('phone')">Phone</button><button data-d="desktop" onclick="applyDevice('desktop')">Desktop</button></div>
{grp("Browse",[("#home","Map","Who's live","map"),("#quiet-feed","Nearby","Feed with photos","list"),("#quiet-feed-b","Nearby B","No photos","list"),("#quiet","Recent map","This week","pin"),("#cafe","Cafe","Who's here","coffee"),("#projects","Projects","Browse, filter","folder"),("#project","Project","Updates","folder")])}
{grp("Post up",[("#post","Post up","Form","plus"),("#where","Where are you?","Pick a cafe","search"),("#where-search","Cafe search","Google results","search"),("#post-signin","Sign in","At post time","lock"),("#posted","Posted","Share link","check"),("#live","You're live","Manage, requests","clock"),("#post-edit","Edit","Change postup","edit")])}
{grp("Join",[("#postup","Postup","Anyone can join","users"),("#postup-ask","Ask to join","Poster approves","lock"),("#ask","Request","Write a reason","send"),("#requested","Request sent","Waiting","send"),("#joined","Joined","Directions, chat","check"),("#chat","Group chat","Postup chat","msg")])}
{grp("Inbox & people",[("#inbox","Inbox","P1 one list · P2 tabs","inbox"),("#activity","Activity","Joins, requests","bell"),("#profile","Profile","Maya","users"),("#me","My profile","Live + settings","users"),("#settings","Settings","Account","gear"),("#report","Report","Reasons","flag"),("#reported","Reported","Block too","ban")])}
{grp("First visit",[("#quiet-feed","Welcome","Strip atop feed","spark"),("#invite","Invite link","Join Maya?","share"),("#invite-ended","Invite ended","Postup over","share")])}
{grp("States",[("#empty-area","Empty area","Be the first","pin"),("#postup-ended","Ended","Postup over","clock"),("#postup-full","Full","No room","users"),("#postup-cancelled","Cancelled","Called off","x"),("#cafe-gfail","Google failed","Fallback","image"),("#loading","Loading","Skeleton","refresh"),("#offline","Offline","Cached","wifi")])}
<h3 class="sh">Notes</h3><div class="grp">{ix("feed-rationale.md","Rationale","Why feed","spark")}{ix("review-2026-10-14.md","UX review","Gaps","list")}</div></div>'''

# ---------- global overlays ----------
def ovs(id,body): return f'<div class="ov" id="ov-{id}"><div class="dim" onclick="ovx()"></div><div class="bs"><span class="grab"></span>{body}</div></div>'
def opt(t,ic,js,dg=False): return f'<button class="lrow wr{" dg" if dg else ""}" onclick="{js}"><span class="ixi">{I(ic,16)}</span><span class="lm">{t}</span></button>'
OVS=ovs('share',f'<h2>Share</h2><div class="link"><span>postup.now/p/7xk2</span><button class="pill" onclick="this.innerHTML=\'Copied\'">{I("copy",14)} Copy</button></div><div class="shr">'+''.join(f'<button onclick="ovx()"><span class="ixi">{I(ic,20)}</span><span class="xs">{t}</span></button>' for t,ic in [('Messages','msg'),('WhatsApp','send'),('Email','inbox'),('More','more')])+'</div><button class="tx" onclick="ovx()">Cancel</button>')
OVS+=ovs('dirs','<h2>Bean Theory</h2><p class="mu">0.4 mi · 8 min walk</p><a class="sso" href="https://maps.apple.com/?q=Bean+Theory" target="_blank" onclick="ovx()">Open in Apple Maps</a><a class="sso" href="https://www.google.com/maps/search/?api=1&query=Bean+Theory" target="_blank" onclick="ovx()">Open in Google Maps</a><button class="tx" onclick="ovx()">Cancel</button>')
OVS+=ovs('leave','<h2>Leave Maya\'s postup?</h2><p class="mu">Maya will get an alert.</p><button class="btn danger" onclick="ovx();go(\'postup\')">Leave</button><button class="tx" onclick="ovx()">Stay</button>')
OVS+=ovs('endlive','<h2>End your postup?</h2><p class="mu">Jon and anyone waiting will get an alert.</p><button class="btn danger" onclick="ovx();go(\'me\')">End now</button><button class="tx" onclick="ovx()">Keep going</button>')
OVS+=ovs('more','<h2>Maya</h2>'+opt('View profile','users',"ovx();go('profile')")+opt('Share','share',"ov('share')")+opt('Report','flag',"ovx();go('report')",True)+opt('Block','ban',"ov('block')",True)+'<button class="tx" onclick="ovx()">Cancel</button>')
OVS+=ovs('msg','<h2>Message</h2>'+opt('Copy','copy',"ovx()")+opt('Report message','flag',"ovx();go('report')",True)+opt('Block sender','ban',"ov('block')",True)+'<button class="tx" onclick="ovx()">Cancel</button>')
OVS+=ovs('block','<h2>Block Maya?</h2><p class="mu">You won\'t see each other\'s postups or messages. She won\'t be told.</p><button class="btn danger" onclick="ovx();go(\'home\')">Block</button><a class="lnk sm" href="#settings" onclick="ovx()">Blocked people (Settings)</a><button class="tx" onclick="ovx()">Cancel</button>')
OVS+=ovs('delacct','<h2>Delete your account?</h2><p class="mu">Your profile, postups and projects will be removed. This can\'t be undone.</p><button class="btn danger" onclick="ovx();setScen(\'out\',null);go(\'home\')">Delete account</button><button class="tx" onclick="ovx()">Cancel</button>')

FULL=['index','quiet-feed','quiet-feed-b','projects','project','posted','inbox','activity','chat','profile','me','settings','report','reported','invite','invite-ended','loading','offline','requested']
DLG=['post','post-signin','where','where-search','post-edit','project-new','project-update','project-attach','attach-signin']
DESK=f'''<aside class="rail"><a class="rlogo" href="#home">{I("coffee",22)}</a>{rl("#home","map","Map")}{rl("#quiet-feed","list","Nearby")}{rl("#projects","folder","Projects")}{rl("#inbox","inbox","Inbox")}<a class="rpost" href="#post">{I("plus",22)}<span>Post up</span></a><span class="rsp"></span><a href="#me" data-r="me" class="rme">{av('ME',36)}</a></aside>
<div class="dmap">{dmapsvg()}{dpins}<span class="you" style="left:47%;top:52%"></span><div class="dsearch">{I("pin",16)} Venice &amp; Mar Vista</div><div class="attr">Map mockup</div></div>'''
# projects welcome + project invite landing
PW=f'<div class="welcome pwel"><span class="ci sm pj">{I("folder",16)}</span><p>See what people are building. Follow along or post up to work on yours.</p><button class="ib" onclick="this.parentNode.remove()" aria-label="Dismiss">{I("x",18)}</button></div>'
S['projects']=S['projects'].replace('<div class="hero">',PW+'<div class="hero">',1)
S['invite-project']=f'''<header class="nb"><span class="ib"></span><b class="brand2">{I("coffee",16)} postup</b><span class="nr"></span></header><div class="pad done inv">
<img class="invimg" src="img/sf64.svg" alt=""><div class="pair">{av('MK',56)}</div><h1>Maya is building Star Fox 64 mod</h1><p class="mu">See updates, follow, or join her next postup.</p>
<a class="btn" href="#project">See updates</a><button class="btn sec" onclick="go('join-signin')">Follow {LOCK}</button><a class="lnk sm" href="#profile">Next postup: weekdays at Bean Theory</a>
<p class="mu sm">PostUp shows who's working from cafes nearby, so you can join them or post up yourself.</p></div>'''
FULL.append('invite-project')
S['index']=S['index'].replace('("#invite-ended","Invite ended","Postup over","share")','("#invite-ended","Invite ended","Postup over","share"),("#projects","Projects welcome","Strip atop list","spark"),("#invite-project","Project link","Follow Maya","share")')
