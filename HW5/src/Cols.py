from Col import *  # type: ignore


class Cols:
    def __init__(self, ss):
        self.names = ss
        self.all = []
        self.x = []
        self.y = []
        for i, val in enumerate(ss):
            col = Col(i, val)
            self.all.append(col)
            if not col.isIgnored:
                if col.isKlass:
                    col.isKlass = col
                if col.isGoal:
                    self.y.append(col)
                else:
                    self.x.append(col)