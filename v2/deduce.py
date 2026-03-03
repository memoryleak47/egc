from term import *

type Subst = dict[Var, Term]

# Equation = (Term, Base) in this context
def deduce(a: Equation, b: Equation) -> Equation|None:
    if (subst := unify(a[0], b[0])) is None: return
    # subst(a[0]) == subst(b[0])
    # -> subst(a[1]) == subst(b[1])
    return (apply_subst(a[1], subst), apply_subst(b[1], subst))

def apply_subst(t: Term, subst) -> Term:
    if isinstance(t, Var):
        if t in subst:
            return subst[t]
        else:
            return t
    args = tuple(apply_subst(a, subst) for a in t.args)
    return Applied(t.sym, args)

# We know that all children of a and b are Base.
def unify(a: Term, b: Term) -> Subst|None:
    if a.sym != b.sym: return
    assert(len(a.args) == len(b.args))
    subst = {}
    for aa, bb in zip(a.args, b.args):
        if not unify_impl(aa, bb, subst): return
    return subst

def unify_impl(l: BaseTerm, r: BaseTerm, subst: Subst) -> bool:
    assert(is_base(l))
    assert(is_base(r))

    if l == r: return True

    if l in subst: return unify_impl(subst[l], r, subst)
    if r in subst: return unify_impl(l, subst[r], subst)

    if isinstance(l, Var):
        return subst_add(l, r, subst)
    if isinstance(r, Var):
        return subst_add(r, l, subst)

    if l.sym != r.sym: return False
    for ll, rr in zip(l.args, r.args):
        if not unify_impl(ll, rr, subst): return False
    return True

def subst_add(v: Var, t: Term, subst: Subst) -> bool:
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
