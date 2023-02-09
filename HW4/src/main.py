from src.misc import cli
import sys
from src.test_engine import test


help = """   
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2 
USAGE:   script.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file    name of file       = ../etc/data/repgrid1.csv
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -p  --p       distance coefficient   = 2
  -s  --seed  random number seed   = 937162211
ACTIONS:
  -g  the	show settings
  -g  copy	check copy
  -g  sym	check syms
  -g  num	check nums
  -g  repcols	checking repcols
  -g  synonyms	checking repcols cluster
  -g  reprows	checking reprows
  -g  prototypes	checking reprows cluster
  -g  position	where's wally
  -g  every	the whole enchilada

"""

the = cli(sys.argv[1:])

test(the)
if the['help']:
    exit (print("\n" + str(help) + "\n"))


