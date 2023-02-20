from misc import *
from Cols import *
def row(the, data, t):
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

