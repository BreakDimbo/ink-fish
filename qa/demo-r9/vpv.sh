#!/bin/sh
# fast-V preview: frames 33 (1.1 s, mid-stroke) and 39 (1.3 s, after lift), light + dark → /tmp/vpv_$TAG.png
cd /workspace/ink-fish/qa/demo-r9
MEASURE=1 NOVIDEO=1 python3 drag.py http://127.0.0.1:8733/index.html light vpL fast 40 > /tmp/vpL.log 2>&1 &
MEASURE=1 NOVIDEO=1 python3 drag.py http://127.0.0.1:8733/index.html dark vpD fast 40 > /tmp/vpD.log 2>&1
wait
python3 - <<'P'
import os
from PIL import Image
im=Image.new('RGB',(1000,600))
for r,run in enumerate(('vpL','vpD')):
  for i,f in enumerate((33,39)): im.paste(Image.open(f'frames/{run}/f{f:04d}.png').crop((560,200,1060,500)),(500*i,300*r))
im.save('/tmp/vpv_'+os.environ.get('TAG','x')+'.png')
P
echo vdone
