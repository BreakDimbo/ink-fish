#!/bin/sh
# render queue: rq.sh LOG "url theme name kind N" ...   (MEASURE/NOVIDEO from env)
LOG=$1; shift
for job in "$@"; do set -- $job; python3 /workspace/ink-fish/qa/demo-r9/drag.py http://127.0.0.1:8733/$1 $2 $3 $4 $5 >> $LOG 2>&1; done
echo DONE >> $LOG
