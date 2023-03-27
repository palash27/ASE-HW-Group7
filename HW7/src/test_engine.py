from Num import *
from misc import *
import random

egs = {}
def eg(key, fun):
    egs[key] = fun



def SAMPLE():
    for i in range(10):
        a = samples(["a","b","c","d","e"])
        print(''.join(samples(["a","b","c","d","e"])))
    

def NUM():
    n = Num([1,2,3,4,5,6,7,8,9,10])
    print("",n.n, n.mu, n.sd)

def GAUSS():
    t = []
    for i in range(1 + 10^4):
        t.append(gaussian(10,2))
    
    n = Num(t)
    print("",n.n,n.mu,n.sd)

def BOOTMU():
    a, b = [],[]
    for i in range(100):
        a.append(gaussian(10,1))
    print("","mu","sd","cliffs","boot","both")
    print("","--","--","------","----","----")
    
    for mu in range(100,111):
        mu = mu/10.0
        b = []
        for i in range(100):
            b.append(gaussian(mu,1))
        
        cl = cliffsDelta(a,b)
        bs = bootstrap(a,b)
        print("",mu,1,cl,bs,cl and bs)
        
def BASIC():
    print("\t\ttruee", bootstrap( [8, 7, 6, 2, 5, 8, 7, 3], 
                                [8, 7, 6, 2, 5, 8, 7, 3]),
              cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3], 
                           [8, 7, 6, 2, 5, 8, 7, 3]))
    print("\t\tfalse", bootstrap(  [8, 7, 6, 2, 5, 8, 7, 3],  
                                 [9, 9, 7, 8, 10, 9, 6]),
             cliffsDelta( [8, 7, 6, 2, 5, 8, 7, 3],  
                          [9, 9, 7, 8, 10, 9, 6])) 
    print("\t\tfalse", 
                    bootstrap([0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6], 
                               [0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9]),
                  cliffsDelta([0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6], 
                              [0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9]))

def PRE():
    print("\neg3")
    d = 1
    for i in range(10):
        t1,t2 = [], []
        for j in range(32):
            t1.append(gaussian(10,1))
            t2.append(gaussian(d*10,1))
        
        print("\t",round(d,2),d<1.1 and "true" or "false",bootstrap(t1,t2),bootstrap(t1,t1))
        d = d + 0.05

def FIVE():
    for rx in tiles(scottKnot(
         [RX([0.34,0.49,0.51,0.6,.34,.49,.51,.6],"rx1"),
         RX([0.6,0.7,0.8,0.9,.6,.7,.8,.9],"rx2"),
         RX([0.15,0.25,0.4,0.35,0.15,0.25,0.4,0.35],"rx3"),
         RX([0.6,0.7,0.8,0.9,0.6,0.7,0.8,0.9],"rx4"),
         RX([0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4],"rx5")])):
            print(rx['name'],rx['rank'],rx['show'])
       
def SIX():
    for rx in tiles(scottKnot(
        [RX([101,100,99,101,99.5,101,100,99,101,99.5],"rx1"),
        RX([101,100,99,101,100,101,100,99,101,100],"rx2"),
         RX([101,100,99.5,101,99,101,100,99.5,101,99],"rx3"),
         RX([101,100,99,101,100,101,100,99,101,100],"rx4")])):
            print(rx['name'],rx['rank'],rx['show'])
            
def TILES():
    rxs,a,b,c,d,e,f,g,h,j,k= [],[],[],[],[],[],[],[],[],[],[]
    for i in range(1000):
        a.append(gaussian(10,1))
        b.append(gaussian(10.1,1))
        c.append(gaussian(20,1))
        d.append(gaussian(30,1))
        e.append(gaussian(30.1,1))
        f.append(gaussian(10,1))
        g.append(gaussian(10,1))
        h.append(gaussian(40,1))
        j.append(gaussian(40,3))
        k.append(gaussian(10,1))
    
    tmp = [a, b, c, d, e, f, g, h, j, k]
    
    for k, v in enumerate(tmp):
        rxs.append(RX(v, "rx" + str(k + 1)))
    
    def fun(rxs):
        for k1, v1 in enumerate(rxs):
            for k2, v2 in enumerate(rxs):
                if mid(v1) < mid(v2):
                    rxs[k2], rxs[k1] = rxs[k1], rxs[k2]
        return rxs
    
    rxs = fun(rxs)
    for rx in tiles(rxs):
        print("",rx['name'],rx['show'])


def SK():
    rxs,a,b,c,d,e,f,g,h,j,k= [],[],[],[],[],[],[],[],[],[],[]
    for i in range(1000):
        a.append(gaussian(10,1))
        b.append(gaussian(10.1,1))
        c.append(gaussian(20,1))
        d.append(gaussian(30,1))
        e.append(gaussian(30.1,1))
        f.append(gaussian(10,1))
        g.append(gaussian(10,1))
        h.append(gaussian(40,1))
        j.append(gaussian(40,3))
        k.append(gaussian(10,1))
    
    tmp = [a, b, c, d, e, f, g, h, j, k]
    
    for k, v in enumerate(tmp):
        rxs.append(RX(v, "rx" + str(k + 1)))
    
    
    for rx in tiles(scottKnot(rxs)):
        print("",rx['name'],rx['show'])




eg('sample', SAMPLE)
eg('num', NUM)
eg('gauss', GAUSS)
eg('bootmu', BOOTMU)
eg('basic', BASIC)
eg('pre', PRE)
eg('five', FIVE)
eg('six', SIX)
eg('tiles', TILES)
eg('sk', SK)



def test():
    for what, fun in egs.items():
        print("\n" + what + "\n")
        fun()