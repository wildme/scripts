#!/usr/bin/env python3
import os
import sys
import re
from multiprocessing  import Process
import mod1_args
import mod2_dots as dots

def dirlist(base = os.getcwd(), rec_l = 3):
    root = [] 
    items = list(map((lambda x: x.path),\
            filter((lambda x: \
            (not x.name.startswith('.')) and os.access(x, os.R_OK) \
            and x.is_dir()), \
            os.scandir(base))))

    for i in items:
        if rec_l == 0:
            exit
        else:
            root.append(i)
            temp = dirlist(i, rec_l = rec_l - 1) # recursion
            for i2 in temp:
                root.append(i2)
    return root 

def fsearch(dirs, filename):
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

def msearch(files, s):
    res = {}
    for k in files.keys():
        for i in files[k]:
            myfile = k + '/' + i
            c = 0
            temp = []
            for line in open(myfile):
                c += 1
                match = re.search(s, line)
                if match:
                    a = 'L%d %s' % (c, line)
                    temp.append(a)
                    res[myfile] = temp
                else:
                    pass
    return res

if __name__ == '__main__':
    if len(sys.argv) == 1:
        current_dir = dirlist()
        for i in current_dir:
            print(i)
    else:
        L =  mod1_args.myargs(sys.argv[1:])
        where = what = inside = None
        # Groups of arguments
        args_g1 = [0, 0] # Group 1. -d, -r. It's WHERE we look for items
        args_g2 = 0 # Group 2. -f. It's WHAT we want to find
        args_g3 = 0 # Group 3. -m. It's what we need INSIDE items
        if L:
            if '-d' in L.keys(): args_g1[0] = 1
            if '-r' in L.keys(): args_g1[1] = 1
            if '-f' in L.keys(): args_g2 = 1
            if '-m' in L.keys(): args_g3 = 1
            
            p = Process(target=dots.tik)
            p.start()
            # Setting targets for searching
            if args_g1[0] == 1 and args_g1[1] == 1: # -d and -r are set
                where = dirlist(base=L['-d'], rec_l=L['-r'])
            else:
                if args_g1[0] == 0 and args_g1[1] == 0: # -d and -r aren't set. Use defaults
                    where = dirlist()
                else:
                    if args_g1[0] == 1:
                        where = dirlist(base=L['-d'])
                    if args_g1[1] == 1:
                        where = dirlist(rec_l=L['-r'])
            if args_g2 == 1:
                what = fsearch(dirs=where,filename=L['-f'])
            if args_g3 == 1:
                inside = msearch(files=what, s=L['-m'])
            p.kill()

            for i in (inside, what, where):
                if i != None:
                    if type(i) == list:
                        for x in i:
                            print(x)
                    if type(i) == dict:
                        for y in i.keys():
                            print(y,':', i[y])
                    break
