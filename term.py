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

# An AppliedId is an id applied to a disjoint set of variables.
type AppliedId = Node

def is_applied_id(t: Term) -> bool:
    if not isinstance(t, Node): return False
    if not isinstance(t.f, Id): return False
    if not all(isinstance(x, Var) for x in t.args): return False
    return len(set(t.args)) == len(t.args)

type Equation = (Term, Term) # s = t
type Goal = (Term, Term) # s != t

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
