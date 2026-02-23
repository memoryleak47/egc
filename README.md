E-Graph completion
==================

An implementation of completion (as in knuth-bendix completion),
just using the e-graph ordering instead of the knuth-bendix ordering.
The e-graph ordering orients `s=t` by choosing a fresh applied id `i` and adding `s -> i` and `t -> i`.

Example: `f(X, h(X, Y)) = g(Y, Z)` becomes
- `f(X, h(X, Y)) -> id1(Y)`
- `g(Y, Z) -> id1(Y)`
