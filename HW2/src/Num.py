import re
from src.misc import *
class Num:
    def __init__(self, at='', txt="") -> None:
        self.n, self.mu, self.m2 = 0,0,0
        self.lo = float('inf')
        self.hi = float('-inf')
        self.at = at
        self.txt = txt
        if re.match("-$", self.txt) is None:
            self.w = 1
        else:
            self.w = -1

    def add(self, n):
        if n != '?':
            self.n = self.n + 1
            d = n - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(n - self.mu)
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)

    def mid(self):
        return self.mu
    
    def div(self):
        return (self.m2 <0 or self.n < 2) and 0 or (self.m2/(self.n-1))**0.5
    
    def rnd(self,x,n):
        if x == "?":
            return x
        else:
            return rnd(x,n)
