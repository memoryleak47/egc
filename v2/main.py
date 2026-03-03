from suf import *

type Base = AppliedId | Slot

type Node = AppliedId | Slot | ... # TODO

class State:
    suf: SlottedUF
    hashcons: dict[Term, Base]
