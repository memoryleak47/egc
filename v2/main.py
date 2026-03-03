from suf import *
from parse import *
import heapq

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)], signature: Signature):
        # actives are hashcons + unionfind.
        # Whenever you add anything to those, you'll have to compute CPs from it.
        # unionfind CPs happen via rebuild/canon, but hashcons CPs need to be added to passives.

        self.weights = {} # dict[Sym, Polynomial]
        self.passives = [] # list[(Term, Term)]

        self.suf = SlottedUF()
        self.hashcons = {} # dict[Applied, Sym]

        # add stringy function symbols
        for f, arity in sig.items():
            self.suf.classes[Sym(f)] = Class(arity)

        for lhs, rhs in eqs:
            self.union(self.canon(lhs), self.canon(rhs))

        self.goals = [(self.canon(x), self.canon(y)) for x, y in goals]

    def canon(self, t: Term) -> Base:
        if isinstance(t, Var):
            return t
        assert(isinstance(t, Applied))

        t = self.suf.find(t) # canonicalize outermost id
        t = Applied(t.sym, tuple(self.canon(a) for a in t.args)) # canonicalize args
        if is_base(t):
            return t
        else:
            d, args = reorder(t.args)
            t = Applied(t.sym, args)
            if t in self.hashcons:
                b = self.hashcons[t]
                if isinstance(b, Var): return d[b]
                assert(isinstance(b, Applied))
                # TODO d correctly applied?
                return Applied(b.f, tuple(d[a] for a in b.args))

            sym = self.suf.alloc(len(args))
            self.hashcons[t] = sym # TODO respect d
            return Applied(sym, args)
            # TODO compute CPs

    def union(self, x: Base, y: Base):
        self.suf.union(x, y)

    def run(self):
        pass # TODO

eqs, diseqs, sig = parse("../example.p")
eg = EGC(eqs, diseqs, sig)
eg.run()
