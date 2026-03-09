from term import *

# l > r
def gt(l: Term, r: Term) -> bool:
    if l == r: return False
    if not vars_of(l).issuperset(vars_of(r)): return False
    if isinstance(r, Var): return True
    if not is_applied_sym(r): return False
    if not is_applied_sym(l): return True
    if len(l.args) > len(r.args): return True
    if len(l.args) < len(r.args): return False

    assert(l.f != r.f) # symmetries not handled yet!

    return sym_gt(l.f, r.f)

def sym_gt(l: Symbol, r: Symbol) -> bool:
    # Id > str
    if isinstance(l, Id) and isinstance(r, str): return True
    if isinstance(l, str) and isinstance(r, Id): return False
    return l > r


