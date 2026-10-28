# Scenarios: signed out/in x live nearby/none. exec'd by build.py after more.py, before notes.py.
# A screen renders variant "<id>--<auth>-<live>", "<id>--<live>" or "<id>--<auth>" when one exists
# (auth: out|in, live: live|none); otherwise the base screen. Smaller differences use classes
# .only-out/.only-in/.only-live/.only-none and the html data-auth/data-live attributes (gen/scen.js).
import re
VAR={}
# sign-in sheet buttons sign you in (flip the toggle) and continue
for k in list(S): S[k]=re.sub(r'(<button class="sso(?: ap)?" )onclick="go\(\'([\w-]+)\'\)"',lambda m:m[1]+"onclick=\"signIn('"+m[2]+"')\"",S[k])
# actions that need an account go through sheet()/act()/follow()
S['postup-ask']=S['postup-ask'].replace("onclick=\"go('ask-signin')\"","onclick=\"sheet('ask-signin')\"")
for k in ['ask-signin','ask']: S[k]=S[k].replace("onclick=\"go('ask-signin')\"","onclick=\"sheet('ask-signin')\"")
S['invite']=S['invite'].replace("onclick=\"go('join-signin')\"","onclick=\"sheet('join-signin')\"")
S['invite-project']=S['invite-project'].replace("onclick=\"go('join-signin')\">Follow","onclick=\"follow(this,'Follow Star Fox 64 mod')\">Follow")
for k in ['project-attach','attach-signin']: S[k]=S[k].replace("onclick=\"go('attach-signin')\"","onclick=\"sheet('attach-signin')\"")
S['project-new']=S['project-new'].replace("onclick=\"go('project')\">Create","onclick=\"act('project','Almost there','Sign in to create your project.')\">Create "+LOCK)
S['project-update']=S['project-update'].replace("onclick=\"go('project')\">Post update","onclick=\"act('project','Almost there','Sign in to post your update.')\">Post update "+LOCK)
FOLLOW_OLD="onclick=\"this.classList.toggle('sec');this.textContent=this.classList.contains('sec')?'Following':'Follow'\""
S['profile']=S['profile'].replace(FOLLOW_OLD,"onclick=\"follow(this,'Follow Maya')\"")
assert "follow(this,'Follow Maya')" in S['profile'] and "follow(this" in S['invite-project'] and "act('project'" in S['project-new']
# signed in: the *-signin screens show their page without the sheet
for k,base in [('post-signin','post'),('join-signin','postup'),('ask-signin','postup-ask'),('attach-signin','project-attach')]:
    VAR[k+'--in']=S[base]
# signed out: account-only pages show a sign-in sheet over themselves
def gate(k,title,sub): VAR[k+'--out']=S[k]+signin(k+'--out',title,sub,k).replace("onclick=\"go('%s')\""%k,"onclick=\"signIn('%s')\""%k)
for k,t,s in [('inbox','Your inbox','Sign in to see your chats and activity.'),('activity','Your inbox','Sign in to see your chats and activity.'),
              ('chat','Join the chat','Sign in to see this postup\'s chat.'),('me','Your profile','Sign in to see your profile.'),
              ('settings','Settings','Sign in to change your settings.'),('live','Your postup','Sign in to manage your postup.'),('post-edit','Your postup','Sign in to edit your postup.')]:
    gate(k,t,s)
# none live nearby
VAR['cafe--none']=re.sub(r'<div class="sp-h"><h2>Here now</h2>.*?</div>\s*<div class="grp">.*?</div>\s*(?=<div class="gcard)','',S['cafe'],count=1,flags=re.S)
VAR['cafe-gfail--none']=re.sub(r'<div class="sp-h"><h2>Here now</h2>.*?</div>\s*<div class="grp">.*?</div>\s*(?=<div class="gcard)','',S['cafe-gfail'],count=1,flags=re.S)
assert 'Here now' not in VAR['cafe--none'] and 'Here now' not in VAR['cafe-gfail--none']
VAR['project--none']=re.sub(r'<div class="sp-h"><h2>Live</h2></div>\s*<div class="lrow card".*?</div></div><span class="ok sm"><span class="dot"></span> Live</span></div>','',S['project'],count=1,flags=re.S)
assert '<h2>Live</h2>' not in VAR['project--none']
VAR['profile--none']=re.sub(r'<a class="card livec sm2c" href="#postup">.*?</a>','',S['profile'],count=1,flags=re.S)
assert 'Live at Bean Theory' not in VAR['profile--none']
VAR['where--none']=S['where'].replace(' · 2 live','')
# Nearby with none live: falls back to projects in general
PCARDS=pcard("Star Fox 64 mod","MK","sf64","Corneria II playable","Yesterday","Bean Theory",2)+pcard("Pixel Garden","TS","pixel","New crop sprites","Tue","Grindhouse",1)+pcard("Bus Stop Zine","JR","sketch","Page 12 inked","Mon","Bean Theory",2)+pcard("Lantern Lights","AL","table2","Wiring the LEDs","Sun","Lantern Tea",1)
for k in ['quiet-feed','quiet-feed-b']:
    v=re.sub(r'<article class="fc">.*</article>(?=\s*<aside class="dside">)',PCARDS,S[k],count=1,flags=re.S)
    v=re.sub(r'(<div class="hero"><h1>Good things happen at cafes</h1><p class="mu">).*?(</p></div>)',r'\1What people are building\2',v,count=1,flags=re.S)
    assert 'class="fc pc"' in v and 'postups nearby this week' not in v.split('<aside')[0], k
    VAR[k+'--none']=v
# phone: projects hero is hidden by default (style.css); show it on home
for k,v in VAR.items():
    S[k]=v
    b=k.split('--')[0]
    if b in FULL and k not in FULL: FULL.append(k)
    elif b in DLG and k not in DLG: DLG.append(k)
# Follow / create / update sign-in sheet (overlay)
OVS+=ovs('signin',f'<h2 id="osi-t">Almost there</h2><p class="mu" id="osi-s">Sign in to continue.</p>'+
 re.search(r'<button class="sso ap".*?Continue with Google</button>',S['post-signin'],re.S).group(0).replace("signIn('posted')","signIn()")+'<button class="tx" onclick="ovx()">Not now</button>')
# index: Home page (/) first, 2x2 scenario matrix
S['index']=S['index'].replace('<h3 class="sh">Style</h3>',
 '<a class="ixr homeix" href="#home"><span class="ixi">'+I("map",18)+'</span><span class="lm"><b>Home page (/)</b><span class="mu sm">What loads at postup.now/ · changes with the scenario</span></span>'+I("chev",18,"mu")+'</a>'
 '<h3 class="sh">Scenario</h3><div class="scm"><span></span><b class="xs">Live nearby</b><b class="xs">None live</b>'
 '<b class="xs">Signed out</b><button data-sc="out-live" onclick="setScen(\'out\',\'live\')">●</button><button data-sc="out-none" onclick="setScen(\'out\',\'none\')">●</button>'
 '<b class="xs">Signed in</b><button data-sc="in-live" onclick="setScen(\'in\',\'live\')">●</button><button data-sc="in-none" onclick="setScen(\'in\',\'none\')">●</button></div>'
 '<h3 class="sh">Style</h3>',1)
S['index']=S['index'].replace("<b>Map</b><span class=\"mu sm\">Who's live</span>","<b>Home page (/)</b><span class=\"mu sm\">Map when live · projects when none</span>",1)
S['index']=S['index'].replace("<b>Recent map</b><span class=\"mu sm\">This week</span>","<b>Recent map</b><span class=\"mu sm\">Old no-live home · not /</span>",1)
S['index']=S['index'].replace('<span class="mu sm">Feed with photos</span>','<span class="mu sm">/nearby · photos · not /</span>',1).replace('<span class="mu sm">No photos</span>','<span class="mu sm">/nearby · no photos</span>',1)
assert S['index'].count('Home page (/)')==2 and 'Old no-live home' in S['index']
assert 'Home page (/)' in S['index'] and 'class="scm"' in S['index']
