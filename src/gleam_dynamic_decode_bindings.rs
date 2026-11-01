//! Rust bindings for the `gleam_dynamic_decode` module, declared alongside the
//! python bindings via `@external(rust, "gleam_dynamic_decode_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn bare_index<anything: Clone + 'static + crate::gleam_builtins::GbCast>(data: crate::gleam_builtins::GbValue, key: anything) -> Result<Option<crate::gleam_builtins::GbValue>, crate::gleam_builtins::GbString> {
{
  let key = crate::gleam_builtins::gb_cast(key);
  match data {
    crate::gleam_builtins::GbValue::List(items) => {
      match &key {
        crate::gleam_builtins::GbValue::Int(n) => {
          if *n < 0 {
            Ok(None)
          } else {
            match items.get(*n as usize) {
              Some(value) => {
                Ok(Some(crate::gleam_builtins::gb_clone(value)))
              }
              None => Ok(None),
            }
          }
        }
        _ => Err(crate::gleam_builtins::gb_string_from_str("Dict")),
      }
    }
    crate::gleam_builtins::GbValue::Tuple(items) => {
      match &key {
        crate::gleam_builtins::GbValue::Int(n) => {
          if *n < 0 {
            Ok(None)
          } else {
            match items.get(*n as usize) {
              Some(value) => {
                Ok(Some(crate::gleam_builtins::gb_clone(value)))
              }
              None => Ok(None),
            }
          }
        }
        _ => Err(crate::gleam_builtins::gb_string_from_str("Dict")),
      }
    }
    crate::gleam_builtins::GbValue::Dict(map) => {
      match map.get(&key) {
        Some(value) => Ok(Some(crate::gleam_builtins::gb_clone(value))),
        None => Ok(None),
      }
    }
    _ => {
      match &key {
        crate::gleam_builtins::GbValue::Int(_) => {
          Err(crate::gleam_builtins::gb_string_from_str("Indexable"))
        }
        _ => Err(crate::gleam_builtins::gb_string_from_str("Dict")),
      }
    }
  }
}
}

pub fn cast<anything: Clone + 'static + crate::gleam_builtins::GbCast>(a: anything) -> crate::gleam_builtins::GbValue {
crate::gleam_builtins::gb_cast(a)
}

pub fn decode_dict(data: crate::gleam_builtins::GbValue) -> Result<std::sync::Arc<std::collections::HashMap<crate::gleam_builtins::GbValue, crate::gleam_builtins::GbValue>>, ()> {
match data {
  crate::gleam_builtins::GbValue::Dict(map) => {
    Ok(std::sync::Arc::new(map))
  }
  _ => Err(()),
}
}

pub fn decode_list<key: Clone + 'static, t: Clone + 'static>(data: crate::gleam_builtins::GbValue, item: std::rc::Rc<dyn Fn(crate::gleam_builtins::GbValue) -> (t, crate::gleam_builtins::GleamList<crate::gleam_dynamic_decode::DecodeError>) + 'static>, push_path: std::rc::Rc<dyn Fn((t, crate::gleam_builtins::GleamList<crate::gleam_dynamic_decode::DecodeError>), key) -> (t, crate::gleam_builtins::GleamList<crate::gleam_dynamic_decode::DecodeError>) + 'static>, index: i64, acc: crate::gleam_builtins::GleamList<t>) -> (crate::gleam_builtins::GleamList<t>, crate::gleam_builtins::GleamList<crate::gleam_dynamic_decode::DecodeError>) {
{
  let elements: Option<Vec<crate::gleam_builtins::GbValue>> = match &data {
    crate::gleam_builtins::GbValue::List(items) => {
      Some(crate::gleam_builtins::gb_clone(items))
    }
    crate::gleam_builtins::GbValue::Tuple(items) => {
      Some(crate::gleam_builtins::gb_clone(items))
    }
    _ => None,
  };
  match elements {
    None => {
      if crate::gleam_builtins::gb_list_len(&acc) == 0 {
        let errors = crate::gleam_builtins::gb_list_cons(
          std::sync::Arc::new(crate::gleam_dynamic_decode::DecodeErrorNode {
            expected: crate::gleam_builtins::gb_string_from_str("List"),
            found: (crate::gleam_dynamic_bindings::classify)(
              crate::gleam_builtins::gb_clone(&data),
            ),
            path: crate::gleam_builtins::gb_list_empty(),
          }),
          crate::gleam_builtins::gb_list_empty(),
        );
        (crate::gleam_builtins::gb_list_empty(), errors)
      } else {
        (acc, crate::gleam_builtins::gb_list_empty())
      }
    }
    Some(elements) => {
      // `acc` arrives newest-first and stays so as decoded elements prepend;
      // the finished list flips to source order at the end.
      let mut out = acc;
      let mut position = index;
      let mut i = 0;
      while i < elements.len() {
        let (value, errors) =
          (item)(crate::gleam_builtins::gb_clone(&elements[i]));
        if crate::gleam_builtins::gb_list_len(&errors) == 0 {
          out = crate::gleam_builtins::gb_list_cons(value, out);
        } else {
          let segment = crate::gleam_builtins::gb_string_from_str(&position.to_string());
          let mut collected: Vec<(
            crate::gleam_builtins::GbString,
            crate::gleam_builtins::GbString,
            crate::gleam_builtins::GleamList<crate::gleam_builtins::GbString>,
          )> = Vec::new();
          {
            let mut current = &errors;
            loop {
              match &**current {
                crate::gleam_builtins::GleamListNode::Empty => break,
                crate::gleam_builtins::GleamListNode::Cons(head, tail) => {
                  match &**head {
                    crate::gleam_dynamic_decode::DecodeErrorNode {
                      expected,
                      found,
                      path,
                    } => {
                      collected.push((
                        crate::gleam_builtins::gb_clone(expected),
                        crate::gleam_builtins::gb_clone(found),
                        crate::gleam_builtins::gb_clone(path),
                      ));
                    }
                  }
                  current = tail;
                }
              }
            }
          }
          let mut mapped = crate::gleam_builtins::gb_list_empty();
          for (expected, found, path) in collected.into_iter().rev() {
            mapped = crate::gleam_builtins::gb_list_cons(
              std::sync::Arc::new(crate::gleam_dynamic_decode::DecodeErrorNode {
                expected,
                found,
                path: crate::gleam_builtins::gb_list_cons(
                  crate::gleam_builtins::gb_clone(&segment),
                  path,
                ),
              }),
              mapped,
            );
          }
          return (crate::gleam_builtins::gb_list_empty(), mapped);
        }
        position += 1;
        i += 1;
      }
      let mut ordered = crate::gleam_builtins::gb_list_empty();
      {
        let mut current = &out;
        loop {
          match &**current {
            crate::gleam_builtins::GleamListNode::Empty => break,
            crate::gleam_builtins::GleamListNode::Cons(head, tail) => {
              ordered = crate::gleam_builtins::gb_list_cons(
                crate::gleam_builtins::gb_clone(head),
                ordered,
              );
              current = tail;
            }
          }
        }
      }
      (ordered, crate::gleam_builtins::gb_list_empty())
    }
  }
}
}

pub fn dynamic_bit_array(data: crate::gleam_builtins::GbValue) -> Result<crate::gleam_builtins::GleamBitString, crate::gleam_builtins::GleamBitString> {
match data {
  crate::gleam_builtins::GbValue::Bits(v) => Ok(v),
  // Lenient where the Python target rejects: Erlang strings ARE binaries,
  // so a `Str` dynamic decodes as a bit array (this is what makes
  // `decode.string` work on `dynamic.string` values, as on Erlang).
  crate::gleam_builtins::GbValue::Str(s) => {
    let bytes = s.as_bytes().to_vec();
    let bits = bytes.len() * 8;
    Ok(crate::gleam_builtins::GleamBitString { data: bytes, bits: bits })
  }
  _ => {
    Err(crate::gleam_builtins::GleamBitString {
      data: Vec::new(),
      bits: 0,
    })
  }
}
}

pub fn dynamic_float(data: crate::gleam_builtins::GbValue) -> Result<f64, f64> {
match data {
  crate::gleam_builtins::GbValue::Float(v) => Ok(v),
  _ => Err(0.0),
}
}

pub fn dynamic_int(data: crate::gleam_builtins::GbValue) -> Result<i64, i64> {
match data {
  crate::gleam_builtins::GbValue::Int(v) => Ok(v),
  _ => Err(0),
}
}

pub fn is_null(a: crate::gleam_builtins::GbValue) -> bool {
a.is_nil()
}
