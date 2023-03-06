import math 
import re
import sys
import random
from csv import reader
from src.Sym import *


#Numerics
help = """   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE:   script.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -f  --file    data file                    = data/data.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
ACTIONS:
  -g  the	show settings
  -g  sym	check syms
  -g  num	check nums
  -g  csv	read from csv
  -g  data	read DATA csv
  -g  stats	stats from DATA
"""


def add(the, col, x, n=1):
    if x != '?':
        col['n'] = col['n'] + n
        if 'isSym' in col:
            col['has'][x] = n + col['has'].get(x, 0)
            if col['has'][x] > col['most']:
                col['most'], col['mode'] = col['has'][x], x
        else:
            col['lo'], col['hi'] = min(x, col['lo']), max(x, col['hi'])
            all = len(col['has'])
            if all < int(the['Max']):
                col['has'].append(x)
            else:
                if rand() < int(the['Max'])/int(col['n']):
                    pos = rint(1,all)
                    col['has'][pos] = x
            col['ok'] = False


def range_f(at,txt,lo,hi):
  """
  -- Create a RANGE  that tracks the y dependent values seen in 
  -- the range `lo` to `hi` some independent variable in column number `at` whose name is `txt`. 
  -- Note that the way this is used (in the `bins` function, below)
  -- for  symbolic columns, `lo` is always the same as `hi`.
  """
  return {
  'at':at,
  'txt':txt,
  'lo':lo,
  'hi':lo or hi or lo,
  'y':sym()
  }


def extend(range, n, s):
    range['lo'] = min(n, range['lo'])
    range['hi'] = max(n, range['hi'])
    add(range['y'], s)

def dist(data, t1, t2, cols):
    if cols is None:
        cols = data['cols']['x']
    d, n = 0, 1/float('inf')
    def dist1(col, x, y):
        if x == '?' and y == '?':
            return 1
        if 'isSym' in col:
            if x == y:
                return 0
            else:
                return 1
        else:
            x, y = norm(col, x), norm(col, y)
            if x == '?':
                if y<0.5:
                    x = 1
                else:
                    x = 1
            if y == '?':
                if x < 0.5:
                    y = 1
                else:
                    y = 1
            return abs(x-y)
    for _, col in cols.items():
        n = n + 1
        d = dist1(col, t1[col['at'], t2[col['at']]**2]) #the.p
    return (d/n)^(1/2) #the.p


def norm(num,n):
    if n=='?':
        return n
    else:
        return (n-num['lo'])/(num['hi'] - num['lo'] + (1/float('inf')))
    
def better(data, row1, row2):
    s1, s2, ys, x, y  = 0, 0, data['cols']['y'], None, None
    for _, col in ys.items():
        x = norm(col, row1[col['at']])
        y = norm(col, row2[col['at']])
        s1 = s1 - math.exp(col['w']*(x-y)/len(ys))
        s2 = s2 - math.exp(col['w']*(x-y)/len(ys))
    return s1/len(ys) < s2/len(ys)


def has(col):
    if 'isSym' not in col and not col['ok']:
        col['has'].sort()
    col['ok'] = True
    return col['has']

def mid(col):
    if 'isSym' in col:
        return col['mode']
    else:
        return per(has(col), 0.5)
    
def div(col):
    if 'isSym' in col:
        e = 0
        for _, n in col['has'].items():
            e = e-n/int(col['n'])*math.log(n/int(col['n']),2)
        return e
    else:
        return (per(has(col),0.9) - per(has(col),0.1))/2.58

def per(t, p=0.5):
    p = math.floor((p*len(t))+0.5)
    return t[max(1, min(len(t),p))]


def show(node, what, cols, nPlaces, lvl=0):
    if node:
        print('| '*lvl + str(len(node['data'].rows)) + " ", end = '')
        if (not node.get('left') or lvl==0):
            print(o(node['data'].stats("mid",node['data'].cols.y, nPlaces )))
        else:
            print("")
        show(node.get('left'), what, cols, nPlaces, lvl+1)
        show(node.get('right'), what, cols, nPlaces, lvl+1)

#Optimization



# Discretization

# def bins(cols, rowss):
#     """
#     -- Return RANGEs that distinguish sets of rows (stored in `rowss`).
#     -- To reduce the search space,
#     -- values in `col` are mapped to small number of `bin`s.
#     -- For NUMs, that number is `the.bins=16` (say) (and after dividing
#     -- the column into, say, 16 bins, then we call `mergeAny` to see
#     -- how many of them can be combined with their neighboring bin).
#     """
#     out={}
#     for _,col in enumerate(cols):
#         ranges={}
#         for y,rows in enumerate(rowss):
#             for _,row in enumerate(rows):
#                 x,k=row[col['at']]
#                 if x!="?":
#                     k=bin(col,x)
#                     ranges[k]=ranges[k] or RANGE(col['at'], col['txt'], x)
#                     extend(ranges[k],x,y)
#         ranges = sorted(map(ranges,itself))
#         out[len(out)] = col['isSym'] and ranges or mergeAny(ranges)
#     return out

# def bin(col,x):
#     """
#     -- Map `x` into a small number of bins. `SYM`s just get mapped
#     -- to themselves but `NUM`s get mapped to one of `the.bins` values.
#     -- Called by function `bins`.
#     """
#     if x=="?" or col['isSym']:
#         return x
#     tmp = (col['hi']-col['lo'])/(the['bins']-1)
#     return col['hi'] == col['lo'] and 1 or math.floor(x/tmp+0.5)*tmp

# def mergeAny(ranges0):
#     def noGaps(t):
#         for j in range(1,len(t)):
#             t[j]['lo'] = t[j-1]['hi']
        
#         t[0]['lo']  = float('-inf')
#         t[-1]['hi'] = float('inf')
        
#         return t
  
#     ranges1, j, left, right, y = [], 0, None, None, None
    
#     while j < len(ranges0):
#         left, right = ranges0[j], None
        
#         if j + 1 < len(ranges1):
#             right = ranges0[j + 1]
#             y = merge2(left['y'],right['y'])
#             if y:
#                 j += 1
#                 left['hi'], left['y'] = right['hi'], y
        
#         ranges1.append(left)
#         j += 1
    
#     return len(ranges0) == len(ranges1) and noGaps(ranges0) or mergeAny(ranges1)

# def merge2(col1, col2):
#     new = merge(col1, col2)
    
#     if div(new) <= (div(col1)*col1['n'] + div(col2)*col2['n'])/new['n']:
#         return new


# def merge(col1, col2):
#     new = copy(col1)
#     if col1['isSym']:
#         for x, n in col2['has'].items():
#             add(new, x, n)
#     else:
#         for _, n in col2['has'].items():
#             add(new, n)
#         new.lo = min(col1['lo'], col2['lo'])
#         new.hi = max(col1['hi'], col2['hi'])
    
#     return new

def rint(lo,hi):
    """
    Rounds to integer
    """
    return math.floor(0.5 + rand(lo, hi))

def rand(lo=0, hi=1, Seed = 937162211):
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def rnd(n, nPlaces=2):
    mult = 10 ** (nPlaces)
    return math.floor(n * mult) / mult

#Lists
def push(t, x):
    t[1+len(t)] = x
    return x
 
def kap(t, fun):
    u = {}
    for k, v in t.items():
        v, k = fun(k ,v)
        u[k or (1 + len(u))] = v
    return u

def map(t,fun):
    u = {}
    for k,v in t.items():
        v,k = fun(v)
        if k is None:
            u[1+len(u)] = v
        else:
            u[k] = v
    return u

def any(t):
    return t[random.randint(1, len(t)-1)]

def many(t, n):
    u = {}
    for i in range(1,n+1):
        u[1+len(u)] = any(t)
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
    keys = list(t.keys())
    keys = sorted(keys)
    sorted_t = {i: t[i] for i in keys }
    output = "{"
    for k, v in sorted_t.items():
        output = output + ":"+str(k) + " " + str(v) + " "
    output = output + "}"
    return output

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

def csv(file_name, fun):
    sep = "([^" + "\," + "]+"
    with open(file_name) as file_obj:
        reader_obj = reader(file_obj)
        for row in reader_obj:
            t = {}
            for element in row:
                t[str(1+len(t))] = coerce(element)
            fun(t)

