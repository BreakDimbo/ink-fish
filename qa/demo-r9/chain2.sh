#!/bin/sh
cd /workspace/ink-fish/qa/demo-r9
python3 wake.py > wake-press.log 2>&1; echo wake-press $? >> chain2.log
HOVER=1 REUSE_STILLS=1 python3 wake.py > wake-hover.log 2>&1; echo wake-hover $? >> chain2.log
python3 drag.py http://127.0.0.1:8733/index.html light after-light combo > render-al.log 2>&1; echo al $? >> chain2.log
python3 drag.py http://127.0.0.1:8733/index.html dark after-dark combo > render-ad.log 2>&1; echo ad $? >> chain2.log
echo DONE >> chain2.log
