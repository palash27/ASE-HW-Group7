from src.misc import *
from src.Row import *
def new_data():
    """
    Create a `DATA` to contain `rows`, summarized in `cols`.
    """
    return {'rows':{}, 'cols': None}

def read_data(the, sfile):
    """
    -- Create a new DATA by reading csv file whose first row 
    -- are the comma-separate names processed by `COLS` (above).
    -- into a new `DATA`. Every other row is stored in the DATA by
    -- calling the 
    -- `row` function (defined below).
    """
    data = new_data()
    def fun(t):
        row(the, data,t)
    csv(sfile, fun)
    return data

def data_clone(data, ts={}):
    """
    -- Create a new DATA with the same columns as  `data`. Optionally, load up the new
    -- DATA with the rows inside `ts`.
    """
    data1 = row(new_data(), data['cols']['names'])
    for _, t in ts.items():
        row(data1, t)

def sway(the, data):
    """
    -- Recursively prune the worst half the data. Return
    -- the survivors and some sample of the rest.
    """
    def worker(rows,worse,above=None):
        if len(rows) <= len(data['rows'])**float(the['min']):
            return rows,many(worse,the['rest']*len(rows))
        else:
            l,r,A,B=half(the, data,rows,above)
            if better(data,B,A):
                l,r,A,B=r,l,B,A
                map(r,push(worse,row))
                return worker(l,worse,A)
    best,rest=worker(data['rows'],{})
    return data_clone(data,best), data_clone(data,rest)

def half(the, data, rows=None, above=None, cols=None):
    """
    -- Cluster `rows` into two sets by
    -- dividing the data via their distance to two remote points.
    -- To speed up finding those remote points, only look at
    -- `some` of the data. Also, to avoid outliers, only look
    -- `the.Far=.95` (say) of the way across the space. 
    """
    left, right = [], []
    far,some,tmp,A,B,c = None,None,None,None,None,None
    def gap(r1, r2):
        return dist(data, r1, r2, cols) 
    def cos(a,b,c):
        return (a**2 + c**2 - b**2)/(2*c)
    def proj(r):
        return {'row':r, 'x':cos(gap(r,A), gap(r,B),c)}
    def fun(r):
        return {'row':r, 'd':gap(r, A)}
    if rows is None:
        rows = data['rows']
    some = many(rows, the['Halves'])
    # if the['Reuse']:
    #     A = above
    # else:
    #     A = any(some)
    if above is not None:
        A = above
    else:
        A = any(some)
    l = []
    for _, val in some.items():
        l.append(fun(val))
    sorted_list = sorted(l, key=lambda x:x['d'])
    far = sorted_list[int((len(sorted_list)*float(the['Far']))//1)]
    B, c = far['row'], far['d']
    print("B", B)
    print("c", c )
    r = []
    for _, val in rows.items():
        r.append(proj(val))
    rows_sorted_list = sorted(r, key=lambda x:x['x'])
    # print(rows_sorted_list)
    # tmp = map(some, fun)
    # print("tmp", tmp)

def dist(data, t1, t2, cols):
    """
    -- A query that returns the distances 0..1 between rows `t1` and `t2`.   
    -- If any values are unknown, assume max distances.
    """
    if cols is None:
        cols = data['cols']['x']
    d, n = 0, 1/float('inf')
    def dist1(col, x, y):
        if x == '?' and y == '?':
            return 1
        if 'isSym' in col:
            if x == y:
                return 0
            else:
                return 1
        else:
            x, y = norm(col, x), norm(col, y)
            if x == '?':
                if y<0.5:
                    x = 1
                else:
                    x = 1
            if y == '?':
                if x < 0.5:
                    y = 1
                else:
                    y = 1
            return abs(x-y)
    for _, col in cols.items():
        n = n + 1
        d = d + dist1(col, t1[col['at']], t2[col['at']])**2 #the.p
    return (d/n)**(1/2) #the.p

def norm(num,n):
    """
    -- A query that normalizes `n` 0..1. Called by (e.g.) the `dist` function.
    """
    if n=='?':
        return n
    else:
        return (float(n) - float(num['lo']))/(float(num['hi']) - float(num['lo']) + (1/float('inf')))
    
def better(data, row1, row2):
    """
    -- A query that returns true if `row1` is better than another.
    -- This is Zitzler's indicator predicate that
    -- judges the domination status 
    -- of pair of individuals by running a “what-if” query. 
    -- It checks what we lose if we (a) jump from one 
    -- individual to another (see `s1`), or if we (b) jump the other way (see `s2`).
    -- The jump that losses least indicates which is the best row.
    """
    s1, s2, ys, x, y  = 0, 0, data['cols']['y'], None, None
    for _, col in ys.items():
        x = norm(col, row1[col['at']])
        y = norm(col, row2[col['at']])
        s1 = s1 - math.exp(col['w']*(x-y)/len(ys))
        s2 = s2 - math.exp(col['w']*(x-y)/len(ys))
    return s1/len(ys) < s2/len(ys)