//! Rust bindings for the `gleam_string_tree` module, declared alongside the
//! python bindings via `@external(rust, "gleam_string_tree_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn append_tree(tree: crate::gleam_builtins::GbValue, suffix: crate::gleam_builtins::GbValue) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_append_tree(tree, suffix)
}

pub fn byte_size(tree: crate::gleam_builtins::GbValue) -> i64 {
crate::gleam_builtins::gb_tree_length(&tree)
}

pub fn concat(trees: crate::gleam_builtins::GleamList<crate::gleam_builtins::GbValue>) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_concat_list(crate::gleam_builtins::to_vec(&trees))
}

pub fn do_to_graphemes(string: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GleamList<crate::gleam_builtins::GbString> {
crate::gleam_builtins::to_gleam_list(
  string.chars().map(|c| crate::gleam_builtins::gb_string_from_str(&c.to_string())).collect::<Vec<crate::gleam_builtins::GbString>>(),
)
}

pub fn erl_split(a: crate::gleam_builtins::GbValue, b: crate::gleam_builtins::GbString, c: crate::gleam_string_tree::Direction) -> crate::gleam_builtins::GleamList<crate::gleam_builtins::GbValue> {
crate::gleam_builtins::to_gleam_list(
  crate::gleam_builtins::to_vec(&crate::gleam_builtins::gb_split_all(
    &crate::gleam_builtins::gb_tree_string(&a),
    &b,
  ))
  .into_iter()
  .map(crate::gleam_builtins::gb_tree_from_str)
  .collect::<Vec<crate::gleam_builtins::GbValue>>(),
)
}

pub fn from_string(string: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_from_str(string)
}

pub fn from_strings(strings: crate::gleam_builtins::GleamList<crate::gleam_builtins::GbString>) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_from_strings(crate::gleam_builtins::to_vec(&strings))
}

pub fn lowercase(tree: crate::gleam_builtins::GbValue) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_from_str(
  crate::gleam_builtins::gb_string_from_str(
    &crate::gleam_builtins::gb_tree_string(&tree).to_lowercase(),
  ),
)
}

pub fn replace(tree: crate::gleam_builtins::GbValue, pattern: crate::gleam_builtins::GbString, substitute: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_from_str(
  crate::gleam_builtins::gb_string_from_str(
    &crate::gleam_builtins::gb_tree_string(&tree).replace(pattern.as_ref(), substitute.as_ref()),
  ),
)
}

pub fn to_string(tree: crate::gleam_builtins::GbValue) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_tree_string(&tree)
}

pub fn uppercase(tree: crate::gleam_builtins::GbValue) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_tree_from_str(
  crate::gleam_builtins::gb_string_from_str(
    &crate::gleam_builtins::gb_tree_string(&tree).to_uppercase(),
  ),
)
}
