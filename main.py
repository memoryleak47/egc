from dataclasses import dataclass
from term import *
from deduce import *

# TODO next things to be done:
# - We shouldn't orient all equations towards a new id. Eg. if it already is an Id equation
# - simplify?
# - what to do with symmetries?
# - use prio queue
# - canonicalize variable names, and deduplicate based on it
# - unify requires disjoint varnames, which I didn't do yet.

def gt(l: Term, r: Term) -> bool:
    if not is_applied_id(r): return False
    if not is_applied_id(l): return True
    if len(l.args) > len(r.args): return True
    if len(l.args) < len(r.args): return False
    return l.f.i > r.f.i

class EGC:
    def __init__(self, eqs: list[(Term, Term)]):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0

    def add_active(self, e: Equation):
        print(str(e[0]) + " -> " + str(e[1]))
        self.actives.append(e)
        for e2 in self.actives:
            self.passives.extend(deduce(e, e2))
            self.passives.extend(deduce(e2, e))

    def run(self):
        while self.passives:
            # TODO pop from prio queue in order, later
            lhs, rhs = self.passives.pop()
            if lhs == rhs: continue
            if (lhs, rhs) in self.actives: continue

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

f = lambda x, y: Node("f", (x, y))
g = lambda x, y: Node("g", (x, y))
h = lambda x: Node("h", (x,))
a = Node("a", ())
b = Node("b", ())

X = Var(0)
Y = Var(1)

l = [
    (f(X, Y), h(X))
]

e = EGC(l)
e.run()
