//! Rust bindings for the `gleam_dynamic` module, declared alongside the
//! python bindings via `@external(rust, "gleam_dynamic_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn array(a: crate::gleam_builtins::GleamList<crate::gleam_builtins::GbValue>) -> crate::gleam_builtins::GbValue {
{
  let mut items = Vec::new();
  let mut current = &a;
  loop {
    match &**current {
      crate::gleam_builtins::GleamListNode::Empty => break,
      crate::gleam_builtins::GleamListNode::Cons(head, tail) => {
        items.push(crate::gleam_builtins::gb_clone(head));
        current = tail;
      }
    }
  }
  crate::gleam_builtins::GbValue::Tuple(items)
}
}

pub fn bit_array(a: crate::gleam_builtins::GleamBitString) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::GbValue::Bits(a)
}

pub fn bool(a: bool) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::GbValue::Bool(a)
}

pub fn cast<anything: Clone + 'static + crate::gleam_builtins::GbCast>(a: anything) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_cast(a)
}

pub fn classify(data: crate::gleam_builtins::GbValue) -> crate::gleam_builtins::GbString {
match &data {
  crate::gleam_builtins::GbValue::Bool(_) => crate::gleam_builtins::gb_string_from_str("Bool"),
  crate::gleam_builtins::GbValue::Int(_) => crate::gleam_builtins::gb_string_from_str("Int"),
  crate::gleam_builtins::GbValue::Float(_) => crate::gleam_builtins::gb_string_from_str("Float"),
  crate::gleam_builtins::GbValue::Str(_) => crate::gleam_builtins::gb_string_from_str("crate::gleam_builtins::GbString"),
  crate::gleam_builtins::GbValue::Bits(_) => crate::gleam_builtins::gb_string_from_str("BitArray"),
  crate::gleam_builtins::GbValue::Nil => crate::gleam_builtins::gb_string_from_str("Nil"),
  crate::gleam_builtins::GbValue::List(_) => crate::gleam_builtins::gb_string_from_str("List"),
  crate::gleam_builtins::GbValue::Tuple(_) => crate::gleam_builtins::gb_string_from_str("Tuple"),
  crate::gleam_builtins::GbValue::Dict(_) => crate::gleam_builtins::gb_string_from_str("Dict"),
  _ => crate::gleam_builtins::gb_string_from_str("CustomType"),
}
}

pub fn float(a: f64) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::GbValue::Float(a)
}

pub fn int(a: i64) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::GbValue::Int(a)
}

pub fn list(a: crate::gleam_builtins::GleamList<crate::gleam_builtins::GbValue>) -> crate::gleam_builtins::GbValue {
{
  let mut items = Vec::new();
  let mut current = &a;
  loop {
    match &**current {
      crate::gleam_builtins::GleamListNode::Empty => break,
      crate::gleam_builtins::GleamListNode::Cons(head, tail) => {
        items.push(crate::gleam_builtins::gb_clone(head));
        current = tail;
      }
    }
  }
  crate::gleam_builtins::GbValue::List(items)
}
}

pub fn string(a: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::GbValue::Str(a)
}
