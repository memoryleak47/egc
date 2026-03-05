from term import *

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

