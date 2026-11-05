#!/bin/sh
# r14 side-by-sides after the perf fix (d512d3f: a pure stroke lets its ring go). Earlier outputs are kept as they were
cd /workspace/ink-fish-r14/qa/demo-r14
F=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
L() { echo "drawtext=fontfile=$F:text='$1':x=20:y=20:fontsize=$4:fontcolor=$2:box=1:boxcolor=$3@0.55:boxborderw=8"; }
for t in light dark; do
  if [ $t = light ]; then fc=black; bc=white; else fc=white; bc=black; fi
  ffmpeg -y -loglevel error -i drag-v151-$t.mp4 -i drag-new2-$t.mp4 -filter_complex \
   "[0]$(L 'v1.5.1 (live)' $fc $bc 34)[a];[1]$(L 'v1.5.2 (new)' $fc $bc 34)[b];[a][b]hstack=2,scale=2160:-2" \
   -c:v libx264 -pix_fmt yuv420p -crf 20 drag-sbs2-$t.mp4; echo drag $t $?
done
for s in s10_peak_light s09_peak_dark; do
  case $s in *light) fc=black; bc=white;; *) fc=white; bc=black;; esac
  ffmpeg -y -loglevel error -framerate 15 -i /workspace/inkfish-promo/footage/frames/$s/f%04d.png -framerate 15 -i stage/v151/$s/f%04d.png -framerate 15 -i stage/new2/$s/f%04d.png -filter_complex \
   "[0]trim=end_frame=40,scale=1280:-2,$(L 'promo film (v1.3.1)' $fc $bc 30)[a];[1]trim=end_frame=40,scale=1280:-2,$(L 'v1.5.1 (live)' $fc $bc 30)[b];[2]trim=end_frame=40,scale=1280:-2,$(L 'v1.5.2 (new)' $fc $bc 30)[c];[a][b][c]vstack=3" \
   -c:v libx264 -pix_fmt yuv420p -crf 16 dragstart-sbs2-$s-halfspeed.mp4; echo dragstart $s $?
done
