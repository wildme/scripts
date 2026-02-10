#!/usr/bin/env python3
"""
This script looks for LO Impress files in the current directory and
loops over them starting LO Impress presentations with the specified
time interval.
"""

from pathlib import Path
from subprocess import Popen
import sys
import time
import _thread

sys.path.append('../')
from mods.txtviz import Counter

SWITCH_INTERVAL:int = 60

def show_counter():
    counter = Counter(SWITCH_INTERVAL)
    for _ in range(SWITCH_INTERVAL):
        if counter.value >= 0:
            time.sleep(1)
            counter.decrement()
            counter.update_decr(counter.value)

def main():
    print("Press CTRL+C to exit the program")
    print("The next slide will open in...%s" % (SWITCH_INTERVAL), end='', flush=True)
    while True:
        for file in Path('.').glob('./*.odp'):
            try:
                pr = Popen(['libreoffice', \
                        '--norestore', \
                        '--nologo', \
                        '--impress', \
                        '--show', \
                        str(file)])
                _thread.start_new_thread(show_counter, ())
                time.sleep(SWITCH_INTERVAL)
                pr.terminate()
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(1)

if __name__ == '__main__':
    main()
