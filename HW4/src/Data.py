from misc import *
from Rows import *
from Cols import *
import copy

class Data:
    """
    Store many rows, summarized into columns
    """
    def __init__(self,src):
        self.cols = None
        self.rows =[]
        self.n=0
        if isinstance(src,str):
            self.csv(src)
        else:
            if isinstance(src[0],str):
                self.add(src)
            else:
                for line in src:
                    self.add(line)

            
    def add(self,t):
        """
        add a new row, update column headers
        """
        if self.cols:       # true if we have already seen the column names
            if isinstance(t, list):     # ensure is a ROW, reusing old rows in the are passed in -- t =ROW(t.cells and t.cells or t) -- make a new ROW
                t = Row(t)
            self.rows.append(t)      # add new data to "self.rows"
            self.cols.add(t)        # update the summary information in "self.cols"
        else:
            self.cols = Cols(t)     # here, we create "self.cols" from the first row
        
    def clone(self, initial=None):
        """
        DATA; return a DATA with same structure as `ii. 
        """
        initial = [] if not initial else initial
        data = Data(self.cols.names)
        _ = list(map(data.add,initial))
        return data

    def stats(self, what, cols, nPlaces):
        """
        reports mid or div of cols (defaults to self.cols.y)
        """
        def fun(col):
            _x = getattr(col,what)
            return col.rnd(_x(), nPlaces), col.txt
        return kap(cols, fun)
        
    def dist(self, the, row1, row2, cols=None):
        """
        n; returns 0..1 distance `row1` to `row2`
        """
        n, d = 0, 0 
        c = cols or self.cols.x

        p = 2
        for _, col in enumerate(c):
            n = n + 1
            d = (d + col.dist(row1.cells[col.at], row2.cells[col.at]) ** p)
        return (d/n)**(1/p)
    
    def around(self, the, row1, rows=None, cols=None):
        """
        t; sort other `rows` by distance to `row`
        """
        rows = rows or self.rows
        def fun(row2):
            return {"row": row2, "dist": self.dist(the, row1, row2, cols)}
        sorted_list_of_rows = sorted(list(map(fun, rows)), key=lambda x:x['dist'])
        return sorted_list_of_rows
    
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
    
    def furthest(self, the, row1, rows, cols=None):
        """
        sort other `rows` by distance to `row`
        """
        t = self.around(the,row1,rows,cols)
        return t[len(t)-1]
    
    def half(self, the,rows = None, cols = None, above = None):
        """
        t,t,row,row,row,n; divides data using 2 far points
        """
        def project(row):
            x,y = cosine(sub_dist(row,A), sub_dist(row,B),c)
            row.x = row.x or x
            row.y = row.y or y
            return {'row' : row, 'x' : x, 'y' : y}
        
        def sub_dist(row1,row2):
            return self.dist(the,row1,row2,cols)
        
        rows = rows or self.rows
        A = above or any(rows)
        B = self.furthest(the,A,rows)["row"]
        c = sub_dist(A,B)
        left = []
        right = []
        n = 0
        mid = None
        for tmp in sorted(list(map(project, rows)), key= lambda x: x['x']):
            n += 1
            if n <= len(rows) / 2:
                left.append(tmp['row'])
                mid = tmp['row']
            else:
                right.append(tmp['row'])
        return left, right, A, B, mid, c
    
    def cluster(self, the, rows = None,cols = None,above = None):
        """
        returns `rows`, recursively halved
        """
        rows = rows or self.rows
        cols = cols or self.cols.x
        node = {}
        node["data"] = self.clone(rows)
        if len(rows) >= 2:
            left, right, node['A'], node['B'], node['mid'], node['c'] = self.half(the,rows,cols,above)
            node['left']  = self.cluster(the,left, cols, node['A'])
            node['right'] = self.cluster(the,right, cols, node['B'])
        if "left" not in node:
            node['left'] = None
        if "right" not in node:
            node["right"] = None
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
            
    def csv(self,sFilename):
        """
        call `fun` on rows (after coercing cell text)
        """
        with open(sFilename, "r") as file_obj:
            lines = file_obj.readlines()
            for line in lines:
                t = line.replace("\n","").rstrip().split(",")
                t = [coerce(i) for i in t]
                self.add(t)
                self.n+=len(t)
