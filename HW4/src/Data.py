from misc import *
from Rows import *
from Cols import *

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
        else:
            self.add(src)
            
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

    # def add(self, t):
    #     if self.cols:
    #         if isinstance(t, list):
    #             t = Rows(t)
    #             self.rows.append(t)
    #             self.cols.add(t)
    #     else:
    #         self.cols = Cols(t)
        
    def clone(self, initial):
        """
        DATA; return a DATA with same structure as `ii. 
        """
        data = Data(self.cols.names)
        for _,r in initial.items():
            data.add(r)
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
        
    def dist(self, row1, row2, the, cols=None):
        """
        n; returns 0..1 distance `row1` to `row2`
        """
        n, d = 0, 0 
        if cols is None:
            cols = self.cols.x
        p = the["p"]
        for _, col in self.cols.x.items():
            n = n + 1
            d = d + (col.dist(row1.cells[col.at], row2.cells[col.at])) ** p
        return (d/n)**(1/p)
    
    def around(self, row1 ,the, rows=None):
        """
        t; sort other `rows` by distance to `row`
        """
        if rows == None:
            rows = self.rows
        def fun(row2):
            return {"row": row2, "dist": rnd(self.dist(row1, row2, the),2)}
        l = []
        for _, v in rows.items():
            l.append(fun(v))
        sorted_list = sorted(l, key=lambda x:x['dist'])
        return sorted_list
    
    def better(self,row1,row2):
        """
        true if `row1` dominates
        """
        s1,s2,ys = 0,0,self.cols.y
        x,y = None, None
        
        for _,col in ys.items():
            x  = col.norm(row1.cells[col.at])
            y  = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)
    
    def furthest(self, row1, rows, cols, t):
        """
        sort other `rows` by distance to `row`
        """
        t = self.around(row1,rows,cols)
        return t[len(t)]
    
    def half(self, the, rows = None, cols = None, above = None):
        """
        t,t,row,row,row,n; divides data using 2 far points
        """
        def project(row, x, y):
            x,y = cosine(dist(row,A), dist(row,B),c)
            if row.x == None:
                row.x = x
            if row.y == None:
                row.y = y
            return {'row' : row, 'x' : x, 'y' : y}
        
        def dist(row1,row2,the): 
            return self.dist(row1,row2,the,cols)
        
        rows = rows or self.rows
        some = many(rows,the['Sample'])
        A = above or any(some)
        B = self.furthest(A,rows).row
        #B = self.around(A, the, some)[int(float(the['Far']) * len(rows))//1]['row']
        c = dist(A,B, the)
        l = []
        left, right = [], []
        for _, row in rows.items():
            l.append(project(row))
        sorted_list = sorted(l, key=lambda x:x['dist'])
        for n, tmp in enumerate(sorted_list):
            if n <= len(rows) // 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])
        return left, right, A, B, mid, c
    
    def cluster(self, the, rows = None,min = None,cols = None,above = None):
        """
        returns `rows`, recursively halved
        """
        if rows == None:
            rows = self.rows
        elif type(rows) == list:
            rows = dict(enumerate(rows))
        if min == None:
            #min = len(rows)^the.min
            min = len(rows)**0.5
        if cols == None:
            cols = self.cols.x
        node = {}
        node["data"] = self.clone(rows)
        if len(rows) > 2*min:
            left, right, node['A'], node['B'], node['mid'], c = self.half(the,rows,cols,above)
            node['left']  = self.cluster(the, left,  min, cols, node['A'])
            node['right'] = self.cluster(the, right, min, cols, node['B'])
        return node
    
    def sway(self, the, rows=None, min=None, cols=None, above=None):
        """
        t; returns best half, recursively
        """
        rows = rows or self.rows
        min = min or len(rows)**0.5 #the.min
        cols = cols or self.cols.x
        if type(rows) == list:
            rows = dict(enumerate(rows))
        node = {'data': self.clone(rows)}
        if len(rows) > 2*min:
            left, right, node['A'], node['B'], node['mid'], c = self.half(the,rows,cols,above)
            if self.better(node['B'], node['A']):
                left,right,node['A'],node['B'] = right,left,node['B'],node['A']
            node['left'] = self.sway(the, left, min, cols, node['A'])
        return node


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

            

