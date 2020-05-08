#!/usr/bin/env python3.8

def myargs(l_args):
    D = {} 
    OPTS = ['-d', '-r', '-f', '-m', '-h']
    helpmsg="Usage: scand [OPTION]\n\
            -d PATH\tdirectory where the search starts\n\
            -r NUMBER\trecursion level. Default value: 3\n\
            -f STRING\tfile name\n\
            -m STRING\tthe string sequence to be search in files\n\
            -h\t\tshow this help"
    for arg in l_args:
        if arg not in OPTS and arg.startswith('-'):
            print("Invalid option: ", arg)
            print("Usage: scand [-d path] [-r number]", end=' ')
            print("[-f string] [-m string]")
            D = {}
            break
        if arg in D:
            print('Error:', arg, 'is duplicated')
            D = {}
            break
        if arg in OPTS:
            ind = (l_args).index(arg)
            c = 0
            try:
                if arg == '-h': raise SyntaxError
            except SyntaxError:
                print(helpmsg)
                D = {}
                break
            try:
                D[arg] = l_args[ind + 1]
            except IndexError:
                print("Syntax error:", end=' ')
                print(arg, 'is missing an argument')
                D = {}
                break
            try:
                if D[arg].startswith('-'): raise SyntaxError
            except SyntaxError:
                print("Syntax error:", end=' ')
                print(arg, 'is missing an argument. hyphen is not allowed.')
                D = {}
                break
            try:
                if arg == '-m' and '-f' not in l_args: raise SyntaxError
            except SyntaxError:
                print('-m option requires a file to be specified. Use -f <string>')
                D = {}
                break
            try:
                if arg == '-r': raise TypeError
            except TypeError:
                D[arg] = int(l_args[ind + 1])
        if c > 1:
            print ("Syntax error: too much arguments")
            print("Usage: scand [-d path] [-r number]", end=' ')
            print("[-f string] [-m string]")
            D = {}
            break
        else:
            c += 1
            pass
    return D
