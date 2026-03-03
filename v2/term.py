from dataclasses import dataclass

# Covers both e-class ids (int) and function symbols (str).
@dataclass(frozen=True)
class Id:
    i: int
    s: str|None

    def __repr__(self):
        if isinstance(self.v, str):
            return self.v
        else:
            return f"id{self.v}"

# combination of Node & AppliedId.
@dataclass(frozen=True)
class Applied:
    id: Id
    args: tuple[Term]

    def __repr__(self):
        if self.args:
            return str(self.id) + "(" + ", ".join(map(str, self.args)) + ")"
        else:
            return str(self.id)

@dataclass(frozen=True)
class Var:
    i: int

    def __repr__(self):
        return "X" + str(self.i)

type Term = Applied | Var
