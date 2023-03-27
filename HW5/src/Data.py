from src.misc import *
from src.Rows import *
from src.Cols import *
import operator
import math 
import copy

class Data:
    """
    Create a `DATA` to contain `rows`, summarized in `cols`.
    """
    def __init__(self,src):
        self.rows, self.cols = [], None
        def fun(x):
            self.add(x)
        if type(src) == str:
            csv(src,fun)
        else:
            self.add(src)

    def add(self,t):
        """
        -- Create a new DATA by reading csv file whose first row 
        -- are the comma-separate names processed by `COLS` (above).
        -- into a new `DATA`. Every other row is stored in the DATA by
        -- calling the 
        -- `row` function (defined below).
        """
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
        """
        -- A query that returns `mid` or `div` of `cols` (defaults to `data.cols.y`).
        """
        def fun(_, col):
            if what == 'div':
                value = col.div()
            else:
                value = col.mid()
            rounded_value = col.rnd(value, nPlaces)
            return rounded_value, col.txt

        return kap(cols or self.cols.y, fun)
        
    def clone(self, initial):
        """
        -- Create a new DATA with the same columns as  `data`. Optionally, load up the new
        -- DATA with the rows inside `ts`.
        """
        data = Data(self.cols.names)
        def push(x):
            data.add(x)
        list(map(push, initial))
        return data
   
    def dist(self, row1, row2, the, cols=None):
        """
        -- A query that returns the distances 0..1 between rows `t1` and `t2`.   
        -- If any values are unknown, assume max distances.
        """
        n, d = 0, 0 
        if cols is None:
            cols = self.cols.x
        for col in self.cols.x:
            n = n + 1
            d = d + col.dist(row1.cells[int(col.at)], row2.cells[int(col.at)]) ** 2 #the['p']
        return (d/n)**(1/2)
    

    def around(self, row1 ,the, rows=None, cols=None):
        if rows == None:
            rows = self.rows
        def fun(row2):
            return {"row": row2, "dist": self.dist(row1, row2, the, cols)}
        return sorted(list(map(fun, rows or self.rows)), key = lambda k : k["dist"])
    
    def furthest(self, row1, rows = None, cols = None):
        t = self.around(row1,rows,cols)
        return t[len(t)-1]

    def half(self, the, rows = None, cols = None, above = None):
        """
        -- Cluster `rows` into two sets by
        -- dividing the data via their distance to two remote points.
        -- To speed up finding those remote points, only look at
        -- `some` of the data. Also, to avoid outliers, only look
        -- `the.Far=.95` (say) of the way across the space. 
        """
        def project(row):
            return {'row' : row, 'dist' : cosine(gap(row,A), gap(row,B), c)}
        def gap(r1, r2):
            return self.dist(r1, r2, the, cols)
        def function(r):
            return {'row' : r, 'dist' : gap(r, A)}
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
    
    def sway(self, the):
        """
        -- Recursively prune the worst half the data. Return
        -- the survivors and some sample of the rest.
        """
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
        """
        -- Cluster, recursively, some `rows` by  dividing them in two, many times
        """
        rows = rows or self.rows
        mini  = mini or len(rows)**the['min']
        cols = cols or self.cols.x
        node = { 'data' : self.clone(rows) }
        if len(rows) >= 2*mini:
            left, right, node['A'], node['B'], node['mid'], _ = self.half(rows,cols,above)
            node['left']  = self.tree(left,  mini, cols, node['A'])
            node['right'] = self.tree(right, mini, cols, node['B'])
        return node
    
  
    
   
    
    
    