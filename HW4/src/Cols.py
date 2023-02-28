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
        print(t)
        for n, s in enumerate(t):
            print(n)
            print(s)
            if re.match(r"^[A-Z]+", str(s)):
                col = Num(n,s)
            else:
                col = Sym(n,s)
            push(self.all, col)
            if s[-1] != "X":
                if s[-1] == "$":
                    self.klass = col
                elif s[-1] == '+' or s[-1] == "-" or s[-1] == "!":
                    if s[-1] == "-":
                        col.w = -1
                    else:
                        col.w = 1
                    push(self.y, col)
                else:
                    push(self.x, col)
    
    def add(self, row):
        """
        update the (not skipped) columns with details from `row`
        """
        for _,col in self.x.items():
            col.add(float(row.cells[col.at]))
            # for _,col in t.items():
            #     col.add(row.cells[col.at])
        
        for _,col in self.y.items():
            col.add(float(row.cells[col.at]))
                                    
            # for _,col in t.items():
            #     col.add(row.cells[col.at])
            



                
