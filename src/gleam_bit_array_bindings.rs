//! Rust bindings for the `gleam_bit_array` module, declared alongside the
//! python bindings via `@external(rust, "gleam_bit_array_bindings", ..)` so the Rust
//! target can compile this package unmodified.

pub fn base16_decode(input: crate::gleam_builtins::GbString) -> Result<crate::gleam_builtins::GleamBitString, ()> {
{
  let text = input.trim();
  if text.len() % 2 == 1 {
    Err(())
  } else {
    let mut bytes = Vec::with_capacity(text.len() / 2);
    let mut ok = true;
    let mut chars = text.chars();
    while ok {
      match chars.next() {
        None => break,
        Some(high) => {
          match chars.next() {
            None => {
              ok = false;
            }
            Some(low) => {
              match high.to_digit(16).and_then(|h| {
                low.to_digit(16).map(|l| h * 16 + l)
              }) {
                Some(byte) => bytes.push(byte as u8),
                None => {
                  ok = false;
                }
              }
            }
          }
        }
      }
    }
    if ok {
      let bits = bytes.len() * 8;
      Ok(crate::gleam_builtins::GleamBitString { data: bytes, bits: bits })
    } else {
      Err(())
    }
  }
}
}

pub fn base16_encode(input: crate::gleam_builtins::GleamBitString) -> crate::gleam_builtins::GbString {
{
  let bytes = &input.data;
  let mut out = String::with_capacity(bytes.len() * 2);
  for byte in bytes {
    out.push_str(&format!("{:02x}", byte));
  }
  crate::gleam_builtins::gb_string_from_str(&out)
}
}

pub fn base64_encode(input: crate::gleam_builtins::GleamBitString, padding: bool) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_base64_encode(&input.data, false, padding)
}

pub fn bit_array_to_int_and_size(a: crate::gleam_builtins::GleamBitString) -> (i64, i64) {
{
  let mut value: i64 = 0;
  for byte in &a.data {
    value = value.wrapping_shl(8) | *byte as i64;
  }
  (value, a.bits as i64)
}
}

pub fn bit_size(x: crate::gleam_builtins::GleamBitString) -> i64 {
x.bits as i64
}

pub fn byte_size(x: crate::gleam_builtins::GleamBitString) -> i64 {
x.data.len() as i64
}

pub fn concat(bit_arrays: crate::gleam_builtins::GleamList<crate::gleam_builtins::GleamBitString>) -> crate::gleam_builtins::GleamBitString {
{
  let mut data: Vec<u8> = Vec::new();
  let mut bits: usize = 0;
  for part in crate::gleam_builtins::to_vec(&bit_arrays) {
    let take = part.bits.min(part.data.len() * 8);
    let full = take / 8;
    data.extend_from_slice(&part.data[..full]);
    bits += take;
  }
  crate::gleam_builtins::GleamBitString { data: data, bits: bits }
}
}

pub fn decode64(a: crate::gleam_builtins::GbString) -> Result<crate::gleam_builtins::GleamBitString, ()> {
match crate::gleam_builtins::gb_base64_decode(a.as_ref(), false) {
  Some(bytes) => {
    let bits = bytes.len() * 8;
    Ok(crate::gleam_builtins::GleamBitString { data: bytes, bits: bits })
  }
  None => Err(()),
}
}

pub fn from_string(x: crate::gleam_builtins::GbString) -> crate::gleam_builtins::GleamBitString {
{
  let bytes = x.as_bytes().to_vec();
  let bits = bytes.len() * 8;
  crate::gleam_builtins::GleamBitString { data: bytes, bits: bits }
}
}

pub fn is_utf8_loop(bits: crate::gleam_builtins::GleamBitString) -> bool {
{
  if bits.bits % 8 != 0 {
    false
  } else {
    let take = bits.bits / 8;
    if take <= bits.data.len() {
      std::str::from_utf8(&bits.data[..take]).is_ok()
    } else {
      std::str::from_utf8(&bits.data).is_ok()
    }
  }
}
}

pub fn slice(string: crate::gleam_builtins::GleamBitString, position: i64, length: i64) -> Result<crate::gleam_builtins::GleamBitString, ()> {
{
  let bits = string.bits as i64;
  if position < 0 || length < 0 || position + length > bits {
    Err(())
  } else {
    let bytes = &string.data;
    let start_byte = (position / 8) as usize;
    let mut end_byte = ((position + length + 7) / 8) as usize;
    if end_byte > bytes.len() {
      end_byte = bytes.len();
    }
    let start_byte = if start_byte > end_byte { end_byte } else { start_byte };
    Ok(crate::gleam_builtins::GleamBitString {
      data: bytes[start_byte..end_byte].to_vec(),
      bits: length as usize,
    })
  }
}
}

pub fn unsafe_to_string(a: crate::gleam_builtins::GleamBitString) -> crate::gleam_builtins::GbString {
crate::gleam_builtins::gb_string_from_str(&String::from_utf8_lossy(&a.data))
}
