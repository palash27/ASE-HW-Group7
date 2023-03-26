from Sym import *
from Num import *
from Data import *
from misc import *
import random



egs = {}
def eg(key, str, fun):
    egs[key] = fun


def SOME(the):
    the['Max'] = 32
    num1 = Num()
    for i in range(1,10000):
        add(the, num1, i)
    print(has(num1))

def NUM(the):
    num1 = Num()
    num2 = Num()
    
    for _ in range(1,10001):
        add(the, num1, rand())
    for _ in range(1,10001):
        add(the, num2, rand()**2)
    print("1", rnd(mid(num1)), rnd(div(num1)))
    print("2", rnd(mid(num2)), rnd(div(num2)))
    return 0.6 == rnd(mid(num1),1) and rnd(mid(num1))>rnd(mid(num2))

def SYM(the):
    sym1 = Sym()
    for x in ["a","a","a","a","b","b","c"]:
        add(the, sym1, x)
    print(mid(sym1), rnd(div(sym1))) 
    return 1.38 == rnd(div(sym1))

def DATA(the):
    data = Data().read(the, the['file'])
    col = data.cols.x[1]
    print(col.col.lo, col.col.hi, mid(col.col), div(col.col))
    oo(stats(data))
    

def BINS(the):
    data = Data().read(the, str(the['file']))
    best, rest = sway(the, data)
    print("all", "", "", "", o({"best": len(best.rows), "rest": len(rest.rows)}))
    b4 = None
    for k, t in enumerate(bins(the, data.cols.x, {"best": best.rows, "rest": rest.rows})):
        for range in t:
            if range.txt != b4:
                print("")
            b4 = range.txt
            print(
                range.txt,
                range.lo,
                range.hi,
                rnd(value(range.y.has, len(best.rows), len(rest.rows), "best")),
                o(range.y.has),
            )

def THE(the):
    oo(the)

def RAND(the):
    seed = 1
    t = []
    for i in range(1,1000):
        t.append(rint(0,100))
        
    u = []
    for i in range(1,1000):
        u.append(rint(0,100))
        
    for k,v in enumerate(t):
        assert v == u[k]
        
def CSV(the):
    n = 0
    def fun(t):
        nonlocal n 
        n = n + len(t)
    #csv('data/data.csv', fun)
    csv('data.csv', fun)
    return n == 8*399



def CLONE(the):
    d = Data()
    data1 = d.read(the, the['file'])
    data2 = d.clone(the, data1, data1.rows)
    oo(stats(data1))
    oo(stats(data2))


def HALF(the):
    data = Data().read(the, the["file"])
    left, right, A, B, c = half(the, data)
    print(len(left), len(right))
    l,r = data.clone(the, data,left), data.clone(the, data,right)
    print("l",o(stats(l)))
    print("r",o(stats(r))) 


def CLIFF(the):
    assert False == cliffsDelta(the, [8,7,6,2,5,8,7,3], [8,7,6,2,5,8,7,3])
    assert True  == cliffsDelta(the, [8,7,6,2,5,8,7,3], [9,9,7,8,10,9,6])
    t1, t2 = [], []
    for i in range(1,1001):
        t1.append(rand())
        
    for i in range(1,1001):
        t2.append(rand()**0.5)
        
    assert False == cliffsDelta(the, t1, t1) 
    assert True  == cliffsDelta(the, t1, t2)
    
    diff, j = False, 1.0
    
    while not diff:
        def fun(x):
            return x * j
            
        t3 = map(t1,fun)
        diff = cliffsDelta(the, t1, t3)
        print(">", rnd(j), diff) 
        j = j*1.025 

def DIST(the):
    data = Data().read(the, the['file'])
    num  = Num()
    
    for row in data.rows:
        add(the, num, dist(the, data, row, data.rows[1]))
    
    res = {'lo' : num.lo, 'hi' : num.hi, 'mid' : rnd(mid(num)), 'div' : rnd(div(num))}
    print(res)

def TREE(the):
    showTree(tree(the, Data().read(the, the['file'])))

def SWAY(the):
    data = Data().read(the, the['file'])
    best, rest = sway(the, data)
    print("\nall ", o(stats(data))) 
    print("    ",   o(stats(data,div))) 
    print("\nbest", o(stats(best))) 
    print("    ", o(stats(best,div))) 
    print("\nrest", o(stats(rest))) 
    print("    ", o(stats(rest,div))) 
    print("\nall ~= best?", o(diffs(the, best.cols.y, data.cols.y)))
    print("best ~= rest?", o(diffs(the, best.cols.y, rest.cols.y)))   

eg("the", "show options", THE)
eg("rand", "demo random number generation", RAND)
eg("some", 'demo of reservoir sampling', SOME)
eg("nums", "demo of NUM", NUM)
eg("syms", "demo SYMS", SYM)
eg("csv", "read from csv", CSV)
eg("data", "showing data sets", DATA)
eg("clone", "replicate structure of a DATA", CLONE)
eg("cliffs", "stats tests", CLIFF)
eg("dist", "distance test", DIST)
eg("half", "divide data in halg", HALF)
eg("tree", "make snd show tree of clusters", TREE)
eg("sway", "optimizing", SWAY)
eg("bins", "find deltas between best and rest", BINS)





def test(the):
    fails = 0
    for what, fun in egs.items():
        if the['go'] == "all" or what == the['go']:
            random.seed = the["seed"]
            if egs[what] == "CSV" or egs[what] == 'CLONE':
                if egs[what]() == False:
                    fails += 1
                    print("❌ fail:",what)
                else:
                    print("✅ pass:",what) 
            else:
                if egs[what](the) == False:
                    fails += 1
                    print("❌ fail:",what)
                else:
                    print("✅ pass:",what)  

