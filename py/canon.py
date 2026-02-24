from term import *

def canon(thing):
    it = map(Var, range(100000))
    return canon_generic(thing, it)

def canon_odd(thing):
    it = map(Var, range(1, 100000, 2))
    return canon_generic(thing, it)

def canon_even(thing):
    it = map(Var, range(0, 100000, 2))
    return canon_generic(thing, it)

def canon_generic(thing: Term | Equation | Goal, it: iter[Var]):
    d = dict()
    if isinstance(thing, Node) or isinstance(thing, Var):
        return canon_impl(t, d, it)
    elif isinstance(thing, tuple):
        lhs, rhs = thing
        lhs = canon_impl(lhs, d, it)
        rhs = canon_impl(rhs, d, it)
        return (lhs, rhs)

def canon_impl(t: Term, d: dict[Var, Var], it: iter[Var]) -> Term:
    if isinstance(t, Var):
        if t not in d:
            v = next(it)
            d[t] = v
        return d[t]
    elif isinstance(t, Node):
        args = tuple([canon_impl(a, d, it) for a in t.args])
        return Node(t.f, args)
