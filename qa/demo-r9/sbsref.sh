#!/bin/sh
# triptych: the existing side-by-side (v1.3.1 | v1.4) + a 10 s real-water reference clip (research-real-water/clips, local only, not committed)
# usage: sbsref.sh SBS.mp4 CLIP START LABEL OUT
F=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
ffmpeg -y -loglevel error -i "$1" -ss "$3" -t 10 -i "$2" -filter_complex "[1:v]scale=960:600:force_original_aspect_ratio=increase,crop=960:600,fps=30,drawtext=fontfile=$F:fontsize=15:fontcolor=0xffffff:box=1:boxcolor=0x000000@0.5:boxborderw=5:x=12:y=12:text='$4'[r];[0:v][r]hstack=inputs=2" -t 10 -c:v libx264 -pix_fmt yuv420p -crf 20 -preset medium "$5"
