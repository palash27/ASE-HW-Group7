import math 
import re
import sys
from csv import reader

#Numerics
help = """   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE:   script.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file    name of file       = data/data.csv
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211
ACTIONS:
  -g  the	show settings
  -g  sym	check syms
  -g  num	check nums
  -g  csv	read from csv
  -g  data	read DATA csv
  -g  stats	stats from DATA
"""


def rint(lo, hi):
    """
    a integer lo..hi-1
    """
    return math.floor(0.5 + rand(lo, hi))

def rand(lo, hi, Seed):
    """
    a float "x" lo<=x < x
    """
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def rnd(n, nPlaces=3):
    """
    return `n` rounded to `nPlaces`
    """
    mult = 10 ** (nPlaces)
    return math.floor(n * mult + 0.5) / mult

#Lists
def push(t, x):
    """
    push `x` to end of list; return `x` 
    """
    t[1 + len(t)] = x
    return x
 
def kap(t, fun):
    """
    map function `fun`(k,v) over list (skip nil results) 
    """
    u = {}
    for k, v in t.items():
        v, k = fun(k ,v)
        u[k or (1 + len(u))] = v
    return u
#strings

def coerce(s):
    """
    return int or float or bool or string from `s`
    """
    def fun(s1):
        if s1 == "true":
            return True
        elif s1 == "false":
            return False
        else:
            return s1
    if s.isnumeric():
        return int(s)
    elif type(s) != bool:
        return fun(re.search('^[\s]*[\S+]*[\s]*$', s).group(0))



def oo(t):
    """
    print `t` then return it
    """
    print(o(t))
    return t

def o(t):
    """
    convert `t` to a string. sort named keys. 
    """
    keys = list(t.keys())
    keys = sorted(keys)
    sorted_t = {i: t[i] for i in keys }
    output = "{"
    for k, v in sorted_t.items():
        output = output + ":"+str(k) + " " + str(v) + " "
    output = output + "}"
    return output

def settings(s):
    """
    parse help string to extract a table of options
    """
    t = {}
    for k,v in re.findall("[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s): 
        t[k] = coerce(v)
    return t

def cli(command_line_args):
    """
    update key,vals in `t` from command-line flags
    """
    options = {}
    options = settings(help)
    for k, v in options.items():
        v = str(v)
        for n, x in enumerate(command_line_args):
            if x == '-'+k[0] or x == '--'+k:
                if v == "true":
                    v = "false"
                elif v == "false":
                    v = "true"
                else:
                    v = command_line_args[n+1]
        options[k] = coerce(v)

    return options

def csv(file_name, fun):
    """
    call `fun` on rows (after coercing cell text)
    """
    sep = "([^" + "\," + "]+"
    with open(file_name) as file_obj:
        reader_obj = reader(file_obj)
        for row in reader_obj:
            t = {}
            for element in row:
                t[str(1+len(t))] = coerce(element)
            fun(t)
