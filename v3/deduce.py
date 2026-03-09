from term import *
from canon import *

def deduce(x: Equation, y: Equation) -> list[Equation]:
    x = canon_odd(x)
    y = canon_even(y)

    out = []
    for p in positions_of(y[0]):
        subst = unify(x[0], pos_get(y[0], p))
        if not subst: continue
        sub = pos_set(y[0], p, x[1])
        ll = apply_subst(sub, subst)
        rr = apply_subst(y[1], subst)
        eq = (ll, rr)
        out.append(eq)
    return out

def unify(l: Term, r: Term):
    subst = {}
    if unify_impl(l, r, subst):
        return subst

def unify_impl(l: Term, r: Term, subst: dict[Var, Term]) -> bool:
    if l == r: return True

    if l in subst: return unify_impl(subst[l], r, subst)
    if r in subst: return unify_impl(l, subst[r], subst)

    if isinstance(l, Var):
        return subst_add(l, r, subst)
    if isinstance(r, Var):
        return subst_add(r, l, subst)

    if l.f != r.f: return False
    for (ll, rr) in zip(l.args, r.args):
        if not unify_impl(ll, rr, subst): return False
    return True

def subst_add(v: Var, t: Term, subst: dict[Var, Term]) -> bool:
    # Three kinds of variables:
    # - A_i (those already mapped by subst)
    # - B_i (those not mapped by subst)
    # - v (the one that we'll now set in subst)

    # currently:
    # - t contains A, B, v
    # - subst.values() contain B, v.

    t = apply_subst(t, subst)

    if t == v: return True

    # cycles are forbidden!
    if v in vars_of(t): return False

    subst[v] = t

    for (v2, t2) in subst.items():
        subst[v2] = apply_subst(t2, subst)
    return True

def apply_subst(t: Term, subst: dict[Var, Term]):
    if t in subst: return subst[t]
    if isinstance(t, Node):
        return Node(t.f, tuple([apply_subst(a, subst) for a in t.args]))
    return t


