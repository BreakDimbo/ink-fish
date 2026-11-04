#!/bin/sh
# quick preview: tap packet frames 12 (0.4 s) and 21 (0.7 s), light+dark, water only → /tmp/pv_'+__import__('os').environ.get('TAG','x')+'.png (crop 500×400, 1:1)
cd /workspace/ink-fish/qa/demo-r9
MEASURE=1 NOVIDEO=1 python3 drag.py http://127.0.0.1:8733/index.html light pvL tap ${N:-22} > /tmp/pvL.log 2>&1 &
MEASURE=1 NOVIDEO=1 python3 drag.py http://127.0.0.1:8733/index.html dark pvD tap ${N:-22} > /tmp/pvD.log 2>&1
wait
python3 - <<'P'
from PIL import Image
fr=[6,12,21]; im=Image.new('RGB',(500*len(fr),800))
for r,run in enumerate(('pvL','pvD')):
  for i,f in enumerate(fr): im.paste(Image.open(f'frames/{run}/f{f:04d}.png').crop((450,90,950,490)),(500*i,400*r))
im.save('/tmp/pv_'+__import__('os').environ.get('TAG','x')+'.png')
P
cat /tmp/pvL.log /tmp/pvD.log
python3 - <<'P'
from PIL import Image
im=Image.new('RGB',(960,240))
for i,run in enumerate(('pvL','pvD')):
  for j,f in enumerate((12,21)):
    im.paste(Image.open(f'frames/{run}/f{f:04d}.png').crop((660,250,740,330)).resize((240,240),Image.LANCZOS),(480*i+240*j,0))
im.save('/tmp/pvz_'+__import__('os').environ.get('TAG','x')+'.png')
P
