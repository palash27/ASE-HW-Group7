import re
def num(n=0,s=""):
    if re.match("-$", s) is None:
        w = 1
    else:
        w = -1
    return {'at': n, 'txt': s, 'n':0, 'hi':float('inf'), 'lo':float('-inf'), 'ok':True, 'has':[], 'w':w }