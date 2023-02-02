from src.misc import cli
import sys
from src.test_engine import test


help = """   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE:   script.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file    name of file       = data/data.csv
  -F  --Far     distance to "faraway"  = .95	
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed  random number seed   = 937162211
  -S  --Sample  sampling data size     = 512
ACTIONS:
  -g  the	show settings
  -g  sym	check syms
  -g  num	check nums
  -g  csv	read from csv
  -g  data	read DATA csv
  -g  stats	stats from DATA
  -g  clone	duplicate structure
  -g  around	sorting nearest neighbors
  -g  half	1-level bi-clustering
  -g  cluster	N-level bi-clustering
  -g  optimize	semi-supervised optimization

"""

the = cli(sys.argv[1:])

test(the)
if the['help']:
    exit (print("\n" + str(help) + "\n"))


