from dataclasses import dataclass

# TODO next things to be done:
# - We shouldn't orient all equations towards a new id. Eg. if it already is an Id equation
# - simplify?
# - what to do with symmetries?
# - use prio queue
# - canonicalize variable names, and deduplicate based on it
# - unify requires disjoint varnames, which I didn't do yet.

type Symbol = str | Id

@dataclass(frozen=True)
class Node:
    f: Symbol
    args: tuple["Term"]

    def __repr__(self):
        if self.args:
            return str(self.f) + "(" + ", ".join(map(str, self.args)) + ")"
        else:
            return str(self.f)

@dataclass(frozen=True)
class Id:
    i: int

    def __repr__(self):
        return "id" + str(self.i)

@dataclass(frozen=True)
class Var:
    v: int

    def __repr__(self):
        return "X" + str(self.v)

type Term = Node | Var

# An AppliedId is an id applied to a disjoint set of variables.
type AppliedId = Node

def is_applied_id(t: Term) -> bool:
    if not isinstance(t, Node): return False
    if not isinstance(t.f, Id): return False
    if not all(isinstance(x, Var) for x in t.args): return False
    return len(set(t.args)) == len(t.args)

type Equation = (Term, Term)

def vars_of(x):
    s = set()
    if isinstance(x, Var):
        s.add(x)
    elif isinstance(x, Node):
        for y in x.args:
            s.update(vars_of(y))
    return s

type Pos = tuple[int]

def positions_of(x: Term) -> list[Pos]:
    positions = [()]
    if isinstance(x, Node):
        for i, a in enumerate(x.args):
            for p in positions_of(a):
                positions.append((i, *p))
    return positions

def pos_get(x: Term, p: Pos) -> Term:
    if p == (): return x
    return pos_get(x.args[p[0]], p[1:])

def pos_set(x: Term, p: Pos, t: Term) -> Term:
    if p == (): return t
    args = list(x.args)
    args[p[0]] = pos_set(x.args[p[0]], p[1:], t)
    x = Node(x.f, tuple(args))
    return x

def deduce(x: Equation, y: Equation) -> list[Equation]:
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

def gt(l: Term, r: Term) -> bool:
    if not is_applied_id(r): return False
    if not is_applied_id(l): return True
    if len(l.args) > len(r.args): return True
    if len(l.args) < len(r.args): return False
    return l.f.i > r.f.i

class EGC:
    def __init__(self, eqs: list[(Term, Term)]):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0

    def add_active(self, e: Equation):
        print(str(e[0]) + " -> " + str(e[1]))
        self.actives.append(e)
        for e2 in self.actives:
            self.passives.extend(deduce(e, e2))
            self.passives.extend(deduce(e2, e))

    def run(self):
        while self.passives:
            # TODO pop from prio queue in order, later
            lhs, rhs = self.passives.pop()
            if lhs == rhs: continue
            if (lhs, rhs) in self.actives: continue

            if gt(lhs, rhs):
                self.add_active((lhs, rhs))
            elif gt(rhs, lhs):
                self.add_active((rhs, lhs))
            else:
                # TODO handle symmetries
                s = vars_of(lhs).intersection(vars_of(rhs))
                i = Node(Id(self.next_id), tuple(s))
                self.next_id += 1

                self.add_active((lhs, i))
                self.add_active((rhs, i))

f = lambda x, y: Node("f", (x, y))
g = lambda x, y: Node("g", (x, y))
h = lambda x: Node("h", (x,))
a = Node("a", ())
b = Node("b", ())

X = Var(0)
Y = Var(1)

l = [
    (f(X, Y), h(X))
]

e = EGC(l)
e.run()
