//! Rust bindings for the `gleam_string` module, declared alongside the
//! python bindings via `@external(rust, "gleam_string_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn byte_size(string: crate::gleam_builtins::GbString) -> i64 {
string.len() as i64
}

pub fn contains(haystack: crate::gleam_builtins::GbString, needle: crate::gleam_builtins::GbString) -> bool {
haystack.contains(needle.as_ref())
}

pub fn crop(string: crate::gleam_builtins::GbString, substring: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbString {
match string.find(substring.as_ref()) {
  Some(index) => crate::gleam_builtins::gb_string_from_str(&string[index..]),
  None => crate::gleam_builtins::gb_string_from_str(""),
}
}

pub fn do_inspect<anything: Clone + 'static + crate::gleam_builtins::GbInspect>(term: anything) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::GbValue::Str(crate::gleam_builtins::gb_inspect(&term))
}

pub fn ends_with(string: crate::gleam_builtins::GbString, suffix: crate::gleam_builtins::GbString) -> bool {
string.ends_with(suffix.as_ref())
}

pub fn erl_split(a: crate::gleam_builtins::GbString, b: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GleamList<crate::gleam_builtins::GbString> {
crate::gleam_builtins::gb_split_all(&a, &b)
}

pub fn erl_trim(a: crate::gleam_builtins::GbString, b: crate::gleam_string::Direction) -> crate::gleam_builtins::GbString {
match (&*(b)) {
  crate::gleam_string::DirectionNode::Leading => {
    crate::gleam_builtins::gb_string_from_str(&*a.trim_start().to_string())
  }
  crate::gleam_string::DirectionNode::Trailing => {
    crate::gleam_builtins::gb_string_from_str(&*a.trim_end().to_string())
  }
}
}

pub fn from_utf_codepoints(utf_codepoints: crate::gleam_builtins::GleamList<i64>) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_string_from_str(
  &crate::gleam_builtins::to_vec(&utf_codepoints)
    .into_iter()
    .map(|code| { char::from_u32(code as u32).unwrap_or('�') })
    .collect::<String>(),
)
}

pub fn grapheme_slice(string: crate::gleam_builtins::GbString, index: i64, length: i64) -> crate::gleam_builtins::GbString {
{
  let chars: Vec<char> = string.chars().collect();
  let start = if index < 0 { 0 } else { index as usize };
  let end = start.saturating_add(if length < 0 { 0 } else { length as usize });
  let end = if end > chars.len() { chars.len() } else { end };
  let start = if start > chars.len() { chars.len() } else { start };
  crate::gleam_builtins::gb_string_from_str(
    &chars[start..end].iter().collect::<String>(),
  )
}
}

pub fn length(string: crate::gleam_builtins::GbString) -> i64 {
string.chars().count() as i64
}

pub fn less_than(a: crate::gleam_builtins::GbString, b: crate::gleam_builtins::GbString) -> bool {
a < b
}

pub fn lowercase(string: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_string_from_str(&string.to_lowercase())
}

pub fn pop_grapheme(string: crate::gleam_builtins::GbString) -> Result<(crate::gleam_builtins::GbString, crate::gleam_builtins::GbString), ()> {
// UAX #29 grapheme-cluster rule GB3: CR x LF is a SINGLE cluster, so "\r\n"
// is one grapheme. Splitting it on chars made every caller that matches a
// CRLF literal miss -- e.g. a TOML lexer skipping whitespace on ["\r\n", ..].
if let Some(rest) = string.as_ref().strip_prefix("\r\n") {
return Ok((
crate::gleam_builtins::gb_string_from_str("\r\n"),
crate::gleam_builtins::gb_string_from_str(rest),
));
}
match string.chars().next() {
  Some(first) => {
    let rest = crate::gleam_builtins::gb_string_from_str(&string[first.len_utf8()..]);
    Ok((crate::gleam_builtins::gb_string_from_str(&first.to_string()), rest))
  }
  None => Err(()),
}
}

pub fn remove_prefix(string: crate::gleam_builtins::GbString, prefix: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbString {
match string.strip_prefix(prefix.as_ref()) {
  Some(rest) => crate::gleam_builtins::gb_string_from_str(rest),
  None => string,
}
}

pub fn remove_suffix(string: crate::gleam_builtins::GbString, suffix: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbString {
match string.strip_suffix(suffix.as_ref()) {
  Some(rest) => crate::gleam_builtins::gb_string_from_str(rest),
  None => string,
}
}

pub fn starts_with(string: crate::gleam_builtins::GbString, prefix: crate::gleam_builtins::GbString) -> bool {
string.starts_with(prefix.as_ref())
}

pub fn string_to_codepoint_integer_list(string: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GleamList<i64> {
crate::gleam_builtins::to_gleam_list(
  string.chars().map(|c| c as i64).collect::<Vec<i64>>(),
)
}

pub fn unsafe_byte_slice(string: crate::gleam_builtins::GbString, index: i64, length: i64) -> crate::gleam_builtins::GbString {
match string.as_bytes().get({
  let start = if index < 0 { 0 } else { index as usize };
  let end = start.saturating_add(if length < 0 { 0 } else { length as usize });
  start..end
}) {
  Some(bytes) => crate::gleam_builtins::gb_string_from_str(&String::from_utf8_lossy(bytes)),
  None => crate::gleam_builtins::gb_string_from_str(""),
}
}

pub fn unsafe_int_to_utf_codepoint(a: i64) -> i64 {
a
}

pub fn uppercase(string: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_string_from_str(&string.to_uppercase())
}

pub fn utf_codepoint_to_int(cp: i64) -> i64 {
cp
}
