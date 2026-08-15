from gleam_builtins import EmptyGleamList, GleamList


class BytesTree:
    def __init__(self, segments=None):
        self.segments = segments if segments is not None else []

    def __eq__(self, other):
        if not isinstance(other, BytesTree):
            return False
        return self.segments == other.segments


def append_tree(a: BytesTree, b: BytesTree) -> BytesTree:
    return BytesTree(a.segments + b.segments)


def concat(trees: GleamList[BytesTree] | None) -> BytesTree:
    result = BytesTree()
    head = trees
    while isinstance(head, GleamList):
        result.segments.extend(head.value.segments)
        head = head.tail
    return result


def concat_bit_arrays(bits: GleamList[bytes] | None) -> BytesTree:
    result = BytesTree()
    head = bits
    while isinstance(head, GleamList):
        result.segments.append(head.value)
        head = head.tail
    return result


def from_string(string: str) -> BytesTree:
    return BytesTree([string])


def from_string_tree(tree) -> BytesTree:
    return BytesTree([tree])


def from_bit_array(bits: bytes) -> BytesTree:
    return BytesTree([bits])


def to_bit_array(tree: BytesTree) -> bytes:
    parts = []
    for segment in tree.segments:
        if isinstance(segment, bytes):
            parts.append(segment)
        elif isinstance(segment, str):
            parts.append(segment.encode("utf-8"))
        else:
            parts.append(bytes(segment))
    return b"".join(parts)


def byte_size(tree: BytesTree) -> int:
    return len(to_bit_array(tree))
