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
    pass # TODO
