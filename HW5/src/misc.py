import math 
import re
import sys
import random
from csv import reader
from src.Sym import *
import copy
import io 
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
  -r  --rest    how many of rest to sample   = 4
  -b  --bins    initial number of bins       = 16
  -H  --Halves  search space for clustering  = 512
  -R  --Reuse   child splits reuse a parent pole = true
ACTIONS:
  -g  the	show settings
  -g  sym	check syms
  -g  num	check nums
  -g  csv	read from csv
  -g  data	read DATA csv
  -g  stats	stats from DATA
"""


def show(node, what, cols, nPlaces, lvl=0):
    if node:
        print('| '*lvl + str(len(node['data'].rows)) + " ", end = '')
        if (not node.get('left') or lvl==0):
            print(o(node['data'].stats("mid",node['data'].cols.y, nPlaces )))
        else:
            print("")
        show(node.get('left'), what, cols, nPlaces, lvl+1)
        show(node.get('right'), what, cols, nPlaces, lvl+1)



def rint(lo,hi):
    """
    Rounds to integer
    """
    return math.floor(0.5 + rand(lo, hi))

def rand(lo, hi, Seed = 937162211):
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def rnd(n, nPlaces=3):
    mult = 10 ** (nPlaces)
    return math.floor(n * mult + 0.5) / mult

#Lists
def push(t, x):
    t[1 + len(t)] = x
    return x
 
def kap(t, fun):
    x = {}
    for i in t:
        k = t.index(i)
        i, k =fun(k,i)
        x[k or len(x)] = i
    return x
    # u = {}
    # for k, v in t.items():
    #     v, k = fun(k ,v)
    #     u[k or (1 + len(u))] = v
    # return u

# def map(t,fun):
#     u = {}
#     for k,v in t.items():
#         v,k = fun(v)
#         if k is None:
#             u[1+len(u)] = v
#         else:
#             u[k] = v
#     return u

def any(t):
    return t[random.randint(0, len(t)-1)]

def many(t, n):
    u = []
    for i in range(1,n+1):
        u.append(any(t))
    return u

def cosine(a,b,c):
    temp = 1 if c == 0 else 2*c
    x1 = (a**2 + c**2 - b**2) // temp
    x2 = max(0, min(1, x1)) 
    y  = abs((a**2 - x2**2)**0.5)
    return x2, y

def coerce(s):
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
    print(o(t))
    return t

def o(t):
    # keys = list(t.keys())
    # keys = sorted(keys)
    # sorted_t = {i: t[i] for i in keys }
    # output = "{"
    # for k, v in sorted_t.items():
    #     output = output + ":"+str(k) + " " + str(v) + " "
    # output = output + "}"
    # return output
    if type(t)!=dict:
        return str(t)
    def show(k,v):
        if "^_" not in str(k):
            v=o(v)
            return str(k)+" : "+str(v)
    u=[]
    for k in t:
        u.append(show(k,t[k]))
    if len(t)==0:
        u.sort()
    return " ".join(u)

def settings(s):
    t = {}
    for k,v in re.findall("[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s): 
        t[k] = coerce(v)
    return t

def cli(command_line_args):
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

# def csv(file_name, fun):
#     sep = "([^" + "\," + "]+"
#     with open(file_name) as file_obj:
#         reader_obj = reader(file_obj)
#         for row in reader_obj:
#             t = {}
#             for element in row:
#                 t[str(1+len(t))] = coerce(element)
#             fun(t)

def csv(sFilename, fun):
    if sFilename:
        src = io.open(sFilename)
        t = []
        for _,l in enumerate(src):
            s = l.strip().split(',')
            r = list(map(coerce, s))
            t.append(r)
            fun(r)
    else:
        print("not opeinng")

def deepcopy(t):
    return copy.deepcopy(t)

def cliffsDelta(the, ns1, ns2):
    if(len(ns1)>256):
        ns1 = many(ns1, 256)
    if(len(ns2)>256):
        ns2 = many(ns2, 256)
    if(len(ns1)>10*len(ns2)):
        ns1 = many(ns1, 10*len(ns2))
    if(len(ns2)>10*len(ns1)):
        ns2= many(ns2, 10*len(ns1))
    
    n, gt, lt = 0, 0, 0
    for _,x in enumerate(ns1):
        for _,y in enumerate(ns2):
            n+=1
            if x > y:
                gt = gt + 1
            if x < y: 
                lt = lt + 1
    
    return abs(lt-gt)/n > the['cliffs']

# def diffs(nums1, nums2):
#     return kap(nums1, cliffsDelta(nums['has'], nums2[k]['has'], nums.txt))

def bins(the,cols,rowss):
    out =[]
    for col in cols:
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                x = row.cells[col.at]
                if x!= '?':
                    k = int(bin(the,col,x))
                    if not k in ranges:
                        ranges[k] = RANGE(col.at, col.txt, x)
                    extend(ranges[k], x, y)
        ranges = list(dict(sorted(ranges.items())).values())
        if(isinstance(col, Sym)):
            r = ranges
        else:
            r = mergeAny(ranges)
        out.append(r)
    return out

def bin(the,col,x):
    if x=="?" or isinstance(col, Sym):
        return x
    tmp = (col.hi - col.lo)/(int(the['bins']) - 1)
    return  1 if col.hi == col.lo else math.floor(float(x)/tmp + 0.5)*tmp

def merge(col1,col2):
  new = deepcopy(col1)
  if isinstance(col1, Sym):
      for n in col2.has:
        new.add(n)
  else:
    for n in col2.has:
        new.add(new,n)
    new.lo = min(col1.lo, col2.lo)
    new.hi = max(col1.hi, col2.hi) 
  return new

def RANGE(at,txt,lo,hi=None):
    return {'at':at,'txt':txt,'lo':lo,'hi':lo or hi or lo,'y':Sym()}

def extend(range,n,s):
    range['lo'] = min(float(n), float(range['lo']))
    range['hi'] = max(float(n), float(range['hi']))
    range['y'].add(s)

def itself(x):
    return x

def value(has,nB = None, nR = None, sGoal = None):
    sGoal,nB,nR = sGoal or True, nB or 1, nR or 1
    b,r = 0,0
    for x,n in has.items():
        if x==sGoal:
            b = b + n
        else:
            r = r + n
    b,r = b/(nB+1/float("inf")), r/(nR+1/float("inf"))
    return b**2/(b+r)


def merge2(col1,col2):
  new = merge(col1,col2)
  if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
    return new

def mergeAny(ranges0):
    def noGaps(t):
        for j in range(1,len(t)):
            t[j]['lo'] = t[j-1]['hi']
        t[0]['lo']  = float("-inf")
        t[len(t)-1]['hi'] =  float("inf")
        return t

    ranges1,j = [],0
    while j <= len(ranges0)-1:
        left = ranges0[j]
        right = None if j == len(ranges0)-1 else ranges0[j+1]
        if right:
            y = merge2(left['y'], right['y'])
            if y:
                j = j+1
                left['hi'], left['y'] = right['hi'], y
        ranges1.append(left)
        j = j+1
    return noGaps(ranges0) if len(ranges0)==len(ranges1) else mergeAny(ranges1)