//! Rust bindings for the `gleam_int` module, declared alongside the
//! python bindings via `@external(rust, "gleam_int_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn bitwise_and(x: i64, y: i64) -> i64 {
x & y
}

pub fn bitwise_exclusive_or(x: i64, y: i64) -> i64 {
x ^ y
}

pub fn bitwise_not(x: i64) -> i64 {
!x
}

pub fn bitwise_or(x: i64, y: i64) -> i64 {
x | y
}

pub fn bitwise_shift_left(x: i64, y: i64) -> i64 {
x.wrapping_shl(y as u32)
}

pub fn bitwise_shift_right(x: i64, y: i64) -> i64 {
x.wrapping_shr(y as u32)
}

pub fn do_base_parse(a: crate::gleam_builtins::GbString, b: i64) -> Result<i64, ()> {
crate::gleam_builtins::gb_int_from_base_string(&a, b)
}

pub fn do_to_base_string(a: i64, b: i64) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_int_to_base_string(a, b)
}

pub fn parse(string: crate::gleam_builtins::GbString) -> Result<i64, ()> {
{
  let trimmed = string.trim();
  if trimmed.contains('_') {
    Err(())
  } else {
    match trimmed.parse::<i64>() {
      Ok(n) => Ok(n),
      Err(_) => Err(()),
    }
  }
}
}

pub fn to_float(x: i64) -> f64 {
x as f64
}

pub fn to_string(x: i64) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_string_from_str(&x.to_string())
}
