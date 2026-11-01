//! Rust bindings for the `gleam_io` module, declared alongside the
//! python bindings via `@external(rust, "gleam_io_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn print(string: crate::gleam_builtins::GbString) -> () {
print!("{}", string)
}

pub fn print_error(string: crate::gleam_builtins::GbString) -> () {
eprint!("{}", string)
}

pub fn println(string: crate::gleam_builtins::GbString) -> () {
println!("{}", string)
}

pub fn println_error(string: crate::gleam_builtins::GbString) -> () {
eprintln!("{}", string)
}
