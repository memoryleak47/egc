from term import *
from canon import *
from deduce import apply_subst

type Subst = dict[Var, Term]

def simplify(eq: Equation | Disequation, eqs):
    eq = canon_even(eq) # The thing we want to simplify is even
    lhs, rhs = eq
    lhs = simplify_term(lhs, eqs)
    rhs = simplify_term(rhs, eqs)
    return (lhs, rhs)

def simplify_term(t: Term, eqs):
    # only even vars!
    for a in vars_of(t):
        assert(a.v%2 == 0)

    while True:
        changed = False
        for pos in positions_of(t):
            for eq in eqs:
                lhs, rhs = canon_odd(eq) # The thing we simplify with is odd.
                subst = pat_match(lhs, pos_get(t, pos))
                if subst is None: continue
                rhs2 = apply_subst(rhs, subst)
                t = pos_set(t, pos, rhs2)
                changed = True
                break
            if changed: break
        if not changed:
            return t

def pat_match(pat: Term, term: Term) -> Subst:
    pat_vars = vars_of(pat)

    assert(pat_vars.isdisjoint(vars_of(term)))

    subst = {}
    if pat_match_impl(pat, term, subst, pat_vars):
        return subst

def pat_match_impl(pat, term, subst, pat_vars) -> bool:
    if isinstance(pat, Var):
        if pat in subst:
            return pat_match_impl(subst[pat], term, subst, pat_vars)
        elif pat in pat_vars:
            subst[pat] = term
            return True
        else:
            return pat == term
    elif isinstance(pat, Node):
        if not isinstance(term, Node): return False
        if pat.f != term.f: return False
        for pp, tt in zip(pat.args, term.args):
            if not pat_match_impl(pp, tt, subst, pat_vars): return False
        return True
