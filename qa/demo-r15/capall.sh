#!/bin/bash
# r15 · all device-equivalent captures (30 Hz step = 30 fps real time), two lanes
cd /workspace/ink-fish-r15/qa/demo-r15
lane1() {
  MEASURE=1 python3 stepcap.py http://127.0.0.1:8851/index.html light s152-jclick-light jclick 4 30
  MEASURE=1 python3 stepcap.py http://127.0.0.1:8851/index.html light s152-drag-light drag 4 30
  MEASURE=1 python3 stepcap.py http://127.0.0.1:8852/index.html light s153-drag-light drag 4 30
  for th in light dark; do python3 stepcap.py http://127.0.0.1:8851/index.html $th v152-jclick-$th jclick 4.5 30; python3 stepcap.py http://127.0.0.1:8851/index.html $th v152-drag-$th drag 4 30; done
}
lane2() {
  MEASURE=1 python3 stepcap.py http://127.0.0.1:8851/index.html light s152-moveclick-light moveclick 3 30
  MEASURE=1 python3 stepcap.py http://127.0.0.1:8852/index.html light s153-moveclick-light moveclick 3 30
  for th in light dark; do python3 stepcap.py http://127.0.0.1:8852/index.html $th v153-jclick-$th jclick 4.5 30; python3 stepcap.py http://127.0.0.1:8852/index.html $th v153-drag-$th drag 4 30; done
}
lane1 > /workspace/r15tmp/lane1.log 2>&1 &
lane2 > /workspace/r15tmp/lane2.log 2>&1 &
wait; echo ALLDONE
