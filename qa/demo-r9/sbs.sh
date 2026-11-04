#!/bin/sh
# side-by-side: before (v1.3.1) left, after (v1.4) right, same deterministic combo script, real time (30 fps), small labels
# usage: sbs.sh BEFORE.mp4 AFTER.mp4 OUT.mp4 light|dark
B=$1; A=$2; O=$3; T=$4
F=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf; [ -f $F ] || F=$(fc-match -f '%{file}' sans)
if [ "$T" = dark ]; then C=0xd8d4cc; BX=0x000000@0.35; else C=0x2a2622; BX=0xffffff@0.55; fi
PH="drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=(w-tw)/2:y=h-28:text='%{eif\:t\:d}'"
CAP="press + slow drag 200 px/s"
ffmpeg -y -loglevel error -i "$B" -i "$A" -filter_complex "\
[0:v]scale=960:600:flags=lanczos,drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=12:y=12:text='before · v1.3.1 (live)'[l];\
[1:v]scale=960:600:flags=lanczos,drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=12:y=12:text='after · v1.4'[r];\
[l][r]hstack=inputs=2,\
drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=(w-tw)/2:y=h-30:text='0.5 s press · hold':enable='between(t,0.5,0.9)',\
drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=(w-tw)/2:y=h-30:text='slow drag 200 px/s (below 23 cm/s)':enable='between(t,0.9,4.5)',\
drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=(w-tw)/2:y=h-30:text='4.5 s lift':enable='between(t,4.5,5.6)',\
drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=(w-tw)/2:y=h-30:text='6.0 s press · fast flick 1250 px/s':enable='between(t,6.0,6.7)',\
drawtext=fontfile=$F:fontsize=15:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=5:x=(w-tw)/2:y=h-30:text='6.7 s lift':enable='between(t,6.7,8.2)',\
drawtext=fontfile=$F:fontsize=13:fontcolor=$C:box=1:boxcolor=$BX:boxborderw=4:x=w-tw-12:y=h-26:text='t %{eif\:t\:d}.%{eif\:mod(t*10\,10)\:d} s'" \
 -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -r 30 "$O"
