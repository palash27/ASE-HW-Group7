from src.misc import *
from src.Rows import *
from src.Cols import *

class Data:
    """
    Store many rows, summarized into columns
    """
    def __init__(self,src):
        self.rows, self.cols = {}, None
        def fun(x):
            self.add(x)
        if type(src) == str:
            csv(src,fun)
            
#loading from list needs to be implemented
    def add(self,t):
        """
        add a new row, update column headers
        """
        if self.cols:       # true if we have already seen the column names
            if hasattr(t, "cells"):     # ensure is a ROW, reusing old rows in the are passed in -- t =ROW(t.cells and t.cells or t) -- make a new ROW
                t = t
            else:
                t = Row(t)      
            push(self.rows, t)      # add new data to "self.rows"
            self.cols.add(t)        # update the summary information in "self.cols"
        else:
            self.cols = Cols(t)     # here, we create "self.cols" from the first row
        
    def clone(self,data,init = {}):
        data = Data(self.cols['names'])
        
        def fun(x):
            data.add(x)
           
        map(init,fun)
        return data
        
    def stats(self, what, cols, nPlaces):
        """
        reports mid or div of cols (defaults to self.cols.y)
        """
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

            

