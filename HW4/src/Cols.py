import re
from Sym import *
from Num import *
from misc import *

class Cols:
    """
    Factory for managing a set of NUMs or SYMs
    """
    def __init__(self, t):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None
        for n, s in enumerate(t):
            if re.match(r"^[A-Z]+", s):
                col = Num(n,s)
            else:
                col = Sym(n,s)
            push(self.all, col)
            if s[-1] != "X":
                if "!" in s:
                    self.klass=col
                isY = re.search(r'[!+-]',s)
                if isY:
                    push(self.y, col)
                else:
                    push(self.x, col)
    
    def add(self, row):
        """
        update the (not skipped) columns with details from `row`
        """
        for col in self.x+self.y:
            col.add(row.cells[col.at])
                                    
            # for _,col in t.items():
            #     col.add(row.cells[col.at])
            



                
