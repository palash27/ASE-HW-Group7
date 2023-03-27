from src.misc import *
from src.Rows import *
from src.Cols import *
import operator
import math 
import copy
class Data:
    def __init__(self,src):
        self.rows, self.cols = [], None
        def fun(x):
            self.add(x)
        if type(src) == str:
            csv(src,fun)
        else:
            self.add(src)

    def add(self,t):
        # if self.cols:
        #     if hasattr(t, "cells"):
        #         t = t
        #     else:
        #         t = Row(t)
        #     push(self.rows, t)
        #     self.cols.add(t)
        # else:
        #     self.cols = Cols(t)
        if self.cols:
            if type(t) == list:
                t = Row(t)
            else:
                t = t
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = Cols(t)

        
    def stats(self, what, cols, nPlaces):
        def fun(_, col):
            if what == 'div':
                value = col.div()
            else:
                value = col.mid()
            rounded_value = col.rnd(value, nPlaces)
            return rounded_value, col.txt

        return kap(cols or self.cols.y, fun)
        # x_mid = {}
        # y_div = {}
        # if what == "mid":
        #     for _, col in cols.items():
        #         x_mid[col.txt] = col.rnd(col.mid(),2)
        #     return x_mid
        # elif what == "div":
        #     for _, col in cols.items():
        #         y_div[col.txt] = col.rnd(col.div(), 2)
        #     return y_div
        
    def clone(self, initial):
        data = Data(self.cols.names)
        # for _,r in initial.items():
        #     data.add(r)
        # return data
        def push(x):
            data.add(x)
        list(map(push, initial))
        return data
   
    def dist(self, row1, row2, the, cols=None):
        n, d = 0, 0 
        if cols is None:
            cols = self.cols.x
        for col in self.cols.x:
            n = n + 1
            d = d + col.dist(row1.cells[int(col.at)], row2.cells[int(col.at)]) ** 2 #the['p']
        # for _, col in self.cols.x.items():
        #     n = n + 1
        #     d = d + (col.dist(row1.cells[col.at], row2.cells[col.at])) ** p
        return (d/n)**(1/2)
    

    def around(self, row1 ,the, rows=None, cols=None):
        if rows == None:
            rows = self.rows
        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, the, cols)}
        # l = []
        # for _, v in rows.items():
        #     l.append(fun(v))
        # sorted_list = sorted(l, key=lambda x:x['dist'])
        # return sorted_list
        return sorted(list(map(fun, rows or self.rows)), key = lambda k : k["dist"])
    
    def furthest(self, row1, rows = None, cols = None):
        t = self.around(row1,rows,cols)
        return t[len(t)-1]

    def half(self, the, rows = None, cols = None, above = None):
        def project(row):
            return {'row' : row, 'dist' : cosine(gap(row,A), gap(row,B), c)}
        def gap(r1, r2):
            return self.dist(r1, r2, the, cols)
        def function(r):
            return {'row' : r, 'dist' : gap(r, A)}
        
        # def project(row):
        #     x, y = cosine(dist(row,A,the), dist(row,B,the), c)
        #     try:
        #         row.x = row.x
        #         row.y = row.y
        #     except:
        #         row.x = x
        #         row.y = y
        #     return {'row' : row, 'x' : x, 'y' : y}
        
        # def dist(row1,row2,the): 
        #     return self.dist(row1,row2,the,cols)
        
        rows = rows or self.rows
        some = many(rows,the['Halves'])
        # A = above or any(some)
        # A = above or rows[1]
        A = above if above and the['Reuse'] else any(some)
        temp = sorted(list(map(function, some)), key = lambda k : k["dist"])
        far = temp[int(float(the['Far']) * len(rows)//1)]
        # B = self.around(A, the, some)[int(float(the['Far']) * len(rows))//1]['row']
        # B = self.furthest(A,rows)['row']
        B = far['row']
        c = far['dist']
        # c = dist(A,B, the)
        left, right = [], []
        # for _, row in rows.items():
        #     l.append(project(row))
        # sorted_list = sorted(l, key=lambda x:x['dist'])
        sorted_list = sorted(list(map(project, rows)), key=lambda k: k["dist"])
        for n, tmp in enumerate(sorted_list):
            if n <= len(rows) // 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])
        evals = 1 if the['Reuse'] and above else 2
        return left, right, A, B, c, evals


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

    def better(self,row1,row2):
        """
        true if `row1` dominates
        """
        s1,s2,ys = 0,0,self.cols.y
        x,y = None, None
        
        for col in ys:
            x  = col.norm(row1.cells[col.at])
            y  = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)
    
    # def sway(self, the, rows=None, min=None, cols=None, above=None):
    #     rows = rows or self.rows
    #     min = min or len(rows)**0.5 #the.min
    #     cols = cols or self.cols.x
    #     if type(rows) == list:
    #         rows = dict(enumerate(rows))
    #     node = {'data': self.clone(rows)}
    #     if len(rows) > 2*min:
    #         left, right, node['A'], node['B'], node['mid'], c = self.half(the,rows,cols,above)
    #         if self.better(node['B'], node['A']):
    #             left,right,node['A'],node['B'] = right,left,node['B'],node['A']
    #         node['left'] = self.sway(the, left, min, cols, node['A'])
    #     return node

    def sway(self, the):
        data = self
        def worker(rows, worse, evals=None, above=None):
            if len(rows) <= len(data.rows)**float(the['min']):
                return rows, many(worse, int(the['rest'])*len(rows)),evals
            else:
                l, r, A, B, c, evals1 = self.half(the, rows, None, above) 
                if self.better(B, A):
                    l,r,A,B = r,l,B,A
                for row in r:
                    worse.append(row)
                if evals == None:
                    e = evals1
                else:
                    e = evals+evals1
                return worker(l,worse,e,A) 
        best,rest,evals1 = worker(data.rows,[])
        return self.clone(best), self.clone(rest), evals1  
    
    def tree(self, the, rows = None , mini = None, cols = None, above = None):
        rows = rows or self.rows
        mini  = mini or len(rows)**the['min']
        cols = cols or self.cols.x
        node = { 'data' : self.clone(rows) }
        if len(rows) >= 2*mini:
            left, right, node['A'], node['B'], node['mid'], _ = self.half(rows,cols,above)
            node['left']  = self.tree(left,  mini, cols, node['A'])
            node['right'] = self.tree(right, mini, cols, node['B'])
        return node
    
  
    
   
    
    
    