import dataclasses
import math
import re as _re
import unicodedata

from gleam_builtins import EmptyGleamList, GleamList, GleamBitArray, Ok, Error, Nil

try:
    import regex as _regex

    _grapheme_regex = _regex.compile(r"\X")
except ImportError:
    _grapheme_regex = None


@dataclasses.dataclass(frozen=True)
class UtfCodepoint:
    value: int


def do_length(a: str) -> int:
    return len(a)


def do_lowercase(a: str) -> str:
    return a.lower()


def do_uppercase(a: str) -> str:
    return a.upper()


def less_than(a: str, b: str) -> bool:
    return a < b


def do_slice(string: str, idx: int, len: int) -> str:
    return string[idx : idx + len]


def crop(string: str, substring: str) -> str:
    if string.startswith(substring):
        return string[len(substring) :]
    return string


def contains(haystack: str, needle: str) -> bool:
    return needle in haystack


def do_starts_with(a: str, b: str) -> bool:
    return a.startswith(b)


def do_ends_with(a: str, b: str) -> bool:
    return a.endswith(b)


def do_split_once(x: str, substring: str) -> Ok | Error:
    if substring in x:
        idx = x.index(substring)
        before = x[:idx]
        after = x[idx + len(substring) :]
        return Ok((before, after))
    return Error(Nil)


def erl_split(a: str, b: str) -> GleamList[str] | None:
    # Mirrors Erlang string:split/2, which splits on the FIRST occurrence and
    # returns a two-element list [before, after]. string.split_once matches
    # that shape exactly and reports an error when the substring is absent.
    idx = a.find(b)
    if idx < 0:
        return EmptyGleamList()
    before = a[:idx]
    after = a[idx + len(b):]
    return GleamList(before, GleamList(after, EmptyGleamList()))


def do_join(strings: GleamList[str] | None, separator: str) -> str:
    parts = []
    head = strings
    while isinstance(head, GleamList):
        parts.append(head.value)
        head = head.tail
    return separator.join(parts)


def _erl_whitespace(ch: str) -> bool:
    return ch in " \t\n\v\f\r"


def _erl_trim_left(string: str) -> str:
    i = 0
    length = len(string)
    while i < length and _erl_whitespace(string[i]):
        i += 1
    return string[i:]


def _erl_trim_right(string: str) -> str:
    j = len(string)
    while j > 0 and _erl_whitespace(string[j - 1]):
        j -= 1
    return string[:j]


def do_trim(string: str) -> str:
    return _erl_trim_right(_erl_trim_left(string))


def erl_trim(a: str, b) -> str:
    name = b.__class__.__name__
    if name == "Both":
        return _erl_trim_right(_erl_trim_left(a))
    elif name == "Leading":
        return _erl_trim_left(a)
    elif name == "Trailing":
        return _erl_trim_right(a)
    return a


def do_trim_start(string: str) -> str:
    return _erl_trim_left(string)


def do_trim_end(string: str) -> str:
    return _erl_trim_right(string)


_PREPEND_RANGES = (
    range(0x0600, 0x0606),
    range(0x06DD, 0x06DE),
    range(0x070F, 0x0710),
    range(0x0890, 0x0892),
    range(0x08E2, 0x08E3),
    range(0x110BD, 0x110BE),
    range(0x110CD, 0x110CE),
    range(0x111C2, 0x111C4),
    range(0x1193F, 0x11940),
    range(0x11941, 0x11942),
    range(0x11A3A, 0x11A3B),
    range(0x11A84, 0x11A8A),
    range(0x11D46, 0x11D47),
    range(0x11F02, 0x11F03),
)


def _is_prepend(cp: int) -> bool:
    for r in _PREPEND_RANGES:
        if cp in r:
            return True
    return False


def _is_continuation(prev_cp: int, cp: int) -> bool:
    if prev_cp == 0x0D and cp == 0x0A:
        return True
    if unicodedata.category(chr(cp))[0] == "M":
        return True
    if cp == 0x200D or prev_cp == 0x200D:
        return True
    if 0x1F3FB <= cp <= 0x1F3FF:
        return True
    if 0x1F1E6 <= prev_cp <= 0x1F1FF and 0x1F1E6 <= cp <= 0x1F1FF:
        return True
    if _is_prepend(prev_cp):
        return True
    return False


def _graphemes(string: str) -> list[str]:
    if _grapheme_regex is not None:
        return _grapheme_regex.findall(string)
    codepoints = [ord(ch) for ch in string]
    clusters = []
    start = 0
    for i in range(1, len(codepoints)):
        if not _is_continuation(codepoints[i - 1], codepoints[i]):
            clusters.append(string[start:i])
            start = i
    if codepoints:
        clusters.append(string[start:])
    return clusters


def do_pop_grapheme(string: str) -> Ok | Error:
    if string == "":
        return Error(Nil)
    if _grapheme_regex is not None:
        first = _grapheme_regex.match(string).group(0)
    else:
        # Scan only as far as the first grapheme boundary instead of
        # splitting the whole string into graphemes, which is O(n) per pop
        # and turns repeated pops into O(n^2).
        first = string
        prev = None
        for i, ch in enumerate(string):
            cp = ord(ch)
            if prev is not None and not _is_continuation(prev, cp):
                first = string[:i]
                break
            prev = cp
    return Ok((first, string[len(first) :]))


def to_graphemes(string: str) -> GleamList[str] | None:
    result = EmptyGleamList()
    for grapheme in reversed(_graphemes(string)):
        result = GleamList(grapheme, result)
    return result


def unsafe_int_to_utf_codepoint(a: int) -> UtfCodepoint:
    return UtfCodepoint(a)


def string_to_codepoint_integer_list(a: str) -> GleamList[int] | None:
    result = EmptyGleamList()
    for char in reversed(a):
        result = GleamList(ord(char), result)
    return result


def from_utf_codepoints(utf_codepoints: GleamList[UtfCodepoint] | None) -> str:
    chars = []
    head = utf_codepoints
    while isinstance(head, GleamList):
        chars.append(chr(head.value.value))
        head = head.tail
    return "".join(chars)


def do_utf_codepoint_to_int(cp: UtfCodepoint) -> int:
    return cp.value


def _inspect_string(a: str) -> str:
    out = ['"']
    for ch in a:
        cp = ord(ch)
        if cp == 0x22:
            out.append('\\"')
        elif cp == 0x5C:
            out.append("\\\\")
        elif cp == 0x0A:
            out.append("\\n")
        elif cp == 0x0D:
            out.append("\\r")
        elif cp == 0x09:
            out.append("\\t")
        elif cp == 0x0C:
            out.append("\\f")
        elif cp < 0x20 or 0x7F <= cp < 0xA0:
            out.append("\\u{%04X}" % cp)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def do_inspect(term) -> str:
    if isinstance(term, str):
        return _inspect_string(term)
    if isinstance(term, UtfCodepoint):
        return str(term.value)
    if term is True or term is False:
        return "True" if term else "False"
    if term is None:
        return "Nil"
    if isinstance(term, int):
        return str(term)
    if isinstance(term, float):
        return _inspect_float(term)
    if isinstance(term, tuple):
        inner = ", ".join(do_inspect(item) for item in term)
        return "#(" + inner + ")"
    if isinstance(term, (GleamList, EmptyGleamList)):
        return _inspect_list(term)
    if isinstance(term, dict):
        entries = ", ".join(
            "#(" + do_inspect(key) + ", " + do_inspect(value) + ")"
            for key, value in term.items()
        )
        return "dict.from_list([" + entries + "])"
    if isinstance(term, bytes):
        return _inspect_bytes(term)
    if isinstance(term, GleamBitArray):
        return _inspect_bit_array(term)
    if dataclasses.is_dataclass(term):
        name = type(term).__name__
        values = ", ".join(
            do_inspect(getattr(term, field.name))
            for field in dataclasses.fields(term)
        )
        return name + ("(" + values + ")" if values else "")
    return repr(term)


def _inspect_float(value: float) -> str:
    string = repr(value).replace("+", "")
    if "." in string or "e" in string or "E" in string:
        return string
    return string + ".0"


def _inspect_list(list_: GleamList) -> str:
    elements = []
    head = list_
    while isinstance(head, GleamList):
        elements.append(do_inspect(head.value))
        head = head.tail
    return "[" + ", ".join(elements) + "]"


def _inspect_bytes(data: bytes) -> str:
    try:
        return _inspect_string(data.decode("utf-8"))
    except UnicodeDecodeError:
        values = ", ".join(str(byte) for byte in data)
        return "<<" + values + ">>"


def _inspect_bit_array(term: GleamBitArray) -> str:
    data = term.data
    bits = term.bits
    if bits == 0:
        return "<<>>"
    full = bits // 8
    rest = bits % 8
    parts = [str(byte) for byte in data[:full]]
    if rest:
        last_byte = data[full] if full < len(data) else 0
        value = last_byte >> (8 - rest)
        parts.append(f"{value}:size({rest})")
    return "<<" + ", ".join(parts) + ">>"


def byte_size(string: str) -> int:
    return len(string.encode("utf-8"))


def unsafe_byte_slice(string: str, index: int, length: int) -> str:
    return string[index : index + length]


def remove_prefix(string: str, prefix: str) -> str:
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


def remove_suffix(string: str, suffix: str) -> str:
    if suffix and string.endswith(suffix):
        return string[: -len(suffix)]
    return string
