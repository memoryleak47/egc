from dataclasses import dataclass
from term import *
from poly import *
from deduce import *
from parse import *
from canon import *
from simplify import *

# TODO next things to be done:
# - what to do with symmetries?
# - use prio queue

# l > r
def gt(l: Term, r: Term) -> bool:
    if l == r: return False
    if not vars_of(l).issuperset(vars_of(r)): return False
    if isinstance(r, Var): return True
    if not is_applied_sym(r): return False
    if not is_applied_sym(l): return True
    if len(l.args) > len(r.args): return True
    if len(l.args) < len(r.args): return False

    assert(l.f != r.f) # symmetries not handled yet!

    return sym_gt(l.f, r.f)

def sym_gt(l: Symbol, r: Symbol) -> bool:
    # Id > str
    if isinstance(l, Id) and isinstance(r, str): return True
    if isinstance(l, str) and isinstance(r, Id): return False
    return l > r

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
        self.update_weight(e)

        for e2 in self.actives:
            self.passives.extend(deduce(e, e2))
            self.passives.extend(deduce(e2, e))

    def score_passive(self, e: Equation):
        poly = poly_of(e[0], self.weights) + poly_of(e[1], self.weights)
        s = poly.constant
        for (_, n) in poly.vars.items():
            s += n
        return s

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

    def update_weight(self, e: Equation):
        body, app_id = e
        if not is_applied_sym(app_id): return
        if not isinstance(app_id.f, Id): return
        app_id, body = canon((app_id, body))
        i = app_id.f

        # app_id should be in "default" application.
        assert(app_id.args == tuple(Var(x) for x in range(len(app_id.args))))

        poly = poly_of(body, self.weights)

        # Redundancy! If we have `f(X, g(Y)) = id5(X)`, then the polynomial of id5 should be X+3, as the Y gets redundant.
        for v in list(poly.vars):
            if v not in app_id.args:
                vars2 = poly.vars.copy()
                count = vars2[v]
                del vars2[v]
                poly = Polynomial(poly.constant + count, vars2)

        assert(set(poly.vars) == set(app_id.args))

        if (i not in self.weights) or poly < self.weights[i]:
            self.weights[i] = poly

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
