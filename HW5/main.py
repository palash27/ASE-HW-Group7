import math

help = """   
bins: multi-objective semi-supervised discetization
(c) 2023 Tim Menzies <timm@ieee.org> BSD-2
  
USAGE: lua bins.lua [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -f  --file    data file                    = ../etc/data/auto93.csv
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
"""

magic = "\n[%s]+[-][%S][%s]+[-][-]([%S]+)[^\n]+= ([%S]+)"

def COL(n, s):
  """
  -- Create a `NUM` or a `SYM`. Column
  -- names are a little language that    
  -- e.g. makes `NUM`s if name starts in upper case; or
  -- e.g. makes goals if the name ends with
  -- the maximize (`+`) or minimize (`-`) or klass (`!`) symbol.
  """
  col = NUM(n, s) if s.startswith("^[A-Z]") else SYM(n, s)
  col['isIgnored'] = True if s.endswith("X") else False
  col['isKlass'] = True if s.endswith("!") else False
  col['isGoal'] = True if s.endswith("!") or s.endswith("+") or s.endswith("-") else False
  return col

def NUM(n, s):
  """
  -- Create a `NUM` to summarize a stream of numbers.
  """
  return {
  'at': n or 0,
  'txt': s or "",
  'n': 0,
  'hi': -math.inf,
  'lo': math.inf,
  'ok': True,
  'has': [],
  'w': -1 if s and s.endswith("-") else 1
  }

def SYM(n,s):
  """
  -- Create a `SYM` to summarize a stream of symbols.
  """
  return {
  'at': n or 0,
  'txt': s or "",
  'n': 0,
  'mode': None,
  'most': 0,
  'isSym': True,
  'has': []
  }

def COLS(ss):
  """
  -- Create a set of `NUM`s or `SYM`s columns.
  -- Once created, all cols are stored in `all`
  -- while the non-skipped cols are also stored as
  -- either `cols.x` independent input variables or
  -- `cols.y` dependent goal variables.
  """
  cols={
  'name': ss,
  'all': [],
  'x': [],
  'y': []
  }
  for n,s in enumerate(ss):
    col = push(cols['all'], COL(n,s))
    if not col['sIgnored']:
      if col['isKlass']:
        cols['klass']=col
      push(col['isGoal'] and cols['y'] or cols['x'], col)
  return cols

def RANGE(at,txt,lo,hi):
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
  'y':SYM()
  }


# logistical functions

def push(t,x):
  t[len(t)] = x
  return x
