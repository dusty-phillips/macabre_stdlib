from gleam_builtins import EmptyGleamList, GleamList, Ok, Error, Nil


def do_append(a: str, b: str) -> str:
    return a + b


def do_from_strings(a: GleamList[str] | None) -> str:
    parts = []
    head = a
    while isinstance(head, GleamList):
        parts.append(head.value)
        head = head.tail
    return "".join(parts)


def do_concat(a: GleamList[str] | None) -> str:
    parts = []
    head = a
    while isinstance(head, GleamList):
        parts.append(head.value)
        head = head.tail
    return "".join(parts)


def do_from_string(a: str) -> str:
    return a


def do_to_string(a: str) -> str:
    return a


def do_byte_size(a: str) -> int:
    return len(a.encode("utf-8"))


def do_lowercase(a: str) -> str:
    return a.lower()


def do_uppercase(a: str) -> str:
    return a.upper()


def do_reverse(builder: str) -> str:
    return builder[::-1]


def do_to_graphemes(string: str) -> GleamList[str] | None:
    result = EmptyGleamList()
    for char in reversed(string):
        result = GleamList(char, result)
    return result


def do_split(iodata: str, pattern: str) -> GleamList[str] | None:
    result = EmptyGleamList()
    for part in reversed(iodata.split(pattern)):
        result = GleamList(part, result)
    return result


def erl_split(a: str, b: str, c) -> GleamList[str] | None:
    result = EmptyGleamList()
    for part in reversed(a.split(b)):
        result = GleamList(part, result)
    return result


def replace(tree: str, pattern: str, substitute: str) -> str:
    return tree.replace(pattern, substitute)


def is_equal(a: str, b: str) -> bool:
    return a == b


def is_empty(builder: str) -> bool:
    return builder == ""
