from suf import *
from parse import *

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)]):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0
        self.goals = goals
        self.weights = {} # dict[Id, Polynomial]

        self.hashcons = {}

    def canon(self, t: Term) -> Base:
        if isinstance(t, Var):
            return t
        assert(isinstance(t, Applied))
        fcanon = self.canon(Applied(t.f, map(Var, range(len(t.args)))))
        t = Applied(t.f, tuple(self.canon(a) for a in t.args))
        if is_base(t):
            return t
        else:
            # TODO hashcons
            pass

    def run(self):
        pass # TODO

eqs, diseqs = parse("../example.p")
e = EGC(eqs, diseqs)
e.run()
