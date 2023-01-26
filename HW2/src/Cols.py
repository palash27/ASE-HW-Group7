import re
from src.Sym import *
from src.Num import *
from src.misc import *
class Cols:
    """
    This is Cols
    """
    def __init__(self, t):
        self.names = t
        self.all = {}
        self.x = {}
        self.y = {}
        self.klass = None
        for n, s in t.items():
            if re.match("^[A-Z]+", s) == None:
                col = Sym(n,s)
            else:
                col = Num(n,s)
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
        for _,col in self.x.items():
            col.add(float(row.cells[col.at]))
            # for _,col in t.items():
            #     col.add(row.cells[col.at])
        
        for _,col in self.y.items():
            col.add(float(row.cells[col.at]))
                                    
            # for _,col in t.items():
            #     col.add(row.cells[col.at])
            



                
