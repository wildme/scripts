#!/usr/bin/env python3.7
import time
import sys
def tik(start=0, dots=3):
    if start == 0: sys.stdout.write('Processing')
    if dots !=0:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)
        y = tik(start=1, dots=dots - 1)
    else:
        sys.stdout.write('\b' * 3)
        sys.stdout.write(' ' * 3)
        sys.stdout.write('\b' * 3)
    return tik(start=1)
