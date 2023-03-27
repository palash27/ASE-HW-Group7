import re
import math
from src.misc import *
class Num:
    def __init__(self, at='', txt="") -> None:
        self.n, self.mu, self.m2 = 0,0,0
        self.lo = math.inf
        self.hi = -math.inf
        self.at = at
        self.txt = txt
        if re.match("-$", self.txt) is None:
            self.w = 1
        else:
            self.w = -1
        self.has = {}

    def add(self, x):
        if x != '?':
            self.n = self.n + 1
            if self.n <= 512: # the['max]
                self.has[x] = x
            d = float(x) - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(float(x) - self.mu)
            self.lo = min(float(x), self.lo)
            self.hi = max(float(x), self.hi)
       

    def mid(self):
        return self.mu
    
    def div(self):
        return 0 if (self.m2 <0 or self.n < 2) else (self.m2/(self.n-1))**0.5
    
    def rnd(self,x,n):
        if x == "?":
            return x
        else:
            return rnd(x,n)
        
    def norm(self, n):
        if n == "?":
            return n
        else:
            return (float(n) - self.lo)/(self.hi - self.lo + math.pow(10, -32))
        
    def dist(self, n1, n2):
        if n1  == "?" and n2 == "?":
            return 1
        n1 = self.norm(n1)
        n2 = self.norm(n2)
        if n1 == "?":
            if n2 < 0.5:
                n1 = 1
            else:
                n1 = 0
        if n2 == "?":
            if n1 < 0.5:
                n2 = 1
            else:
                n2 = 0
        return abs(n1 - n2)