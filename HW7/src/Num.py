class Num:
    """
    A class to represent a numerical summary of a list of numbers, including the count, mean, standard deviation,
    and other relevant statistics.
    """
    def __init__(self, t = None):
        """
        Constructs a Num object and initializes its properties.
        """
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        if t == None:
            t = []

        for x in t or []:
            self.add(x)

    def add(self, x):
        """
        Updates the Num object with a new value x.
        """
        self.n = self.n + 1
        d = x - self.mu
        self.mu = self.mu + (d/self.n)
        self.m2 = self.m2 + (d*(x-self.mu))
        if self.n < 2:
            self.sd = 0
        else:
            self.sd = (self.m2/(self.n - 1))**0.5
