# usage: shot1.sh name query size   (one browser, 25s timeout)
cd /workspace/postup-pm/mockups
timeout -k 5 25 google-chrome --headless=new --no-sandbox --hide-scrollbars --disable-gpu --virtual-time-budget=1500 --window-size=$3 --screenshot=shots/new/$1.png "file://$PWD/index.html?notes=0&$2" >/dev/null 2>&1
