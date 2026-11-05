#!/bin/sh
# r14 side-by-sides (labels burned in)
cd /workspace/ink-fish-r14/qa/demo-r14
F=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
L() { echo "drawtext=fontfile=$F:text='$1':x=20:y=20:fontsize=$4:fontcolor=$2:box=1:boxcolor=$3@0.55:boxborderw=8"; }
for t in light dark; do
  if [ $t = light ]; then fc=black; bc=white; else fc=white; bc=black; fi
  # clicks: promo build | live | new (pointer parked on the spot; click at 0.5 s, still hold 2.6–3.6 s)
  ffmpeg -y -loglevel error -i pclick-v131-$t.mp4 -i pclick-v151-$t.mp4 -i pclick-new-$t.mp4 -filter_complex \
   "[0]crop=960:600:220:30,$(L 'v1.3.1 (promo build)' $fc $bc 30)[a];[1]crop=960:600:220:30,$(L 'v1.5.1 (live)' $fc $bc 30)[b];[2]crop=960:600:220:30,$(L 'v1.5.2 (new)' $fc $bc 30)[c];[a][b][c]hstack=3" \
   -c:v libx264 -pix_fmt yuv420p -crf 18 click-sbs-$t.mp4; echo click $t $?
  # drags: live | new (whole 10 s combo)
  ffmpeg -y -loglevel error -i drag-v151-$t.mp4 -i drag-new-$t.mp4 -filter_complex \
   "[0]$(L 'v1.5.1 (live)' $fc $bc 34)[a];[1]$(L 'v1.5.2 (new)' $fc $bc 34)[b];[a][b]hstack=2,scale=2160:-2" \
   -c:v libx264 -pix_fmt yuv420p -crf 20 drag-sbs-$t.mp4; echo drag $t $?
done
# drag starts on the promo stage, first 40 frames (1.3 s; press at 0.3 s), stacked promo | live | new, played at half speed
for s in s10_peak_light s09_peak_dark; do
  case $s in *light) fc=black; bc=white;; *) fc=white; bc=black;; esac
  ffmpeg -y -loglevel error -framerate 15 -i /workspace/inkfish-promo/footage/frames/$s/f%04d.png -framerate 15 -i stage/v151/$s/f%04d.png -framerate 15 -i stage/new/$s/f%04d.png -filter_complex \
   "[0]trim=end_frame=40,scale=1280:-2,$(L 'promo film (v1.3.1)' $fc $bc 30)[a];[1]trim=end_frame=40,scale=1280:-2,$(L 'v1.5.1 (live)' $fc $bc 30)[b];[2]trim=end_frame=40,scale=1280:-2,$(L 'v1.5.2 (new)' $fc $bc 30)[c];[a][b][c]vstack=3" \
   -c:v libx264 -pix_fmt yuv420p -crf 16 dragstart-sbs-$s-halfspeed.mp4; echo dragstart $s $?
done
