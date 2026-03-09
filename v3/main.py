from dataclasses import dataclass
from term import *
from order import *
from deduce import *
from parse import *
from canon import *
from simplify import *

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)]):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0
        self.goals = goals
        self.weights = {} # dict[Id, Polynomial]

    def add_active(self, e: Equation):
        e = canon(e)
        if e in self.actives: return

        print(str(e[0]) + " -> " + str(e[1]))

        self.actives.append(e)

        for e2 in self.actives:
            self.passives.extend(deduce(e, e2))
            self.passives.extend(deduce(e2, e))

    def score_passive(self, e: Equation):
        return 1

    def pop_passive(self):
        best = None
        best_score = 1000000000000
        for e in self.passives:
            score = self.score_passive(e)
            if score < best_score:
                best = e
                best_score = score
        if best:
            self.passives.remove(best)
            return best

    def run(self):
        while self.passives:
            e = self.pop_passive()

            lhs, rhs = simplify(e, self.actives)
            if lhs == rhs: continue

            if gt(lhs, rhs):
                self.add_active((lhs, rhs))
            elif gt(rhs, lhs):
                self.add_active((rhs, lhs))
            else:
                # TODO handle symmetries
                s = vars_of(lhs).intersection(vars_of(rhs))
                i = Node(Id(self.next_id), tuple(s))
                self.next_id += 1

                self.add_active((lhs, i))
                self.add_active((rhs, i))

            self.check_goals()

    def check_goals(self):
        goals = []
        for g in self.goals:
            g2 = simplify(g, self.actives)
            if g2[0] == g2[1]:
                print("Proof found!")
                print(g)
                print("simplifies to")
                print(g2)
                import sys
                sys.exit(0)
            g2 = canon(g2)
            goals.append(g2)
        self.goals = goals

eqs, diseqs = parse("../example_7_5.p")
e = EGC(eqs, diseqs)
e.run()
