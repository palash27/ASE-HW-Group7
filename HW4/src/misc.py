import math 
import re
import sys
from csv import reader
import random
import copy
from src.Data import Data

#Numerics
help = """   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE:   script.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file    name of file       = data/data.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512
ACTIONS:
  -g  the	show settings
  -g  sym	check syms
  -g  num	check nums
  -g  csv	read from csv
  -g  data	read DATA csv
  -g  stats	stats from DATA
"""

def transpose(t):
    u=[]
    for i in range(0, len(t[0])):
        u[i] = []
        for j in range(0, len(t)):
            u[i][j] = t[j][i]
    return u

def repCols(cols):
    cols = copy.deepcopy(cols)
    for i in range(len(cols)):
        col = cols[i]
        col[len(col) - 1] = col[0] + ":" + col[len(col) - 1]
        for j in range(1, len(col) - 1):
            col[j - 1] = col[j]
        col.pop()
    cols.insert(0, ["Num" + str(k) for k in range(len(cols[0]))])
    cols[0][len(cols[0]) - 1] = "thingX"
    data = Data(cols)
    return data

def show(node, what, cols, nPlaces, lvl=0):
    """
    nil; prints the tree generated from `DATA:tree`.
    """
    if node:
        print('| '*lvl + str(len(node['data'].rows)) + " ", end = '')
        if (not node.get('left') or lvl==0):
            print(o(node['data'].stats("mid",node['data'].cols.y, nPlaces )))
        else:
            print("")
        show(node.get('left'), what, cols, nPlaces, lvl+1)
        show(node.get('right'), what, cols, nPlaces, lvl+1)


def rint(lo, hi):
    """
    a integer lo..hi-1
    """
    return math.floor(0.5 + rand(lo, hi))

def rand(lo, hi, Seed):
    """
    a float "x" lo<=x < x
    """
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def rnd(n, nPlaces=3):
    """
    return `n` rounded to `nPlaces`
    """
    mult = 10 ** (nPlaces)
    return math.floor(n * mult + 0.5) / mult

def any(t):
    """
    x; returns one items at random
    """
    return t[random.randint(1, len(t)-1)]

def many(t, n):
    """
    t1; returns some items from `t`
    """
    u = {}
    for i in range(1,n+1):
        u[1+len(u)] = any(t)
    return u

def last(t):
    """
    x
    """
    return t[len(t)-1]

def cosine(a,b,c):
    """
    n,n;  find x,y from a line connecting `a` to `b`
    """
    temp = 1 if c == 0 else 2*c
    x1 = (a**2 + c**2 - b**2) // temp
    x2 = max(0, min(1, x1)) 
    y  = abs((a**2 - x2**2)**0.5)
    return x2, y

#Lists
def push(t, x):
    """
    push `x` to end of list; return `x` 
    """
    t[1 + len(t)] = x
    return x

def map(t,fun):
    """
    t; map a function `fun`(v) over list (skip nil results) 
    """
    u = {}
    for k,v in t.items():
        v,k = fun(v)
        if k is None:
            u[1+len(u)] = v
        else:
            u[k] = v
    return u
    
def kap(t, fun):
    """
    map function `fun`(k,v) over list (skip nil results) 
    """
    u = {}
    for k, v in t.items():
        v, k = fun(k ,v)
        u[k or (1 + len(u))] = v
    return u
#strings

def coerce(s):
    """
    return int or float or bool or string from `s`
    """
    def fun(s1):
        if s1 == "true":
            return True
        elif s1 == "false":
            return False
        else:
            return s1
    if s.isnumeric():
        return int(s)
    elif type(s) != bool:
        return fun(re.search('^[\s]*[\S+]*[\s]*$', s).group(0))



def oo(t):
    """
    print `t` then return it
    """
    print(o(t))
    return t

def o(t):
    """
    convert `t` to a string. sort named keys. 
    """
    keys = list(t.keys())
    keys = sorted(keys)
    sorted_t = {i: t[i] for i in keys }
    output = "{"
    for k, v in sorted_t.items():
        output = output + ":"+str(k) + " " + str(v) + " "
    output = output + "}"
    return output

def settings(s):
    """
    parse help string to extract a table of options
    """
    t = {}
    for k,v in re.findall("[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s): 
        t[k] = coerce(v)
    return t

def cli(command_line_args):
    """
    update key,vals in `t` from command-line flags
    """
    options = {}
    options = settings(help)
    for k, v in options.items():
        v = str(v)
        for n, x in enumerate(command_line_args):
            if x == '-'+k[0] or x == '--'+k:
                if v == "true":
                    v = "false"
                elif v == "false":
                    v = "true"
                else:
                    v = command_line_args[n+1]
        options[k] = coerce(v)

    return options

def csv(file_name, fun):
    """
    call `fun` on rows (after coercing cell text)
    """
    sep = "([^" + "\," + "]+"
    with open(file_name) as file_obj:
        reader_obj = reader(file_obj)
        for row in reader_obj:
            t = {}
            for element in row:
                t[str(1+len(t))] = coerce(element)
            fun(t)
