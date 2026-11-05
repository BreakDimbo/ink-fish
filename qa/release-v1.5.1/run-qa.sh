#!/bin/sh
# release QA for v1.5.1: perf vs live v1.5.0 (interleaved), func, touch, behave (incl. click), demo shots
R=/workspace/ink-fish/qa/release-v1.5.1
cd $R && CASES="1440,1,idle;1440,1,drag;390,4,idle;390,4,drag" ONLY=v1.5 OUT=$R/perf.json python3 -u perfx.py > $R/perf.log 2> $R/perf.err; echo perf $?
python3 perfsum.py perf.log "Release perf gate, v1.5.1 vs live v1.5.0" perf.md v1.5.0 v1.5.1 > /dev/null; echo perfsum $?
cd /workspace/ink-fish/qa/demo-r9 && python3 -u func.py > $R/func.log 2>&1; echo func $?
python3 -u touchonly.py http://127.0.0.1:8733/index.html > $R/touch.log 2>&1; echo touch $?
cd $R && python3 -u behave.py > behave.json 2> behave.err; echo behave $?
python3 -u shots.py > shots.json 2> shots.err; echo shots $?
echo ALLDONE

