use std::fmt::*;
use std::sync::OnceLock;

static C: OnceLock<Vec<String>> = OnceLock::new();

#[derive(Hash, PartialEq, Eq)]
pub struct Id(usize); // This also includes function symbols.

impl Display for Id {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        let i = self.0;
        let h = C.get().unwrap();
        if self.0 < h.len() {
            write!(f, "{}", h[i])
        } else {
            write!(f, "id{i}")
        }
    }
}

impl Debug for Id {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result { write!(f, "{}", self) }
}

pub fn init_ids(names: Vec<String>) {
    C.set(names);
}
