import math
import random
import re
from Num import *

the = {'bootstrap': 512, 'conf' : 0.05, 'cliff' : 0.4, 'cohen' : 0.35, 'Fmt' : """"%6.2f", width=40"""}

def coerce(s):
    """
    -- Coerce string to boolean, int,float or (failing all else) strings.
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
        
def settings(s):
    t = {}
    for k,v in re.findall("[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s): 
        t[k] = coerce(v)
    return t
    
def cli(command_line_args):
    """
    -- Update `t` using command-line options. For boolean
    -- flags, just flip the default values. For others, read
    -- the new value from the command line.
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
    
def erf(x):
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    return sign*y


def gaussian(mu, sd):
    mu = mu or 0
    sd = sd or 1
    return mu + sd * math.sqrt(-2 * math.log(random.random())) * math.cos(2 * math.pi * random.random())

def samples(t, n=None):
    u = []
    for i in range(1, n or len(t)+1):
        u.append(t[random.randint(0, len(t)-1)])
    return u


def cliffsDelta(ns1, ns2):
    n, gt, lt = 0, 0, 0
    if len(ns1) > 128:
        ns1 = samples(ns1, 128)
    if len(ns2) > 128:
        ns2 = samples(ns2, 128)
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1
    # return math.abs(lt - gt) / n <= the.cliff  Add the.cliff
    
def delta(i, other):
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / ((e + y.sd**2/y.n + z.sd**2/z.n)**0.5)
    
def bootstrap(y0,z0):
  x, y, z, yhat, zhat = Num(), Num(), Num(), [], []
  
  # x will hold all of y0,z0
  # y contains just y0
  # z contains just z0
  for y1 in y0:
    x.add(y1)
    y.add(y1)
  
  for z1 in z0:
    x.add(z1)
    z.add(z1)
  
  xmu, ymu, zmu = x.mu, y.mu, z.mu
  
  for y1 in y0:
    yhat.append(y1 - ymu + xmu)
  
  for z1 in z0:
    zhat.append(z1 - zmu + xmu)
    
  
  tobs = delta(y,z)
  n = 0
  for i in range(0,the['bootstrap'] + 1):
    if delta(Num(samples(yhat)), Num(samples(zhat))) > tobs:
        n = n + 1 
   
  return (n/the['bootstrap']) >= the['conf']
  
def RX(t, s = None):
    t.sort()
    
    if s == None:
        return {'name': '', 'rank': 0, 'n': len(t), 'show': '', 'has': t}
    
    return {'name': s, 'rank': 0, 'n': len(t), 'show': '', 'has': t}

def mid(t):
    if 'has' in t.keys():
        t = t['has']
    
    n = len(t) // 2
    if len(t) % 2 == 0:
        return (t[n] + t[n+1])/2
        
    return t[n+1]

def div(t):
    if 'has' in t.keys():
        t = t['has']
    
    return (t[int(len(t)*9/10)] - t[int(len(t)*1/10)]) / 2.56

def merge(rx1, rx2):
    rx3 = RX([], rx1['name'])
    rx3['has'] = rx1['has'] + rx2['has']
    rx3['has'].sort()
    rx3['n'] = len(rx3['has'])
    return rx3
    
def scottKnot(rxs):
    def merges(i, j):
        out = RX([], rxs[i]['name'])
        for k in range(i, j+1):
            out = merge(out, rxs[k])
        return out

    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut+1, hi)
        return cliffsDelta(l['has'], r['has']) and bootstrap(l['has'], r['has'])

    def recurse(lo, hi, rank):
        b4 = merges(lo, hi)
        cut, best = None, 0
        for j in range(lo, hi):
            if j < hi:
                l = merges(lo, j)
                r = merges(j+1, hi)
                now = (l['n']*(mid(l) - mid(b4))**2 + r['n']*(mid(r) - mid(b4))**2) / (l['n'] + r['n'])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if cut is not None and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut+1, hi, rank)
        else:
            for i in range(lo, hi+1):
                rxs[i]['rank'] = rank
        return rank

    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(1, len(rxs))) * the['cohen']
    recurse(0, len(rxs)-1, 1)
    return rxs
    
def tiles(rxs):
    lo, hi = math.inf, -math.inf
    for rx in rxs:
        lo, hi = min(lo, rx.has[0]), max(hi, rx.has[-1])
    for rx in rxs:
        t, u = rx.has, [' '] * the.width
        def of(x, most): return max(1, min(most, x))
        def at(x): return t[of(math.floor(len(t)*x), len(t)-1)]
        def pos(x): return math.floor(of(the.width*(x-lo)/(hi-lo+1E-32), the.width-1))
        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B+1): u[i] = '-'
        for i in range(D, E+1): u[i] = '-'
        u[the.width//2] = '|'
        u[C] = '*'
        rx.show = ''.join(u) + ' {' + the.Fmt.format(a)
        for x in [b,c,d,e]:
            rx.show += ', ' + the.Fmt.format(x)
        rx.show += '}'
    return rxs

