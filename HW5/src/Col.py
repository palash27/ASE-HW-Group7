from src.Num import *
from src.Sym import *

def COL(n, s):
    is_num = s[0].isupper()
    if is_num:
        col = Num(n,s)
    else:
        col = Sym(n, s)
    col.isIgnored = s.endswith("X")
    col.isKlass = s.endswith("!")
    col.isGoal = s.endswith("!") or s.endswith("+") or s.endswith("-")
    
    return col