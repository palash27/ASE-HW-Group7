from misc import *
from typing import Any, List, Union
from Cols import *


class Data:
    
    def __init__(self) -> None:
        """
        Create a `DATA` to contain `rows`, summarized in `cols`.
        """
        self.cols = None
        self.rows = []
        self.n = 0

    def read(self, the, file_name):
        """
        -- Create a new DATA by reading csv file whose first row 
        -- are the comma-separate names processed by `COLS` (above).
        -- into a new `DATA`. Every other row is stored in the DATA by
        -- calling the 
        -- `row` function (defined below).
        """
        data = Data()
        csv(file_name, lambda t: row(the, data, t))
        return data

    def stats(self, what: str, cols: Union[Cols, None], n_places: int):
        
        def fun(col):
            _callable = getattr(col, what)
            return col.rnd(_callable(), n_places), col.txt

        return lists.kap(cols, fun)

    def dist(self, the, row1, row2, cols=None):
        n, d = 0, 0
        for _, col in enumerate(cols or self.cols.x):
            n = n + 1
            d = (
                d
                + col.dist(row1.cells[col.at], row2.cells[col.at])
                ** the['p']
            )
        return (d / n) ** (1 / the['p'])

    def clone(self, the, data, ts=None):
        """
        -- Create a new DATA with the same columns as  `data`. Optionally, load up the new
        -- DATA with the rows inside `ts`.
        """
        data1 = row(the, Data(), data.cols.names)
        for t in ts or []:
            row(the, data1, t)
        return data1

    def around(self, row1, rows=None, cols=None):
        def distance(row2):
            return {"row": row2, "dist": self.dist(row1, row2, cols)}

        rows = rows or self.rows
        sorted_rows = sorted(list(map(distance, rows)), key=lambda x: x["dist"])

        return sorted_rows

    def cluster(self, rows=None, cols=None, above=None):
        rows = rows or self.rows
        cols = cols or self.cols.x
        node = {"data": self.clone(rows)}
        if len(rows) >= 2:
            left, right, node["A"], node["B"], node["mid"], node["c"] = self.half(
                rows, cols, above
            )
            node["left"] = self.cluster(left, cols, node["A"])
            node["right"] = self.cluster(right, cols, node["B"])
        if "left" not in node:
            node["left"] = None
        if "right" not in node:
            node["right"] = None
        return node

    def half(self, rows=None, cols=None, above=None):
        def project(row):
            x, y = utils.cosine(distD(row, A), distD(row, B), c)
            row.x = row.x or x
            row.y = row.y or y
            return {"row": row, "x": x, "y": y}

        def distD(row1, row2):
            return self.dist(row1, row2, cols)

        rows = rows or self.rows
        A = above or utils.any(rows)
        B = self.furthest(A, rows)["row"]
        c = distD(A, B)

        left, right, nums, mid = [], [], 0, None
        for tmp in sorted(list(map(project, rows)), key=lambda x: x["x"]):
            nums += 1
            if nums <= len(rows) / 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])

        return left, right, A, B, mid, c

    def furthest(self, row1, rows, cols=None):
        t = self.around(row1, rows, cols)
        return t[-1]