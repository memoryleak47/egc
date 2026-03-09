E-Graph completion
==================

An implementation of completion (as in knuth-bendix completion),
just using the e-graph ordering instead of the knuth-bendix ordering.
The e-graph ordering orients `s=t` by choosing a fresh applied id `i` and adding `s -> i` and `t -> i`.

Example: `f(X, h(X, Y)) = g(Y, Z)` becomes
- `f(X, h(X, Y)) -> id1(Y)`
- `g(Y, Z) -> id1(Y)`

Takeaway from the experiment:
- It "seems to work" in the sense that it was able to prove the groups example.
- It does produce many more CPs than naive knuth-bendix completion, as there are many equivalent ways to express the same facts using all these symbols
-- Normal KBC takes 13 steps, whereas we require 75 steps on the group example
- I expect this to be a semi-decision procedure for the word problem of any equational theory (just like the other completion algorithms)
-- I think this only works, due to the CP scoring function that associates a "weight" to applied ids corresponding to the terms they represent
- Maybe there is a way to make this work more efficiently, by restricting what "definitions" you add, or by restricting what CPs/facts we generate
- Potential advantage: a "step" could be implemented much more efficiently (i.e. locally) in a fully hashconsed system than in a term-based system

Implementations:
- v1: purely term-rewriting based
- v2: based on slotted e-graph
- v3: knuth-bendix completion, and only add ids incase you can't orient
