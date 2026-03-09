from term import *

# s > t
def gt(s: Term, t: Term) -> bool:
    vars_s = get_vars(s, {})
    vars_t = get_vars(t, {})
    for x in vars_t:
        if x not in vars_s: return False
        if vars_t[x] > vars_s[x]: return False
    
    ws = weight(s)
    wt = weight(t)
    if ws > wt: return True
    if ws < wt: return False

    assert(ws == wt)

    if not isinstance(s, Node): return False
    if not isinstance(t, Node): return False

    if sym_gt(s.f, t.f): return True
    if sym_gt(t.f, s.f): return False

    assert(s.f == t.f)
    assert(len(s.args) == len(t.args))

    for (cs, ct) in zip(s.args, t.args):
        if gt(cs, ct): return True
        if cs == ct: continue
        return False

    assert(s == t)
    return False

def weight(t: Term) -> int:
    if isinstance(t, Var):
        return 1
    elif isinstance(t, Node):
        if t.f == "n":
          return sum(map(weight, t.args))
        else:
          return 1 + sum(map(weight, t.args))
    else:
        raise "oh no"

def get_vars(t: Term, out=None) -> dict[Var, int]:
    if isinstance(t, Var):
        if t not in out:
            out[t] = 0
        out[t] += 1
        return out
    elif isinstance(t, Node):
        for a in t.args:
            get_vars(a, out)
        return out
    else:
        raise "oh no"

def sym_gt(l: Symbol, r: Symbol) -> bool:
    # Id > str
    if isinstance(l, Id) and isinstance(r, str): return True
    if isinstance(l, str) and isinstance(r, Id): return False
    # hardcoded precedence
    prec = ["n","m","e"]
    if isinstance(l, str) and isinstance(r, str): return prec.index(l) < prec.index(r)
    return l > r
