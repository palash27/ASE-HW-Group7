from src.Sym import *
from src.Num import *
from src.Data import *
from src.misc import *
import random
import copy

egs = {}
def eg(key, str, fun):
    """
    register an example.
    """
    egs[key] = fun

def SYM(the):
    sym = Sym()
    for x in ["a","a","a","a","b","b","c"]:
        sym.add(x)
    if "a" == sym.mid() and 1.379 == rnd(sym.div()):
        return True
    else:
        return False

def NUM(the):
    num = Num()
    for x in [1,1,1,1,2,2,3]:
        num.add(x)
    if 11/7 == num.mid() and 0.787 == rnd(num.div()):
        return True
    else:
        return False

def THE(the):
    oo(the)

def RAND(the):
    num1  = Num()
    num2 = Num()
    random.seed = the["seed"]
    for _ in range(1, (10**3)):
        num1.add(rand(0, 1, the["seed"]))
    random.seed = the["seed"]
    for _ in range(1, (10**3)):
        num2.add(rand(0, 1, the["seed"]))
    m1 = rnd(num1.mid(), 10)
    m2 = rnd(num2.mid(), 10)
    # print(m1)
    # print(m2)
    # print(rnd(m1,1))
    if m1 == m2 and .6  == rnd(m1, 1):
        return True
    else:
        return False

def CSV(the):
    n = 0
    def fun(t):
        nonlocal n 
        n = n + len(t)
    csv('data/data.csv', fun)
    return n == 8*399

def DATA(the):
    data = Data(str(the['file']))
    return len(data.rows) == 398 and len(data.cols.x) == 4 and int(data.cols.x[1].at) == 1 and int(data.cols.y[1].w) == -1

def STATS(the):
    data = Data(str(the['file']))
    dict = {'y': data.cols.y, 'x': data.cols.x }
    for k,cols in dict.items():
            print(k, "   ", "mid", "   ", o(data.stats("mid", cols, 2)))
            print("", "    ", "div", "   ", o(data.stats("div", cols, 2)))

def CLONE(the):
    data1 = Data(str(the['file']))
    data2 = data1.clone(data1.rows)
    return len(data1.rows) == len(data2.rows) and len(data1.cols.x) == len(data2.cols.x) and int(data1.cols.x[1].at) == int(data2.cols.x[1].at) and int(data1.cols.y[1].w) == int(data2.cols.y[1].w)

def AROUND(the):
    data = Data(str(the['file']))
    # print(0, 0, o(data.rows[1].cells))
    for i, t in enumerate(data.around(data.rows[1], the)):
        if i%50 == 0:
            print(i, t['dist'], (t['row'].cells))

def HALF(the):
    data = Data(str(the["file"]))
    left, right, A, B, mid, c = data.half(the)
    print(len(left), len(right), len(data.rows))
    print(o(A.cells), c)
    print(o(mid.cells))
    print(o(B.cells))

def CLUSTER(the):
    data = Data(str(the['file']))
    show(data.cluster(the), "mid", data.cols.y, 1)  

def OPTIMIZE(the):
    data = Data(str(the['file']))
    show(data.sway(the), "mid", data.cols.y,1)

def COPY(the):
    t1 = {"a": 1, "b": {"c": 2, "d": [3]}}
    t2 = copy.deepcopy(t1)
    t2["b"]["d"][0] = 10000
    print("b4", t1, "\nafter", t2)

eg("sym", "check syms", SYM)
eg("num", "check nums", NUM)
eg("the", "show settings", THE)
eg("rand", "generate, reset, regenerate same", RAND)
eg("csv", "read from csv", CSV)
eg("data", "read DATA csv", DATA)
eg("stats", "stats from DATA", STATS)
eg("clone", "duplicate structure", CLONE)
eg("around", "sorting nearest neighbors", AROUND)
eg("half", "1-level bi-clustering", HALF)
eg("cluster", "N-level bi-clustering",CLUSTER)
eg("optimize", "semi-supervised optimization",OPTIMIZE)
eg("copy", "check copy", COPY)

def test(the):
    fails = 0
    for what, fun in egs.items():
        if the['go'] == "all" or what == the['go']:
            random.seed = the["seed"]
            if egs[what] == "SYM" or egs[what] == "NUM" or egs[what] == "CSV" or egs[what] == "CLONE":
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

