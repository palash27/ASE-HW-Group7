from Num import *
from Sym import *
from misc import *

class Col:
    def __init__(self, n, s):
        """
        -- Create a `NUM` or a `SYM`. Column
        -- names are a little language that    
        -- e.g. makes `NUM`s if name starts in upper case; or
        -- e.g. makes goals if the name ends with
        -- the maximize (`+`) or minimize (`-`) or klass (`!`) symbol.
        """
        self.col = Num(n, s) if s[0].isupper() else Sym(n, s)
        self.isIgnored = self.col.txt.endswith("X")
        self.isKlass = self.col.txt.endswith("!")
        self.isGoal = self.col.txt[-1] in ["!", "+", "-"]