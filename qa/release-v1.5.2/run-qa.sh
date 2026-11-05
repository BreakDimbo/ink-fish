#!/bin/sh
# release QA for v1.5.2 (served from the worktree on 8861): func, touch, behave, demo shots. Perf gate already passed
# (qa/demo-r14/perf3-*.md, perf4-*.md)
R=/workspace/ink-fish-r14/qa/release-v1.5.2; U=http://127.0.0.1:8861/ink-fish/index.html
cd /workspace/ink-fish-r14/qa/demo-r14 && U=$U python3 -u func.py > $R/func.log 2>&1; echo func $?
python3 -u touchonly.py $U > $R/touch.log 2>&1; echo touch $?
cd $R && python3 -u behave.py > behave.json 2> behave.err; echo behave $?
python3 -u shots.py > shots.json 2> shots.err; echo shots $?
echo ALLDONE
