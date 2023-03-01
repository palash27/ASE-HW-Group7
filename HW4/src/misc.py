import math 
import re
import sys
from csv import reader
import random
import copy
import json

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
  -g  the   show settings
  -g  copy  check copy
  -g  repcols   checking repcols
  -g  synonyms  checking repcols cluster
  -g  reprows   checking reprows
  -g  prototypes    checking reprows cluster
  -g  position  where's wally
  -g  every the whole enchilada
"""

def transpose(t):
    """
    returns transpose of a matrix / 2d list
    """
    u=[]
    for i in range(0, len(t[0])):
        u.insert(i,[])
        for j in range(0, len(t)):
            u[i].insert(j, t[j][i])
    return u

def repCols(cols, Data):
    """
    returns Data(cols)
    """
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

def repRows(t, rows, Data=None):
    """
    returns Data(rows)
    """
    rows = copy.deepcopy(rows)
    for j, s in enumerate(rows[len(rows) - 1]):
        rows[0][j] = rows[0][j] + ":" + s
    rows.pop()
    for n, row in enumerate(rows):
        if n == 0:
            row.append("thingX")
        else:
            u = t["rows"][len(t["rows"]) - n]
            row.append(u[len(u) - 1])
    data = Data(rows)
    return data

def repPlace(data,n=20):
    """
    prints g[y]
    """
    g = []
    for i in range(n + 1):
        g.append([])
        for j in range(n + 1):
            g[i].append(" ")
    maxy = 0
    print("")
    print(data.rows)
    for r, row in enumerate(data.rows):
        c = chr(65 + r)
        print(c, row["cells"][-1])
        x, y = int(row["x"] * n), int(row["y"] * n)
        maxy = max(maxy, y + 1)
        g[y + 1][x + 1] = c
    print("")
    for y in range(1, maxy + 1):
        oo(g[y])

def dofile(file_path):
    """
    function to read custom csv in lua
    """
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = file.read()

    return_statement = re.findall(r"(?<=return )[^.]*", file_contents)[0]
    text = (return_statement.replace("{", "[").replace("}", "]").replace("=", ":").replace("[\n", "{\n").replace(" ]", " }").replace("'", '"').replace("_", '"_"'))

    json_text = re.sub(r"(\w+):", r'"\1":', text)[:-2] + "}"
    file_json = json.loads(json_text)

    return file_json

def repgrid(sFile, Data=None):
    """
    repgrid function to work on the file passed
    """
    t=dofile(sFile)
    rows = repRows(t, transpose(t["cols"]), Data)
    cols = repCols(t["cols"], Data)
    show(rows.cluster(rows.cols.all))
    show(cols.cluster(cols.cols.all))
    repPlace(rows)

def show(node, what=0, cols=0, nPlaces=0, lvl=0):
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
    t.append(x)
    return x

def map(t,fun):
    """
    t; map a function `fun`(v) over list (skip nil results) 
    """
    u = {}
    print(t)
    for k,v in enumerate(t):
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
    for k, v in enumerate(t):
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

# def o(t):
#     """
#     convert `t` to a string. sort named keys. 
#     """
#     keys = list(t.keys())
#     keys = sorted(keys)
#     sorted_t = {i: t[i] for i in keys }
#     output = "{"
#     for k, v in sorted_t.items():
#         output = output + ":"+str(k) + " " + str(v) + " "
#     output = output + "}"
#     return output

def o(t, isKeys=False):
    """
    convert `t` to a string. sort named keys. 
    """
    if type(t) != dict:
        return str(t)
    
    def to_str(k, v):
        if not str(k).startswith("_"):
            return f":{o(k)} {o(v)}"
    
    pairs = []
    for k, v in sorted(t.items(), key=lambda x: str(x[0]) if not isinstance(x[0], int) else x[0]):
        if isKeys or isinstance(k, int):
            pairs.append(o(v))
        else:
            pair_str = to_str(k, v)
            if pair_str is not None:
                pairs.append(pair_str)
    
    if not pairs:
        return "{}"
    elif len(pairs) == 1:
        return pairs[0]
    else:
        return "{" + " ".join(pairs) + "}"

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
