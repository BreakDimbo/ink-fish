#!/bin/sh
cd /workspace/ink-fish/qa/demo-r11
python3 -u drag.py http://127.0.0.1:8733/index.html light after-light combo > render-al.log 2>&1; echo al $? >> chain.log
python3 -u drag.py http://127.0.0.1:8733/index.html dark after-dark combo > render-ad.log 2>&1; echo ad $? >> chain.log
./sbs.sh ../demo-r9/before-light.mp4 after-light.mp4 sbs-light.mp4 light; echo sl $? >> chain.log
./sbs.sh ../demo-r9/before-dark.mp4 after-dark.mp4 sbs-dark.mp4 dark; echo sd $? >> chain.log
echo DONE >> chain.log
