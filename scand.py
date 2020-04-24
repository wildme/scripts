#!/usr/bin/env python3
import os
import sys
import re
import procarg

def dirlist(base = os.getcwd(), rec_l = 4):
    root = [] 
    items = list(map((lambda x: x.path),\
            filter((lambda x: \
            (not x.name.startswith('.')) and os.access(x, os.R_OK)\
            and x.is_dir()),\
            os.scandir(base))))

    for i in items:
        if rec_l == 0:
            exit
        else:
            root.append(i)
            temp = dirlist(i, rec_l = rec_l - 1)
            for i2 in temp:
                root.append(i2)
    return root 

def fsearch(path, filename):
    dirs = dirlist(path)
    res = {}
    for d in dirs:
        items = list(filter((lambda x: re.search(filename, x)), \
                map((lambda x: x.name), \
                filter((lambda x: \
                (not x.name.startswith('.')) \
                and x.is_file()), os.scandir(d)))))
        if(items):
            res[d] = items
    return res

def msearch(p, f, s):
    files = fsearch(p, f)
    for k in files.keys():
        for i in files[k]:
            myfile = k + '/' + i
            c = 0
            print(myfile)
            for line in open(myfile):
                c += 1
                match = re.search(s, line)
                if match:
                    print('L%d %s' % (c, line), end='')
                else:
                    pass
    return 0

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dl = scand.dirlist()
        for i in dl:
            print(i, end='\n')
    else:
        L =  procarg.myargs(sys.argv[1:])


