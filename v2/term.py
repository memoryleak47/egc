from dataclasses import dataclass

# Symbols: Covers both e-class ids (int) and function symbols (str).
@dataclass(frozen=True)
class Sym:
    v: int|str

    def __post_init__(self):
        assert(isinstance(self.v, int) or isinstance(self.v, str))

    def __repr__(self):
        if isinstance(self.v, str):
            return self.v
        else:
            return f"id{self.v}"

    def __lt__(self, other: Sym):
        if isinstance(self.v, str) and isinstance(other.v, int): return True
        if isinstance(self.v, int) and isinstance(other.v, str): return False
        return self.v < other.v

# combination of Node & AppliedId.
@dataclass(frozen=True)
class Applied:
    sym: Sym
    args: tuple[Term]

    def __post_init__(self):
        assert(isinstance(self.sym, Sym))
        assert(isinstance(self.args, tuple))

    def __repr__(self):
        if self.args:
            return str(self.sym) + "(" + ", ".join(map(str, self.args)) + ")"
        else:
            return str(self.sym)

@dataclass(frozen=True)
class Var:
    i: int

    def __post_init__(self):
        assert(isinstance(self.i, int))

    def __repr__(self):
        return "X" + str(self.i)

type Term = Applied | Var

type Base = Term # A base term. Either an AppliedId or a Var.

def is_base(t: Term) -> bool:
    if isinstance(t, Var): return True
    assert(isinstance(t, Applied))
    s = set()
    for a in t.args:
        if not isinstance(a, Var): return False
        if a in s: return False
        s.add(a)
    return True

def vars_of(t: Term) -> set[Var]:
    if isinstance(t, Var):
        return {t}
    assert(isinstance(t, Applied))
    s = set()
    for x in t.args:
        s.update(vars_of(x))
    return s

def base_lt(l: Base, r: Base) -> bool:
    if isinstance(l, Var) and not isinstance(r, Var): return True
    if isinstance(r, Var) and not isinstance(l, Var): return False
    return l.sym < r.sym

type Subst = dict[Var, Term]

def apply_subst(t: Term, subst) -> Term:
    if isinstance(t, Var):
        if t in subst:
            return subst[t]
        else:
            return t
    args = tuple(apply_subst(a, subst) for a in t.args)
    return Applied(t.sym, args)

