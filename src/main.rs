use std::collections::HashMap;

#[derive(Hash, PartialEq, Eq)]
struct Var(usize);

#[derive(Hash, PartialEq, Eq)]
struct Id(usize); // This also includes function symbols.

#[derive(Hash, PartialEq, Eq)]
enum BaseTerm {
    Var(Var),
    AppId(Id, Box<[Var]>),
}

// should variables be valid node terms?
#[derive(Hash, PartialEq, Eq)]
struct NodeTerm {
    id: Id,
    args: Box<[BaseTerm]>,
}

struct Class {
    leader: BaseTerm,
    group: (), // TODO
    usages: (), // TODO for efficient rebuilding
}

struct State {
    classes: Vec<Class>,
    hashcons: HashMap<NodeTerm, BaseTerm>,
}

fn main() {
    println!("Hello, world!");
}
