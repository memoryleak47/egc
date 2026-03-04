from dataclasses import dataclass

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

# An AppliedSym is a sym applied to a disjoint set of variables.
type AppliedSym = Node

def is_applied_sym(t: Term) -> bool:
    if not isinstance(t, Node): return False
    if not all(isinstance(x, Var) for x in t.args): return False
    return len(set(t.args)) == len(t.args)

type Equation = (Term, Term) # s = t
type Goal = (Term, Term) # s != t

def vars_of(x):
    s = set()
    if isinstance(x, tuple):
        for a in x:
            s.update(vars_of(a))
        return s

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

@dataclass(frozen=True)
class Polynomial:
    constant: int
    vars: dict[Var, int]

    def __add__(self, other: Polynomial):
        vs = self.vars.copy()
        for (v, n) in other.vars.items():
            if v not in vs:
                vs[v] = n
            else:
                vs[v] = vs[v] + n
        return Polynomial(self.constant + other.constant, vs)

    def __mul__(self, other: int):
        assert(isinstance(other, int))
        vs = {}
        for (v, n) in self.vars.items():
            vs[v] = n*other
        return Polynomial(self.constant*other, vs)

    def __gt__(self, other: Polynomial):
        var_bigger = False
        for (a, k) in other.vars.items():
            assert(k > 0) # we shouldn't have zero entries!
            if a not in self.vars: return False
            if self.vars[a] < k: return False
            if self.vars[a] > k: var_bigger = True
        return var_bigger or self.constant > other.constant

def poly_of(x: Term, weights: dict[Id, Polynomial]) -> Polynomial:
    if isinstance(x, Var):
        vs = dict()
        vs[x] = 1
        return Polynomial(0, vs)
    elif isinstance(x, Node):
        if isinstance(x.f, Id):
            id_poly = weights[x.f]
            poly = Polynomial(id_poly.constant, {})
            k = len(id_poly.vars)
            assert(k == len(x.args))
            for i in range(k):
                n = id_poly.vars[Var(i)]
                child_poly = poly_of(x.args[i], weights) * n
                poly = poly + child_poly
            return poly
        elif isinstance(x.f, str):
            poly = Polynomial(1, {})
            for a in x.args:
                poly = poly + poly_of(a, weights)
            return poly
