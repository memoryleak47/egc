from dataclasses import dataclass
from term import *

type AppliedId = Applied # An Applied with only Vars as args.

class Class:
    def __init__(self, arity: int):
        self.group = Group(arity)
        self.arity = arity
        self.leader = None

# Reorders the slots a bunch of Bases, so that they are lexicographically minimal.
def reorder(bases: tuple(Base)) -> (dict[Var, Var], tuple(Base)):
    d = {}
    out = []
    for a in bases:
        if isinstance(a, Var):
            if a not in d:
                d[a] = Var(len(d))
            out.append(d[a])
        else:
            args = []
            for s in a.args:
                if s not in d:
                    d[s] = Var(len(d))
                args.append(d[s])
            args = tuple(args)
            out.append(Applied(a.sym, args))
    return (d, tuple(out))

class SlottedUF:
    classes: dict[Sym, Class]
    next_id: int

    def __init__(self):
        self.classes = {}
        self.next_id = 0

    def alloc(self, arity: int) -> Sym:
        i = Sym(self.next_id)
        self.next_id += 1
        self.classes[i] = Class(arity)
        return i

    # This find accepts that `x` may be be applied to non-Vars.
    def find(self, x: Base) -> Base:
        if isinstance(x, Var): return x
        assert(isinstance(x, Applied))

        while True:
            l = self.classes[x.sym].leader
            if l == None:
                return x
            # if id7[0, 1, 2] -> id3[2, 1] is a leader edge, then we want to simplify
            #    id7[a, b, c] -> id3[c, b]
            args = tuple(x.args[a.i] for a in l.args)
            x = Applied(l.sym, args)

    def union(self, x: Base, y: Base):
        while True:
            x = self.find(x)
            y = self.find(y)
            if vars_of(x) != vars_of(y):
                # redundant slots!

                # Example: if id3[a, b] = id7[a], then id3[a, b] doesn't really depend on b anymore.
                # Reasoning: id3[a, b] = id7[a] = id3[a, c]. Thus id3[a, b] = id3[a, c] for any slot c.
                # Thus, we'll mark b redundant in id3[a, b].
                self.mark_slots_redundant(x, vars_of(x) - vars_of(y))
                self.mark_slots_redundant(y, vars_of(y) - vars_of(x))
            else:
                break

        # all redundancies should have been handled now!
        assert(vars_of(x) == vars_of(y))

        if self.is_equal(x, y): return

        if base_lt(x, y): x, y = y, x
        # now x > y
        _, (x, y) = reorder((x, y))

        if isinstance(y, Applied) and x.sym == y.sym:
            # symmetries!
            # Example: if id3[0, 1] = id3[1, 0], we need to store this symmetry [1, 0] in the group of id3!
            self.classes[x.sym].group.add(y.args)
        else:
            self.add_uf_edge(x.sym, y)

    # Makes x point to y in the unionfind.
    def add_uf_edge(self, x: Sym, y: Base):
        assert(isinstance(x, Sym))
        assert(is_base(y))
        self.classes[x].leader = y

        if not isinstance(y, Var):
            x_arity = self.classes[x].arity
            y_arity = self.classes[y.sym].arity

            # y.sym inherits the symmetries from x
            identity = tuple(vrange(x_arity))
            for p in self.classes[x].group.perms:
                # The equation 'lhs = rhs' corresponding to this permutation.
                lhs = Applied(x, identity)
                rhs = Applied(x, p)

                # Tranforming the equation from x to y.sym.
                lhs = self.find(lhs)
                rhs = self.find(rhs)

                _, (lhs, rhs) = reorder((lhs, rhs))

                for s in rhs.args:
                    assert(s.i < y_arity)

                self.classes[y.sym].group.add(rhs.args)

        # x is now "non-canonical", thus it has no reason to a group.
        # If you want to know the symmetries, check the permutation group of the leader.
        self.classes[x].group = None

    def mark_slots_redundant(self, x: Base, slots: set[Var]):
        x = self.find(x)

        redundants = set()
        for s in slots:
            if s not in x.args: continue
            s = x.args.index(s)
            redundants.update(self.classes[x.sym].group.orbit(s))

        if len(redundants) == 0:
            return

        old_arity = self.classes[x.sym].arity
        new_arity = old_arity - len(redundants)
        y = self.alloc(new_arity)
        args = tuple(s for s in vrange(old_arity) if s not in redundants)
        self.add_uf_edge(x.sym, Applied(y, args))

    def is_equal(self, x: Base, y: Base) -> bool:
        x = self.find(x)
        y = self.find(y)

        if isinstance(x, Var) or isinstance(y, Var): return x == y

        if x.sym != y.sym:
            return False
        _, (x, y) = reorder((x, y))
        return self.classes[x.sym].group.contains(y.args)

# a group permutation.
# Required to express equations like id0[0, 1] = id0[1, 0].
type Perm = tuple(Var)

def compose(x: Perm, y: Perm) -> Perm:
    return tuple(x[y[i]] for i in vrange(len(x)))

# The most naive implementation of a permutation group: A set of permutations that is closed under composition.
class Group:
    def __init__(self, arity: int):
        identity_perm = tuple(vrange(arity))
        self.perms = {identity_perm}

    def add(self, x: Perm):
        self.perms.add(x)
        self.complete()

    def complete(self):
        while True:
            n = len(self.perms)
            new = set()
            for x in self.perms:
                for y in self.perms:
                    new.add(compose(x, y))
            self.perms.update(new)
            if n == len(self.perms):
                break

    def orbit(self, s: Var) -> set[Var]:
        orbit = {s}
        for p in self.perms:
            orbit.add(p[s])
        return orbit

    def contains(self, x: Perm) -> bool:
        return x in self.perms

def vrange(n: int):
    return map(Var, range(n))
