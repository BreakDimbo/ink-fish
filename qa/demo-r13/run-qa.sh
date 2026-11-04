#!/bin/sh
# r13 QA on the current commit: perf gate (v1.3.1, v1.5.0, v1.5.1 interleaved, median of 3), func, touch, behave
R=/workspace/ink-fish/qa/demo-r13
cd $R && CASES="1440,1,idle;1440,1,drag;390,4,idle;390,4,drag" OUT=$R/perf.json python3 -u perfx.py > $R/perf.log 2> $R/perf.err; echo perf $?
python3 perfsum.py perf.log "Perf gate, v1.5.1 vs v1.3.1" perf-vs-131.md v1.3.1 v1.5.1 > /dev/null; echo perfsum131 $?
python3 perfsum.py perf.log "Perf gate, v1.5.1 vs v1.5.0" perf-vs-150.md v1.5.0 v1.5.1 > /dev/null; echo perfsum150 $?
cd /workspace/ink-fish/qa/demo-r9 && python3 -u func.py > $R/func.log 2>&1; echo func $?
python3 -u touchonly.py http://127.0.0.1:8733/index.html > $R/touch.log 2>&1; echo touch $?
cd $R && python3 -u behave.py > behave.json 2> behave.err; echo behave $?
echo ALLDONE
