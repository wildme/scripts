import os
import sys
import winshell
import time
import _thread
from collections import deque
from typing import Deque

class CharCircle:
    def __init__(self, chars):
        self.chars = chars
        self.value = self.chars[0]
        self.head = 0
        self.tail = len(self.chars) - 1

    def __iter__(self):
        return self

    def __next__(self):
        # item between head and tail
        self.value = self.head
        self.head = (self.head + 1) % self.tail # reset to 0 after tail
        return self.chars[self.value]

def update_counter(cnt: int) -> None:
    sys.stdout.write('\b' * len(str(eval('cnt - 1'))))
    sys.stdout.write(str(cnt))
    sys.stdout.flush()

def show_activity() -> None:
    for _ in CharCircle(r'-\|/-\|/'):
        sys.stdout.write('\b')
        sys.stdout.write(_)
        sys.stdout.flush()
        time.sleep(0.3)

def find_win_shortcuts(start_dir: str) -> Deque[str]:
    lnk_paths: Deque[str] = deque()
    counter: int = 0

    print("Found files: %s" % (counter,), end='', flush=True)
    for top, dirs, files in os.walk(start_dir):
        if not files:
            continue
        # select .lnk files
        for lnk in [_ for _ in files if _.endswith('.lnk')]:
            # save the path in the list
            lnk_paths.append(os.path.join(top, lnk))
            counter += 1
            update_counter(counter)
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
        _thread.start_new_thread(show_activity, ())
        modify_win_shortcuts(lnk_files, old_str, new_str)
        print('\b\b', 'Done!')

if __name__ == '__main__':
    main()
