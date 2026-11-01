# Anti-trolling for phase 0 and up [M1039]: one live postup per account, and posting only near where you are.
# exec'd by build.py after home.py, before phasev.py. Reached through the data conditions has-live-postup and too-far (model/events.toml).
S['post-already']=f'''{top("Post up")}<div class="pad done">
<div class="okc">{I("clock",30)}</div><h1>You're already posted up</h1><p class="mu">Lot 1 Coffee · till 3:45pm<br>One live postup per account. End it before you post up somewhere else.</p>
<button class="btn" onclick="go('live')">View your postup</button>
<div class="lnks"><a class="lnk" href="#home">Back to map</a></div></div>'''
S['post-far']=f'''{top("Post up")}<div class="pad done">
<div class="okc" style="background:#fdecec;color:#c0392b">{I("pin",30)}</div><h1>You're too far away</h1><p class="mu">Stories Cafe looks about 2 mi from where you are. You can only post up at a place you're at right now.</p>
<button class="btn" onclick="go('where')">Pick a cafe near you</button>
<div class="lnks"><a class="lnk" href="#home">Back to map</a></div></div>'''
