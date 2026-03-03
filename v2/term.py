from dataclasses import dataclass

# Symbols: Covers both e-class ids (int) and function symbols (str).
@dataclass(frozen=True)
class Sym:
    v: int|str

    def __repr__(self):
        if isinstance(self.v, str):
            return self.v
        else:
            return f"id{self.v}"

# combination of Node & AppliedId.
@dataclass(frozen=True)
class Applied:
    sym: Sym
    args: tuple[Term]

    def __repr__(self):
        if self.args:
            return str(self.sym) + "(" + ", ".join(map(str, self.args)) + ")"
        else:
            return str(self.sym)

@dataclass(frozen=True)
class Var:
    i: int

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
