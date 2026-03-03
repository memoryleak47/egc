from term import *
from dataclasses import dataclass

def tokenize(s: str) -> list[str]:
    s = s.replace("(", " ( ")
    s = s.replace("!", " ! ")
    s = s.replace("=", " = ")
    s = s.replace(")", " ) ")
    s = s.replace(".", " . ")
    s = s.replace(",", " , ")
    s = s.replace("\n", " ")
    s = s.replace("\t", " ")
    for _ in range(10):
        s = s.replace("  ", " ")
    return s.split()

def assemble_term(toks) -> (list[str], Term):
    tok = toks[0]
    if tok[0] == "X":
        i = int(tok[1:])
        return (toks[1:], Var(i))
    assert(tok[0].islower())
    if toks[1] != "(":
        return (toks[1:], Applied(tok, ()))
    assert(toks[1] == "(")
    toks = toks[2:]
    args = []
    while True:
        toks, ch = assemble_term(toks)
        args.append(ch)
        if toks[0] == ")":
            break
        assert(toks[0] == ",")
        toks = toks[1:]
    assert(toks[0] == ")")
    toks = toks[1:]
    t = Applied(tok, tuple(args))
    return (toks, t)

def assemble_item(toks, eqs, diseqs) -> list[str]:
    # cnf(a,axiom, lhs = rhs).
    assert(toks[0] == "cnf")
    assert(toks[1] == "(")
    assert(toks[3] == ",")
    assert(toks[4] == "axiom")
    assert(toks[5] == ",")
    toks, lhs = assemble_term(toks[6:])
    if toks[0] == "!" and toks[1] == "=":
        target = diseqs
        toks = toks[2:]
    elif toks[0] == "=":
        target = eqs
        toks = toks[1:]
    toks, rhs = assemble_term(toks)
    assert(toks[0] == ")")
    assert(toks[1] == ".")
    target.append((lhs, rhs))
    return toks[2:]

def assemble(toks: list[str]) -> (Equation, Goal):
    eqs = []
    diseqs = []
    while toks:
        toks = assemble_item(toks, eqs, diseqs)
    return eqs, diseqs

def parse(filename):
    lines = open(filename).read()
    toks = tokenize(lines)
    return assemble(toks)
