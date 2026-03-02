#[derive(Hash, PartialEq, Eq)]
pub struct Id(pub i32); // This also includes function symbols.
// Negative: variables.
// Non-negative: First function symbols, then fresh ids.

mod fmt {
    use crate::Id;
    use std::sync::OnceLock;
    use std::fmt::*;

    pub static C: OnceLock<Vec<String>> = OnceLock::new();

    impl Display for Id {
        fn fmt(&self, f: &mut Formatter<'_>) -> Result {
            let i = self.0;
            let h = C.get().unwrap();
            if i < 0 {
                write!(f, "X{}", -(i+1))
            } else {
                let i = i as usize;
                if i < h.len() {
                    write!(f, "{}", h[i])
                } else {
                    write!(f, "id{i}")
                }
            }
        }
    }

    impl Debug for Id {
        fn fmt(&self, f: &mut Formatter<'_>) -> Result { write!(f, "{}", self) }
    }

    pub fn init_ids(names: Vec<String>) {
        C.set(names);
    }
}
pub use fmt::init_ids;
