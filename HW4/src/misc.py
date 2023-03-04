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
    for i,col in enumerate(cols):
        col[len(col) - 1] = col[0] + ":" + col[len(col) - 1]
        for j in range(1, len(col)):
            col[j - 1] = col[j]
        col.pop()
    s=[]
    for i in range(len(cols[0])):
        s.append("Num"+str(i))
    cols.insert(0, s)
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

def repPlace(data, n=20):
    """
    Args:
        data:
        n:
    Returns:
    """
    g = [[" " for _ in range(n + 1)] for i in range(n + 1)]
    maxy = 0
    print()
    for r, row in enumerate(data.rows):
        c = chr(65 + r)
        print(c, row.cells[-1])
        x, y = int(row.x * n // 1), int(row.y * n // 1)
        maxy = max(maxy, y + 1)
        g[y + 1][x + 1] = c
    print()
    for y in range(maxy):
        print(*g[y])

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
        string = "|.." * lvl
        if node["left"] is None:
            print(string, o(last(last(node["data"].rows).cells)))
        else:
            string1 = "%.f" % (rnd(100 * node["c"]))
            print(string, string1)
        show(node["left"], what, cols, nPlaces, lvl + 1)
        show(node["right"], what, cols, nPlaces, lvl + 1)

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
    return t[random.randint(0, len(t)-1)]

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

def mapM(t,fun):
    """
    t; map a function `fun`(v) over list (skip nil results) 
    """
    u=[]
    print(t)
    for k,v in enumerate(t):
        print(k)
        print(v)
        x,res = fun(v)
        print(x)
        if res is not None:
            u[res['dist'] if len(res) > 1 else len(u) + 1] = x
    return u
    
def kap(t, fun):
    """
    map function `fun`(k,v) over list (skip nil results) 
    """
    u = {}
    for k, v in enumerate(t):
        v, k = fun(k,v)
        u[k or (1 + len(u))] = v
    return u
#strings

def coerce(s):
    """
    return int or float or bool or string from `s`
    """
    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    if s == "true":
        return True
    elif s == "false":
        return False
    elif s.isnumeric():
        return int(s)
    elif isfloat(s):
        return float(s)
    else:
        return s

def oo(t):
    """
    print `t` then return it
    """
    print(o(t))
    return t

def o(t, isKeys=False):
    def fun(k, v):
        if not str(k).startswith("_"):
            return f":{o(k)} {o(v)}"
    if not isinstance(t, dict):
        return str(t)
    items = t.items() if isKeys else sorted(t.items())
    return "{" + " ".join(o(k) + " " + o(v) for k, v in items if fun(k, v)) + "}"

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