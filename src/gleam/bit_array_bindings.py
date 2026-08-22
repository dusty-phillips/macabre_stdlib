import base64
import binascii

from gleam_builtins import EmptyGleamList, GleamList, GleamBitArray, Ok, Error, Nil


def _data_and_bits(x):
    if isinstance(x, GleamBitArray):
        return x.data, x.bits
    return x, len(x) * 8


def from_string(x: str) -> bytes:
    return x.encode("utf-8")


def byte_size(x: bytes) -> int:
    _, bits = _data_and_bits(x)
    return (bits + 7) // 8


def bit_size(x: bytes) -> int:
    return _data_and_bits(x)[1]


def slice(string: bytes, position: int, length: int) -> Ok | Error:
    try:
        data = _data_and_bits(string)[0]
        start = min(position, position + length)
        end = max(position, position + length)
        if start < 0 or end > len(data):
            return Error(Nil)
        return Ok(data[start:end])
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
    bits = []
    head = bit_arrays
    while isinstance(head, GleamList):
        data, nbits = _data_and_bits(head.value)
        for i in range(nbits):
            byte_i = data[i // 8] if i // 8 < len(data) else 0
            bits.append((byte_i >> (7 - (i % 8))) & 1)
        head = head.tail
    total = len(bits)
    out = bytearray((total + 7) // 8)
    for i, bit in enumerate(bits):
        if bit:
            out[i // 8] |= 1 << (7 - (i % 8))
    if total % 8 == 0:
        return bytes(out)
    return GleamBitArray(bytes(out), total)


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
