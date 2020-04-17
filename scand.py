#!/usr/bin/env python3
import os
import re

def dirlist(base='/usr/share', rec_l = 3):
    root = [] 
    items = list(map((lambda x: x.path),\
            filter((lambda x: (not x.name.startswith('.')) and x.is_dir()), os.scandir(base))))
    #print(rec_l)

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
        items = list(map((lambda x: x.name), \
                filter((lambda x: (not x.name.startswith('.')) and x.is_file()), os.scandir(d))))
        if filename in items:
            res[d] = filename
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

D = dirlist()
for i in D:
    print(i)

#text = msearch('/home/kostya/python/test', 'file.txt', '1234')
#for k in text.keys():
#    print('file: ', k, 'strings: ', text[k])

#files = fsearch('1', 'file.txt')
#sp = 0
#for x in files:
#    if len(x) > sp:
#        sp = len(x)
#
#for k in files:
#    print('dir:', k, ' ' * (sp - len(k)), 'file:', files[k], end='\n')

#text = textmatch('test', 'file.txt', '124')
#print(text)
