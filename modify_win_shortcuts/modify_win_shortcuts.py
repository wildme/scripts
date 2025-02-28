import os
import sys
import winshell

def find_win_shortcuts(start_dir: str) -> list[str]:
    lnk_paths: list[str] = []
    cwd: str = os.getcwd()
    out_file = open(f'{cwd}\\lnk_files.txt', 'w')
    tmp_full_path: str = ''

    for top, dirs, files in os.walk(start_dir):
        if not files:
            continue
        # select only .lnk files
        for lnk in [_ for _ in files if _.endswith('.lnk')]:
            tmp_full_path = os.path.join(top, lnk)
            # save the path in the list
            lnk_paths.append(tmp_full_path)
            # save the path to the file
            print(tmp_full_path, file=out_file)
    out_file.close()

    return lnk_paths

def modify_win_shortcuts(lnks: list[str], old_str: str, new_str: str) -> None:
    for lnk_file in lnks:
        with winshell.shortcut(lnk_file) as lnk:
            lnk.working_directory = lnk.working_directory.replace(old_str, new_str)
            lnk.path = lnk.path.replace(old_str, new_str)
            lnk.write()

if __name__ == '__main__':
    working_dir: str = sys.argv[1]
    old_str: str = sys.argv[2]
    new_str: str = sys.argv[3]

    lnk_files = find_win_shortcuts(working_dir)
    modify_win_shortcuts(lnk_files, old_str, new_str)
