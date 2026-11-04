#!/bin/sh
# side-by-sides from the r13 renders (labels burned in)
cd /workspace/ink-fish/qa/demo-r13
L() { echo "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='$1':x=24:y=24:fontsize=34:fontcolor=$2:box=1:boxcolor=$3@0.55:boxborderw=10"; }
for t in light dark; do
  if [ $t = light ]; then fc=black; bc=white; else fc=white; bc=black; fi
  ffmpeg -y -loglevel error -i click-v150-$t.mp4 -i click-v121-$t.mp4 -i click-new-$t.mp4 -filter_complex \
   "[0]crop=960:600:220:30,$(L 'v1.5.0 (live)' $fc $bc)[a];[1]crop=960:600:220:30,$(L 'v1.2.1 (original)' $fc $bc)[b];[2]crop=960:600:220:30,$(L 'v1.5.1 (new)' $fc $bc)[c];[a][b][c]hstack=3" \
   -c:v libx264 -pix_fmt yuv420p -crf 20 click-sbs-$t.mp4; echo click $t $?
  ffmpeg -y -loglevel error -i drag-v150-$t.mp4 -i $(if [ $t = light ]; then echo drag-new2-light.mp4; else echo drag-new-dark.mp4; fi) -filter_complex \
   "[0]$(L 'v1.5.0 (live)' $fc $bc)[a];[1]$(L 'v1.5.1 (new)' $fc $bc)[b];[a][b]hstack=2,scale=2160:-2" \
   -c:v libx264 -pix_fmt yuv420p -crf 20 drag-sbs-$t.mp4; echo drag $t $?
done
