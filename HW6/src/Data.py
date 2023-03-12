from src.misc import *
from src.Row import *

def new_data():
    """
    Create a `DATA` to contain `rows`, summarized in `cols`.
    """
    return {'rows':{}, 'cols': None}

def read_data(the, sfile):
    """
    -- Create a new DATA by reading csv file whose first row 
    -- are the comma-separate names processed by `COLS` (above).
    -- into a new `DATA`. Every other row is stored in the DATA by
    -- calling the 
    -- `row` function (defined below).
    """
    data = new_data()
    def fun(t):
        row(the, data,t)
    csv(sfile, fun)
    return data

def data_clone(data, ts={}):
    """
    -- Create a new DATA with the same columns as  `data`. Optionally, load up the new
    -- DATA with the rows inside `ts`.
    """
    data1 = row(new_data(), data['cols']['names'])
    for _, t in ts.items():
        row(data1, t)