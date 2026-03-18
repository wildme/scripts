#!/usr/bin/python3

import sys
import json
from typing import Any

def print_subnets(subnets: set[str]) -> None:
    for _ in subnets:
        print(_, end=',') # print the resulting set
    sys.stdout.write('\b \b\n') # delete the last comma and insert a new line

def subnets_for(web_target: dict[str, Any]) -> set[str]:
    subs: set[str] = set()

    for k in web_target.keys():
        if isinstance(web_target[k], list): # this is a list of subnets
            for _ in web_target[k]:
                subs.add(_)
        else:
            subs.add(web_target[k]) # this is a string
    return subs

def main(web_targets: list[str] | None = None) -> None:
    db_file: str = 'subnets.json'
    data: dict[str, str] = {}
    res: set[str] = set()
    tmp: set[str] = set()

    try:
        json_file = open(db_file, 'r')
    except:
        print(f'Error: cannot access {db_file}. Exiting...')
        sys.exit(1)

    data = json.load(json_file)
    json_file.close()

    if web_targets == None:
        web_targets = [x for x in data.keys()]

    for _ in web_targets:
        try:
            tmp = subnets_for(data[_])
        except KeyError:
            print(f'{_} target not found. Check {db_file} for available targets')
        res.update(tmp)

    if len(res) > 0:
        print_subnets(res)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        main(sys.argv[1:])
