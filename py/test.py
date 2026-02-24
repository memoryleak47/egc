from simplify import *

def test1():
    lhs = Node("a", ())
    rhs = Node(Id(0), ())
    eqs = [(lhs, rhs)]

    out = simplify_term(lhs, eqs)
    assert(out == rhs)

tests = [
    test1
]

for t in tests:
    t()
