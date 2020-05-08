#!/usr/bin/env python3.7
import time
import sys
def tik(start=0, dots=3):
    if start == 0: sys.stderr.write('Processing')
    if dots !=0:
        sys.stderr.write('.')
        sys.stderr.flush()
        time.sleep(1)
        y = tik(start=1, dots=dots - 1)
    else:
        sys.stderr.write('\b' * 3)
        sys.stderr.write(' ' * 3)
        sys.stderr.write('\b' * 3)
    return tik(start=1)
