import re
from src.Sym import *
from src.Num import *
from src.misc import *
class Cols:
    def __init__(self,t):
        """
        -- Create a `NUM` or a `SYM`. Column
        -- names are a little language that    
        -- e.g. makes `NUM`s if name starts in upper case; or
        -- e.g. makes goals if the name ends with
        -- the maximize (`+`) or minimize (`-`) or klass (`!`) symbol.
        """
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None
        for n,s in enumerate(t):
            pattern = "^[A-Z]+"
            col_cond = re.search(pattern, s)
            if col_cond:
                col = Num(n,s)
            else:
                col = Sym(n,s)
            self.all.append(col)
            if not re.search("X$", s):
                if re.search("[!+-]$", s):
                    self.y.append(col)
                else:
                    self.x.append(col)
                if re.search("!$", s):
                    self.klass = col
    
    def add(self,r):
        """
        -- Update a COL with multiple items from `t`. This is useful when `col` is being
        -- used outside of some DATA.
        """
        for t in [self.x, self.y]:
            for col in t:
                col.add(r.cells[col.at])

    

                        
            



                