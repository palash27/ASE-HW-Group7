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
  col.isIgnored = True if s.endswith("X") else False
  col.isKlass = True if s.endswith("!") else False
  col.isGoal = True if s.endswith("!") or s.endswith("+") or s.endswith("-") else False
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
  'has': {},
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
  'mode':nil,
  'most':0,
  'isSym': True,
  'has': {}
  }
