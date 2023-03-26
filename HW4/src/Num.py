import re
from src.misc import *

class Num:
    """
    Summarizes a stream of numbers.
    """
    def __init__(self, at=0, txt="") -> None:
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
        """
        add `n`, update lo,hi and stuff needed for standard deviation
        """
        if n != '?':
            self.n = self.n + 1
            d = n - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(n - self.mu)
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)

    def mid(self):
        """
        return mean
        """
        return self.mu
    
    def div(self):
        """
        return standard deviation using Welford's algorithm http://.ly/nn_W
        """
        return (self.m2 <0 or self.n < 2) and 0 or (self.m2/(self.n-1))**0.5
    
    def rnd(self,x,n):
        """
        return number, rounded
        """
        if x == "?":
            return x
        else:
            return rnd(x,n)

    def norm(self, n):
        """
        normalize
        """
        if n == "?":
            return n
        else:
            return (float(n) - self.lo)/(self.hi - self.lo + 1e-32)

    def dist(self, n1, n2):
        """
        1 or returns absolute difference of n1 and n2
        """
        if n1 == "?" and n2 == "?":
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
