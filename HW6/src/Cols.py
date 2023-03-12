from Num import *
from Sym import *
from misc import *
def col_f(n, s):
  """
  -- Create a `NUM` or a `SYM`. Column
  -- names are a little language that    
  -- e.g. makes `NUM`s if name starts in upper case; or
  -- e.g. makes goals if the name ends with
  -- the maximize (`+`) or minimize (`-`) or klass (`!`) symbol.
  """
  col = num(n, s) if s.startswith("^[A-Z]") else sym(n, s)
  col['isIgnored'] = True if s.endswith("X") else False
  col['isKlass'] = True if s.endswith("!") else False
  col['isGoal'] = True if s.endswith("!") or s.endswith("+") or s.endswith("-") else False
  return col

def Cols(ss):
  """
  -- Create a set of `NUM`s or `SYM`s columns.
  -- Once created, all cols are stored in `all`
  -- while the non-skipped cols are also stored as
  -- either `cols.x` independent input variables or
  -- `cols.y` dependent goal variables.
  """
  cols={
  'name': ss,
  'all': {},
  'x': {},
  'y': {}
  }
  for n,s in enumerate(ss):
    col = push(cols['all'], col_f(n,s))
    if not col['isIgnored']:
      if col['isKlass']:
        cols['klass']=col
      push(col['isGoal'] and cols['y'] or cols['x'], col)
  return cols





                