#!/usr/bin/env python3
import sys
import scand

OPTS = ['-d', '-r', '-f', '-m']
D = {} 
if len(sys.argv) == 1:
    dl = scand.dirlist()
    for i in dl:
        print(i, end='\n')
else:
    for arg in sys.argv[1:]:
        if arg not in OPTS and arg.startswith('-'):
            print("Invalid option: ", arg)
            print("Usage: scand [-d path] [-r number]", end=' ')
            print("[-f file] [-m text]")
            D = {}
            break
        if arg in D:
            print('Error:', arg, 'is duplicated')
            D = {}
            break
        if arg in OPTS:
            ind = (sys.argv).index(arg)
            c = 0
            try:
                D[arg] = sys.argv[ind + 1]
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
                if arg == '-m' and '-f' not in sys.argv[1:]: raise SyntaxError
            except SyntaxError:
                print('-m option requires a file to be specified. Use -f <file>')
                D = {}
                break
        if c > 1:
            print ("Syntax error: too much arguments")
            print("Usage: scand [-d path] [-r number]", end=' ')
            print("[-f file] [-m text]")
            D = {}
            break
        else:
            c += 1
            pass
#print(D)
