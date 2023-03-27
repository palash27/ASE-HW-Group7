import re
from src.Sym import *
from src.Num import *
from src.misc import *
class Cols:
    """
    This is Cols class used to initialize a new Cols structure
    """
    def __init__(self,t):
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

    

                        
            



                