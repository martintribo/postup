cd /workspace/postup-pm/mockups
L="index home quiet quiet-feed quiet-feed-b cafe post post-signin posted postup join-signin joined project project-new project-update project-attach"
for s in $L; do google-chrome --headless=new --no-sandbox --hide-scrollbars --virtual-time-budget=2500 --window-size=390,844 --screenshot=shots/$s.png "file://$PWD/index.html#$s" 2>/dev/null & done; wait
python3 -c "
from PIL import Image
n='$L'.split()
for k in range(2):
  ims=[Image.open('shots/'+x+'.png').resize((260,563)) for x in n[k*8:k*8+8]]
  c=Image.new('RGB',(260*4,563*2),'white')
  for i,im in enumerate(ims): c.paste(im,((i%4)*260,(i//4)*563))
  c.save('/tmp/cs%d_'%k+str(__import__('time').time_ns())[-6:]+'.png')"
