import base64
import binascii

from gleam_builtins import EmptyGleamList, GleamList, Ok, Error, Nil


def from_string(x: str) -> bytes:
    return x.encode("utf-8")


def byte_size(x: bytes) -> int:
    return len(x)


def bit_size(x: bytes) -> int:
    return len(x) * 8


def slice(bits: bytes, position: int, length: int) -> Ok | Error:
    try:
        start = min(position, position + length)
        end = max(position, position + length)
        if start < 0 or end > len(bits):
            return Error(Nil)
        return Ok(bits[start:end])
    except (IndexError, TypeError):
        return Error(Nil)


def unsafe_to_string(a: bytes) -> str:
    return a.decode("utf-8")


def do_to_string(bits: bytes) -> Ok | Error:
    try:
        return Ok(bits.decode("utf-8"))
    except UnicodeDecodeError:
        return Error(Nil)


def concat(bit_arrays: GleamList[bytes] | None) -> bytes:
    result = bytearray()
    head = bit_arrays
    while isinstance(head, GleamList):
        result.extend(head.value)
        head = head.tail
    return bytes(result)


def base64_encode(input: bytes, padding: bool) -> str:
    encoded = base64.b64encode(input).decode("ascii")
    if not padding:
        encoded = encoded.rstrip("=")
    return encoded


def decode64(a: str) -> Ok | Error:
    try:
        return Ok(base64.b64decode(a))
    except Exception:
        return Error(Nil)


def base16_encode(input: bytes) -> str:
    return binascii.hexlify(input).decode("ascii").upper()


def base16_decode(input: str) -> Ok | Error:
    try:
        return Ok(binascii.unhexlify(input))
    except Exception:
        return Error(Nil)


def inspect(input: bytes) -> str:
    return repr(input)


def bit_array_to_int_and_size(a: bytes) -> tuple:
    return (int.from_bytes(a, byteorder="big") if a else 0, len(a) * 8)


def do_is_utf8(a: bytes) -> bool:
    try:
        a.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
