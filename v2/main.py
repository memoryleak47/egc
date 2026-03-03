from suf import *
from parse import *

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)]):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0
        self.goals = goals
        self.weights = {} # dict[Id, Polynomial]

    def run(self):
        pass # TODO

eqs, diseqs = parse("../example.p")
e = EGC(eqs, diseqs)
e.run()
