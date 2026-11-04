#!/bin/sh
cd /workspace/ink-fish/qa/demo-r9
python3 drag.py http://127.0.0.1:8733/index.html light after13-light combo > render13-al.log 2>&1; echo al $? >> chain13.log
python3 drag.py http://127.0.0.1:8733/index.html dark after13-dark combo > render13-ad.log 2>&1; echo ad $? >> chain13.log
MEASURE=1 NOVIDEO=1 python3 drag.py http://127.0.0.1:8733/index.html dark tapD tap 120 > render13-td.log 2>&1; echo td $? >> chain13.log
echo DONE >> chain13.log
