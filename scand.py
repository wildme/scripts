#!/usr/bin/env python3
import os
import re

def dirlist(base = os.getcwd(), rec_l = 4):
    root = [] 
    items = list(map((lambda x: x.path),\
            filter((lambda x: (not x.name.startswith('.')) and x.is_dir()),\
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
                #if filename in items:
            #res[d] = filename
    return res

def msearch(p, f, s):
    files = fsearch(p, f)
    mres = {} # collect results in a dictionary
    for k in files.keys():
        mstr = [] # collect matches strings per a file
        myfile = k + '/' + files[k]
        for line in open(myfile):
            match = re.search(s, line)
            if match:
                mstr.append(line)
            if mstr:
                mres[myfile] = mstr
            else:
                mres[myfile] = ['no match']
    return mres
