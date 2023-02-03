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
        """
        return a DATA with same structure as `ii.
        """
        data = Data(self.cols.names)
        
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
    
    def better(self,row1,row2,s1,s2,ys,x,y):
        """
        true if `row1` dominates
        """
        s1,s2,ys = 0,0,self.cols.y
        x = y = None
        
        for _,col in ys.items():
            x  = col.norm(row1.cells[col.at])
            y  = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)
    
    def dist(self,row1,row2,n,d,cols = None):
        """
        returns 0..1 distance `row1` to `row2`
        """
        n,d = 0,0
        if cols == None:
            cols = self.cols.x
        
        for _,col in pairs(cols):
            n = n + 1
            #d = d + col.dist(row1.cells[col.at], row2.cells[col.at])^the.p
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at])^2
        
        #return (d/n)^(1/the.p)
        return (d/n)^(1/2)
    
    def cluster(self,rows = None,min = None,cols = None,above = None):
        """
        returns `rows`, recursively halved
        """
        if rows == None:
            rows = self.rows
        if min == None:
            #min = len(rows)^the.min
            min = len(rows)^0.5
        if cols == None:
            cols = self.cols
        node = {}
        node["data"] = self.clone(rows)
        if len(rows) > 2*min:
            left, right, node['A'], node['B'], node['mid'] = self.half(rows,cols,above)
            node['left']  = self.cluster(left,  min, cols, node['A'])
            node['right'] = self.cluster(right, min, cols, node['B'])
        
        return node

        """
    def sway(self, rows, min_var, cols, above):
        rows = rows or self.rows
        min_var = min_var or (len(rows))**min_var
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows) > 2*min_var:
            left, right, node.A, node.B, node.mid = self.half(rows,cols,above)
            if self.better(node.B,node.A):
                left, right, node.A, node.B = right, left, node.B, node.A
            node.left = self.sway(left, min_var, cols, node.A)
        return node
        """

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

            

