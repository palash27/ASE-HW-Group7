from src.misc import *
from src.Cols import *
def row(the, data, t):
    """
    -- Update `data` with  row `t`. If `data.cols`
    -- does not exist, the use `t` to create `data.cols`.
    -- Otherwise, add `t` to `data.rows` and update the summaries in `data.cols`.
    -- To avoid updating skipped columns, we only iterate
    -- over `cols.x` and `cols.y`.
    """
    if data['cols'] != None:
        push(data['rows'],t)
        print("t", t)
        print(data['cols']['x'])
        for _,cols in data['cols']['x'].items():
            for _,col in cols.items():
                add(the, col, t[col['at']])
        for _,cols in data['cols']['y'].items():
            for _,col in cols.items():
                add(the, col, t[col['at']])
    else:
        data['cols'] = Cols(t)
    return data

