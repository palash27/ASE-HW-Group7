import sys
#from test_engine import test
from misc import *
import random
from Num import *

# help = """   
# script.lua : an example script with help text and a test suite
# (c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
# USAGE:   script.lua  [OPTIONS] [-g ACTION]
# OPTIONS:
  # -b  --bins    initial number of bins       = 16
  # -c  --cliffs  cliff's delta threshold      = .147
  # -f  --file    data file                    = data/data.csv
  # -F  --Far     distance to distant          = .95
  # -g  --go      start-up action              = nothing
  # -h  --help    show help                    = false
  # -H  --Halves  search space for clustering  = 512
  # -m  --min     size of smallest cluster     = .5
  # -M  --Max     numbers                      = 512
  # -p  --p       dist coefficient             = 2
  # -r  --rest    how many of rest to sample   = 4
  # -R  --Reuse   child splits reuse a parent pole = true
  # -s  --seed    random number seed           = 937162211
# ACTIONS:
  # -g  the	show settings
  # -g  sym	check syms
  # -g  num	check nums
  # -g  csv	read from csv
  # -g  data	read DATA csv
  # -g  stats	stats from DATA
# """
# the = cli(sys.argv[1:])
# print(the)
# test(the)
# if the['help']:
    # exit (print("\n" + str(help) + "\n"))

random.seed(1)

# Test1
def sample():
    for i in range(10):
        a = samples(["a","b","c","d","e"])
        print(''.join(samples(["a","b","c","d","e"])))
    

def num():
    n = Num([1,2,3,4,5,6,7,8,9,10])
    print("",n.n, n.mu, n.sd)

def gauss():
    t = []
    for i in range(1 + 10^4):
        t.append(gaussian(10,2))
    
    n = Num(t)
    print("",n.n,n.mu,n.sd)

gauss()


