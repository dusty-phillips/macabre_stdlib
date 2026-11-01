//! Rust bindings for the `gleam_dict` module, declared alongside the
//! python bindings via `@external(rust, "gleam_dict_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn do_fold<acc: Clone + 'static, k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(fun: std::rc::Rc<dyn Fn(k, v, acc) -> acc + 'static>, initial: acc, dict: std::sync::Arc<std::collections::HashMap<k, v>>) -> acc {
{
  let mut acc = initial;
  for (key, value) in dict.iter() {
    acc = (fun)(
      crate::gleam_builtins::gb_clone(key),
      crate::gleam_builtins::gb_clone(value),
      acc,
    );
  }
  acc
}
}

pub fn do_has_key<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(key: k, dict: std::sync::Arc<std::collections::HashMap<k, v>>) -> bool {
dict.contains_key(&key)
}

pub fn do_insert<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(key: k, value: v, dict: std::sync::Arc<std::collections::HashMap<k, v>>) -> std::sync::Arc<std::collections::HashMap<k, v>> {
{
  let mut dict = dict;
  std::sync::Arc::make_mut(&mut dict).insert(key, value);
  dict
}
}

pub fn do_map_values<a: Clone + 'static, k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(f: std::rc::Rc<dyn Fn(k, v) -> a + 'static>, dict: std::sync::Arc<std::collections::HashMap<k, v>>) -> std::sync::Arc<std::collections::HashMap<k, a>> {
{
  let mut out =
    std::collections::HashMap::with_capacity(dict.len());
  for (key, value) in dict.iter() {
    out.insert(
      crate::gleam_builtins::gb_clone(key),
      (f)(
        crate::gleam_builtins::gb_clone(key),
        crate::gleam_builtins::gb_clone(value),
      ),
    );
  }
  std::sync::Arc::new(out)
}
}

pub fn from_transient<key: Eq + std::hash::Hash + Clone + 'static, value: Clone + 'static>(transient: std::collections::HashMap<key, value>) -> std::sync::Arc<std::collections::HashMap<key, value>> {
std::sync::Arc::new(transient)
}

pub fn get<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(from: std::sync::Arc<std::collections::HashMap<k, v>>, get: k) -> Result<v, ()> {
match from.get(&get) {
  Some(value) => Ok(crate::gleam_builtins::gb_clone(value)),
  None => Err(()),
}
}

pub fn new<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>() -> std::sync::Arc<std::collections::HashMap<k, v>> {
std::sync::Arc::new(std::collections::HashMap::new())
}

pub fn size<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(dict: std::sync::Arc<std::collections::HashMap<k, v>>) -> i64 {
dict.len() as i64
}

pub fn to_transient<key: Eq + std::hash::Hash + Clone + 'static, value: Clone + 'static>(dict: std::sync::Arc<std::collections::HashMap<key, value>>) -> std::collections::HashMap<key, value> {
std::sync::Arc::try_unwrap(dict).unwrap_or_else(|shared| (*shared).clone())
}

pub fn transient_delete<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(a: k, b: std::collections::HashMap<k, v>) -> std::collections::HashMap<k, v> {
{
  let mut b = b;
  b.remove(&a);
  b
}
}

pub fn transient_insert<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(key: k, value: v, transient: std::collections::HashMap<k, v>) -> std::collections::HashMap<k, v> {
{
  let mut transient = transient;
  transient.insert(key, value);
  transient
}
}

pub fn transient_update_with<k: Eq + std::hash::Hash + Clone + 'static, v: Clone + 'static>(key: k, fun: std::rc::Rc<dyn Fn(v) -> v + 'static>, init: v, transient: std::collections::HashMap<k, v>) -> std::collections::HashMap<k, v> {
{
  let mut transient = transient;
  let updated = match transient.remove(&key) {
    Some(existing) => (fun)(existing),
    None => init,
  };
  transient.insert(key, updated);
  transient
}
}
