import math 
import re
import sys
import random
from csv import reader
from Sym import *
from Range import *
from Cols import *

#Numerics
help = """   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE:   script.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -f  --file    data file                    = data.csv
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

# Update
def row(the, data, t):
    """
    -- Update `data` with  row `t`. If `data.cols`
    -- does not exist, the use `t` to create `data.cols`.
    -- Otherwise, add `t` to `data.rows` and update the summaries in `data.cols`.
    -- To avoid updating skipped columns, we only iterate
    -- over `cols.x` and `cols.y`.
    """
    if data.cols is None:
        data.cols = Cols(t)
    else:
        data.rows.append(t)
        for cols in [data.cols.x, data.cols.y]:
            for col in cols:
                add(the, col.col, t[col.col.at])
    return data


def add(the, col, x, n=1):
    """
    -- Update one COL with `x` (values from one cells of one row).
    -- Used  by (e.g.) the `row` and `adds` function.
    -- `SYM`s just increment a symbol counts.
    -- `NUM`s store `x` in a finite sized cache. When it
    -- fills to more than `the.Max`, then at probability 
    -- `the.Max/col.n` replace any existing item
    -- (selected at random). If anything is added, the list
    -- may not longer be sorted so set `col.ok=false`.
    """
    if x != "?":
        col.n = col.n + n  # Source of variable 'n'
        if hasattr(col, "isSym") is False or col.isSym is False:
            x = float(x)
            col.lo = min(x, col.lo)
            col.hi = max(x, col.hi)
            all = len(col.has)
            if all < the['Max']:
                pos = all + 1
            elif random.random() < the['Max'] / col.n:
                pos = rint(1, all)
            else:
                pos = None
            if pos:
                if isinstance(col.has, dict):
                    col.has[pos] = x
                else:
                    col.has.append(x)
        else:
            col.has[x] = n + col.has.get(x, 0)
            if col.has[x] > col.most:
                col.most, col.mode = col.has[x], x
            


def extend(the, range, n, s):
    """
    -- Update a RANGE to cover `x` and `y`
    """
    range.lo = min(n, range.lo)
    range.hi = max(n, range.hi)
    add(the, range.y, s)


def adds(col, t):
    """
    -- Update a COL with multiple items from `t`. This is useful when `col` is being
    -- used outside of some DATA.
    """
    if t is None:
        return col
    for x in t:
        add(the, col, x)
    return col

#--------------------------------------------------------------------------------------------#

# Query
def div(col):
    """
    -- A query that returns a `col`'s deviation from central tendency    
    -- (entropy for `SYM`s and standard deviation for `NUM`s)..
    """
    if hasattr(col, "isSym"):
        e = 0
        if isinstance(col.has, dict):
            for n in col.has.values():
                e = e - n / col.n * math.log(n / col.n, 2)
        else:
            for n in col.has:
                e = e - n / col.n * math.log(n / col.n, 2)
        return e
    else:
        return (per(has(col), 0.9) - per(has(col), 0.1)) / 2.58


def has(col):
    """
    -- A query that returns contents of a column. If `col` is a `NUM` with
    -- unsorted contents, then sort before return the contents.
    -- Called by (e.g.) the `mid` and `div` functions.
    """
    if not hasattr(col, "isSym") and not col.ok:
        if isinstance(col.has, dict):
            col.has = dict(sorted(col.has.items(), key=lambda item: item[1]))
        else:
            col.has.sort()
    col.ok = True
    return col.has


def mid(col):
    """
    -- A query that  returns a `cols`'s central tendency  
    -- (mode for `SYM`s and median for `NUM`s). Called by (e.g.) the `stats` function.
    """
    if hasattr(col, "isSym") and col.isSym:
        return col.mode
    else:
        t = has(col)
        p = 0.5
        p = math.floor((p*len(t))+0.5)
        return t[max(1, min(len(t),p))]



def stats(data, fun=None, cols=None, n_places=2):
    """
    -- A query that returns `mid` or `div` of `cols` (defaults to `data.cols.y`).
    """

    def helper(k, col):
        col = col.col
        return round((fun or mid)(col), n_places), col.txt

    cols = cols or data.cols.y

    temp = kap(cols, helper)
    temp["N"] = len(data.rows)
    return temp


def norm(num, n):
    """
    -- A query that normalizes `n` 0..1. Called by (e.g.) the `dist` function.
    """
    return n if n == "?" else (n - num.lo) / (num.hi - num.lo + 1 / float("inf"))


def value(has, nB=1, nR=1, sGoal=True):
    """
    -- A query that returns the score a distribution of symbols inside a SYM.
    """
    b, r = 0, 0
    for x, n in has.items():
        if x == sGoal:
            b = b + n
        else:
            r = r + n
    b, r = b / (nB + 1 / float("inf")), r / (nR + 1 / float("inf"))
    return (b**2) / (b + r)


def dist(the, data, t1, t2, cols=None):
    """
    -- A query that returns the distances 0..1 between rows `t1` and `t2`.   
    -- If any values are unknown, assume max distances.
    """

    def dist1(col, x, y):
        if x == "?" and y == "?":
            return 1
        if hasattr(col, "isSym"):
            if x == y:
                return 0
            else:
                return 1
        else:
            x, y = norm(col, x), norm(col, y)

            if x == "?":
                if y < 0.5:
                    x = 1
                else:
                    x = 1
            if y == "?":
                if x < 0.5:
                    y = 1
                else:
                    y = 1
            return abs(x - y)

    d, n = 0, 1 / float("inf")
    cols = cols or data.cols.x
    for col in cols:
        n += 1
        d += (
            dist1(col.col, float(t1[col.col.at]), float(t2[col.col.at]))
            ** the['p']
        )

    return (d / n) ** (1 / the['p'])


def better(data, row1, row2):
    """
    -- A query that returns true if `row1` is better than another.
    -- This is Zitzler's indicator predicate that
    -- judges the domination status 
    -- of pair of individuals by running a “what-if” query. 
    -- It checks what we lose if we (a) jump from one 
    -- individual to another (see `s1`), or if we (b) jump the other way (see `s2`).
    -- The jump that losses least indicates which is the best row.
    """
    s1, s2, ys = 0, 0, data.cols.y
    for _, col in enumerate(ys):
        x = norm(col.col, row1[col.col.at])
        y = norm(col.col, row2[col.col.at])

        s1 = s1 - math.exp(col.col.w * (x - y) / len(ys))
        s2 = s2 - math.exp(col.col.w * (y - x) / len(ys))

    return s1 / len(ys) < s2 / len(ys)


def per(t, p=0.5):
    """
    -- Return the `p`-ratio item in `t`; e.g. `per(t,.5)` returns the medium.
    """
    p = math.floor((p*len(t))+0.5)
    return t[max(1, min(len(t),p))]

# Clustering
def half(the, data, rows=None, cols=None, above=None):
    """
    -- Cluster `rows` into two sets by
    -- dividing the data via their distance to two remote points.
    -- To speed up finding those remote points, only look at
    -- `some` of the data. Also, to avoid outliers, only look
    -- `the.Far=.95` (say) of the way across the space. 
    """
    def gap(r1, r2):
        return dist(the, data, r1, r2, cols)

    def cos(a, b, c):
        return (a**2 + c**2 - b**2) / (2 * c)

    def proj(r):
        return {"row": r, "x": cos(gap(r, A), gap(r, B), c)}

    rows = rows or data.rows
    some = many(rows, the['Halves'])
    A = above or any(some)
    tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
    far = tmp[int(len(tmp) * the['Far']) // 1]
    B, c, left, right = far["row"], far["d"], [], []
    #print(map(rows, proj))
    for n, two in enumerate(sorted(map(rows, proj).items(), key=lambda x: x[1]['x'])):
        if n <= (len(rows) - 1) / 2:
           left.append(two[1]["row"])
        else:
           right.append(two[1]["row"])
    return left, right, A, B, c


def tree(the, data, rows=None, cols=None, above=None):
    """
    -- Cluster, recursively, some `rows` by  dividing them in two, many times
    """
    rows = rows or data.rows
    here = {"data": data.clone(the, data, rows)}
    if len(rows) >= 2 * (len(data.rows) ** the['min']):
        left, right, A, B, _ = half(the, data, rows, cols, above)
        here["left"] = tree(the, data, left, cols, A)
        here["right"] = tree(the, data, right, cols, B)
    return here


def showTree(tree, lvl=0, post=None):
    """
    -- Cluster can be displayed by this function.
    """
    if tree:
        print("{}[{}]".format("|.. " * lvl, len(tree["data"].rows)), end="")
        if lvl == 0 or ("left" not in tree):
            print(stats(tree["data"]))
        else:
            print("")
        showTree(tree["left"] if "left" in tree else None, lvl + 1)
        showTree(tree["right"] if "right" in tree else None, lvl + 1)

def show(node, what, cols, nPlaces, lvl=0):
    """
    -- Cluster can be displayed by this function.
    """
    if node:
        print('| '*lvl + str(len(node['data'].rows)) + " ", end = '')
        if (not node.get('left') or lvl==0):
            print(o(node['data'].stats("mid",node['data'].cols.y, nPlaces )))
        else:
            print("")
        show(node.get('left'), what, cols, nPlaces, lvl+1)
        show(node.get('right'), what, cols, nPlaces, lvl+1)

#--------------------------------------------------------------------------------------#

#Optimization
def sway(the, data):
    """
    -- Recursively prune the worst half the data. Return
    -- the survivors and some sample of the rest.
    """

    def worker(rows, worse, above=None):
        if len(rows) <= len(data.rows) ** the['min']:
            return rows, many(worse, the['rest'] * len(rows))
        else:
            l, r, A, B, _ = half(the, data, rows, None, above)
            if better(data, B, A):
                l, r, A, B = r, l, B, A
            for row in r:
                worse.append(row)
            return worker(l, worse, A)

    best, rest = worker(data.rows, [])
    return data.clone(the, data, best), data.clone(the, data, rest)


#--------------------------------------------------------------------------------------#

# Discretization
def bins(the, cols, rowss):
    """
    -- Return RANGEs that distinguish sets of rows (stored in `rowss`).
    -- To reduce the search space,
    -- values in `col` are mapped to small number of `bin`s.
    -- For NUMs, that number is `the.bins=16` (say) (and after dividing
    -- the column into, say, 16 bins, then we call `mergeAny` to see
    -- how many of them can be combined with their neighboring bin).
    """
    out = []
    for col in cols:
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                if isinstance(col, Col):
                    col = col.col
                x = row[col.at]
                if x != "?":
                    k = int(bin(the, col, float(x) if x != "?" else x))
                    ranges[k] = (
                        ranges[k]
                        if k in ranges
                        else RANGE(col.at, col.txt, float(x) if x != "?" else x)
                    )
                    extend(the, ranges[k], float(x), y)
        ranges = {
            key: value for key, value in sorted(ranges.items(), key=lambda x: x[1].lo)
        }
        new_ranges_dict = {}
        i = 0
        for key in ranges:
            new_ranges_dict[i] = ranges[key]
            i += 1
        new_ranges_list = []
        if hasattr(col, "isSym") and col.isSym:
            for item in new_ranges_dict.values():
                new_ranges_list.append(item)
        out.append(
            new_ranges_list
            if hasattr(col, "isSym") and col.isSym
            else merge_any(the, new_ranges_dict)
        )
    return out


def bin(the, col, x):
    """
    -- Map `x` into a small number of bins. `SYM`s just get mapped
    -- to themselves but `NUM`s get mapped to one of `the.bins` values.
    -- Called by function `bins`.
    """
    if x == "?" or hasattr(col, "isSym"):
        return x
    tmp = (col.hi - col.lo) / (the['bins'] - 1)
    return 1 if col.hi == col.lo else math.floor(x / tmp + 0.5) * tmp


def merge_any(the, ranges0):
    """
    -- Given a sorted list of ranges, try fusing adjacent items
    -- (stopping when no more fuse-ings can be found). When done,
    -- make the ranges run from minus to plus infinity
    -- (with no gaps in between).
    -- Called by function `bins`.
    """

    def no_gaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j - 1].hi
        t[0].lo = -math.inf
        t[-1].hi = math.inf
        return t

    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j + 1] if j + 1 < len(ranges0) else None
        if right:
            y = merge2(the, left.y, right.y)
            if y:
                j += 1  
                left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1
    return no_gaps(ranges0) if len(ranges0) == len(ranges1) else merge_any(the, ranges1)


def merge2(the, col1, col2):
    """
    -- If the whole is as good (or simpler) than the parts,
    -- then return the 
    -- combination of 2 `col`s.
    -- Called by function `mergeMany`.
    """
    new = merge(the, col1, col2)
    if div(new) <= (div(col1) * col1.n + div(col2) * col2.n) / new.n:
        return new


def merge(the, col1, col2):
    """
    -- Merge two `cols`. Called by function `merge2`.
    """
    new = copy(col1)
    if col1.isSym:
        for x, n in col2.has.items():
            add(the, new, x, n)
    else:
        for n in col2.has.values():
            add(the, new, n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new
    

#--------------------------------------------------------------------------------------#

def rint(lo,hi):
    """
    Rounds to integer
    """
    return math.floor(0.5 + rand(lo, hi))

def rand(lo=0, hi=1, Seed = 937162211):
    """
    random floats
    """
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def rnd(n, nPlaces=2):
    """
    Round numbers
    """
    mult = 10 ** (nPlaces)
    return math.floor(n * mult + 0.5) / mult

#Lists
def push(t, x):
    """
    Push an item `x` onto  a list. 
    """
    t[1+len(t)] = x
    return x
 
def kap(t, fun):
    """
    Map a function on table (results in items key1,key2,...)
    """
    u = {}
    for k, v in enumerate(t):
        v, k = fun(k ,v)
        u[k or (1 + len(u))] = v
    return u

def map(t,fun):
    """
    Map a function on  table (results in items 1,2,3...) 
    """
    u = {}
    for i, v in enumerate(t):
        u[i + 1] = fun(v)
    return u
    

def any(t):
    """
    Return one item at random.    
    """
    return t[random.randint(1, len(t)-1)]

def many(t, n):
    """
    Return many items, selected at random.
    Args:
        t:
        n:
    Returns:
    """
    u = []
    for i in range(1, n + 1):
        u.append(any(t))
    return u

def cosine(a,b,c):
    temp = 1 if c == 0 else 2*c
    x1 = (a**2 + c**2 - b**2) // temp
    x2 = max(0, min(1, x1)) 
    y  = abs((a**2 - x2**2)**0.5)
    return x2, y


def oo(t):
    """
    Print a nested table (sorted by the keys of the table).
    """
    print(o(t))
    return t

def o(t):
    """
    implementation of `o` used in `oo` for printing a nested table
    """
    if type(t) != dict and type(t) != list:
        return str(t)

    def fun(k, v):
        if str(k).find("_") != 0:
            v = o(v)
            return ":" + str(k) + " " + o(v)

        else:
            return False

    array = []
    if type(t) == dict:
        for key in t:
            output = fun(key, t[key])
            if output:
                array.append(output)
            array.sort()
    elif type(t) == list:
        array = t
    return "{" + " ".join(str(val) for val in array) + "}"


def settings(s):
    t = {}
    for k,v in re.findall("[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s): 
        t[k] = coerce(v)
    return t

def cli(command_line_args):
    """
    -- Update `t` using command-line options. For boolean
    -- flags, just flip the default values. For others, read
    -- the new value from the command line.
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

#############################################

def coerce(s: str):
    """
    -- Coerce string to boolean, int,float or (failing all else) strings.
    """

    def fun(s1):
        if s1 == "true":
            return True
        elif s1 == "false":
            return False
        return s1

    if s.isdigit() == False:
        if s.replace(".", "", 1).isdigit():
            return float(s)
        else:
            return fun(s.strip())
    else:
        return int(s)

def cells(s):
    """
    -- Split a string `s`  on commas.
    """
    t = []
    for s1 in s.split(","):
        t.append(coerce(s1.strip()))
    return t


def lines(file_name, fun):
    """
    -- Run `fun` for all lines in a file.
    """
    with open(file_name, "r") as src:
        for line in src:
            fun(line.rstrip("\r\n"))


def csv(file_name, fun):
    """
    -- Run `fun` on the cells  in each row of a csv file.
    """
    lines(file_name, lambda line: fun(cells(line)))
    
def copy(t):
    """
    -- Deep copy of a table `t`.
    """
    if type(t) is not dict:
        return t
    u = {}
    for k, v in t.items():
        u[k] = copy(v)
    return u

def cliffsDelta(the, ns1,ns2):
    if len(ns1) > 256:
        ns1 = many(ns1,256)
  
    if len(ns2) > 256:
        ns2 = many(ns2,256)
    
    if len(ns1) > 10*len(ns2):
        ns1 = many(ns1,10*len(ns2))
    
    if len(ns2) > 10*len(ns1):
        ns2 = many(ns2,10*len(ns1))
  
    n,gt,lt = 0,0,0
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x > y:
                gt = gt + 1
            if x < y:
                lt = lt + 1
    
    return abs(lt - gt)/n > the['cliffs']
    
def diffs(the, nums1, nums2):
    def kaps(nums, fn):
        return [fn(k, v) for k, v in enumerate(nums)]

    return kaps(nums1, lambda k, nums: (cliffsDelta(the, nums.col.has, nums2[k].col.has), nums.col.txt))
    