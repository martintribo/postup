cd /workspace/postup-pm/mockups; mkdir -p shots/new
N="index quiet-feed where where-search post live postup-ask ask requested joined chat inbox activity profile me settings report reported invite invite-ended empty-area postup-ended postup-full postup-cancelled cafe-gfail loading offline projects"
run(){ google-chrome --headless=new --no-sandbox --hide-scrollbars --virtual-time-budget=2500 --window-size=$3 --screenshot=shots/new/$1.png "file://$PWD/index.html?notes=0&$2" 2>/dev/null; }
for s in $N; do run phone-fresh-$s "style=fresh&device=phone#$s" 390,844 & run desktop-fresh-$s "style=fresh&device=desktop#$s" 1440,900 & done; wait
for s in share dirs leave more msg block endlive delacct; do run phone-fresh-ov-$s "style=fresh&device=phone&ov=$s#joined" 390,844 & done
for s in home quiet-feed live chat profile postup-ask; do run phone-bold-$s "style=bold&device=phone#$s" 390,844 & run desktop-bold-$s "style=bold&device=desktop#$s" 1440,900 & done; wait
