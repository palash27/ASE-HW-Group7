from src.misc import *
from src.Row import *
def new_data():
    return {'rows':{}, 'cols': None}

def read_data(the, sfile):
    data = new_data()
    def fun(t):
        row(the, data,t)
    csv(sfile, fun)
    return data

def data_clone(data, ts={}):
    data1 = row(new_data(), data['cols']['names'])
    for _, t in ts.items():
        row(data1, t)