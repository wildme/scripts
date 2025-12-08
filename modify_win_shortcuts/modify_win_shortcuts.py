#!/usr/bin/env python3
"""
This script recursivly vists subdirectories in the specified path and
saves the path to every .lnk file it finds. The path and working_directory
attributes of .lnk files will be altered according to the input from the
user.
"""
import os
import sys
import winshell
import _thread
from collections import deque
from typing import Deque

sys.path.append('../')
from mods.txtviz import CharCircle, Counter

def find_win_shortcuts(start_dir: str) -> Deque[str]:
    lnk_paths: Deque[str] = deque()
    counter = Counter()

    print("Found files: %s" % (counter.value,), end='', flush=True)
    for top, dirs, files in os.walk(start_dir):
        if not files:
            continue
        # select .lnk files
        for lnk in [_ for _ in files if _.endswith('.lnk')]:
            # save the path in the list
            lnk_paths.append(os.path.join(top, lnk))
            counter.increment()
            counter.update_inc(counter.value)
    print()

    return lnk_paths

def modify_win_shortcuts(lnks: Deque[str], old_str: str, new_str: str) -> None:
    for lnk_file in lnks:
        with winshell.shortcut(lnk_file) as lnk:
            lnk.working_directory = lnk.working_directory.replace(old_str, new_str)
            lnk.path = lnk.path.replace(old_str, new_str)
            lnk.write()

def main() -> None:
    working_dir: str = sys.argv[1]
    old_str: str = sys.argv[2]
    new_str: str = sys.argv[3]

    lnk_files: Deque[str] = find_win_shortcuts(working_dir)

    if len(lnk_files):
        print('Processing files: /', end='', flush=True)
        circle = CharCircle(r'-\|/-\|/')
        _thread.start_new_thread(circle.start, ())
        modify_win_shortcuts(lnk_files, old_str, new_str)
        print('\b\b', 'Done!')

if __name__ == '__main__':
    if os.name != 'nt':
        print('Error: This platform is not supported. Windows only.')
        sys.exit(1)
    if len(sys.argv) < 4:
        input_err_msg: str = """
        ARGS: <top> <pattern> <replacement>
        top - the full path to the directory where the search begins
        pattern - pattern in the string
        replacement - a new string
        """
        print(input_err_msg)
        sys.exit(1)
    main()
