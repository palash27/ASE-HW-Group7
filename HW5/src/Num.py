import re

class Num:
    def __init__(self, n=0, s=""):
        """
        Create a `NUM` to summarize a stream of numbers
        """
        self.at = n
        self.txt = s
        self.n = 0
        self.ok = True
        self.has = []
        self.lo = float("inf")
        self.hi = float("-inf")
        self.w = 1 if re.match("-$", s) else -1