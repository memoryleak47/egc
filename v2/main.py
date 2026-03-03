from suf import *
from parse import *

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)], signature: Signature):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0
        self.goals = goals
        self.weights = {} # dict[Id, Polynomial]

        self.suf = SlottedUF()
        self.hashcons = {}

        # add stringy function symbols
        for f, arity in sig.items():
            f = Sym(f)
            self.suf.classes[f] = Class(arity)

    def canon(self, t: Term) -> Base:
        if isinstance(t, Var):
            return t
        assert(isinstance(t, Applied))

        t = self.suf.find(t) # canonicalize outermost id
        t = Applied(t.sym, tuple(self.canon(a) for a in t.args)) # canonicalize args
        if is_base(t):
            return t
        else:
            # TODO hashcons
            pass

    def run(self):
        pass # TODO

eqs, diseqs, sig = parse("../example.p")

eg = EGC(eqs, diseqs, sig)

# for debugging for now!
for (l, r) in eqs + diseqs:
    eg.canon(l)
    eg.canon(r)

eg.run()
