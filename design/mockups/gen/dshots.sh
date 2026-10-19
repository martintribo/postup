cd /workspace/postup-pm/mockups
for s in home quiet-feed cafe post post-signin project; do google-chrome --headless=new --no-sandbox --hide-scrollbars --virtual-time-budget=2500 --window-size=1440,900 --screenshot=shots/desktop/fresh-$s.png "file://$PWD/index.html?notes=0&style=fresh&device=desktop#$s" 2>/dev/null & done
for st in cozy night bold; do google-chrome --headless=new --no-sandbox --hide-scrollbars --virtual-time-budget=2500 --window-size=1440,900 --screenshot=shots/desktop/$st-home.png "file://$PWD/index.html?notes=0&style=$st&device=desktop#home" 2>/dev/null & done
google-chrome --headless=new --no-sandbox --hide-scrollbars --virtual-time-budget=2500 --window-size=1440,900 --screenshot=shots/desktop/night-post-signin.png "file://$PWD/index.html?notes=0&style=night&device=desktop#post-signin" 2>/dev/null &
google-chrome --headless=new --no-sandbox --hide-scrollbars --virtual-time-budget=2500 --window-size=1440,900 --screenshot=shots/desktop/bold-cafe.png "file://$PWD/index.html?notes=0&style=bold&device=desktop#cafe" 2>/dev/null &
wait
