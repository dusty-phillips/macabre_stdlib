//! Rust bindings for the `gleam_float` module, declared alongside the
//! python bindings via `@external(rust, "gleam_float_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn ceiling(x: f64) -> f64 {
x.ceil()
}

pub fn do_log(x: f64) -> f64 {
x.ln()
}

pub fn do_power(a: f64, b: f64) -> f64 {
a.powf(b)
}

pub fn do_to_float(a: i64) -> f64 {
a as f64
}

pub fn exponential(x: f64) -> f64 {
x.exp()
}

pub fn floor(x: f64) -> f64 {
x.floor()
}

pub fn js_round(a: f64) -> i64 {
(a + 0.5).floor() as i64
}

pub fn parse(string: crate::gleam_builtins::GbString) -> Result<f64, ()> {
{
  let has_dot_or_exp =
    string.contains('.') || string.contains('e') || string.contains('E');
  if !has_dot_or_exp {
    Err(())
  } else {
    match string.trim().parse::<f64>() {
      Ok(n) => {
        if n.is_finite() {
          Ok(n)
        } else {
          Err(())
        }
      }
      Err(_) => Err(()),
    }
  }
}
}

pub fn random() -> f64 {
{
  let bytes = crate::gleam_builtins::gb_random_bytes(8);
  let mut n: u64 = 0;
  for byte in bytes {
    n = (n << 8) | byte as u64;
  }
  (n as f64) / (u64::MAX as f64)
}
}

pub fn to_string(x: f64) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_string_from_str(&format!("{}", x))
}

pub fn truncate(x: f64) -> i64 {
x as i64
}
