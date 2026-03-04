from suf import *
from parse import *
from deduce import *
import heapq

class EGC:
    def __init__(self, eqs: list[(Term, Term)], goals: list[(Term, Term)], signature: Signature):
        # actives are hashcons + unionfind.
        # Whenever you add anything to those, you'll have to compute CPs from it.
        # unionfind CPs happen via rebuild/canon, but hashcons CPs need to be added to passives.

        self.weights = {} # dict[Sym, Polynomial]
        self.passives = eqs # set of non-interned terms
        self.goals = goals

        self.suf = SlottedUF()
        self.hashcons = {} # dict[Applied, Base]; hashcons should behave like an identity function semantically

        # add stringy function symbols
        for f, arity in sig.items():
            self.suf.classes[Sym(f)] = Class(arity)

    def canon(self, t: Term) -> Base:
        t = self.suf.find(t) # canonicalize outermost id
        if isinstance(t, Var):
            return t
        assert(isinstance(t, Applied))

        t = Applied(t.sym, tuple(self.canon(a) for a in t.args)) # canonicalize args
        if is_base(t):
            return t
        else:
            d, args = reorder(t.args)
            t = Applied(t.sym, args)
            if t not in self.hashcons:
                id_args = tuple(vrange(len(vars_of(t))))
                sym = self.suf.alloc(len(id_args))
                rhs = Applied(sym, id_args)
                self.add_hashcons_eq(t, rhs)

            b = self.hashcons[t]
            assert(is_base(b))
            out = apply_subst(b, rev(d))
            assert(is_base(out))
            return out

    def add_hashcons_eq(self, lhs: Term, rhs: Base):
        self.hashcons[lhs] = rhs
        assert(is_base(rhs))
        print(f"hashcons: {lhs} -> {rhs}")
        e1 = (lhs, rhs)
        for e2 in self.hashcons.items():
            if e3 := deduce(e1, e2):
                print(f"new CP: {e3}")
                self.passives.append(e3)

    def rebuild(self):
        hashcons = {}
        for (sh, x) in self.hashcons.items():
            sh = self.shape(sh) # TODO
            x = self.canon(x)
            if sh in hashcons:
                self.suf.union(hashcons[sh], x)
            else:
                hashcons[sh] = x # TODO We also need CPs from those!
        self.hashcons = hashcons
        print("new hashcons:")
        for sh, x in hashcons.items():
            print(f"new hashcons: {t} -> {rhs}")

    def run(self):
        while len(self.passives) > 0:
            self.dump()
            x, y = self.passives.pop(0)
            print(f"Handling passive {x} = {y}!")
            x = self.canon(x)
            y = self.canon(y)
            print(f"  updates to {x} = {y}!")
            self.suf.union(x, y)

        self.check_goals()
        #self.rebuild()

    def check_goals(self):
        goals = []
        for a, b in self.goals:
            a = self.canon(a)
            b = self.canon(b)
            if self.suf.is_equal(a, b):
                raise "proof found!"
            print(f"Goal {a} = {b}")
            goals.append((a, b))
        self.goals = goals

    def dump(self):
        print("--- DUMP:")
        for l, r in self.hashcons.items():
            print(f"hashcons: {l} -> {r}")
        for (s, c) in self.suf.classes.items():
            args = tuple(vrange(c.arity))
            s = Applied(s, args)
            if c.leader is not None:
                print(f"unionfind: {s} -> {c.leader}")

eqs, diseqs, sig = parse("../example.p")
eg = EGC(eqs, diseqs, sig)
eg.run()
