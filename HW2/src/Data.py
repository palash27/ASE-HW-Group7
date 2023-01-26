from src.misc import *
from src.Rows import *
from src.Cols import *
class Data:
    def __init__(self,src):
        self.rows, self.cols = {}, None
        def fun(x):
            self.add(x)
        if type(src) == str:
            csv(src,fun)
#loading from list needs to be implemented
    def add(self,t):
        if self.cols:
            if hasattr(t, "cells"):
                t = t
            else:
                t = Row(t)
            push(self.rows, t)
            self.cols.add(t)
        else:
            self.cols = Cols(t)
        
    def stats(self, what, cols, nPlaces):
        x_mid = {}
        y_div = {}
        if what == "mid":
            for _, col in cols.items():
                x_mid[col.txt] = col.rnd(col.mid(),2)
            return x_mid
        elif what == "div":
            for _, col in cols.items():
                y_div[col.txt] = col.rnd(col.div(), 2)
            return y_div

        # x_mid = {}
        # if what == "mid":
        #     x_mid[cols.txt] = cols.mid()
        # print(x_mid)
        # return cols.txt, cols.mid()
        
        # if what == "div":
        #     return cols.txt, cols.div()
        #     print(cols, cols.txt, cols.div())
        # print(cols)
        # if hasattr(cols, "rnd"):
        #     print(cols.rnd(cols.txt, nPlaces))

            

