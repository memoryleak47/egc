from dataclasses import dataclass
from term import *
from deduce import *
from parse import *
from canon import *

# TODO next things to be done:
# - simplify?
# - what to do with symmetries?
# - use prio queue

def gt(l: Term, r: Term) -> bool:
    if not is_applied_id(r): return False
    if not is_applied_id(l): return True
    if len(l.args) > len(r.args): return True
    if len(l.args) < len(r.args): return False
    return l.f.i > r.f.i

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)]):
        self.actives = [] # (Term, Term)
        self.passives = eqs
        self.next_id = 0
        self.goals = goals

    def add_active(self, e: Equation):
        e = canon(e)
        if e in self.actives: return

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

eqs, diseqs = parse("example.p")
e = EGC(eqs, diseqs)
e.run()
