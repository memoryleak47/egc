mod id;
pub use id::*;

mod minqueue;
pub use minqueue::*;

use std::collections::HashMap;

#[derive(Hash, PartialEq, Eq)]
struct BaseTerm {
    id: Id,
    args: Box<[Id]>,
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
    usages: (), // TODO for efficient rebuilding & CPs?
}

struct State {
    classes: Vec<Class>,
    hashcons: HashMap<NodeTerm, BaseTerm>,

    passive: MinPrioQueue<usize, ((), ())>, // how to represent terms in the passive set? already interned?
    goals: Vec<(BaseTerm, BaseTerm)>,
}

impl State {
    fn tick_cp(&mut self) {
        todo!()
        // TODO:
        // - pop CP from the passive set
        // - simplify it.
        // - add to active set (i.e. hashcons & UF)
        // - compute CPs from it, simplify them, and add them to the passive set.

        // - simplify & check goals (goal simplification could also be done via usages)
    }

    fn add(&mut self, node: NodeTerm) -> BaseTerm {
        todo!()
    }

    fn union(&mut self, b1: BaseTerm, b2: BaseTerm) {
        todo!()
    }

    fn add_goal(&mut self, x: BaseTerm, y: BaseTerm) {
        self.goals.push((x, y));
    }
}

fn main() {
    println!("Hello, world!");
}
